from django.urls import path
from .views import CommentTaskCreateView, CommentTaskDeleteView

app_name = "commentapp"

urlpatterns = [
    path('comments/new/', CommentTaskCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/delete/', CommentTaskDeleteView.as_view(), name='comment_delete'),
]