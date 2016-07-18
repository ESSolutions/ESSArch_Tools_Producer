from __future__ import unicode_literals

import uuid

from celery import states as celery_states

from django.db import models
from django.utils.translation import ugettext as _

from picklefield.fields import PickledObjectField


class ArchiveObject(models.Model):
    ObjectUUID = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                  editable=False)

    class Meta:
        db_table = u'ArchiveObject'

class Process(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, blank=True)
    progress = models.IntegerField(blank=True, default=0)


class ProcessStep(Process):
    StatusProcess_CHOICES = (
        (0, 'Pending'),
        (2, 'Initiate'),
        (5, 'Progress'),
        (20, 'Success'),
        (100, 'FAIL'),
    )

    Type_CHOICES = (
        (0, "Receive new object"),
        (5, "The object is ready to remodel"),
        (9, "New object stable"),
        (10, "Object don't exist in AIS"),
        (11, "Object don't have any projectcode in AIS"),
        (12, "Object don't have any local policy"),
        (13, "Object already have an AIP!"),
        (14, "Object is not active!"),
        (19, "Object got a policy"),
        (20, "Object not updated from AIS"),
        (21, "Object not accepted in AIS"),
        (24, "Object accepted in AIS"),
        (25, "SIP validate"),
        (30, "Create AIP package"),
        (40, "Create package checksum"),
        (50, "AIP validate"),
        (60, "Try to remove IngestObject"),
        (1000, "Write AIP to longterm storage"),
        (1500, "Remote AIP"),
        (2009, "Remove temp AIP object OK"),
        (3000, "Archived"),
        (5000, "ControlArea"),
        (5100, "WorkArea"),
        (9999, "Deleted"),
    )

    type = models.IntegerField(null=True, choices=StatusProcess_CHOICES)
    user = models.CharField(max_length=45)
    result = PickledObjectField(blank=True)
    status = models.IntegerField(blank=True, default=0, choices=Type_CHOICES)
    posted = models.DateTimeField(auto_now_add=True)
    archiveobject = models.ForeignKey('ArchiveObject', to_field='ObjectUUID', blank=True, null=True)
    hidden = models.BooleanField(default=False)

    class Meta:
        db_table = u'ProcessStep'

        def __unicode__(self):
            return '%s - %s - archiveobject:%s' % (self.name, self.id, self.archiveobject.ObjectUUID)

class ProcessTask(Process):
    TASK_STATE_CHOICES = zip(celery_states.ALL_STATES,
                             celery_states.ALL_STATES)

    task_id = models.CharField(_('task id'), max_length=255, unique=True)
    status = models.CharField(_('state'), max_length=50,
                              default=celery_states.PENDING,
                              choices=TASK_STATE_CHOICES)
    result = PickledObjectField(null=True, default=None, editable=False)
    date_done = models.DateTimeField(_('done at'), null=True)
    traceback = models.TextField(_('traceback'), blank=True, null=True)
    hidden = models.BooleanField(editable=False, default=False, db_index=True)
    meta = PickledObjectField(null=True, default=None, editable=False)
    processstep = models.ForeignKey('ProcessStep', blank=True, null=True)

    class Meta:
        db_table = 'ProcessTask'

        def __unicode__(self):
            return '%s - %s' % (self.name, self.id)

class Step(models.Model):
    name = models.CharField(primary_key=True, max_length=128, unique=True)

    class Meta:
        db_table = 'Step'

class Task(models.Model):
    name = models.CharField(primary_key=True, max_length=128, unique=True)

    class Meta:
        db_table = 'Task'
