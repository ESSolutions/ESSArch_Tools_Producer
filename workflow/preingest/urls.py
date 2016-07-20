from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^run_step/(?P<name>[a-zA-Z.]+)/$', views.run_step, name='run_step'),
    url(r'^run_task/(?P<name>[a-zA-Z.]+)/$', views.run_task, name='run_task'),
    url(r'^steps/$', views.steps, name='steps'),
    url(r'^tasks/$', views.tasks, name='tasks'),
    url(r'^history/$', views.history, name='history'),
    url(r'^history/(?P<step_id>[-\w]+)/$', views.history_detail, name='history_detail'),
    url(r'^undo_task/(?P<processtask_id>[-\w]+)/$', views.undo_task, name='undo_task'),
]
