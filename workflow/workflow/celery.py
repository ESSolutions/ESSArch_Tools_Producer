from __future__ import absolute_import

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'workflow.settings')

from django.conf import settings  # noqa

app = Celery('workflow')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

import django
django.setup()

from preingest.models import Task
from celery import current_app

current_app.loader.import_default_modules()

ignored = ["preingest.dbtask.DBTask"]
tasks = [t for t in current_app.tasks.keys()
         if not t.startswith("celery.") and t not in ignored]

Task.objects.all().delete()

for t in tasks:
    Task(name=t).save()
