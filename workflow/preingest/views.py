import sys

from celery.result import AsyncResult

from django.http import HttpResponse
from django.template import loader

from tasks import Sleepy

from preingest.dbtask import DBTask
from preingest.models import Task

def index(request):
    template = loader.get_template('preingest/index.html')
    context = {
        'tasks' : Task.objects.all()
    }
    return HttpResponse(template.render(context, request))

def run(request, name, *args, **kwargs):
    import importlib
    [module, task] = name.rsplit('.', 1)
    getattr(importlib.import_module(module), task)().delay()
    return HttpResponse("Running {}".format(name), request)
