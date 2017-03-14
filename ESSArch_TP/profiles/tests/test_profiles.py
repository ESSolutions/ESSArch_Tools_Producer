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

from rest_framework import status
from rest_framework.test import APIClient

from ESSArch_Core.ip.models import InformationPackage

from ESSArch_Core.profiles.models import SubmissionAgreement


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
