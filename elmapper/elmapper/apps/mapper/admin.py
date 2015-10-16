from django.contrib import admin

from elmapper.apps.mapper import models

admin.site.register(models.Product)
admin.site.register(models.Brand)
admin.site.register(models.Category)
admin.site.register(models.Color)
