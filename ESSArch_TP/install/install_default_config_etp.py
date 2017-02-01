# -*- coding: UTF-8 -*-

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

import django
django.setup()

from django.contrib.auth.models import User, Group, Permission
from ESSArch_Core.configuration.models import EventType, Path


def installDefaultConfiguration():
    print "Installing users, groups and permissions..."
    installDefaultUsers()
    print "\nInstalling paths..."
    installDefaultPaths()
    print "\nInstalling event types..."
    installDefaultEventTypes()

    return 0


def installDefaultUsers():
    user_user, _ = User.objects.get_or_create(
        username='user', email='usr1@essolutions.se'
    )
    user_user.set_password('user')
    user_user.save()

    user_admin, _ = User.objects.get_or_create(
        username='admin', email='admin@essolutions.se',
        is_staff=True
    )
    user_admin.set_password('admin')
    user_admin.save()

    user_sysadmin, _ = User.objects.get_or_create(
        username='sysadmin', email='sysadmin@essolutions.se',
        is_staff=True, is_superuser=True
    )
    user_sysadmin.set_password('sysadmin')
    user_sysadmin.save()

    group_user, _ = Group.objects.get_or_create(name='user')
    group_admin, _ = Group.objects.get_or_create(name='admin')
    group_sysadmin, _ = Group.objects.get_or_create(name='sysadmin')

    can_add_ip_event = Permission.objects.get(codename='add_eventip')
    can_change_ip_event = Permission.objects.get(codename='change_eventip')
    can_delete_ip_event = Permission.objects.get(codename='delete_eventip')

    group_user.permissions.add(can_add_ip_event, can_change_ip_event, can_delete_ip_event)

    group_user.user_set.add(user_user)
    group_admin.user_set.add(user_admin)
    group_sysadmin.user_set.add(user_sysadmin)

    return 0


def installDefaultPaths():
    dct = {
        'path_mimetypes_definitionfile': '/ESSArch/config/mime.types',
        'path_definitions': '/ESSArch/etp/env',
        'path_preingest_prepare': '/ESSArch/data/etp/prepare',
        'path_preingest_reception': '/ESSArch/data/etp/reception',
        'path_ingest_reception': '/ESSArch/data/eta/reception/eft',
    }

    for key in dct:
        print '-> %s: %s' % (key, dct[key])
        Path.objects.get_or_create(entity=key, value=dct[key])

    return 0


def installDefaultEventTypes():
    dct = {
        'Other': '10000',
        'Prepare IP': '10100',
        'Create IP root directory': '10110',
        'Create physical model': '10115',
        'Upload file': '10120',
        'Create SIP': '10200',
        'Calculate checksum ': '10210',
        'Identify format': '10220',
        'Generate XML files': '10230',
        'Append events': '10240',
        'Copy schemas': '10250',
        'Validate file format': '10260',
        'Validate XML file': '10261',
        'Validate logical representation against physical representation': '10262',
        'Validate checksum': '10263',
        'Create TAR': '10270',
        'Create ZIP': '10271',
        'Delete files': '10275',
        'Update IP status': '10280',
        'Update IP path': '10285',
        'Submit SIP': '10300',
    }

    for key in dct:
        print '-> %s: %s' % (key, dct[key])
        EventType.objects.get_or_create(eventType=dct[key], eventDetail=key)

    return 0


if __name__ == '__main__':
    installDefaultConfiguration()
