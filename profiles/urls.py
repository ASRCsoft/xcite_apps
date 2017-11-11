from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^date_range$', views.date_range, name='date_range'),
    url(r'^available_scans$', views.available_scans, name='available_scans'),
    url(r'^plot\.png$', views.plot, name='plot'),
    url(r'^datasets\.html$', views.datasets, name='datasets'),
]
