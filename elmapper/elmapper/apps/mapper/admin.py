from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import RegexURLPattern 

from elmapper.apps.mapper import models


#class ImportedProductCSVAdmin(admin.ModelAdmin):

#    def get_urls(self):

#        urls = super(ImportedProductCSVAdmin, self).get_urls()
#        my_urls = RegexURLPattern(r'^my_view/$', test_view, name="")
#        import ipdb; ipdb.set_trace()
#        #return [my_urls] + urls
#        return [my_urls]

#        #def save_model(self, request, obj, form, change):
#        #    import ipdb; ipdb.set_trace()


admin.site.register(models.Product)
admin.site.register(models.Brand)
admin.site.register(models.Category)
admin.site.register(models.Color)
admin.site.register(models.ImportedProductCSV)
#admin.site.register(models.FieldMappingConfig)
admin.site.register(models.MappingConfig)
