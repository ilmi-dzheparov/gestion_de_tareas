from django.urls import path
from .views import task_index
from .views import TasksListView, TaskDetailView, TaskCreateView, TaskDeleteView, TaskUpdateView
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
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]