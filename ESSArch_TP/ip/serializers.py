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
    ProfileIPSerializer,
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
    profile_transfer_project = ProfileIPSerializer(
        source="profile_transfer_project_rel",
        read_only=True,
    )
    profile_content_type = ProfileIPSerializer(
        source="profile_content_type_rel",
        read_only=True,
    )
    profile_data_selection = ProfileIPSerializer(
        source="profile_data_selection_rel",
        read_only=True,
    )
    profile_classification = ProfileIPSerializer(
        source="profile_classification_rel",
        read_only=True,
    )
    profile_import = ProfileIPSerializer(
        source="profile_import_rel",
        read_only=True,
    )
    profile_submit_description = ProfileIPSerializer(
        source="profile_submit_description_rel",
        read_only=True,
    )
    profile_sip = ProfileIPSerializer(
        source="profile_sip_rel",
        read_only=True,
    )
    profile_aip = ProfileIPSerializer(
        source="profile_aip_rel",
        read_only=True,
    )
    profile_dip = ProfileIPSerializer(
        source="profile_dip_rel",
        read_only=True,
    )
    profile_workflow = ProfileIPSerializer(
        source="profile_workflow_rel",
        read_only=True,
    )
    profile_preservation_metadata = ProfileIPSerializer(
        source="profile_preservation_metadata_rel",
        read_only=True,
    )
    profile_event = ProfileIPSerializer(
        source="profile_event_rel",
        read_only=True,
    )

    class Meta:
        model = InformationPackage
        fields = (
            'url', 'id', 'Label', 'Content', 'Responsible', 'CreateDate',
            'State', 'status', 'step_state', 'ObjectSize', 'ObjectNumItems', 'ObjectPath',
            'Startdate', 'Enddate', 'OAIStype', 'SubmissionAgreement',
            'ArchivalInstitution', 'ArchivistOrganization', 'ArchivalType',
            'ArchivalLocation', 'SubmissionAgreementLocked',
            'profile_transfer_project', 'profile_content_type',
            'profile_data_selection', 'profile_classification',
            'profile_import', 'profile_submit_description', 'profile_sip',
            'profile_aip', 'profile_dip', 'profile_workflow',
            'profile_preservation_metadata', 'profile_event',
        )

class EventIPSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventIP
        fields = (
                'url', 'id', 'eventType', 'eventDateTime', 'eventDetail',
                'eventApplication', 'eventVersion', 'eventOutcome',
                'eventOutcomeDetailNote', 'linkingAgentIdentifierValue',
                'linkingObjectIdentifierValue',
        )
