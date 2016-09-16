"""
    ESSArch Tools - ESSArch is an Electronic Preservation Platform
    Copyright (C) 2005-2016  ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
"""

# Create your models here.
from django.db import models

from configuration.models import Path

from preingest.models import ProcessStep, ProcessTask

from profiles.models import (
    ProfileLock, SubmissionAgreement as SA
)

import os
import uuid


class ArchivalInstitution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'ArchivalInstitution'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.name, self.id)


class ArchivistOrganization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'ArchivistOrganization'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.name, self.id)


class ArchivalType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'ArchivalType'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.name, self.id)


class ArchivalLocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'ArchivalLocation'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s - %s' % (self.name, self.id)


class InformationPackage(models.Model):
    """
    Informaion Package
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    Label = models.CharField(max_length=255)
    Content = models.CharField(max_length=255)
    Responsible = models.CharField(max_length=255)
    CreateDate = models.DateTimeField(auto_now_add=True)
    State = models.CharField(max_length=255)
    ObjectSize = models.CharField(max_length=255)
    ObjectNumItems = models.CharField(max_length=255)
    ObjectPath = models.CharField(max_length=255)
    Startdate = models.DateTimeField(null=True)
    Enddate = models.DateTimeField(null=True)
    OAIStype = models.CharField(max_length=255)
    SubmissionAgreement = models.ForeignKey(
        SA,
        on_delete=models.CASCADE,
        related_name='information_packages',
        default=None,
        null=True,
    )
    ArchivalInstitution = models.ForeignKey(
        ArchivalInstitution,
        on_delete=models.CASCADE,
        related_name='information_packages',
        default=None,
        null=True
    )
    ArchivistOrganization = models.ForeignKey(
        ArchivistOrganization,
        on_delete=models.CASCADE,
        related_name='information_packages',
        default=None,
        null=True
    )
    ArchivalType = models.ForeignKey(
        ArchivalType,
        on_delete=models.CASCADE,
        related_name='information_packages',
        default=None,
        null=True
    )
    ArchivalLocation = models.ForeignKey(
        ArchivalLocation,
        on_delete=models.CASCADE,
        related_name='information_packages',
        default=None,
        null=True
    )

    def status(self):
        steps = self.steps.all()

        if steps:
            try:
                progress = sum([s.progress() for s in steps])
                return progress / len(steps)
            except:
                return 0

        return 0

    def locks(self):
        return ProfileLock.objects.filter(
            information_package=self,
            submission_agreement=self.SubmissionAgreement
        )

    class Meta:
        ordering = ["id"]
        verbose_name = 'Information Package'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s' % self.id

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return {
            field.name: field.value_to_string(self)
            for field in InformationPackage._meta.fields
        }

    def prepare(self):
        sa = self.SubmissionAgreement
        path = Path.objects.get(entity="path_preingest_prepare").value

        step = ProcessStep.objects.create(
            name = "Prepare IP",
            information_package = self,
        )

        profile_sip = sa.profile_sip_rel.active()

        tasks = [
            ProcessTask.objects.create(
                name="preingest.tasks.CreatePhysicalModel",
                params={
                    "structure": profile_sip.structure,
                    "root": os.path.join(path, str(self.pk))
                },
                processstep_pos = 0,
            ),
        ]

        step.tasks = tasks
        step.save()
        step.run()

class EventIP(models.Model):
    """
    Events related to IP
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eventType = models.ForeignKey(
        'configuration.EventType',
        on_delete=models.CASCADE
    )
    eventDateTime = models.DateTimeField(auto_now_add=True)
    eventDetail = models.CharField(max_length=255)
    eventApplication = models.CharField(max_length=255)
    eventVersion = models.CharField(max_length=255)
    eventOutcome = models.CharField(max_length=255)
    eventOutcomeDetailNote = models.CharField(max_length=1024)
    linkingAgentIdentifierValue = models.CharField(max_length=255)
    linkingObjectIdentifierValue = models.ForeignKey(
        'InformationPackage',
        on_delete=models.CASCADE,
        related_name='events'
    )

    class Meta:
        ordering = ["eventType"]
        verbose_name = 'Events related to IP'

    def __unicode__(self):
        # create a unicode representation of this object
        return '%s (%s)' % (self.eventDetail, self.id)

    def get_value_array(self):
        # make an associative array of all fields  mapping the field
        # name to the current value of the field
        return {
            field.name: field.value_to_string(self)
            for field in EventIP._meta.fields
        }
