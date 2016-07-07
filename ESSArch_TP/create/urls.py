from django.conf.urls import patterns, url
from views import (
    PrepareIPCreate,
    CreateIPList,
    CreateIP,
)
from . import views

urlpatterns = patterns('',
    url(r'^prepareipcreate/$', PrepareIPCreate.as_view(), name='create_prepareipcreate'),
    url(r'^createiplist/$',CreateIPList.as_view(),name='create_createiplist'),
    url(r'^createip/(?P<id>\d+)$', CreateIP.as_view(), name='create_createip'),
    url(r'^createiptest/$', views.index, name='create_createiptest'),
)
