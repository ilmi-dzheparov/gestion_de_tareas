from django.urls import path
from .views import task_index
from .views import TasksListView
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
]