import django_filters

from ESSArch_Core.filters import ListFilter

from ESSArch_Core.ip.models import InformationPackage


class InformationPackageFilter(django_filters.FilterSet):
    state = ListFilter(name='State')

    archival_institution = django_filters.CharFilter(name="ArchivalInstitution__name")
    archivist_organization = django_filters.CharFilter(name='ArchivistOrganization__name')
    archival_type = django_filters.CharFilter(name='ArchivalType__name')
    archival_location = django_filters.CharFilter(name='ArchivalLocation__name')

    class Meta:
        model = InformationPackage
        fields = [
            'state', 'archival_institution', 'archivist_organization',
            'archival_type', 'archival_location'
        ]
