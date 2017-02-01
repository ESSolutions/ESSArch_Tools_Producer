"""
    ESSArch is an open source archiving and digital preservation system

    ESSArch Tools for Producer (ETP)
    Copyright (C) 2005-2017 ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
"""

"""etp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from rest_framework import routers

from ESSArch_Core.configuration.views import (
    AgentViewSet,
    EventTypeViewSet,
    ParameterViewSet,
    PathViewSet,
    SysInfoView,
)

from ip.views import (
    ArchivalInstitutionViewSet,
    ArchivistOrganizationViewSet,
    ArchivalTypeViewSet,
    ArchivalLocationViewSet,
    EventIPViewSet,
    InformationPackageViewSet,
)

from preingest.views import (
    GroupViewSet,
    PermissionViewSet,
    ProcessStepViewSet,
    ProcessTaskViewSet,
    UserViewSet,
)

from profiles.views import (
    ProfileViewSet,
    ProfileSAViewSet,
    ProfileIPViewSet,
    SubmissionAgreementViewSet,
)

admin.site.site_header = 'ESSArch Tools Producer Administration'
admin.site.site_title = 'ESSArch Tools Producer Administration'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'archival-institutions', ArchivalInstitutionViewSet)
router.register(r'archivist-organizations', ArchivistOrganizationViewSet)
router.register(r'archival-types', ArchivalTypeViewSet)
router.register(r'archival-locations', ArchivalLocationViewSet)
router.register(r'information-packages', InformationPackageViewSet)
router.register(r'steps', ProcessStepViewSet)
router.register(r'tasks', ProcessTaskViewSet)
router.register(r'events', EventIPViewSet)
router.register(r'event-types', EventTypeViewSet)
router.register(r'submission-agreements', SubmissionAgreementViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'profile-sa', ProfileSAViewSet)
router.register(r'profile-ip', ProfileIPViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'parameters', ParameterViewSet)
router.register(r'paths', PathViewSet)

urlpatterns = [
    url(r'^', include('frontend.urls'), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/sysinfo/', SysInfoView.as_view()),
    url(r'^api/', include(router.urls)),
    url(r'^accounts/changepassword', auth_views.password_change, {'post_change_redirect': '/'} ),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^template/', include('ESSArch_Core.essxml.ProfileMaker.urls')),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]
