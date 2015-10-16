from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()


class Category(models.Model):
    label = models.CharField(max_length=250)
    description = models.TextField()


class Color(models.Model):
    name = models.CharField(max_length=250)


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    brand = models.ForeignKey(Brand)
    category = models.ForeignKey(Category)
    color = models.ForeignKey(Color)
