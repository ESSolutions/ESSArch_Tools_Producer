from __future__ import absolute_import, division

from celery import chain, states as celery_states, Task

from django.utils import timezone

from preingest.models import ProcessTask, ProcessStep

class DBStep(object):

    def __init__(self, name, tasks):
        """
        Creates a process step with the given tasks

        Args:
            tasks: A dict of tasks containing the name and params of the task
        """

        self.stepobj = ProcessStep.objects.create(name=name)

        fns = []

        for pos, t in enumerate(tasks):
            import importlib
            [module, task] = t["name"].rsplit('.', 1)
            fn = getattr(importlib.import_module(module), task)()
            fns.append((fn, t["params"]))

        self.chain = chain(fn.si(processstep=self.stepobj, params=params)
                           for (fn, params) in fns)

    def run(self):
        return self.chain()

    def get_process_obj(self):
        return self.stepobj

    def undo_last(self, n=1):
        for i in xrange(n):
            #task = get last task
            print "undoing last task ({}) in step with id {}".format(self.stepobj.id, task.id)
        pass

    def after_return(self):
        print "finalize step with id {}".format(self.id)
        #self.stepobj.status = status
        self.stepobj.save()

    def on_failure(self):
        self.stepobj.save()

    def on_success(self):
        self.stepobj.save()

    def set_progress(self, progress, total=None):
        """
        self.update_state(state=celery_states.PENDING,
                          meta={'current': progress, 'total': total})
        """
        self.stepobj.progress = (progress/total) * 100
        self.stepobj.save()
