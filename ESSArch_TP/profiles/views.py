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

import os

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from rest_framework import exceptions, status
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from ESSArch_Core.WorkflowEngine.models import ProcessStep, ProcessTask
from ESSArch_Core.configuration.models import Path
from ESSArch_Core.ip.models import Agent, EventIP, InformationPackage
from ESSArch_Core.ip.permissions import CanLockSA
from ESSArch_Core.profiles.models import SubmissionAgreement, Profile, ProfileSA, ProfileIP
from ESSArch_Core.profiles.serializers import ProfileSerializer, ProfileDetailSerializer, ProfileWriteSerializer, \
    ProfileSASerializer, SubmissionAgreementSerializer
from ESSArch_Core.profiles.views import SubmissionAgreementViewSet as SAViewSetCore


class SubmissionAgreementViewSet(SAViewSetCore):
    @detail_route(methods=['post'], url_path='include-type')
    def include_type(self, request, pk=None):
        sa = SubmissionAgreement.objects.get(pk=pk)
        ptype = request.data["type"]

        setattr(sa, "include_profile_%s" % ptype, True)
        sa.save()

        return Response({
            'status': 'Including profile type %s in SA %s' % (ptype, sa)
        })

    @detail_route(methods=['post'], url_path='exclude-type')
    def exclude_type(self, request, pk=None):
        sa = SubmissionAgreement.objects.get(pk=pk)
        ptype = request.data["type"]

        setattr(sa, "include_profile_%s" % ptype, False)
        sa.save()

        return Response({
            'status': 'Excluding profile type %s in SA %s' % (ptype, sa)
        })

    @detail_route(methods=['post'])
    def save(self, request, pk=None):
        if not request.user.has_perm('profiles.create_new_sa_generation'):
            raise exceptions.PermissionDenied

        sa = self.get_object()

        try:
            new_name = request.data["new_name"]
        except KeyError:
            new_name = ''

        if not new_name:
            return Response(
                {'status': 'No name specified'},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_data = request.data.get("data", {})

        changed_data = False

        for field in sa.template:
            if field.get('templateOptions', {}).get('required', False):
                if not new_data.get(field['key'], None):
                    return Response(
                        {"status': 'missing required field '%s'" % field['key']},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        for k, v in new_data.iteritems():
            if v != getattr(sa, k):
                changed_data = True
                break

        if not changed_data:
            return Response({'status': 'no changes, not saving'}, status=status.HTTP_400_BAD_REQUEST)

        new_sa = sa.copy(new_data=new_data, new_name=new_name,)
        serializer = SubmissionAgreementSerializer(
            new_sa, context={'request': request}
        )
        return Response(serializer.data)

    def get_profile_types(self):
        return 'sip', 'transfer_project', 'submit_description', 'preservation_metadata'

    @transaction.atomic
    @detail_route(methods=["post"])
    def lock(self, request, pk=None):
        sa = self.get_object()
        ip_id = request.data.get("ip")
        permission = CanLockSA()

        try:
            ip = InformationPackage.objects.get(pk=ip_id)
        except InformationPackage.DoesNotExist:
            raise exceptions.ParseError('Information Package with id %s does not exist')

        if ip.submission_agreement_locked:
            raise exceptions.ParseError('IP already has a locked SA')

        if not permission.has_object_permission(request, self, ip):
            self.permission_denied(request, message=getattr(permission, 'message', None))

        if ip.submission_agreement != sa:
            raise exceptions.ParseError('This SA is not connected to the selected IP')

        ip.submission_agreement_locked = True
        if sa.archivist_organization:
            existing_agents_with_notes = Agent.objects.all().with_notes([])
            ao_agent, _ = Agent.objects.get_or_create(role='ARCHIVIST', type='ORGANIZATION',
                                                      name=sa.archivist_organization, pk__in=existing_agents_with_notes)
            ip.agents.add(ao_agent)
        ip.save()

        ip.create_profile_rels(self.get_profile_types(), request.user)
        return Response({'status': 'Locked submission agreement'})


class ProfileSAViewSet(viewsets.ModelViewSet):
    queryset = ProfileSA.objects.all()
    serializer_class = ProfileSASerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
    """
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileSerializer

        if self.action == 'retrieve':
            return ProfileDetailSerializer

        return ProfileWriteSerializer

    def get_queryset(self):
        queryset = Profile.objects.all()
        profile_type = self.request.query_params.get('type', None)

        if profile_type is not None:
            queryset = queryset.filter(profile_type=profile_type)

        return queryset

    @detail_route(methods=['post'])
    def save(self, request, pk=None):
        profile = Profile.objects.get(pk=pk)
        new_data = request.data.get("specification_data", {})
        new_structure = request.data.get("structure", {})

        changed_data = (profile.specification_data.keys().sort() == new_data.keys().sort() and
                        profile.specification_data != new_data)

        changed_structure = profile.structure != new_structure

        if (changed_data or changed_structure):
            try:
                new_profile = profile.copy(
                    specification_data=new_data,
                    new_name=request.data["new_name"],
                    structure=new_structure,
                )
            except ValidationError as e:
                return Response(e.message, status=status.HTTP_400_BAD_REQUEST)

            serializer = ProfileSerializer(
                new_profile, context={'request': request}
            )
            return Response(serializer.data)

        return Response({'status': 'no changes, not saving'}, status=status.HTTP_400_BAD_REQUEST)
