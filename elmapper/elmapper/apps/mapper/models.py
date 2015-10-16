# -*- coding: utf-8 -*-
from django.db import models


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


class FieldMappingConfig(models.Model):
    """A mapping between an external and an internal field name"""
    original_field_name = models.CharField(max_length=250)
    product_field = models.CharField(
        max_length=250,
        choices=tuple([(field.name, field.name) for field in Product._meta.fields]),
    )

    def __str__(self):
        return "{} => {}".format(self.original_field_name, self.product_field)

    __unicode__ = __str__


class MappingConfig(models.Model):
    """Base class for obj mapping"""
    original_fk = models.CharField(max_length=250)

    def __str__(self):
        return "{} => {}".format(self.original_field_name, self.internal_fk)

    __unicode__ = __str__

    class Meta:
        abstract = True  # It´s just a abstract class. Don´t let Django creates the associated table


class CategoryConfig(MappingConfig):
    """A mapping between an external and an internal category foreign keys"""
    internal_fk = models.ForeignKey(Category)


class ColorConfig(MappingConfig):
    """A mapping between an external and an internal color foreign keys"""
    internal_fk = models.ForeignKey(Color)


class BrandConfig(MappingConfig):
    """A mapping between an external and an internal brand foreign keys"""
    internal_fk = models.ForeignKey(Brand)
