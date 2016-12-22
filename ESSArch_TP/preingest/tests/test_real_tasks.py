import os
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from install.install_default_config_etp import installDefaultEventTypes

from ESSArch_Core.configuration.models import (
    Path,
)

from ESSArch_Core.ip.models import (
    EventIP,
    InformationPackage,
)

from ESSArch_Core.WorkflowEngine.models import (
    ProcessTask,
)


def setUpModule():
    installDefaultEventTypes()


class test_tasks(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root = os.path.dirname(os.path.realpath(__file__))
        cls.prepare_path = os.path.join(cls.root, "prepare")

        try:
            os.makedirs(cls.prepare_path)
        except OSError as e:
            if e.errno != 17:
                raise

        Path.objects.create(
            entity="path_preingest_prepare",
            value=cls.prepare_path
        )

    @classmethod
    def tearDownClass(cls):
        try:
            shutil.rmtree(cls.prepare_path)
        except:
            pass
        finally:
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
            log=EventIP,
            responsible=user
        )
        task.run()

        self.assertTrue(
            InformationPackage.objects.filter(Label=label).exists()
        )

        self.assertTrue(
            EventIP.objects.filter(
                linkingAgentIdentifierValue=user,
                linkingObjectIdentifierValue__Label=label
            ).exists()
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
