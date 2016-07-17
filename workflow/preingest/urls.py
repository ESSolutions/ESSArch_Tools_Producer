from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^run/(?P<name>[a-zA-Z.]+)/$', views.run, name='run')
]
