"""
    Views for API
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from tasks.services.kpi import get_categories_kpi, get_asignee_kpi
from tasks.services.asignee import get_parent_by_id_or_none, get_asignee_by_id_or_none
from tasks.serializers import TaskSerializer, KPISerializer
from tasks.models import Task


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req) -> Response:
        if task_id := req.data.get("task_id"):
            task = get_object_or_404(Task, id=task_id)
            return Response({"task": TaskSerializer(task).data})

        asignee = req.user
        if asignee_id := req.data.get("asignee_id", None):
            asignee = get_object_or_404(User, id=asignee_id)

        query = Task.objects.filter(asignee=asignee)

        if priority := req.data.get("priority"):
            query = query.filter(priority=priority)

        if category := req.data.get("category"):
            query = query.filter(category=category)

        if order_by := req.data.get("sort_by"):
            if order_by in ("-priority", "priority"):
                query = query.order_by(order_by)

        tasks = query.all()
        return Response({"tasks": TaskSerializer(tasks, many=True).data})

    def post(self, req) -> Response:
        task = Task.objects.create(
            title=req.data.get("title", "My task"),
            description=req.data.get("description", "My description"),
            category=req.data.get("description", "default"),
            asignee=get_asignee_by_id_or_none(req, int(req.data.get("asignee_id", -1))),
            parent=Task.objects.get(id=req.data.get("parent_id", 0)),
        )
        return Response({"task": TaskSerializer(task).data})

    def patch(self, req) -> Response:
        task = get_object_or_404(Task, id=req.data.get("task_id"))
        asignee, is_asignee_change = get_asignee_by_id_or_none(
            req, int(req.data.get("asignee_id", "-1"))
        )
        is_changed = False
        parent, is_parent_change = get_parent_by_id_or_none(
            int(req.data.get("parent_id", "0"))
        )

        if is_asignee_change:
            task.asignee = asignee
            is_changed = True

        if is_parent_change:
            task.parent = parent
            is_changed = True

        if is_changed:
            task.save()

        return Response({"task": TaskSerializer(task).data, "is_changed": is_changed})

    def delete(self, req) -> Response:
        task_id = req.data.get("task_id")
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        task.save()
        return Response({"task": TaskSerializer(task).data, "deleted": True})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def kpi_efficiency(req) -> Response:
    if asignee_id := req.data.get("asignee_id", None):
        asignee = (
            req.user if asignee_id == "-1" else get_object_or_404(User, id=asignee_id)
        )
        return Response(get_asignee_kpi(asignee))
    else:
        return Response({"categories": get_categories_kpi()})
