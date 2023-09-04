from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from tasks.models import Task


def get_asignee_by_id_or_none(req, asignee_id: int) -> tuple[User | None, bool]:
    asignee = None
    if asignee_id == 0:
        asignee = req.user
    elif asignee_id != -1:
        try:
            asignee = User.objects.get(id=asignee_id)
        except User.DoesNotExist:
            return None, False
    return asignee, True


def get_parent_by_id_or_none(task_id: int) -> tuple[Task | None, bool]:
    parent = None
    if task_id != -1:
        try:
            parent = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None, False
    return parent, True
