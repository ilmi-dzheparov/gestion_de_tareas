from django.urls import path
from .views import (CommentTaskCreateView,
                    CommentTaskDeleteView,
                    CommentTaskEditView,
                    CommentStageCreateView,
                    CommentStageDeleteView,
                    CommentStageEditView,)

app_name = "commentapp"

urlpatterns = [
    path('task_comment/new/', CommentTaskCreateView.as_view(), name='task_comment_create'),
    path('task_comment/<int:pk>/delete/', CommentTaskDeleteView.as_view(), name='task_comment_delete'),
    path('task_comment/<int:pk>/edit/', CommentTaskEditView.as_view(), name='task_comment_edit'),
    path('stage_comment/new/', CommentStageCreateView.as_view(), name='stage_comment_create'),
    path('stage_comment/<int:pk>/delete/', CommentStageDeleteView.as_view(), name='stage_comment_delete'),
    path('stage_comment/<int:pk>/edit/', CommentStageEditView.as_view(), name='stage_comment_edit'),
]