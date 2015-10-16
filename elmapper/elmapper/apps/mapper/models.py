# -*- coding: utf-8 -*-
import csv
import itertools
import logging

from django.db import models

PRODUCT_FIELDS = [
    ('name', 'name'),
    ('description', 'description'),
    ('price', 'price'),
    ('brand', 'brand'),
    ('category', 'category'),
    ('color', 'color'),
]


logger = logging.getLogger(__name__)


def get_field_by_name(model_class, field_name):
    """Return specific field for given model class"""
    return [field for field in model_class._meta.fields if field.name == field_name][0]


def get_mapping_modelclass(model_class):
    """Return the mapping config class for given model class"""
    return [klass for klass in CONFIG_CLASSES
            if get_field_by_name(klass, "internal").related_model == model_class.related_model][0]


class Brand(models.Model):
    """Product Brand"""
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    __unicode__ = __str__


class Category(models.Model):
    """Product category"""
    label = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.label

    __unicode__ = __str__


class Color(models.Model):
    """Product color"""
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    __unicode__ = __str__


class Product(models.Model):
    """The product model"""
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    brand = models.ForeignKey(Brand)
    category = models.ForeignKey(Category)
    color = models.ForeignKey(Color)

    def __str__(self):
        return self.name

    __unicode__ = __str__


class ImportedProductCSV(models.Model):
    """Given product CSV File"""
    csv_file = models.FileField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def save(self):
        known_columns = FieldMappingConfig.objects.values_list('product_field', flat=True)
        csv_reader = csv.reader(self.csv_file, delimiter=",", quotechar="\"")
        headers = csv_reader.next()

        # Determine readable fields
        fields = [field for field in headers if field in known_columns]

        # Read rows
        for row in csv_reader:
            mapped_fields = {key: value for key, value in itertools.izip(headers, row)
                             if key in fields}
            result_fields = {}

            for field_name, field_value in mapped_fields.items():
                field_class = [field for field in Product._meta.fields if field.name == field_name][0]
                if isinstance(field_class, models.ForeignKey):
                    mapping_class = get_mapping_modelclass(field_class)
                    result_fields[field_name] = mapping_class.objects.get(original_fk=field_value).internal
                else:
                    result_fields[field_name] = field_value

            #product = Product(**{key: value for key, value in itertools.izip(headers, row)})
            product = Product(**result_fields)
            logging.info(str(product))
            product.save()


class FieldMappingConfig(models.Model):
    """A mapping between an external and an internal field name"""
    original_field_name = models.CharField(max_length=250)
    product_field = models.CharField(
        max_length=250,
        choices=PRODUCT_FIELDS,
    )

    def __str__(self):
        return "{} => {}".format(self.original_field_name, self.product_field)

    __unicode__ = __str__


class MappingConfig(models.Model):
    """Base class for obj mapping"""
    original_fk = models.CharField(max_length=250)
    internal = None  # map to this object

    def __str__(self):
        return "{} => {}".format(self.original_fk, self.internal)

    __unicode__ = __str__

    class Meta:
        abstract = True  # It´s just a abstract class. Don´t let Django creates the associated table


class CategoryConfig(MappingConfig):
    """A mapping between an external and an internal category foreign keys"""
    internal = models.ForeignKey(Category)


class ColorConfig(MappingConfig):
    """A mapping between an external and an internal color foreign keys"""
    internal = models.ForeignKey(Color)


class BrandConfig(MappingConfig):
    """A mapping between an external and an internal brand foreign keys"""
    internal = models.ForeignKey(Brand)


CONFIG_CLASSES = [CategoryConfig, ColorConfig, BrandConfig]
