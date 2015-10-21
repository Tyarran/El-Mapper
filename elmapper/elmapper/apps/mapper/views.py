# -*- coding: utf-8 -*-
import csv
import itertools
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic.base import TemplateView
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import FormView, FormMixin

from elmapper.apps.mapper.forms import ImportedProductCSVForm, MappingForm, ProductForm
from elmapper.apps.mapper.models import ImportedProductCSV, Product, MappingConfig


class ImportCSVView(FormView):
    """CSV import view"""
    template_name = 'import_csv.html'
    form_class = ImportedProductCSVForm

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(reverse('mapping_result', args=((obj.pk, ))))


class MappingResultView(FormMixin, TemplateView):
    """Mapping result view"""
    template_name = "result.html"
    form_class = MappingForm

    def parse_csv(self):
        csv_file = self.imported_csv.csv_file.file
        reader = csv.reader(csv_file)
        return reader.next()

    def get(self, request, pk):
        self.pk = pk
        try:
            self.imported_csv = ImportedProductCSV.objects.get(pk=self.pk)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()
        return super(MappingResultView, self).get(request)

    def get_context_data(self, *args, **kwargs):
        context = super(MappingResultView, self).get_context_data(**kwargs)
        columns = self.parse_csv()
        context['result'] = Mapper(self.imported_csv)()
        context["fields"] = [(column, Product.fieldnames()) for column in columns]
        default_json = {field: '' for field in columns}
        context['mapping_form'] = MappingForm(data={'json': json.dumps(default_json, indent=4)})
        context['existing_mapping'] = MappingConfig.objects.all()
        return context


class Mapper(object):

    def __init__(self, imported_csv):
        self.imported_csv = imported_csv
        self.mapping_config = json.loads(imported_csv.mapping_config.json)
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
