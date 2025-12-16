from django.urls import path
from .views import task_index
from .views import (
    TasksListView,
    TaskDetailView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    StagesListView,
    StageDetailView,
    StageCreateView,
    StageUpdateView,
)
#
#
# app_name = "taskapp"
#
# urlpatterns = [
#     path("", task_index, name="index")
# ]

app_name = "taskapp"

urlpatterns = [
    path("", task_index, name="index"),
    path('tasks/', TasksListView.as_view(), name='tasks_list'),
    path('tasks/new/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('stages/', StagesListView.as_view(), name='stages_list'),
    path('stages/<int:pk>/', StageDetailView.as_view(), name='stage_detail'),
    path('stages/<int:pk>/edit/', StageUpdateView.as_view(), name='stage_update'),
]