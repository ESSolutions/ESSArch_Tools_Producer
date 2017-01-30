"""
    ESSArch is an open source archiving and digital preservation system

    ESSArch Tools for Producer (ETP)
    Copyright (C) 2005-2017 ES Solutions AB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.

    Contact information:
    Web - http://www.essolutions.se
    Email - essarch@essolutions.se
"""

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
            "responsible": responsible,
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
