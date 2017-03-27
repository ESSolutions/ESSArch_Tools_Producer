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
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from ESSArch_Core.configuration.models import EventType
from ESSArch_Core.ip.models import InformationPackage


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
        ip = InformationPackage.objects.create(ObjectPath=self.dst)
        baseurl = reverse('informationpackage-detail', args=(ip.pk,))

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
                self.client.post(baseurl + 'upload/', data, format='multipart')
                total += block_size
                i += 1

        data = {'path': dstfile}
        self.client.post(baseurl + 'merge-uploaded-chunks/', data)

        uploaded_chunks = glob.glob('%s_*' % dstfile)

        self.assertTrue(filecmp.cmp(srcfile, dstfile, False))
        self.assertEqual(uploaded_chunks, [])
