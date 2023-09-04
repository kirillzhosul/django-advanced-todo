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
from tasks.serializers import (
    TaskSerializer,
    TaskPostSerializer,
    TaskPatchSerializer,
    TaskGetSerializer,
)
from tasks.models import Task


class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req) -> Response:
        # TODO: Split into smaller business logic services
        data = TaskGetSerializer(data=req.data)
        if not data.is_valid():
            return Response({"errors": data.errors})

        if data.task_id:
            task = get_object_or_404(Task, id=data.task_id)
            return Response({"task": TaskSerializer(task).data})

        asignee = (
            get_object_or_404(User, id=data.asignee_id) if data.asignee_id else req.user
        )
        query = Task.objects.filter(asignee=asignee)

        query = query.filter(priority=data.priority) if data.priority else query
        query = query.filter(category=data.category) if data.category else query
        query = query.order_by(data.order_by) if data.order_by else query

        tasks = query.all()
        return Response({"tasks": TaskSerializer(tasks, many=True).data})

    def post(self, req) -> Response:
        data = TaskPostSerializer(data=req.data)
        if not data.is_valid():
            return Response({"errors": data.errors})
        task = Task.objects.create(
            title=data.title,
            description=data.description,
            category=data.category,
            asignee=get_asignee_by_id_or_none(req, data.asignee_id),
            parent=Task.objects.get(id=data.parent_id),
        )
        return Response({"task": TaskSerializer(task).data})

    def patch(self, req) -> Response:
        # TODO: Rework with not mess solution
        data = TaskPatchSerializer(data=req.data)
        if not data.is_valid():
            return Response({"errors": data.errors})
        task = get_object_or_404(Task, id=data.task_id)
        asignee, is_asignee_change = get_asignee_by_id_or_none(req, data.asignee_id)
        is_changed = False
        parent, is_parent_change = get_parent_by_id_or_none(data.parent_id)

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
    # TODO: Rework with not mess solution
    if asignee_id := req.data.get("asignee_id", None):
        asignee = (
            req.user if asignee_id == "-1" else get_object_or_404(User, id=asignee_id)
        )
        return Response(get_asignee_kpi(asignee))
    else:
        return Response({"categories": get_categories_kpi()})
