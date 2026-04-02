from django.urls import path
from django.views.generic import RedirectView

from .views import (
    TasksListView,
    TasksCompletedListView,
    TaskDetailView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    StagesListView,
    StageDetailView,
    StageCreateView,
    StageUpdateView,
    StageDeleteView,
    StatisticView,
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
    # Redirección inicial para mejorar la experiencia de usuario
    path('', RedirectView.as_view(url='/index/'), name='root_redirect'),

    # Dashboard principal con métricas y estadísticas de tareas
    path('index/', StatisticView.as_view(), name='main'),

    # Gestión Completa de Tareas (CRUD)
    path('tasks/', TasksListView.as_view(), name='tasks_list'),  # Listado general
    path('tasks_completed/', TasksCompletedListView.as_view(), name='tasks_completed_list'),  # Listado general
    path('tasks/new/', TaskCreateView.as_view(), name='task_create'),  # Formulario de alta
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),  # Detalle y alumnos
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_update'),  # Modificación
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),  # Eliminación

    # Gestión de Etapas/Hitos (Seguimiento del Alumno)
    path('stages/', StagesListView.as_view(), name='stages_list'),
    path('stages/<int:pk>/', StageDetailView.as_view(), name='stage_detail'),
    path('stages/<int:pk>/edit/', StageUpdateView.as_view(), name='stage_update'),
    path('stages/new/', StageCreateView.as_view(), name='stage_create'),
    path('stages/<int:pk>/delete/', StageDeleteView.as_view(), name='stage_delete'),
]