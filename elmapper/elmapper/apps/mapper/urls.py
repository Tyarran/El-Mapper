from django.conf.urls import include, url
from django.contrib import admin

from elmapper.apps.mapper import views

urlpatterns = [
    url(r'^$', views.test_view),
]
