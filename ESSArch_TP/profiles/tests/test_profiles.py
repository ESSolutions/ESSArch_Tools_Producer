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

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from ESSArch_Core.ip.models import InformationPackage

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
