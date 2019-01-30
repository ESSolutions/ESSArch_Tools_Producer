# -*- coding: utf-8 -*-

import errno
import logging
import os
import shutil

from django.conf import settings

from ESSArch_Core.WorkflowEngine.polling.backends.base import BaseWorkflowPoller
from ESSArch_Core.auth.models import Group, GroupMember
from ESSArch_Core.ip.models import InformationPackage
from ESSArch_Core.profiles.models import SubmissionAgreement
from ESSArch_Core.profiles.utils import profile_types
from ESSArch_Core.util import stable_path

logger = logging.getLogger('essarch.etp.workflow.polling.DirectoryWorkflowPoller')
p_types = [p_type.lower().replace(' ', '_') for p_type in profile_types]
proj = settings.PROJECT_SHORTNAME


class DirectoryWorkflowPoller(BaseWorkflowPoller):
    def poll(self, path, sa=None):
        for entry in os.listdir(path):
            subpath = os.path.join(path, entry)

            if os.path.isfile(subpath):
                continue

            objid = os.path.basename(subpath)
            if InformationPackage.objects.filter(object_identifier_value=objid).exists():
                logger.debug(u'Information package with object identifier value "{}" already exists'.format(objid))
                continue

            if not stable_path(subpath):
                continue

            sa = SubmissionAgreement.objects.get(name=sa)
            if sa.profile_workflow is None:
                logger.debug(u'No workflow profile in SA, skipping')
                continue
            if proj not in sa.profile_workflow.specification:
                logger.debug(
                    'No workflow specified in {} for current project {}, skipping'.format(
                        sa.profile_workflow, proj
                    )
                )
                continue

            org = Group.objects.get(name='Default')
            role = 'admin'
            responsible = GroupMember.objects.filter(roles__codename=role, group=org).get().member.django_user

            ip = InformationPackage.objects.create(
                object_identifier_value=objid,
                object_path=subpath,
                package_type=InformationPackage.SIP,
                submission_agreement=sa,
                submission_agreement_locked=True,
                state='Prepared',
                responsible=responsible,
            )
            ip.create_profile_rels(p_types, responsible)
            org.add_object(ip)
            yield ip

    def delete_source(self, path, ip):
        path = os.path.join(path, ip.object_identifier_value)
        try:
            shutil.rmtree(path)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
