from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from taskapp.models import Task, Stage

class CommentTask(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='task_comments',
        verbose_name='tarea'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_task_comments',
        verbose_name='usuario'
    )
    comment = models.TextField(null=False, blank=True, verbose_name='comentario')
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comentario: {self.comment[:20]}... para {self.task.title}"


class CommentStage(models.Model):
    stage = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE,
        related_name='stage_comments',
        verbose_name='etapa'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_stage_comments',
        verbose_name='usuario'
    )
    comment = models.TextField(null=False, blank=True, verbose_name='comentario')
    uploaded_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f"Comentario: {self.comment[:20]}... para {self.stage.title}"