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

import os
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from ESSArch_Core.configuration.models import (
    Path,
)

from ESSArch_Core.ip.models import (
    InformationPackage,
)

from ESSArch_Core.WorkflowEngine.models import (
    ProcessTask,
)


class test_tasks(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root = os.path.dirname(os.path.realpath(__file__))
        cls.prepare_path = os.path.join(cls.root, "prepare")
        cls.preingest_reception = os.path.join(cls.root, "preingest_reception")
        cls.ingest_reception = os.path.join(cls.root, "ingest_reception")

        for path in [cls.prepare_path, cls.preingest_reception, cls.ingest_reception]:
            try:
                os.makedirs(path)
            except OSError as e:
                if e.errno != 17:
                    raise

        Path.objects.create(
            entity="path_preingest_prepare",
            value=cls.prepare_path
        )
        Path.objects.create(
            entity="path_preingest_reception",
            value=cls.preingest_reception
        )
        Path.objects.create(
            entity="path_ingest_reception",
            value=cls.ingest_reception
        )

    @classmethod
    def tearDownClass(cls):
        for path in [cls.prepare_path, cls.preingest_reception, cls.ingest_reception]:
            try:
                shutil.rmtree(path)
            except:
                pass

        super(test_tasks, cls).tearDownClass()

    def setUp(self):
        settings.CELERY_ALWAYS_EAGER = True
        settings.CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

    def test_prepare_ip(self):
        label = "ip1"
        user = User.objects.create(username="user1")

        task = ProcessTask(
            name="preingest.tasks.PrepareIP",
            params={
                "label": label,
                "responsible": user
            },
            responsible=user
        )
        task.run()

        self.assertTrue(
            InformationPackage.objects.filter(Label=label).exists()
        )

        task.undo()

        self.assertFalse(
            InformationPackage.objects.filter(Label=label).exists()
        )

    def test_create_ip_root_dir(self):
        ip = InformationPackage.objects.create(Label="ip1")
        prepare_path = Path.objects.get(entity="path_preingest_prepare").value
        prepare_path = os.path.join(prepare_path, unicode(ip.pk))

        task = ProcessTask(
            name="preingest.tasks.CreateIPRootDir",
            params={
                "information_package": ip,
            },
        )
        task.run()

        self.assertTrue(
            os.path.isdir(prepare_path)
        )

        task.undo()

        self.assertFalse(
            os.path.isdir(prepare_path)
        )

    def test_create_physical_model(self):
        ip = InformationPackage.objects.create(Label="ip1")
        prepare_path = Path.objects.get(entity="path_preingest_prepare").value
        path = os.path.join(prepare_path, unicode(ip.pk))

        task = ProcessTask(
            name="preingest.tasks.CreatePhysicalModel",
            params={
                "structure": [
                    {
                        "name": "dir1",
                        "type": "folder"
                    },
                    {
                        "name": "dir2",
                        "type": "folder",
                    },
                    {
                        "name": "file1",
                        "type": "file"
                    }
                ]
            },
            information_package=ip,
        )
        task.run()

        self.assertTrue(
            os.path.isdir(os.path.join(path, 'dir1'))
        )
        self.assertTrue(
            os.path.isdir(os.path.join(path, 'dir2'))
        )
        self.assertFalse(
            os.path.isfile(os.path.join(path, 'file1'))
        )

        task.undo()

        self.assertFalse(
            os.path.isdir(os.path.join(path, 'dir1'))
        )
        self.assertFalse(
            os.path.isdir(os.path.join(path, 'dir2'))
        )

    def test_create_tar(self):
        # create directory
        prepare_path = Path.objects.get(entity="path_preingest_prepare").value
        dirname = os.path.join(prepare_path, "tardir")
        os.makedirs(dirname)

        # create empty file
        filename = os.path.join(dirname, "file.txt")
        open(filename, "a").close()

        tarname = dirname + ".tar"

        task = ProcessTask(
            name="preingest.tasks.CreateTAR",
            params={
                "dirname": dirname,
                "tarname": tarname
            },
        )
        task.run()

        self.assertTrue(
            os.path.isdir(dirname)
        )
        self.assertTrue(
            os.path.isfile(filename)
        )
        self.assertTrue(
            os.path.isfile(tarname)
        )

        shutil.rmtree(dirname)
        task.undo()

        self.assertTrue(
            os.path.isdir(dirname)
        )
        self.assertTrue(
            os.path.isfile(filename)
        )
        self.assertFalse(
            os.path.isfile(tarname)
        )

    def test_create_zip(self):
        # create directory
        prepare_path = Path.objects.get(entity="path_preingest_prepare").value
        dirname = os.path.join(prepare_path, "zipdir")
        os.makedirs(dirname)

        # create empty file
        filename = os.path.join(dirname, "file.txt")
        open(filename, "a").close()

        zipname = dirname + ".zip"

        task = ProcessTask(
            name="preingest.tasks.CreateZIP",
            params={
                "dirname": dirname,
                "zipname": zipname
            },
        )
        task.run()

        self.assertTrue(
            os.path.isdir(dirname)
        )
        self.assertTrue(
            os.path.isfile(filename)
        )
        self.assertTrue(
            os.path.isfile(zipname)
        )

        shutil.rmtree(dirname)
        task.undo()

        self.assertTrue(
            os.path.isdir(dirname)
        )
        self.assertTrue(
            os.path.isfile(filename)
        )
        self.assertFalse(
            os.path.isfile(zipname)
        )

    def test_submit_sip(self):
        ip = InformationPackage.objects.create(Label="ip1")

        srctar = os.path.join(self.preingest_reception, "%s.tar" % ip.pk)
        srcxml = os.path.join(self.preingest_reception, "%s.xml" % ip.pk)
        dsttar = os.path.join(self.ingest_reception, "%s.tar" % ip.pk)
        dstxml = os.path.join(self.ingest_reception, "%s.xml" % ip.pk)
        open(srctar, "a").close()
        open(srcxml, "a").close()

        task = ProcessTask(
            name="preingest.tasks.SubmitSIP",
            params={
                "ip": ip
            },
        )
        task.run()

        self.assertTrue(os.path.isfile(dsttar))
        self.assertTrue(os.path.isfile(dstxml))

        task.undo()

        self.assertFalse(os.path.isfile(dsttar))
        self.assertFalse(os.path.isfile(dstxml))
