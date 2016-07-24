import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from rest_framework.renderers import JSONRenderer

from preingest.models import ProcessStep, ProcessTask, Step, Task
from preingest.serializers import ProcessStepSerializer, ProcessTaskSerializer

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def index(request):
    template = loader.get_template('preingest/index.html')
    context = {
        'steps' : Step.objects.all(),
        'tasks' : Task.objects.all()
    }
    return HttpResponse(template.render(context, request))

def run_step(request, name, *args, **kwargs):
    newname = name.replace(".", "/").replace("/json", ".json")

    with open(newname) as f:
        data = f.read()
        tasks = json.loads(data)

    step = ProcessStep.objects.create_step(name, tasks)
    step.save()
    step.run()

    template = loader.get_template('preingest/run_step.html')

    context = {
        'step': step
    }

    return HttpResponse(template.render(context, request))

def run_task(request, name, *args, **kwargs):
    import importlib
    [module, task] = name.rsplit('.', 1)
    getattr(importlib.import_module(module), task)().delay()
    return HttpResponse("Running {}".format(name), request)

def steps(request, *args, **kwargs):
    steps = ProcessStep.objects.all()
    serializer = ProcessStepSerializer(steps, many=True)
    return JSONResponse(serializer.data)

def tasks(request, *args, **kwargs):
    tasks = ProcessTask.objects.all()
    serializer = ProcessTaskSerializer(tasks, many=True)
    return JSONResponse(serializer.data)

def history(request, *args, **kwargs):
    template = loader.get_template('preingest/history.html')

    context = {
        'steps': ProcessStep.objects.all()
    }

    return HttpResponse(template.render(context, request))

def history_detail(request, step_id, *args, **kwargs):
    template = loader.get_template('preingest/history_detail.html')

    context = {
        'step': ProcessStep.objects.get(id=step_id)
    }

    return HttpResponse(template.render(context, request))

def undo_failed(request, processstep_id, *args, **kwargs):
    step = ProcessStep.objects.get(id=processstep_id)
    step.undo(only_failed=True)
    return redirect('history_detail', step_id=processstep_id)

def undo_step(request, processstep_id, *args, **kwargs):
    step = ProcessStep.objects.get(id=processstep_id)
    step.undo()
    return redirect('history_detail', step_id=processstep_id)

def retry_step(request, processstep_id, *args, **kwargs):
    step = ProcessStep.objects.get(id=processstep_id)
    step.retry()
    return redirect('history_detail', step_id=processstep_id)
