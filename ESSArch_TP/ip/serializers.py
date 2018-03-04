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

from _version import get_versions
from guardian.shortcuts import get_perms
from rest_framework import serializers

from ESSArch_Core.auth.serializers import UserSerializer
from ESSArch_Core.ip.models import (
    InformationPackage
)
from ESSArch_Core.ip.serializers import (
    ArchivalInstitutionSerializer,
    ArchivistOrganizationSerializer,
    ArchivalTypeSerializer,
    ArchivalLocationSerializer,
)
from ESSArch_Core.profiles.models import SubmissionAgreement
from ESSArch_Core.profiles.serializers import (
    ProfileIPSerializer,
)

VERSION = get_versions()['version']


class InformationPackageSerializer(serializers.HyperlinkedModelSerializer):
    responsible = UserSerializer()
    profiles = ProfileIPSerializer(many=True)
    submission_agreement = serializers.PrimaryKeyRelatedField(queryset=SubmissionAgreement.objects.all())
    archival_institution = ArchivalInstitutionSerializer(read_only=True)
    archivist_organization = ArchivistOrganizationSerializer(read_only=True)
    archival_type = ArchivalTypeSerializer(read_only=True)
    archival_location = ArchivalLocationSerializer(read_only=True)
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        request = self.context.get('request')
        if hasattr(request, 'user'):
            return get_perms(request.user, obj)

        return []

    class Meta:
        model = InformationPackage
        fields = (
            'url', 'id', 'object_identifier_value', 'label', 'content',
            'responsible', 'create_date', 'entry_date', 'state', 'status', 'step_state',
            'object_path', 'object_size', 'object_num_items', 'start_date',
            'end_date', 'package_type', 'submission_agreement',
            'archival_institution', 'archivist_organization', 'archival_type',
            'archival_location', 'submission_agreement_locked', 'profiles',
            'permissions',
        )


class InformationPackageReadSerializer(InformationPackageSerializer):
    def to_representation(self, obj):
        data = super(InformationPackageReadSerializer, self).to_representation(obj)
        profiles = data['profiles']
        data['profiles'] = {}

        types = [
            'transfer_project', 'content_type', 'data_selection',
            'authority_information', 'archival_description',
            'import', 'submit_description', 'sip', 'aip',
            'dip', 'workflow', 'preservation_metadata',
        ]

        for ptype in types:
            data['profile_%s' % ptype] = None

        for p in profiles:
            data['profile_%s' % p['profile_type']] = p

        data.pop('profiles', None)

        return data

    class Meta:
        model = InformationPackageSerializer.Meta.model
        fields = InformationPackageSerializer.Meta.fields

