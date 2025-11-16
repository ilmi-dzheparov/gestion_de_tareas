from django.urls import path
from .views import task_index


app_name = "taskapp"

urlpatterns = [
    path("", task_index, name="index")
]