#!/usr/bin/env /ESSArch/python27/bin/python
# -*- coding: UTF-8 -*-
'''
    ESSArch Tools - ESSArch is an Electronic Preservation Platform
    Copyright (C) 2005-2013  ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
'''

from django.conf.urls import include, url, handler404
from django.views.generic import DetailView, ListView
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#from create.views import CreateTmpWorkareaUploadView, CreateTmpWorkareaUploadCompleteView, ETPChunkedUploadView, ETPChunkedUploadCompleteView
#from create.views import ETPChunkedUploadView, ETPChunkedUploadCompleteView
from create.views import IPcontentasJSON, ETPUploadView, ETPUploadCompleteView
from configuration.views import about, installedpackages, index
from configuration import views as configuration_views
from deliver import views as deliver_views
from logevents import views as logevents_views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # Standard URLS:
    url(r'^$', configuration_views.index, name='home'),
    #url(r'^', index, name='home'),
    #url(r'^logout$', 'configuration.views.logout_view'),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login' ),
    url(r'^accounts/login/$', auth_views.login ),
    #url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'} ),
    url(r'^accounts/logout/$', auth_views.logout, {'next_page': '/'} ),
    #url(r'^admin/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'} ),
    url(r'^admin/logout/$', auth_views.logout, {'next_page': '/'} ),
    url(r'^changepassword$', configuration_views.change_password),
    
    # URLS to include:
    #url(r'^receive/', include('receive.urls')),
    url(r'^submit/', include('submit.urls')),
    url(r'^create/', include('create.urls')),
    #url(r'^api/', include('api.urls')),

    # Configuration URLS:    
    url(r'^about$', configuration_views.sysinfo),
    #url(r'^configuration/logevents$', 'configuration.views.logevents'),
    url(r'^configuration/logevents/install_defaults$', configuration_views.installogdefaults),
    url(r'^configuration/logevents/install_defaultschemas$', configuration_views.installdefaultschemaprofiles),
    url(r'^configuration/logevents/install_defaultparameters$', configuration_views.installdefaultparameters),
    url(r'^configuration/logevents/install_defaultusers$', configuration_views.createdefaultusers),
    url(r'^installedpackages/(?P<ipid>[^&]*)$', installedpackages.as_view(), name='installedpackages'),
    #url(r'^configuration/logevents/install_defaultadditionalmetadata$', 'configuration.views.installAdditionalMetadata'),
    #url(r'^configuration/logevents/add$', 'configuration.views.newlogevent'),
    #url(r'^configuration/logevents/(?P<eventId>\d+)$', 'configuration.views.editlogevent' ),
    #url(r'^configuration/logevents/(?P<eventId>\d+)/del$', 'configuration.views.deletelogevent' ),
    #url(r'^configuration/parameters$', 'configuration.views.parameters'),
    #url(r'^configuration/parameters/(?P<username>\w+)$', 'configuration.views.userparameters'),

    # Prepare IP URLS:
    #url(r'^prepare$', 'prepare.views.index'),
    #url(r'^prepare/new$', 'prepare.views.new'),

    # Create IP URLS:
    #url(r'^create$', 'create.views.index'), ##
    #url(r'^create/(?P<id>\d+)$', 'create.views.manageip'),
    #url(r'^create/(?P<id>\d+)/create$', 'create.views.createip'),
    #url(r'^create/(?P<id>\d+)/status$', 'create.views.ipstatus'),
    #url(r'^create/(?P<id>\d+)/delete$', 'create.views.deleteip'),
    #url(r'^create/(?P<id>\d+)/fail$', 'create.views.failip'),
    #url(r'^create/(?P<id>\d+)/progress$', 'create.views.getprogress'),
    #url(r'^create/status$', 'create.views.createip'),
    #url(r'^status$', 'create.views.createip'), ##
    #url(r'^create/list$', 'create.views.listIPs'),
    #url(r'^create/(?P<id>\d+)$', 'create.views.createip'), ##
    #url(r'^create/view$', 'create.views.viewIPs'), ##
    #url(r'^create_upload/?$', CreateTmpWorkareaUploadView.as_view(), name='chunked_upload'),
    #url(r'^create_upload_complete/?$', CreateTmpWorkareaUploadCompleteView.as_view(), name='chunked_upload_complete'),
    url(r'^directoryinfo/(?P<ipid>[^&]*)$', IPcontentasJSON.as_view(), name='directoryinfo'), 
    url(r'^etp_upload/?$', ETPUploadView.as_view(), name='etp_chunked_upload'),
    #url(r'^etp_upload_complete/?$', ETPUploadCompleteView.as_view(), name='etp_chunked_upload_complete'), 
    url(r'^etp_upload_complete/(?P<ipid>[^&]*)$', ETPUploadCompleteView.as_view(), name='etp_chunked_upload_complete'),
    #url(r'^create/view/(?P<uuid>[^//]+)/(?P<creator>[^//]+)/(?P<label>[^//]+)/(?P<startdate>[^//]+)/(?P<enddate>[^//]+)/(?P<iptype>[^//]+)/(?P<createdate>[^//]+)/(?P<state>[^//]+)$', 'create.views.viewIPs'),
        
    # Deliver IP URLS:
    #url(r'^prepare$', 'prepare.views.index'),
    url(r'^deliver$', deliver_views.index),
    url(r'^deliver/(?P<id>\d+)$', deliver_views.deliverip),

    # Log Events URLS:
    url(r'^logevents$', logevents_views.index),
    url(r'^logevents/create$', logevents_views.createlog),
    url(r'^logevents/list$', logevents_views.listlog),
    #url(r'^logevents/view/(?P<uuid>[^//]+)/(?P<creator>[^//]+)/(?P<system>[^//]+)/(?P<version>[^//]+)$', 'logevents.views.viewlog'),
#    url(r'^logevents/view/(?P<uuid>[^//]+)/(?P<archivist_organization>[^//]+)/(?P<label>[^//]+)/(?P<startdate>[^//]+)/(?P<enddate>[^//]+)/(?P<iptype>[^//]+)/(?P<createdate>[^//]+)$', 'logevents.views.viewlog'),
    url(r'^logevents/view/(?P<uuid>[^//]+)/(?P<archivist_organization>[^//]+)/(?P<label>[^//]+)/(?P<iptype>[^//]+)/(?P<createdate>[^//]+)$', logevents_views.viewlog),    
    url(r'^logevents/out$', logevents_views.listlog),
    #url(r'^logevents/view$', 'logevents.views.viewlog'),
#    url(r'^logevents/(?P<id>\d+)$', 'logevents.views.viewlog'), ##
        
    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include('admin.site.urls')),
    url(r'^admin/', admin.site.urls),

    #url(r'^accounts/login/$', 'django.contrib.auth.views.login' ),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'})
    #url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    #url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'} ),
    url(r'^demo/', include('demo.urls')),
]
