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

import filecmp
import glob
import os
import shutil

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import F
from django.test import TestCase
from django.urls import reverse

import mock

from rest_framework import status
from rest_framework.test import APIClient

from ESSArch_Core.configuration.models import EventType, Path
from ESSArch_Core.ip.models import InformationPackage
from ESSArch_Core.profiles.models import Profile, ProfileIP, SubmissionAgreement
from ESSArch_Core.WorkflowEngine.models import ProcessTask


class test_create_ip(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.root = os.path.dirname(os.path.realpath(__file__))
        self.datadir = os.path.join(self.root, 'datadir')

        Path.objects.create(entity='path_preingest_prepare', value=self.datadir)

        self.url = reverse('informationpackage-list')

        try:
            os.mkdir(self.datadir)
        except OSError as e:
            if e.errno != 17:
                raise

    def tearDown(self):
        try:
            shutil.rmtree(self.datadir)
        except:
            pass

    def test_create_ip(self):
        data = {'label': 'my label', 'object_identifier_value': 'my objid'}

        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            InformationPackage.objects.filter(
                Responsible=self.user,
                Label=data['label'],
                ObjectIdentifierValue=data['object_identifier_value'],
            ).exists()
        )

    def test_create_ip_without_objid(self):
        data = {'label': 'my label'}

        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        InformationPackage.objects.filter(
            Responsible=self.user,
            Label=data['label'],
            ObjectIdentifierValue=F('pk')
        ).exists()

    def test_create_ip_without_label(self):
        data = {'object_identifier_value': 'my objid'}

        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertFalse(InformationPackage.objects.exists())

    def test_create_ip_with_same_objid_as_existing(self):
        existing = InformationPackage.objects.create(ObjectIdentifierValue='objid')

        data = {'label': 'my label', 'object_identifier_value': 'objid'}

        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(InformationPackage.objects.count(), 1)
        self.assertEqual(InformationPackage.objects.first().pk, existing.pk)

    def test_create_ip_with_same_label_as_existing(self):
        InformationPackage.objects.create(Label='label')

        data = {'label': 'label'}

        res = self.client.post(self.url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InformationPackage.objects.filter(Label='label').count(), 2)


class test_delete_ip(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.root = os.path.dirname(os.path.realpath(__file__))
        self.datadir = os.path.join(self.root, 'datadir')

        self.ip = InformationPackage.objects.create(ObjectPath=self.datadir)
        self.url = reverse('informationpackage-detail', args=(str(self.ip.pk),))

        try:
            os.mkdir(self.datadir)
        except OSError as e:
            if e.errno != 17:
                raise

    def tearDown(self):
        try:
            shutil.rmtree(self.datadir)
        except:
            pass

    def test_delete_ip_without_permission(self):
        res = self.client.delete(self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(os.path.exists(self.datadir))

    def test_delete_ip_with_permission(self):
        InformationPackage.objects.filter(pk=self.ip.pk).update(
            Responsible=self.user
        )

        res = self.client.delete(self.url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(os.path.exists(self.datadir))


class test_submit_ip(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.root = os.path.dirname(os.path.realpath(__file__))
        self.datadir = os.path.join(self.root, 'datadir')

        Path.objects.create(entity='path_preingest_prepare', value=self.datadir)
        Path.objects.create(entity='path_preingest_reception', value=self.datadir)

        self.ip = InformationPackage.objects.create()
        self.url = reverse('informationpackage-detail', args=(self.ip.pk,))
        self.url = self.url + 'submit/'

        try:
            os.mkdir(self.datadir)
        except OSError as e:
            if e.errno != 17:
                raise

    def tearDown(self):
        try:
            shutil.rmtree(self.datadir)
        except:
            pass

    def test_not_responsible(self):
        res = self.client.post(self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_created(self):
        self.ip.Responsible = self.user
        self.ip.save()
        res = self.client.post(self.url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_submit_description_profile(self):
        self.ip.Responsible = self.user
        self.ip.State = 'Created'
        self.ip.save()
        res = self.client.post(self.url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('ip.views.creation_date', return_value=0)
    @mock.patch('ip.views.ProcessStep.run')
    def test_no_mail(self, mock_step, mock_time):
        self.ip.Responsible = self.user
        self.ip.State = 'Created'
        self.ip.save()

        sd = Profile.objects.create(profile_type='submit_description')
        ProfileIP.objects.create(ip=self.ip, profile=sd)

        res = self.client.post(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertFalse(ProcessTask.objects.filter(name="ESSArch_Core.tasks.SendEmail").exists())
        mock_step.assert_called_once()

    def test_with_mail_without_subject(self):
        self.ip.Responsible = self.user
        self.ip.State = 'Created'
        self.ip.save()

        tp = Profile.objects.create(
            profile_type='transfer_project',
            specification_data={'preservation_organization_receiver_email': 'foo'}
        )
        ProfileIP.objects.create(ip=self.ip, profile=tp)

        res = self.client.post(self.url, {'body': 'foo'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_mail_without_body(self):
        self.ip.Responsible = self.user
        self.ip.State = 'Created'
        self.ip.save()

        tp = Profile.objects.create(
            profile_type='transfer_project',
            specification_data={'preservation_organization_receiver_email': 'foo'}
        )
        ProfileIP.objects.create(ip=self.ip, profile=tp)

        res = self.client.post(self.url, {'subject': 'foo'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('ip.views.creation_date', return_value=0)
    @mock.patch('ip.views.ProcessStep.run')
    def test_with_mail(self, mock_step, mock_time):
        self.ip.Responsible = self.user
        self.ip.State = 'Created'
        self.ip.save()

        tp = Profile.objects.create(
            profile_type='transfer_project',
            specification_data={'preservation_organization_receiver_email': 'foo'}
        )
        ProfileIP.objects.create(ip=self.ip, profile=tp)

        sd = Profile.objects.create(profile_type='submit_description')
        ProfileIP.objects.create(ip=self.ip, profile=sd)

        res = self.client.post(self.url, {'subject': 'foo', 'body': 'bar'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertTrue(ProcessTask.objects.filter(name="ESSArch_Core.tasks.SendEmail").exists())
        mock_step.assert_called_once()


class test_set_uploaded(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.ip = InformationPackage.objects.create()
        self.url = reverse('informationpackage-detail', args=(str(self.ip.pk),))

    def test_set_uploaded_without_permission(self):
        res = self.client.post('%sset-uploaded/' % self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.ip.refresh_from_db()
        self.assertEqual(self.ip.State, '')

    def test_set_uploaded_with_permission(self):
        InformationPackage.objects.filter(pk=self.ip.pk).update(
            Responsible=self.user
        )

        res = self.client.post('%sset-uploaded/' % self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.ip.refresh_from_db()
        self.assertEqual(self.ip.State, 'Uploaded')


class test_upload(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', password='pass')
        self.client = APIClient()
        self.client.login(username='user', password='pass')

        EventType.objects.create(eventType=10120)

        self.root = os.path.dirname(os.path.realpath(__file__))
        self.datadir = os.path.join(self.root, 'datadir')
        self.src = os.path.join(self.datadir, 'src')
        self.dst = os.path.join(self.datadir, 'dst')

        self.ip = InformationPackage.objects.create(ObjectPath=self.dst)
        self.baseurl = reverse('informationpackage-detail', args=(self.ip.pk,))

        for path in [self.src, self.dst]:
            try:
                os.makedirs(path)
            except OSError as e:
                if e.errno != 17:
                    raise

    def tearDown(self):
        try:
            shutil.rmtree(self.datadir)
        except:
            pass

    def test_upload_file(self):
        InformationPackage.objects.filter(pk=self.ip.pk).update(
            Responsible=self.user
        )

        srcfile = os.path.join(self.src, 'foo.txt')
        srcfile_chunk = os.path.join(self.src, 'foo.txt_chunk')
        dstfile = os.path.join(self.dst, 'foo.txt')

        with open(srcfile, 'w') as fp:
            fp.write('bar')

        open(srcfile_chunk, 'a').close()

        fsize = os.path.getsize(srcfile)
        block_size = 1
        i = 0
        total = 0

        with open(srcfile) as fp, open(srcfile_chunk, 'r+') as chunk:
            while total < fsize:
                chunk = SimpleUploadedFile(srcfile_chunk, fp.read(block_size), content_type='multipart/form-data')
                data = {
                    'flowChunkNumber': i,
                    'flowRelativePath': os.path.basename(srcfile),
                    'file': chunk,
                }
                res = self.client.post(self.baseurl + 'upload/', data, format='multipart')
                self.assertEqual(res.status_code, status.HTTP_200_OK)
                total += block_size
                i += 1

        data = {'path': dstfile}
        res = self.client.post(self.baseurl + 'merge-uploaded-chunks/', data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        uploaded_chunks = glob.glob('%s_*' % dstfile)

        self.assertTrue(filecmp.cmp(srcfile, dstfile, False))
        self.assertEqual(uploaded_chunks, [])

    def test_upload_without_permission(self):
        srcfile = os.path.join(self.src, 'foo.txt')

        with open(srcfile, 'w') as fp:
            fp.write('bar')

        with open(srcfile) as fp:
            chunk = SimpleUploadedFile(srcfile, fp.read(), content_type='multipart/form-data')
            data = {
                'flowChunkNumber': 0,
                'flowRelativePath': os.path.basename(srcfile),
                'file': chunk,
            }
            res = self.client.post(self.baseurl + 'upload/', data, format='multipart')
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_file_with_square_brackets_in_name(self):
        InformationPackage.objects.filter(pk=self.ip.pk).update(
            Responsible=self.user
        )

        srcfile = os.path.join(self.src, 'foo[asd].txt')
        dstfile = os.path.join(self.dst, 'foo[asd].txt')

        with open(srcfile, 'w') as fp:
            fp.write('bar')

        with open(srcfile) as fp:
            chunk = SimpleUploadedFile(srcfile, fp.read(), content_type='multipart/form-data')
            data = {
                'flowChunkNumber': 0,
                'flowRelativePath': os.path.basename(srcfile),
                'file': chunk,
            }
            self.client.post(self.baseurl + 'upload/', data, format='multipart')

            data = {'path': dstfile}
            self.client.post(self.baseurl + 'merge-uploaded-chunks/', data)
            self.assertTrue(filecmp.cmp(srcfile, dstfile, False))


class test_change_sa(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.ip = InformationPackage.objects.create(Responsible=self.user)
        self.url = reverse('informationpackage-detail', args=(str(self.ip.pk),))

        self.sa = SubmissionAgreement.objects.create()
        self.sa_url = reverse('submissionagreement-detail', args=(str(self.sa.pk),))

    def test_no_sa(self):
        res = self.client.patch(self.url, {'SubmissionAgreement': self.sa_url}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.ip.refresh_from_db()
        self.assertEqual(self.ip.SubmissionAgreement, self.sa)

    def test_unlocked_sa(self):
        self.ip.SubmissionAgreement = SubmissionAgreement.objects.create()
        self.ip.save()

        res = self.client.patch(self.url, {'SubmissionAgreement': self.sa_url}, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.ip.refresh_from_db()
        self.assertEqual(self.ip.SubmissionAgreement, self.sa)

    def test_locked_sa(self):
        self.ip.SubmissionAgreement = SubmissionAgreement.objects.create()
        self.ip.SubmissionAgreementLocked = True
        self.ip.save()

        res = self.client.patch(self.url, {'SubmissionAgreement': self.sa_url}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.ip.refresh_from_db()
        self.assertNotEqual(self.ip.SubmissionAgreement, self.sa)


class test_change_profile(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.ip = InformationPackage.objects.create(Responsible=self.user)
        self.url = reverse('informationpackage-detail', args=(str(self.ip.pk),))
        self.url = '%schange-profile/' % self.url

        self.profile_type = 'foo'
        self.profile = Profile.objects.create(profile_type=self.profile_type)

    def test_no_profile(self):
        res = self.client.put(self.url, {'new_profile': str(self.profile.pk)}, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(ProfileIP.objects.filter(profile=self.profile, ip=self.ip).exists())

    def test_unlocked_profile(self):
        ProfileIP.objects.create(profile=Profile.objects.create(profile_type=self.profile_type), ip=self.ip)
        res = self.client.put(self.url, {'new_profile': str(self.profile.pk)}, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(ProfileIP.objects.filter(profile=self.profile, ip=self.ip).exists())

    def test_locked_profile(self):
        ProfileIP.objects.create(
            profile=Profile.objects.create(profile_type=self.profile_type), ip=self.ip, LockedBy=self.user
        )
        res = self.client.put(self.url, {'new_profile': str(self.profile.pk)}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(ProfileIP.objects.filter(profile=self.profile, ip=self.ip).exists())
