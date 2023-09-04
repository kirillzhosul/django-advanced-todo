from tasks.models import Task


def get_parent_by_id_or_none(task_id: int) -> tuple[Task | None, bool]:
    parent = None
    if task_id != -1:
        try:
            parent = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None, False
    return parent, True
