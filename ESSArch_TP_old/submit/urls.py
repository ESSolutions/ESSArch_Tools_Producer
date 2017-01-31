from django.conf.urls import url
from views import (
    SubmitIPList,
    SubmitIPCreate,
)

urlpatterns = [   
    url(r'^submitiplist/$', SubmitIPList.as_view(),name='submit_submitiplist'),
    url(r'^submitipcreate/(?P<id>\d+)$', SubmitIPCreate.as_view(), name='submit_submitipcreate'),
]
