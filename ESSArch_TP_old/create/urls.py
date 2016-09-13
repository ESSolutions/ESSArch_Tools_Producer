from django.conf.urls import url
from views import (
    PrepareIPCreate,
    CreateIPList,
    CreateIP,
)
from . import views

urlpatterns = [
    url(r'^prepareipcreate/$', PrepareIPCreate.as_view(), name='create_prepareipcreate_new'),
    url(r'^prepareipcreate/$', PrepareIPCreate.as_view(), name='create_prepareipcreate'),
    url(r'^createiplist/$',CreateIPList.as_view(),name='create_createiplist'),
    url(r'^createip/(?P<id>\d+)$', CreateIP.as_view(), name='create_createip'),
]
