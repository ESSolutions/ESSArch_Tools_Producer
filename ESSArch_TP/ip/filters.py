import django_filters

from ESSArch_Core.filters import ListFilter

from ESSArch_Core.ip.models import InformationPackage


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
