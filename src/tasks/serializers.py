from rest_framework import serializers

from tasks.models import Task


class KPISerializer(serializers.Serializer):
    task_completion_kpi = serializers.FloatField(required=True)
    completed_tasks = serializers.IntegerField(required=True)
    uncompleted_tasks = serializers.IntegerField(required=True)
    total_tasks = serializers.IntegerField(required=True)


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "asignee_id",
            "title",
            "description",
            "priority",
            "priority_named",
            "parent_id",
            "childrens",
            "category",
        ]

    priority_named = serializers.SerializerMethodField()

    def get_priority_named(self, obj):
        # Sorry, IK this is not required and weird mess!
        PRIORITIES = ["low", "medium", "high"]
        if obj.priority - 1 > len(PRIORITIES):
            return "unknown"
        return PRIORITIES[obj.priority - 1]

    childrens = serializers.SerializerMethodField()

    def get_childrens(self, obj):
        return TaskSerializer(obj.task_set, many=True).data


class TaskPostSerializer(serializers.Serializer):
    asignee_id = serializers.IntegerField(required=False, default=-1)
    parent_id = serializers.IntegerField(required=False, default=0)
    category = serializers.CharField(required=False, default="default")
    priority = serializers.IntegerField(required=False, default=1)
    description = serializers.CharField(required=False, default="My description")
    title = serializers.CharField(required=False, default="My title")


class TaskPatchSerializer(TaskPostSerializer):
    task_id = serializers.IntegerField(required=True, default=None)
    category = serializers.CharField(required=False, default=None)
    description = serializers.CharField(required=False, default=None)
    title = serializers.CharField(required=False, default=None)


class TaskGetSerializer(serializers.Serializer):
    task_id = serializers.IntegerField(required=False, default=None)
    asignee_id = serializers.IntegerField(required=False, default=None)
    category = serializers.CharField(required=False, default=None)
    priority = serializers.IntegerField(required=False, default=1)
    order_by = serializers.ChoiceField(["-priority", "priority"], required=False)
