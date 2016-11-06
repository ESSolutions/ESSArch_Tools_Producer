from rest_framework import serializers

from ESSArch_Core.ip.models import (
    ArchivalInstitution,
    ArchivistOrganization,
    ArchivalType,
    ArchivalLocation,
    EventIP,
    InformationPackage
)

from preingest.serializers import ProcessStepSerializer

from profiles.serializers import (
    SAIPLockSerializer,
)

class ArchivalInstitutionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArchivalInstitution
        fields = ('url', 'id', 'name', 'information_packages',)

class ArchivistOrganizationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArchivistOrganization
        fields = ('url', 'id', 'name', 'information_packages',)

class ArchivalTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArchivalType
        fields = ('url', 'id', 'name', 'information_packages',)

class ArchivalLocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArchivalLocation
        fields = ('url', 'id', 'name', 'information_packages',)

class InformationPackageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InformationPackage
        fields = (
            'url', 'id', 'Label', 'Content', 'Responsible', 'CreateDate',
            'State', 'status', 'step_state', 'ObjectSize', 'ObjectNumItems', 'ObjectPath',
            'Startdate', 'Enddate', 'OAIStype', 'SubmissionAgreement',
            'ArchivalInstitution', 'ArchivistOrganization', 'ArchivalType',
            'ArchivalLocation',
        )


class InformationPackageDetailSerializer(InformationPackageSerializer):
    locks = SAIPLockSerializer(many=True)

    class Meta:
        model = InformationPackageSerializer.Meta.model
        fields = InformationPackageSerializer.Meta.fields + ('locks',)


class EventIPSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventIP
        fields = (
                'url', 'id', 'eventType', 'eventDateTime', 'eventDetail',
                'eventApplication', 'eventVersion', 'eventOutcome',
                'eventOutcomeDetailNote', 'linkingAgentIdentifierValue',
                'linkingObjectIdentifierValue',
        )
