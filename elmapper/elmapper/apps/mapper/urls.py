from django.conf.urls import url

from elmapper.apps.mapper import views

urlpatterns = [
    url(r'^$', views.ResultListView.as_view()),
    url(r'^result/(?P<pk>[-\w]+)$', views.ResultDetailView.as_view(), name='result-detail'),
]
