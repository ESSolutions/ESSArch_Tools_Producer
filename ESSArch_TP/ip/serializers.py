from rest_framework import serializers

from ESSArch_Core.ip.models import (
    ArchivalInstitution,
    ArchivistOrganization,
    ArchivalType,
    ArchivalLocation,
    EventIP,
    InformationPackage
)

from ESSArch_Core.serializers import DynamicHyperlinkedModelSerializer

from preingest.serializers import UserSerializer

from ESSArch_Core.profiles.serializers import (
    ProfileIPSerializer,
)

class ArchivalInstitutionSerializer(DynamicHyperlinkedModelSerializer):
    class Meta:
        model = ArchivalInstitution
        fields = ('url', 'id', 'name', 'information_packages',)

class ArchivistOrganizationSerializer(DynamicHyperlinkedModelSerializer):
    class Meta:
        model = ArchivistOrganization
        fields = ('url', 'id', 'name', 'information_packages',)

class ArchivalTypeSerializer(DynamicHyperlinkedModelSerializer):
    class Meta:
        model = ArchivalType
        fields = ('url', 'id', 'name', 'information_packages',)

class ArchivalLocationSerializer(DynamicHyperlinkedModelSerializer):
    class Meta:
        model = ArchivalLocation
        fields = ('url', 'id', 'name', 'information_packages',)

class InformationPackageSerializer(serializers.HyperlinkedModelSerializer):
    Responsible = UserSerializer()
    profiles = ProfileIPSerializer(many=True)
    ArchivalInstitution = ArchivalInstitutionSerializer(
        fields=['url', 'id', 'name']
    )
    ArchivistOrganization = ArchivistOrganizationSerializer(
        fields=['url', 'id', 'name']
    )
    ArchivalType = ArchivalTypeSerializer(
        fields=['url', 'id', 'name']
    )
    ArchivalLocation = ArchivalLocationSerializer(
        fields=['url', 'id', 'name']
    )

    def to_representation(self, obj):
        data = super(InformationPackageSerializer, self).to_representation(obj)
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
        model = InformationPackage
        fields = (
            'url', 'id', 'Label', 'Content', 'Responsible', 'CreateDate',
            'State', 'status', 'step_state', 'ObjectPath',
            'Startdate', 'Enddate', 'OAIStype', 'SubmissionAgreement',
            'ArchivalInstitution', 'ArchivistOrganization', 'ArchivalType',
            'ArchivalLocation', 'SubmissionAgreementLocked', 'profiles',
        )

class InformationPackageDetailSerializer(InformationPackageSerializer):
    ObjectSize = serializers.SerializerMethodField()
    ObjectNumItems = serializers.SerializerMethodField()

    def _get_object_size_and_num(self, obj):
        if not hasattr(self, '_object_size_and_num'):
            self._object_size_and_num = obj.ObjectSizeAndNum
        return self._object_size_and_num

    def get_ObjectSize(self, obj):
        size, _ = self._get_object_size_and_num(obj)
        return size

    def get_ObjectNumItems(self, obj):
        _, num = self._get_object_size_and_num(obj)
        return num

    class Meta:
        model = InformationPackageSerializer.Meta.model
        fields = InformationPackageSerializer.Meta.fields + (
            'ObjectSize', 'ObjectNumItems',
        )


class EventIPSerializer(serializers.HyperlinkedModelSerializer):
    linkingAgentIdentifierValue = UserSerializer()
    eventDetail = serializers.SlugRelatedField(slug_field='eventDetail', source='eventType', read_only=True)

    class Meta:
        model = EventIP
        fields = (
                'url', 'id', 'eventType', 'eventDateTime', 'eventDetail',
                'eventApplication', 'eventVersion', 'eventOutcome',
                'eventOutcomeDetailNote', 'linkingAgentIdentifierValue',
                'linkingObjectIdentifierValue',
        )
