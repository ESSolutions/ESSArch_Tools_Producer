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
from preingest import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'information-packages', views.InformationPackageViewSet)
router.register(r'steps', views.ProcessStepViewSet)
router.register(r'tasks', views.ProcessTaskViewSet)
router.register(r'events', views.EventIPViewSet)
router.register(r'event-types', views.EventTypeViewSet)
router.register(r'submission-agreements', views.SubmissionAgreementViewSet)
router.register(r'profile-transfer-project', views.ProfileTransferProjectViewSet)
router.register(r'profile-content-type', views.ProfileContentTypeViewSet)
router.register(r'profile-data-selection', views.ProfileDataSelectionViewSet)
router.register(r'profile-classification', views.ProfileClassificationViewSet)
router.register(r'profile-import', views.ProfileImportViewSet)
router.register(r'profile-submit-description', views.ProfileSubmitDescriptionViewSet)
router.register(r'profile-sip', views.ProfileSIPViewSet)
router.register(r'profile-aip', views.ProfileAIPViewSet)
router.register(r'profile-dip', views.ProfileDIPViewSet)
router.register(r'profile-workflow', views.ProfileWorkflowViewSet)
router.register(r'profile-preservation-metadata', views.ProfilePreservationMetadataViewSet)
router.register(r'agents', views.AgentViewSet)
router.register(r'parameters', views.ParameterViewSet)
router.register(r'paths', views.PathViewSet)
router.register(r'schemas', views.SchemaViewSet)

urlpatterns = [
    url(r'^', include('frontend.urls'), name='home'),
    url(r'^preingest/', include('preingest.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^template/', include('templateMaker.urls')),
    url(r'^demo/', include('Demo.urls')),
    url(r'^accounts/login/$', auth_views.login),
]
