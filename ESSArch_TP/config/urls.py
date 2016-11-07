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

from configuration.views import (
    AgentViewSet,
    EventTypeViewSet,
    ParameterViewSet,
    PathViewSet,
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
    url(r'^api/', include(router.urls)),
    url(r'^accounts/changepassword', auth_views.password_change, {'post_change_redirect': '/'} ),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^template/', include('ESSArch_Core.xml.ProfileMaker.urls')),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]
