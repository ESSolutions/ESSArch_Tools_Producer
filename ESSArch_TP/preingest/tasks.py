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

from __future__ import absolute_import

import os
import shutil
import tarfile
import zipfile

from ESSArch_Core.configuration.models import Path
from ESSArch_Core.WorkflowEngine.dbtask import DBTask
from ESSArch_Core.ip.models import InformationPackage
from ESSArch_Core.WorkflowEngine.models import ProcessTask, ProcessStep
from ESSArch_Core.util import (
    delete_content
)
from ESSArch_Core import tasks


class PrepareIP(DBTask):
    event_type = 10100

    def run(self, label="", responsible={}, step=None):
        """
        Prepares a new information package

        Args:
            label: The label of the IP to prepare
            responsible: The responsible user of the IP to prepare
            step: The step to connect the IP to

        Returns:
            The id of the created information package
        """

        ip = InformationPackage.objects.create(
            Label=label,
            Responsible=responsible,
            State="Preparing",
            OAIStype="SIP",
        )

        self.taskobj.information_package = ip
        self.taskobj.save()

        if step is not None:
            s = ProcessStep.objects.get(pk=step)
            ip.steps.add(s)

        self.set_progress(100, total=100)

        return ip

    def undo(self, label="", responsible={}, step=None):
        self.taskobj.information_package.delete()

    def event_outcome_success(self, label="", responsible={}, step=None):
        return "Prepared IP with label '%s'" % label


class CreateIPRootDir(DBTask):
    event_type = 10110

    def create_path(self, information_package_id):
        prepare_path = Path.objects.get(
            entity="path_preingest_prepare"
        ).value

        return os.path.join(
            prepare_path,
            unicode(information_package_id)
        )

    def run(self, information_package=None):
        """
        Creates the IP root directory

        Args:
            information_package_id: The id of the information package the
            directory will be created for

        Returns:
            None
        """

        self.taskobj.information_package = information_package
        self.taskobj.save()

        path = self.create_path(str(information_package.pk))
        os.makedirs(path)

        information_package.ObjectPath = path
        information_package.save()

        self.set_progress(100, total=100)
        return information_package

    def undo(self, information_package=None):
        path = self.create_path(information_package.pk)
        shutil.rmtree(path)

    def event_outcome_success(self, information_package=None):
        return "Created root directory for IP '%s'" % information_package.pk


class CreatePhysicalModel(DBTask):
    event_type = 10115

    def get_root(self):
        root = Path.objects.get(
            entity="path_preingest_prepare"
        ).value
        return os.path.join(root, unicode(self.taskobj.information_package.pk))

    def run(self, structure={}, root=""):
        """
        Creates the IP physical model based on a logical model.

        Args:
            structure: A dict specifying the logical model.
            root: The root directory to be used
        """

        if not root:
            root = self.get_root()

        try:
            delete_content(root)
        except OSError as e:
            if e.errno != 2:
                raise

        for content in structure:
            if content.get('type') == 'folder':
                name = content.get('name')
                dirname = os.path.join(root, name)
                os.makedirs(dirname)

                self.run(content.get('children', []), dirname)

        self.set_progress(1, total=1)

    def undo(self, structure={}, root=""):
        if not root:
            root = self.get_root()

        for content in structure:
            if content.get('type') == 'folder':
                name = content.get('name')
                dirname = os.path.join(root, name)
                shutil.rmtree(dirname)

    def event_outcome_success(self, structure={}, root=""):
        return "Created physical model for IP '%s'" % self.taskobj.information_package.pk


class CalculateChecksum(tasks.CalculateChecksum):
    event_type = 10210


class IdentifyFileFormat(tasks.IdentifyFileFormat):
    event_type = 10220


class GenerateXML(tasks.GenerateXML):
    event_type = 10230


class AppendEvents(tasks.AppendEvents):
    event_type = 10240


class CopySchemas(tasks.CopySchemas):
    event_type = 10250


class ValidateFileFormat(tasks.ValidateFileFormat):
    event_type = 10260


class ValidateXMLFile(tasks.ValidateXMLFile):
    event_type = 10261


class ValidateLogicalPhysicalRepresentation(tasks.ValidateLogicalPhysicalRepresentation):
    event_type = 10262


class ValidateIntegrity(tasks.ValidateIntegrity):
    event_type = 10263


class ValidateFiles(tasks.ValidateFiles):
    fileformat_task = "preingest.tasks.ValidateFileFormat"
    checksum_task = "preingest.tasks.ValidateIntegrity"


class CreateTAR(DBTask):
    event_type = 10270

    """
    Creates a TAR file from the specified directory

    Args:
        dirname: The directory to create a TAR from
        tarname: The name of the tar file
    """

    def run(self, dirname=None, tarname=None):
        base_dir = os.path.basename(os.path.normpath(dirname))
        with tarfile.TarFile(tarname, 'w') as new_tar:
            new_tar.add(dirname, base_dir)

        self.set_progress(100, total=100)
        return tarname

    def undo(self, dirname=None, tarname=None):
        parent_dir = os.path.dirname((os.path.normpath(dirname)))

        with tarfile.open(tarname, 'r') as tar:
            tar.extractall(parent_dir)

        os.remove(tarname)

    def event_outcome_success(self, dirname=None, tarname=None):
        return "Created %s from %s" % (tarname, dirname)


class CreateZIP(DBTask):
    event_type = 10271

    """
    Creates a ZIP file from the specified directory

    Args:
        dirname: The directory to create a ZIP from
        zipname: The name of the zip file
    """

    def run(self, dirname=None, zipname=None):
        with zipfile.ZipFile(zipname, 'w') as new_zip:
            for root, dirs, files in os.walk(dirname):
                for d in dirs:
                    filepath = os.path.join(root, d)
                    arcname = filepath[len(dirname) + 1:]
                    new_zip.write(filepath, arcname)
                for f in files:
                    filepath = os.path.join(root, f)
                    arcname = filepath[len(dirname) + 1:]
                    new_zip.write(filepath, arcname)

        self.set_progress(100, total=100)
        return zipname

    def undo(self, dirname=None, zipname=None):
        with zipfile.ZipFile(zipname, 'r') as z:
            z.extractall(dirname)

        os.remove(zipname)

    def event_outcome_success(self, dirname=None, zipname=None):
        return "Created %s from %s" % (zipname, dirname)


class DeleteFiles(tasks.DeleteFiles):
    event_type = 10275


class UpdateIPStatus(tasks.UpdateIPStatus):
    event_type = 10280


class UpdateIPPath(tasks.UpdateIPPath):
    event_type = 10285


class SubmitSIP(DBTask):
    event_type = 10300

    def run(self, ip=None):
        srcdir = Path.objects.get(entity="path_preingest_reception").value
        reception = Path.objects.get(entity="path_ingest_reception").value
        container_format = ip.get_container_format()

        src = os.path.join(srcdir, str(ip.pk) + ".%s" % container_format)
        dst = os.path.join(reception, str(ip.pk) + ".%s" % container_format)

        ProcessTask.objects.create(
            name="ESSArch_Core.tasks.CopyFile",
            params={
                'src': src,
                'dst': dst
            },
            processstep=self.taskobj.processstep,
            hidden=True
        ).run().get()

        src = os.path.join(srcdir, str(ip.pk) + ".xml")
        dst = os.path.join(reception, str(ip.pk) + ".xml")

        ProcessTask.objects.create(
            name="ESSArch_Core.tasks.CopyFile",
            params={
                'src': src,
                'dst': dst
            },
            processstep=self.taskobj.processstep,
            hidden=True
        ).run().get()

        self.set_progress(100, total=100)

    def undo(self, ip=None):
        reception = Path.objects.get(entity="path_ingest_reception").value
        container_format = ip.get_container_format()

        tar = os.path.join(reception, str(ip.pk) + ".%s" % container_format)
        xml = os.path.join(reception, str(ip.pk) + ".xml")

        os.remove(tar)
        os.remove(xml)

    def event_outcome_success(self, ip=None):
        return "Submitted %s" % (ip.pk)
