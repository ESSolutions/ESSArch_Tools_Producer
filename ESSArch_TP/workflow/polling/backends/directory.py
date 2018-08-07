# -*- coding: utf-8 -*-

import logging
import os

from ESSArch_Core.WorkflowEngine.polling.backends.base import BaseWorkflowPoller
from ESSArch_Core.auth.models import Group, GroupMember
from ESSArch_Core.ip.models import InformationPackage
from ESSArch_Core.profiles.models import SubmissionAgreement
from ESSArch_Core.profiles.utils import profile_types
from ESSArch_Core.util import stable_path

logger = logging.getLogger('essarch.eta.workflow.polling.DirectoryWorkflowPoller')
p_types = [p_type.lower().replace(' ', '_') for p_type in profile_types]


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
