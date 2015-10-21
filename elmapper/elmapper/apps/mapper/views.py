# -*- coding: utf-8 -*-
import csv
import itertools
import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from elmapper.apps.mapper.forms import MappingForm, ProductForm
from elmapper.apps.mapper.models import Product, MappingResult


class ResultListView(FormView):
    model = MappingResult
    form_class = MappingForm
    template_name = 'mapper/mappingresult_list.html'

    def get_context_data(self, **kwargs):
        context = super(ResultListView, self).get_context_data(**kwargs)
        context['url_object'] = [(obj, reverse('result-detail', args=((obj.pk, ))))
                                 for obj in self.model.objects.all()]
        context['form'] = self.form_class()
        return context

    def form_valid(self, form):
        csv, config = form.cleaned_data['csv'], form.cleaned_data['config']
        result = Mapper(csv, config)()
        mapping_result = MappingResult(csv=csv,
                                       config=config,
                                       result=json.dumps(result))
        mapping_result.save()
        return HttpResponseRedirect(reverse('result-detail', args=((mapping_result.pk, ))))


class ResultDetailView(DetailView):
    model = MappingResult

    def get_context_data(self, **kwargs):
        context = super(ResultDetailView, self).get_context_data(**kwargs)
        context['result'] = json.loads(context['object'].result)
        return context


class Mapper(object):

    def __init__(self, imported_csv, mapping_config):
        self.imported_csv = imported_csv
        self.mapping_config = json.loads(mapping_config.json)
        self.csv_file = self.imported_csv.csv_file.file
        self.errors = []

    def get_mapping_config_by_external_name(self, external_name):
        results = [config for config in self.mapping_config if config['external_name'] == external_name]
        if len(results):
            return results[0]
        return None

    def __call__(self):
        reader = csv.reader(self.csv_file)
        headers = reader.next()  # skip headers
        mapped_fields = [field['external_name'] for field in self.mapping_config]

        # Read line by line
        for index, row in enumerate(reader, start=1):
            result = {}  # data for this line
            creation_errors = []
            line_data = {key: value for key, value in itertools.izip(headers, row)}

            for field_name, value in line_data.items():
                if field_name in mapped_fields:
                    # get mapping config for the current field
                    config = self.get_mapping_config_by_external_name(field_name)
                    try:
                        result[config['model_name']] = self.get_value(field_name, value, config)
                    except ObjectDoesNotExist as exc:
                        creation_errors.append(exc.message)

            if not len(creation_errors):
                form = ProductForm(data=result)
                if form.is_valid():
                    form.save()
                else:
                    self.errors.append(((index, row), form.errors))
            else:
                self.errors.append(((index, row), creation_errors))

        return {
            'total': index,
            'imported': index - len(self.errors),
            'errors': self.errors,
            'errors_nb': len(self.errors),
        }

    def get_value(self, field, value, config):
        related_model = Product.related_model(config['model_name'])
        if related_model:
            fk_mapping = [fk_mapping for fk_mapping in config['foreign_key_mapping']
                          if str(fk_mapping['external_fk']) == str(value)]
            if not len(fk_mapping):
                return related_model.objects.get(pk=value).pk
            else:
                fk_mapping = fk_mapping[0]
            if fk_mapping['pattern'] == 'pk':
                return related_model.objects.get(pk=fk_mapping['internal_value']).pk
            else:
                return related_model.objects.get(**{fk_mapping['pattern']: fk_mapping['internal_value']}).pk
        else:
            return value
