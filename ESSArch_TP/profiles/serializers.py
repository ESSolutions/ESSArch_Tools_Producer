from rest_framework import serializers

from ESSArch_Core.profiles.models import (
    SubmissionAgreement,
    Profile,
    ProfileSA,
    ProfileIP
)

class ProfileSASerializer(serializers.HyperlinkedModelSerializer):
    profile_type = serializers.SerializerMethodField()

    def get_profile_type(self, obj):
        return obj.profile.profile_type

    class Meta:
        model = ProfileSA
        fields = (
            'url', 'id', 'profile', 'submission_agreement', 'profile_type', 'LockedBy', 'Unlockable'
        )

class ProfileIPSerializer(serializers.HyperlinkedModelSerializer):
    profile_type = serializers.SerializerMethodField()

    def get_profile_type(self, obj):
        return obj.profile.profile_type

    class Meta:
        model = ProfileIP
        fields = (
            'url', 'id', 'profile', 'ip', 'profile_type', 'LockedBy', 'Unlockable',
        )


class SubmissionAgreementSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    profile_transfer_project = ProfileSASerializer(
        source="profile_transfer_project_rel",
        read_only=True,
    )
    profile_content_type = ProfileSASerializer(
        source="profile_content_type_rel",
        read_only=True,
    )
    profile_data_selection = ProfileSASerializer(
        source="profile_data_selection_rel",
        read_only=True,
    )
    profile_classification = ProfileSASerializer(
        source="profile_classification_rel",
        read_only=True,
    )
    profile_import = ProfileSASerializer(
        source="profile_import_rel",
        read_only=True,
    )
    profile_submit_description = ProfileSASerializer(
        source="profile_submit_description_rel",
        read_only=True,
    )
    profile_sip = ProfileSASerializer(
        source="profile_sip_rel",
        read_only=True,
    )
    profile_aip = ProfileSASerializer(
        source="profile_aip_rel",
        read_only=True,
    )
    profile_dip = ProfileSASerializer(
        source="profile_dip_rel",
        read_only=True,
    )
    profile_workflow = ProfileSASerializer(
        source="profile_workflow_rel",
        read_only=True,
    )
    profile_preservation_metadata = ProfileSASerializer(
        source="profile_preservation_metadata_rel",
        read_only=True,
    )
    profile_event = ProfileSASerializer(
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
                'information_packages', 'profile_transfer_project',
                'profile_content_type', 'profile_data_selection',
                'profile_classification', 'profile_import',
                'profile_submit_description', 'profile_sip', 'profile_aip',
                'profile_dip', 'profile_workflow',
                'profile_preservation_metadata', 'profile_event',
                'include_profile_transfer_project',
                'include_profile_content_type',
                'include_profile_data_selection',
                'include_profile_classification', 'include_profile_import',
                'include_profile_submit_description', 'include_profile_sip',
                'include_profile_aip', 'include_profile_dip',
                'include_profile_workflow',
                'include_profile_preservation_metadata',
                'include_profile_event',
        )

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = (
            'url', 'id', 'profile_type', 'name', 'type', 'status', 'label',
            'schemas', 'representation_info', 'preservation_descriptive_info',
            'supplemental', 'access_constraints', 'datamodel_reference',
            'cm_release_date', 'cm_change_authority', 'cm_change_description',
            'cm_sections_affected','cm_version', 'additional',
            'submission_method', 'submission_schedule',
            'submission_data_inventory', 'structure', 'template',
            'specification_data',
        )
