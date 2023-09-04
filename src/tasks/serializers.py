from rest_framework import serializers

from tasks.models import Task

# MUST be changed. MUST!


class KPISerializer(serializers.Serializer):
    task_completion_kpi = serializers.FloatField(required=True)
    completed_tasks = serializers.IntegerField(required=True)
    uncompleted_tasks = serializers.IntegerField(required=True)
    total_tasks = serializers.IntegerField(required=True)


class CategoryKPISerializer(KPISerializer):
    category = serializers.CharField(required=True)


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
