from rest_framework import serializers

from profiles.models import (
    SubmissionAgreement,
    Profile,
    ProfileLock,
    ProfileRel,
)

class ProfileLockSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProfileLock
        fields = (
            'url', 'id', 'submission_agreement', 'profile',
            'information_package',
        )


class ActiveProfileSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    url = serializers.HyperlinkedIdentityField(
        view_name='profile-detail',
        lookup_field="id",
        lookup_url_kwarg="pk"
    )

    class Meta:
        model = ProfileRel
        fields = ('url', 'id', 'name',)


class ProfileRelSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='profile.id')
    name = serializers.ReadOnlyField(source='profile.name')
    url = serializers.HyperlinkedIdentityField(
        view_name='profile-detail',
        lookup_field="profile_id",
        lookup_url_kwarg="pk"
    )

    class Meta:
        model = ProfileRel
        fields = ('url', 'id', 'name', 'status',)


class ActiveProfileRelSerializer(serializers.Serializer):
    active = ActiveProfileSerializer()
    profiles = ProfileRelSerializer(many=True, source="all")


class SubmissionAgreementSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    profile_transfer_project = ActiveProfileRelSerializer(
        source="profile_transfer_project_rel",
        read_only=True,
    )
    profile_content_type = ActiveProfileRelSerializer(
        source="profile_content_type_rel",
        read_only=True,
    )
    profile_data_selection = ActiveProfileRelSerializer(
        source="profile_data_selection_rel",
        read_only=True,
    )
    profile_classification = ActiveProfileRelSerializer(
        source="profile_classification_rel",
        read_only=True,
    )
    profile_import = ActiveProfileRelSerializer(
        source="profile_import_rel",
        read_only=True,
    )
    profile_submit_description = ActiveProfileRelSerializer(
        source="profile_submit_description_rel",
        read_only=True,
    )
    profile_sip = ActiveProfileRelSerializer(
        source="profile_sip_rel",
        read_only=True,
    )
    profile_aip = ActiveProfileRelSerializer(
        source="profile_aip_rel",
        read_only=True,
    )
    profile_dip = ActiveProfileRelSerializer(
        source="profile_dip_rel",
        read_only=True,
    )
    profile_workflow = ActiveProfileRelSerializer(
        source="profile_workflow_rel",
        read_only=True,
    )
    profile_preservation_metadata = ActiveProfileRelSerializer(
        source="profile_preservation_metadata_rel",
        read_only=True,
    )
    profile_event = ActiveProfileRelSerializer(
        source="profile_event_rel",
        read_only=True,
    )

    class Meta:
        model = SubmissionAgreement
        fields = (
                'url', 'id', 'sa_name', 'sa_type', 'sa_status', 'sa_label',
                'sa_cm_version', 'sa_cm_release_date',
                'sa_cm_change_authority', 'sa_cm_change_description',
                'sa_cm_sections_affected', 'sa_producer_organization',
                'sa_producer_main_name', 'sa_producer_main_address',
                'sa_producer_main_phone', 'sa_producer_main_email',
                'sa_producer_main_additional', 'sa_producer_individual_name',
                'sa_producer_individual_role', 'sa_producer_individual_phone',
                'sa_producer_individual_email',
                'sa_producer_individual_additional',
                'sa_archivist_organization', 'sa_archivist_main_name',
                'sa_archivist_main_address', 'sa_archivist_main_phone',
                'sa_archivist_main_email', 'sa_archivist_main_additional',
                'sa_archivist_individual_name', 'sa_archivist_individual_role',
                'sa_archivist_individual_phone',
                'sa_archivist_individual_email',
                'sa_archivist_individual_additional',
                'sa_designated_community_description',
                'sa_designated_community_individual_name',
                'sa_designated_community_individual_role',
                'sa_designated_community_individual_phone',
                'sa_designated_community_individual_email',
                'sa_designated_community_individual_additional',
                'profile_transfer_project', 'profile_content_type',
                'profile_data_selection', 'profile_classification',
                'profile_import', 'profile_submit_description', 'profile_sip',
                'profile_aip', 'profile_dip', 'profile_workflow',
                'profile_preservation_metadata', 'profile_event',
                'information_packages',
        )
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = (
            'url', 'id', 'profile_type', 'name', 'type', 'status', 'label',
            'schemas', 'representation_info', 'preservation_descriptive_info',
            'supplemental', 'access_constraints', 'datamodel_reference',
            'additional', 'submission_method', 'submission_schedule',
            'submission_data_inventory', 'structure', 'template',
            'specification', 'specification_data', 'submission_agreements',
        )
