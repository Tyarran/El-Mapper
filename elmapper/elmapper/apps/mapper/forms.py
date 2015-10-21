from django import forms

from elmapper.apps.mapper.models import ImportedProductCSV, MappingConfig, Product


class ImportedProductCSVForm(forms.ModelForm):

    class Meta():
        model = ImportedProductCSV
        fields = ['csv_file', 'mapping_config']


class MappingForm(forms.ModelForm):

    class Meta():
        model = MappingConfig
        fields = ['title', 'description', 'json']

class ProductForm(forms.ModelForm):

    class Meta():
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'brand',
            'category',
            'color',
        ]
