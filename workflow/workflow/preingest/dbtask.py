from __future__ import absolute_import

from celery import Task

class DBTask(Task):
    def __call__(self, *args, **kwargs):
        print "init task"
        return self.run(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print "finalize task"
        pass

    def set_progress(self, progress, total=None):
        self.update_state(state='PROGRESS',
                          meta={'current': progress, 'total': total})
