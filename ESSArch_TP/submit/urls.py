from django.conf.urls import patterns, url
from views import (
    SubmitIPList,
    SubmitIPCreate,
)

urlpatterns = patterns('',   
    url(r'^submitiplist/$', SubmitIPList.as_view(),name='submit_submitiplist'),
    url(r'^submitipcreate/(?P<id>\d+)$', SubmitIPCreate.as_view(), name='submit_submitipcreate'),
)