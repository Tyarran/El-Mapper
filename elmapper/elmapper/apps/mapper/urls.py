from django.conf.urls import url

from elmapper.apps.mapper import views

urlpatterns = [
    url(r'^$', views.ImportCSVView.as_view()),
    url(r'^mapping_result/(?P<pk>[0-9]*)$', views.MappingResultView.as_view(), name='mapping_result'),
]
