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

from ESSArch_Core.WorkflowEngine.views import ProcessViewSet, ProcessStepViewSet, ProcessTaskViewSet
from ESSArch_Core.auth.views import GroupViewSet, PermissionViewSet, MeView, UserViewSet, NotificationViewSet
from ESSArch_Core.configuration.views import ParameterViewSet, PathViewSet, SysInfoView
from ESSArch_Core.fixity.views import ValidationViewSet
from ESSArch_Core.ip.views import AgentViewSet, EventIPViewSet
from ESSArch_Core.profiles.views import ProfileIPViewSet, ProfileIPDataViewSet, ProfileIPDataTemplateViewSet, \
    InformationPackageProfileIPViewSet
from ESSArch_Core.routers import ESSArchRouter
from configuration.views import EventTypeViewSet
from ip.views import InformationPackageViewSet
from profiles.views import ProfileViewSet, ProfileSAViewSet, SubmissionAgreementViewSet

admin.site.site_header = 'ESSArch Tools Producer Administration'
admin.site.site_title = 'ESSArch Tools Producer Administration'

router = ESSArchRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'information-packages', InformationPackageViewSet)
router.register(r'information-packages', InformationPackageViewSet).register(
    r'events',
    EventIPViewSet,
    base_name='ip-events',
    parents_query_lookups=['linkingObjectIdentifierValue']
)
router.register(r'information-packages', InformationPackageViewSet).register(
    r'profiles',
    InformationPackageProfileIPViewSet,
    base_name='ip-profiles',
    parents_query_lookups=['ip']
)
router.register(r'notifications', NotificationViewSet)
router.register(r'steps', ProcessStepViewSet)
router.register(r'steps', ProcessStepViewSet, base_name='steps').register(
    r'tasks',
    ProcessTaskViewSet,
    base_name='steps-tasks',
    parents_query_lookups=['processstep']
)
router.register(r'steps', ProcessStepViewSet, base_name='steps').register(
    r'children',
    ProcessViewSet,
    base_name='steps-children',
    parents_query_lookups=['processstep']
)
router.register(r'tasks', ProcessTaskViewSet)
router.register(r'tasks', ProcessTaskViewSet).register(
    r'validations',
    ValidationViewSet,
    base_name='task-validations',
    parents_query_lookups=['task']
)
router.register(r'events', EventIPViewSet)
router.register(r'event-types', EventTypeViewSet)
router.register(r'submission-agreements', SubmissionAgreementViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'profile-sa', ProfileSAViewSet)
router.register(r'profile-ip', ProfileIPViewSet)
router.register(r'profile-ip-data', ProfileIPDataViewSet)
router.register(r'profile-ip-data-templates', ProfileIPDataTemplateViewSet)
router.register(r'parameters', ParameterViewSet)
router.register(r'paths', PathViewSet)

urlpatterns = [
    url(r'^', include('frontend.urls'), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/sysinfo/', SysInfoView.as_view()),
    url(r'^api/me/$', MeView.as_view(), name='me'),
    url(r'^api/', include(router.urls)),
    url(r'^accounts/changepassword', auth_views.password_change, {'post_change_redirect': '/'} ),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('ESSArch_Core.docs.urls')),
    url(r'^template/', include('ESSArch_Core.essxml.ProfileMaker.urls')),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^rest-auth/', include('ESSArch_Core.auth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]
