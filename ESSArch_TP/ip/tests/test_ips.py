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

from rest_framework import status
from rest_framework.test import APIClient

from ESSArch_Core.configuration.models import EventType
from ESSArch_Core.ip.models import InformationPackage


class test_create_ip(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.root = os.path.dirname(os.path.realpath(__file__))
        self.datadir = os.path.join(self.root, 'datadir')

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
                chunk = SimpleUploadedFile(srcfile_chunk, fp.read(block_size), content_type='multipary/form-data')
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
            chunk = SimpleUploadedFile(srcfile, fp.read(), content_type='multipary/form-data')
            data = {
                'flowChunkNumber': 0,
                'flowRelativePath': os.path.basename(srcfile),
                'file': chunk,
            }
            res = self.client.post(self.baseurl + 'upload/', data, format='multipart')
            self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
