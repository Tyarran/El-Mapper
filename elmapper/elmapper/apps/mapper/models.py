# -*- coding: utf-8 -*-
import logging

from django.db import models


logger = logging.getLogger(__name__)


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

    @classmethod
    def fieldnames(cls):
        """Return the list of field names without id/pk field"""
        return [field.name for field in cls._meta.fields if field.name not in ('id', 'pk')]

    __unicode__ = __str__


class MappingConfig(models.Model):
    """A mapping options (in JSON)"""
    json = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=256)
    description = models.TextField()


class ImportedProductCSV(models.Model):
    """Given product CSV File"""
    csv_file = models.FileField()
    upload_date = models.DateTimeField(auto_now_add=True)
    mapping_config = models.ForeignKey(MappingConfig, null=True, blank=True)
