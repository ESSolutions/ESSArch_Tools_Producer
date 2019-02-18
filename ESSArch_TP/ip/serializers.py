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

from rest_framework import serializers

from ESSArch_Core.ip.serializers import InformationPackageSerializer as CoreInformationPackageSerializer
from ESSArch_Core.profiles.serializers import ProfileIPSerializer
from ESSArch_Core.profiles.utils import profile_types


class InformationPackageSerializer(CoreInformationPackageSerializer):
    profiles = serializers.SerializerMethodField()

    def get_profiles(self, obj):
        profiles = getattr(obj, 'profiles', obj.profileip_set)
        return ProfileIPSerializer(profiles, many=True, context=self.context).data

    class Meta(CoreInformationPackageSerializer.Meta):
        fields = CoreInformationPackageSerializer.Meta.fields + ('profiles',)


class InformationPackageReadSerializer(InformationPackageSerializer):
    def to_representation(self, obj):
        data = super().to_representation(obj)
        profiles = data['profiles']
        data['profiles'] = {}

        for ptype in profile_types:
            data['profile_%s' % ptype] = None

        for p in profiles:
            data['profile_%s' % p['profile_type']] = p

        data.pop('profiles', None)

        return data

    class Meta:
        model = InformationPackageSerializer.Meta.model
        fields = InformationPackageSerializer.Meta.fields
