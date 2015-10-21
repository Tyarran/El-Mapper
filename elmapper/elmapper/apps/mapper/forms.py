from django import forms

from elmapper.apps.mapper.models import ImportedProductCSV, MappingConfig, Product


class MappingForm(forms.Form):
    csv = forms.ModelChoiceField(queryset=ImportedProductCSV.objects.all())
    config = forms.ModelChoiceField(queryset=MappingConfig.objects.all())


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
