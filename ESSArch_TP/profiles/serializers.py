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


class SubmissionAgreementSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    profile_transfer_project = ProfileRelSerializer(
        source="profile_transfer_project_rel",
        many=True,
        read_only=True,
    )
    profile_content_type = ProfileRelSerializer(
        source="profile_content_type_rel",
        many=True,
        read_only=True,
    )
    profile_data_selection = ProfileRelSerializer(
        source="profile_data_selection_rel",
        many=True,
        read_only=True,
    )
    profile_classification = ProfileRelSerializer(
        source="profile_classification_rel",
        many=True,
        read_only=True,
    )
    profile_import = ProfileRelSerializer(
        source="profile_import_rel",
        many=True,
        read_only=True,
    )
    profile_submit_description = ProfileRelSerializer(
        source="profile_submit_description_rel",
        many=True,
        read_only=True,
    )
    profile_sip = ProfileRelSerializer(
        source="profile_sip_rel",
        many=True,
        read_only=True,
    )
    profile_aip = ProfileRelSerializer(
        source="profile_aip_rel",
        many=True,
        read_only=True,
    )
    profile_dip = ProfileRelSerializer(
        source="profile_dip_rel",
        many=True,
        read_only=True,
    )
    profile_workflow = ProfileRelSerializer(
        source="profile_workflow_rel",
        many=True,
        read_only=True,
    )
    profile_preservation_metadata = ProfileRelSerializer(
        source="profile_preservation_metadata_rel",
        many=True,
        read_only=True,
    )
    profile_event = ProfileRelSerializer(
        source="profile_event_rel",
        many=True,
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
