from ESSArch_Core.ip.models import EventIP
from ESSArch_Core.WorkflowEngine.models import ProcessStep, ProcessTask


def prepare_ip(label, responsible):
    step = ProcessStep.objects.create(
        name="Prepare IP",
    )

    t1 = ProcessTask.objects.create(
        name="preingest.tasks.PrepareIP",
        params={
            "label": label,
            "responsible": responsible.username or "Anonymous user",
            "step": str(step.pk),
        },
        log=EventIP,
        processstep_pos=0,
        responsible=responsible,
    )

    t2 = ProcessTask.objects.create(
        name="preingest.tasks.CreateIPRootDir",
        params={
        },
        result_params={
            "information_package": t1.pk
        },
        log=EventIP,
        processstep_pos=1,
        responsible=responsible,
    )

    step.tasks = [t1, t2]
    step.save()

    return step
