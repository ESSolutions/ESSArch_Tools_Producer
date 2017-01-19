import django_filters

from ESSArch_Core.filters import ListFilter

from ESSArch_Core.ip.models import (
    ArchivalInstitution,
    ArchivistOrganization,
    ArchivalType,
    ArchivalLocation,
    InformationPackage,
)


class InformationPackageFilter(django_filters.FilterSet):
    state = ListFilter(name='State')

    archival_institution = django_filters.UUIDFilter(name="ArchivalInstitution__pk")
    archivist_organization = django_filters.UUIDFilter(name='ArchivistOrganization__pk')
    archival_type = django_filters.UUIDFilter(name='ArchivalType__pk')
    archival_location = django_filters.UUIDFilter(name='ArchivalLocation__pk')

    class Meta:
        model = InformationPackage
        fields = [
            'state', 'archival_institution', 'archivist_organization',
            'archival_type', 'archival_location'
        ]


class ArchivalInstitutionFilter(django_filters.FilterSet):
    ip_state = ListFilter(name='information_packages__State')

    class Meta:
        model = ArchivalInstitution
        fields = ('ip_state',)


class ArchivistOrganizationFilter(django_filters.FilterSet):
    ip_state = ListFilter(name='information_packages__State')

    class Meta:
        model = ArchivistOrganization
        fields = ('ip_state',)


class ArchivalTypeFilter(django_filters.FilterSet):
    ip_state = ListFilter(name='information_packages__State')

    class Meta:
        model = ArchivalType
        fields = ('ip_state',)


class ArchivalLocationFilter(django_filters.FilterSet):
    ip_state = ListFilter(name='information_packages__State')

    class Meta:
        model = ArchivalLocation
        fields = ('ip_state',)
