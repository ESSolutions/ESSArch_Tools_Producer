from __future__ import absolute_import

from celery import Task

class DBTask(Task):

    def set_progress(self, progress, total=None):
        self.update_state(state='PROGRESS',
                          meta={'current': progress, 'total': total})
