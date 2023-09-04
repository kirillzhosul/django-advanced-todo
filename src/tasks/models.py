from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CategoryField(models.CharField):
    def get_prep_value(self, value: str) -> str:
        value = super().get_prep_value(value)
        value = value.replace(" ", "-")
        return value if value is None else value.lower()


class Task(models.Model):
    """Represents a single item of the task."""

    id = models.AutoField(primary_key=True)
    asignee = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey("Task", on_delete=models.SET_NULL, null=True)
    title = models.CharField(
        max_length=64, verbose_name="Task name to display", null=False
    )
    is_completed = models.BooleanField(
        verbose_name="Describes is task completed (by owner or another user) or not",
        default=False,
        null=False,
    )
    priority = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        verbose_name="Priority in number (1-3)",
    )
    description = models.TextField(verbose_name="Task verbosed description", null=False)
    category = CategoryField(
        verbose_name="Lowercase category naming", null=False, default="default"
    )

    def get_display_title(self) -> str:
        return f"{self.title} (Task №{self.id})"

    def __str__(self):
        return self.get_display_title()

    def __repr__(self):
        return self.get_display_title()
