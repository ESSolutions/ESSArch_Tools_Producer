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

from django_filters import rest_framework as filters

from ESSArch_Core.filters import ListFilter

from ESSArch_Core.ip.models import (
    ArchivalInstitution,
    ArchivistOrganization,
    ArchivalType,
    ArchivalLocation,
    InformationPackage,
)


class InformationPackageFilter(filters.FilterSet):
    state = ListFilter(name='State')

    archival_institution = filters.UUIDFilter(name="ArchivalInstitution__pk", label='Archival Institution')
    archivist_organization = filters.UUIDFilter(name='ArchivistOrganization__pk', label='Archivist Organization')
    archival_type = filters.UUIDFilter(name='ArchivalType__pk', label='Archival Type')
    archival_location = filters.UUIDFilter(name='ArchivalLocation__pk', label='Archival Location')

    class Meta:
        model = InformationPackage
        fields = [
            'state', 'archival_institution', 'archivist_organization',
            'archival_type', 'archival_location'
        ]


class ArchivalInstitutionFilter(filters.FilterSet):
    ip_state = ListFilter(name='information_packages__State', distinct=True)

    class Meta:
        model = ArchivalInstitution
        fields = ('ip_state',)


class ArchivistOrganizationFilter(filters.FilterSet):
    ip_state = ListFilter(name='information_packages__State', distinct=True)

    class Meta:
        model = ArchivistOrganization
        fields = ('ip_state',)


class ArchivalTypeFilter(filters.FilterSet):
    ip_state = ListFilter(name='information_packages__State', distinct=True)

    class Meta:
        model = ArchivalType
        fields = ('ip_state',)


class ArchivalLocationFilter(filters.FilterSet):
    ip_state = ListFilter(name='information_packages__State', distinct=True)

    class Meta:
        model = ArchivalLocation
        fields = ('ip_state',)
