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

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from ESSArch_Core.ip.models import ArchivistOrganization, InformationPackage

from ESSArch_Core.profiles.models import Profile, ProfileIP, SubmissionAgreement


class LockSubmissionAgreement(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.sa = SubmissionAgreement.objects.create()

    def test_lock_to_ip_without_permission(self):
        ip = InformationPackage.objects.create(SubmissionAgreement=self.sa)

        res = self.client.post('/api/submission-agreements/%s/lock/' % str(self.sa.pk), {'ip': str(ip.pk)})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_lock_to_ip_with_permission(self):
        ip = InformationPackage.objects.create(Responsible=self.user, SubmissionAgreement=self.sa)

        res = self.client.post('/api/submission-agreements/%s/lock/' % str(self.sa.pk), {'ip': str(ip.pk)})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(ArchivistOrganization.objects.exists())

    def test_new_archivist_organization(self):
        ip = InformationPackage.objects.create(Responsible=self.user, SubmissionAgreement=self.sa)
        self.sa.archivist_organization = 'ao'
        self.sa.save()

        self.client.post('/api/submission-agreements/%s/lock/' % str(self.sa.pk), {'ip': str(ip.pk)})

        ip.refresh_from_db()
        self.assertEqual(ip.ArchivistOrganization.name, 'ao')

    def test_existing_archivist_organization(self):
        ip = InformationPackage.objects.create(Responsible=self.user, SubmissionAgreement=self.sa)
        ArchivistOrganization.objects.create(name='ao')

        self.sa.archivist_organization = 'ao'
        self.sa.save()

        self.client.post('/api/submission-agreements/%s/lock/' % str(self.sa.pk), {'ip': str(ip.pk)})

        ip.refresh_from_db()
        self.assertEqual(ip.ArchivistOrganization.name, 'ao')
        self.assertEqual(ArchivistOrganization.objects.count(), 1)


class SaveSubmissionAgreement(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")

        content_type = ContentType.objects.get_for_model(SubmissionAgreement)
        perm = Permission.objects.get(
            codename='create_new_sa_generation',
            content_type=content_type,
        )
        self.user.user_permissions.add(perm)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.sa = SubmissionAgreement.objects.create()
        self.ip = InformationPackage.objects.create()

    def test_save_no_name(self):
        url = '/api/submission-agreements/%s/save/' % str(self.sa.pk)

        data = {
            'data': {'archivist_organization': 'new ao'},
            'information_package': str(self.ip.pk),
        }

        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SubmissionAgreement.objects.count(), 1)

    def test_save_empty_name(self):
        url = '/api/submission-agreements/%s/save/' % str(self.sa.pk)

        data = {
            'new_name': '',
            'data': {'archivist_organization': 'new ao'},
            'information_package': str(self.ip.pk),
        }

        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SubmissionAgreement.objects.count(), 1)

    def test_save_no_changes(self):
        url = '/api/submission-agreements/%s/save/' % str(self.sa.pk)
        self.sa.archivist_organization = 'initial'
        self.sa.save()

        data = {
            'new_name': 'new',
            'data': {'archivist_organization': 'initial'},
            'information_package': str(self.ip.pk),
        }

        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SubmissionAgreement.objects.count(), 1)

    def test_save_empty_required_value(self):
        url = '/api/submission-agreements/%s/save/' % str(self.sa.pk)
        self.sa.archivist_organization = ''
        self.sa.template = [
            {
                "key": "archivist_organization",
                "templateOptions": {
                    "required": True,
                },
            }
        ]
        self.sa.save()

        data = {
            'new_name': 'new',
            'data': {'archivist_organization': '', 'label': 'new_data'},
            'information_package': str(self.ip.pk),
        }

        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SubmissionAgreement.objects.count(), 1)

    def test_save_missing_required_value(self):
        url = '/api/submission-agreements/%s/save/' % str(self.sa.pk)
        self.sa.archivist_organization = ''
        self.sa.template = [
            {
                "key": "archivist_organization",
                "templateOptions": {
                    "required": True,
                },
            }
        ]
        self.sa.save()

        data = {
            'new_name': 'new',
            'data': {'label': 'new_data'},
            'information_package': str(self.ip.pk),
        }

        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SubmissionAgreement.objects.count(), 1)

    def test_save_changes(self):
        url = '/api/submission-agreements/%s/save/' % str(self.sa.pk)
        self.sa.archivist_organization = 'initial'
        self.sa.save()

        data = {
            'new_name': 'new',
            'data': {'archivist_organization': 'new ao'},
            'information_package': str(self.ip.pk),
        }

        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(SubmissionAgreement.objects.filter(name='', archivist_organization='initial').exists())
        self.assertTrue(SubmissionAgreement.objects.filter(name='new', archivist_organization='new ao').exists())

    def test_save_changes_without_permission(self):
        self.user.user_permissions.all().delete()
        url = '/api/submission-agreements/%s/save/' % str(self.sa.pk)
        self.sa.archivist_organization = 'initial'
        self.sa.save()

        data = {
            'new_name': 'new',
            'data': {'archivist_organization': 'new ao'},
            'information_package': str(self.ip.pk),
        }

        res = self.client.post(url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class SaveProfile(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.sa = SubmissionAgreement.objects.create()
        self.ip = InformationPackage.objects.create(
            SubmissionAgreement=self.sa,
            SubmissionAgreementLocked=True
        )

    def test_save_no_changes(self):
        profile = Profile.objects.create(
            name='first',
            profile_type='sip',
            specification_data={'foo': 'initial'},
        )

        profile_url = reverse('profile-detail', args=(profile.pk,))
        save_url = '%ssave/' % profile_url

        data = {
            'new_name': 'second',
            'information_package': str(self.ip.pk),
            'specification_data': profile.specification_data,
            'structure': {},
        }

        res = self.client.post(save_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_save_unlocked_profile(self):
        profile = Profile.objects.create(
            name='first',
            profile_type='sip',
            specification_data={'foo': 'initial'}
        )

        profile_url = reverse('profile-detail', args=(profile.pk,))
        save_url = '%ssave/' % profile_url

        data = {
            'new_name': 'second',
            'information_package': str(self.ip.pk),
            'specification_data': {'foo': 'updated'},
            'structure': {},
        }

        res = self.client.post(save_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.ip.get_profile('sip').pk, profile.pk)
        self.assertEqual(self.ip.get_profile('sip').name, data['new_name'])

    def test_save_locked_profile(self):
        profile = Profile.objects.create(
            name='first',
            profile_type='sip',
            specification_data={'foo': 'initial'}
        )

        ProfileIP.objects.create(
            ip=self.ip,
            profile=profile,
            LockedBy=self.user,
        )

        profile_url = reverse('profile-detail', args=(profile.pk,))
        save_url = '%ssave/' % profile_url

        data = {
            'new_name': 'second',
            'information_package': str(self.ip.pk),
            'specification_data': {'foo': 'updated'},
            'structure': {},
        }

        res = self.client.post(save_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.ip.get_profile('sip').pk, profile.pk)
        self.assertNotEqual(self.ip.get_profile('sip').name, data['new_name'])

    def test_save_empty_required_value(self):
        profile = Profile.objects.create(
            name='first',
            profile_type='sip',
            specification_data={'foo': 'initial'},
            template=[
                {
                    "key": "foo",
                    "templateOptions": {
                        "required": True,
                    },
                }
            ]
        )

        profile_url = reverse('profile-detail', args=(profile.pk,))
        save_url = '%ssave/' % profile_url

        data = {
            'new_name': 'second',
            'information_package': str(self.ip.pk),
            'specification_data': {'foo': ''},
            'structure': {},
        }

        res = self.client.post(save_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_save_missing_required_value(self):
        profile = Profile.objects.create(
            name='first',
            profile_type='sip',
            specification_data={'foo': 'initial'},
            template=[
                {
                    "key": "foo",
                    "templateOptions": {
                        "required": True,
                    },
                }
            ]
        )

        profile_url = reverse('profile-detail', args=(profile.pk,))
        save_url = '%ssave/' % profile_url

        data = {
            'new_name': 'second',
            'information_package': str(self.ip.pk),
            'specification_data': {},
            'structure': {},
        }

        res = self.client.post(save_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
