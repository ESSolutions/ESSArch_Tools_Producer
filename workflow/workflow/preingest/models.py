from __future__ import unicode_literals

import uuid

from celery import states as celery_states

from django.db import models
from django.utils.translation import ugettext as _

from picklefield.fields import PickledObjectField


class Process(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, blank=True)
    progress = models.IntegerField(blank=True, default=0)

class ProcessStep(Process):
    ReqStatus_CHOICES = (
        (-1, 'Undefined'),
        (0, 'Success'),
        (1, 'Error'),
        (2, 'Warning'),
    )

    StatusProcess_CHOICES = (
        (-1, 'Undefined'),
        (0, 'Success'),
        (1, 'Error'),
        (2, 'Warning'),
    )

    type = models.IntegerField(null=True, choices=StatusProcess_CHOICES)
    user = models.CharField(max_length=45)
    result = PickledObjectField(blank=True)
    status = models.IntegerField(blank=True, default=0, choices=ReqStatus_CHOICES)
    posted = models.DateTimeField(auto_now_add=True)
    archiveobject = models.ForeignKey('ArchiveObject', to_field='ObjectUUID', blank=True, null=True)
    hidden = models.BooleanField(default=False)

    class Meta:
        db_table = u'ProcessStep'

        def __unicode__(self):
            return '%s - %s - archiveobject:%s' % (self.name, self.id, self.archiveobject.ObjectUUID)

class ProcessTask(Process):
    TASK_STATE_CHOICES = zip(celery_states.ALL_STATES, celery_states.ALL_STATES)

    task_id = models.CharField(_('task id'), max_length=255, unique=True)
    status = models.CharField(_('state'), max_length=50, default=celery_states.PENDING, choices=TASK_STATE_CHOICES)
    result = PickledObjectField(null=True, default=None, editable=False)
    date_done = models.DateTimeField(_('done at'), auto_now=True)
    traceback = models.TextField(_('traceback'), blank=True, null=True)
    hidden = models.BooleanField(editable=False, default=False, db_index=True)
    meta = PickledObjectField(null=True, default=None, editable=False)
    processstep = models.ForeignKey('ProcessStep', blank=True, null=True)

    class Meta:
        db_table = 'ProcessTask'

        def __unicode__(self):
            return '%s - %s' % (self.name, self.id)
