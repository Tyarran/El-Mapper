from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    __unicode__ = __str__


class Category(models.Model):
    label = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.label

    __unicode__ = __str__


class Color(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    __unicode__ = __str__


class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    brand = models.ForeignKey(Brand)
    category = models.ForeignKey(Category)
    color = models.ForeignKey(Color)

    def __str__(self):
        return self.name

    __unicode__ = __str__
