from django.conf.urls import patterns, url
from views import (
    create,
    edit,
    # SubmitIPCreate,
)
# from views import {
#     create,
# }
from . import views

urlpatterns = patterns('',
    url(r'^make-old/$', views.index, name='make_template'),
    url(r'^reset/$', views.resetData, name='reset_data_template'),
    url(r'^struct/addChild/(?P<name>[A-z]+)/(?P<path>[A-z0-9-]+)/$', views.addChild, name='add_data_template'),
    url(r'^struct/(?P<name>[A-z]+)/$', views.getStruct, name='get_data_template'),
    url(r'^struct/(?P<name>[A-z0-9-]+)/(?P<uuid>[A-z0-9-]+)/$', views.getElement, name='get_element_template'),
    url(r'^make/$', create.as_view(), name='create_template'),
    url(r'^edit/$', edit.as_view(), name='edit_template'),
    # url(r'^submitipcreate/(?P<id>\d+)$', SubmitIPCreate.as_view(), name='submit_submitipcreate'),
)
