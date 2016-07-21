import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from rest_framework.renderers import JSONRenderer

from preingest.dbstep import DBStep
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

    step = DBStep(name, tasks)
    step.run()

    template = loader.get_template('preingest/run_step.html')

    context = {
        'step': step.get_process_obj()
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

def undo_task(request, processtask_id, *args, **kwargs):
    task = ProcessTask.objects.get(id=processtask_id)
    step = task.processstep
    undo = task.name
    import importlib
    [module, task] = undo.rsplit('.', 1)
    getattr(importlib.import_module(module), task)().delay(undo=True, processstep=step)
    return HttpResponse("undo {}".format(undo))

def undo_step(request, processstep_id, *args, **kwargs):
    step = ProcessStep.objects.get(id=processstep_id)
    step.undo()
    return redirect('history_detail', step_id=processstep_id)
