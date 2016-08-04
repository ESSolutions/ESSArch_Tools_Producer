from __future__ import absolute_import

from celery import current_app

def sliceUntilAttr(iterable, attr, val):
    for i in iterable:
        if getattr(i, attr) == val:
            return
        yield i

def available_tasks():
    return [t for t in current_app.tasks.keys()
         if not t.startswith("celery.") and t not in ignored]
