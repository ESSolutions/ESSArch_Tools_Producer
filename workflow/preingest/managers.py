from __future__ import absolute_import, division

import uuid

from celery import states as celery_states, Task

from django.db import models


class StepManager(models.Manager):
    def create_step(self, name, tasks):
        """
        Creates a process step with the given tasks

        Args:
            tasks: A dict of tasks containing the name and params of the task
        """

        from preingest.models import ProcessTask

        step = self.create(
            name=name,
            task_set=[d['name'] for d in tasks]
        )

        attempt = uuid.uuid4()

        for pos, t in enumerate(tasks):
            task = ProcessTask(
                processstep=step,
                processstep_pos=pos,
                name=t["name"],
                params=t["params"],
                attempt=attempt,
                status="PREPARED"
            )

            step.tasks.add(task, bulk=False)

        return step

class TaskManager(models.Manager):
    pass
