from ESSArch_Core.WorkflowEngine.models import ProcessStep, ProcessTask


def prepare_ip(label, responsible):
    step = ProcessStep.objects.create(
        name="Prepare IP",
    )

    t1 = ProcessTask.objects.create(
        name="preingest.tasks.PrepareIP",
        params={
            "label": label,
            "responsible": responsible,
            "step": str(step.pk),
        },
        processstep_pos=0,
    )

    t2 = ProcessTask.objects.create(
        name="preingest.tasks.CreateIPRootDir",
        params={
        },
        result_params={
            "information_package": t1.pk
        },
        processstep_pos=1,
    )

    step.tasks = [t1, t2]
    step.save()

    return step
