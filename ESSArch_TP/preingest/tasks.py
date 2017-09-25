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
import uuid
from urlparse import urljoin

import requests

from ESSArch_Core.configuration.models import Path
from ESSArch_Core.WorkflowEngine.dbtask import DBTask
from ESSArch_Core.ip.models import InformationPackage
from ESSArch_Core.storage.copy import copy_file
from ESSArch_Core.WorkflowEngine.models import ProcessTask, ProcessStep
from ESSArch_Core.util import (
    delete_content
)
from ESSArch_Core import tasks


class PrepareIP(DBTask):
    event_type = 10100

    def run(self, label="", responsible={}, object_identifier_value=None, step=None):
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
            object_identifier_value=object_identifier_value,
            label=label,
            responsible_id=responsible,
            state="Preparing",
            package_type=InformationPackage.SIP,
        )

        self.ip = ip.pk

        ProcessTask.objects.filter(pk=self.request.id).update(
            information_package=ip
        )

        if step is not None:
            s = ProcessStep.objects.get(pk=step)
            ip.steps.add(s)

        self.set_progress(100, total=100)

        return ip.pk

    def undo(self, label="", responsible={}, object_identifier_value=None, step=None):
        ProcessTask.objects.get(pk=self.request.id).undone_task.information_package.delete()

    def event_outcome_success(self, label="", responsible={}, object_identifier_value=None, step=None):
        return "Prepared IP with label '%s'" % label


class CreateIPRootDir(DBTask):
    event_type = 10200

    def create_path(self, information_package_id):
        prepare_path = Path.objects.get(
            entity="path_preingest_prepare"
        ).value

        dirname = InformationPackage.objects.values_list(
            'object_identifier_value', flat=True
        ).get(pk=information_package_id)

        return os.path.join(prepare_path, dirname)

    def run(self, information_package=None):
        """
        Creates the IP root directory

        Args:
            information_package_id: The id of the information package the
            directory will be created for

        Returns:
            None
        """

        self.ip = information_package

        ProcessTask.objects.filter(pk=self.request.id).update(
            information_package_id=information_package
        )

        path = self.create_path(information_package)
        os.makedirs(path)

        InformationPackage.objects.filter(pk=information_package).update(
            object_path=path
        )

        self.set_progress(100, total=100)
        return information_package

    def undo(self, information_package=None):
        path = self.create_path(information_package)
        shutil.rmtree(path)

    def event_outcome_success(self, information_package=None):
        return "Created root directory for IP '%s'" % information_package


class CreatePhysicalModel(DBTask):
    event_type = 10300

    def get_root(self):
        root = Path.objects.get(
            entity="path_preingest_prepare"
        ).value
        return os.path.join(root, unicode(self.ip))

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
        return "Created physical model for IP '%s'" % self.ip


class SubmitSIP(DBTask):
    event_type = 10500

    def run(self, ip=None):
        ip = InformationPackage.objects.get(pk=ip)

        srcdir = Path.objects.get(entity="path_preingest_reception").value
        reception = Path.objects.get(entity="path_ingest_reception").value
        container_format = ip.get_container_format()
        src = os.path.join(srcdir, ip.object_identifier_value + ".%s" % container_format)

        try:
            remote = ip.get_profile('transfer_project').specification_data.get(
                'preservation_organization_receiver_url'
            )
        except AttributeError:
            remote = None

        session = None

        if remote:
            try:
                dst, remote_user, remote_pass = remote.split(',')
                dst = urljoin(dst, 'api/ip-reception/upload/')

                session = requests.Session()
                session.verify = False
                session.auth = (remote_user, remote_pass)
            except ValueError:
                remote = None
        else:
            dst = os.path.join(reception, ip.object_identifier_value + ".%s" % container_format)
        copy_file(src, dst, requests_session=session)

        src = os.path.join(srcdir, ip.object_identifier_value + ".xml")
        if not remote:
            dst = os.path.join(reception, ip.object_identifier_value + ".xml")
        copy_file(src, dst, requests_session=session)

        self.set_progress(100, total=100)

    def undo(self, ip=None):
        ip = InformationPackage.objects.get(pk=ip)

        reception = Path.objects.get(entity="path_ingest_reception").value
        container_format = ip.get_container_format()

        tar = os.path.join(reception, ip.object_identifier_value + ".%s" % container_format)
        xml = os.path.join(reception, ip.object_identifier_value + ".xml")

        os.remove(tar)
        os.remove(xml)

    def event_outcome_success(self, ip=None):
        return "Submitted %s" % (ip)
