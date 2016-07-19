from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^run_step/(?P<name>[a-zA-Z.]+)/$', views.run_step, name='run_step'),
    url(r'^run_task/(?P<name>[a-zA-Z.]+)/$', views.run_task, name='run_task'),
    url(r'^steps/$', views.steps, name='steps'),
    url(r'^tasks/$', views.tasks, name='tasks')
]
