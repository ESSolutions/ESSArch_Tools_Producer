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

import requests
from django.db import transaction
from six.moves.urllib.parse import urljoin

# noinspection PyUnresolvedReferences
from ESSArch_Core import tasks  # noqa
from ESSArch_Core.WorkflowEngine.dbtask import DBTask
from ESSArch_Core.configuration.models import Path
from ESSArch_Core.ip.models import Agent, InformationPackage
from ESSArch_Core.ip.utils import get_cached_objid
from ESSArch_Core.storage.copy import copy_file


class ReceiveSIP(DBTask):
    event_type = 20100

    @transaction.atomic
    def run(self):
        ip = InformationPackage.objects.get(pk=self.ip)
        sa = ip.submission_agreement
        prepare_path = Path.objects.get(entity="path_preingest_prepare").value
        dst_dir = os.path.join(prepare_path, ip.object_identifier_value)
        shutil.copytree(ip.object_path, dst_dir)

        if sa.archivist_organization:
            existing_agents_with_notes = Agent.objects.all().with_notes([])
            ao_agent, _ = Agent.objects.get_or_create(
                role='ARCHIVIST', type='ORGANIZATION',
                name=sa.archivist_organization, pk__in=existing_agents_with_notes
            )
            ip.agents.add(ao_agent)

        submit_description_data = ip.get_profile_data('submit_description')
        ip.label = ip.object_identifier_value
        ip.entry_date = ip.create_date
        ip.object_path = dst_dir
        ip.start_date = submit_description_data.get('start_date')
        ip.end_date = submit_description_data.get('end_date')
        ip.save()

    def event_outcome_success(self):
        return "Received IP"


class SubmitSIP(DBTask):
    event_type = 10500

    def run(self):
        ip = InformationPackage.objects.get(pk=self.ip)

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
        block_size = 8 * 1000000  # 8MB
        copy_file(src, dst, requests_session=session, block_size=block_size)

        src = os.path.join(srcdir, ip.object_identifier_value + ".xml")
        if not remote:
            dst = os.path.join(reception, ip.object_identifier_value + ".xml")
        copy_file(src, dst, requests_session=session, block_size=block_size)

        self.set_progress(100, total=100)

    def undo(self):
        ip = InformationPackage.objects.get(pk=self.ip)

        reception = Path.objects.get(entity="path_ingest_reception").value
        container_format = ip.get_container_format()

        tar = os.path.join(reception, ip.object_identifier_value + ".%s" % container_format)
        xml = os.path.join(reception, ip.object_identifier_value + ".xml")

        os.remove(tar)
        os.remove(xml)

    def event_outcome_success(self):
        return "Submitted %s" % get_cached_objid(self.ip)
