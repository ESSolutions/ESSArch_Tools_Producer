from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^run/(?P<name>[a-zA-Z.]+)/$', views.run, name='run'),
    url(r'^steps/$', views.steps, name='steps'),
    url(r'^tasks/$', views.tasks, name='tasks')
]
