from django.db.models import Count
from django.contrib.auth.models import User

from tasks.serializers import KPISerializer
from tasks.models import Task


def get_asignee_kpi(asignee: User) -> dict:
    completed_tasks = Task.objects.filter(is_completed=True, asignee=asignee).count()
    uncompleted_tasks = Task.objects.filter(is_completed=False, asignee=asignee).count()
    kpi = KPISerializer(data=_get_kpi_data(completed_tasks, uncompleted_tasks))
    kpi.is_valid(raise_exception=True)
    return kpi.data


def get_categories_kpi() -> dict[str, KPISerializer]:
    return {
        category: _get_category_kpi(category).data
        for category in [
            row["category"]
            for row in Task.objects.values("category").annotate(
                dcount=Count("category")
            )
        ]
    }


def _get_category_kpi(category: str) -> KPISerializer:
    completed_tasks = Task.objects.filter(is_completed=True).count()
    uncompleted_tasks = Task.objects.filter(is_completed=False).count()
    kpi = KPISerializer(data=_get_kpi_data(completed_tasks, uncompleted_tasks))
    kpi.is_valid(raise_exception=True)
    return kpi


def _get_kpi_data(completed_tasks, uncompleted_tasks) -> dict:
    total_tasks = completed_tasks + uncompleted_tasks
    task_completion_kpi = (
        0 if completed_tasks == 0 else uncompleted_tasks / completed_tasks
    )

    return {
        "task_completion_kpi": task_completion_kpi,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "uncompleted_tasks": uncompleted_tasks,
    }
