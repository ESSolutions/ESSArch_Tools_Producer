from django.conf.urls import patterns, url
from views import (
    PrepareIPCreate,
    CreateIPList,
    CreateIP,
)

urlpatterns = patterns('',
    url(r'^prepareipcreate/$', PrepareIPCreate.as_view(), name='create_prepareipcreate_new'),
    url(r'^prepareipcreate/$', PrepareIPCreate.as_view(), name='create_prepareipcreate'),
    url(r'^createiplist/$',CreateIPList.as_view(),name='create_createiplist'),
    url(r'^createip/(?P<id>\d+)$', CreateIP.as_view(), name='create_createip'),
)
