from django.urls import path

from tasks import views

urlpatterns = [
    path("", views.TaskView.as_view(), name="tasks"),
    path("metrics", views.kpi_efficiency, name="tasks-efficiency"),
]
