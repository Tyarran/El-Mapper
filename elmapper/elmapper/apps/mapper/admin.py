from django.contrib import admin

from elmapper.apps.mapper import models

admin.site.register(models.Product)
admin.site.register(models.Brand)
admin.site.register(models.Category)
admin.site.register(models.Color)
admin.site.register(models.ImportedProductCSV)
admin.site.register(models.FieldMappingConfig)
admin.site.register(models.CategoryConfig)
admin.site.register(models.ColorConfig)
admin.site.register(models.BrandConfig)
