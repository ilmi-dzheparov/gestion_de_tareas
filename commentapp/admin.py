from django.contrib import admin
from .models import CommentTask, CommentStage


# @admin.register(CommentTask)
# class CommentTaskAdmin(admin.ModelAdmin):
#     list_display = ('__str__',)
#
# @admin.register(CommentStage)
# class CommentStageAdmin(admin.ModelAdmin):
#     list_display = ('__str__',)


@admin.register(CommentTask)
class CommentTaskAdmin(admin.ModelAdmin):
    # Mostramos la tarea relacionada y la fecha de creación
    list_display = ('task', 'short_comment', 'uploaded_at')
    # Añadimos un filtro lateral por fecha y tarea
    list_filter = ('uploaded_at', 'task')
    # Buscador para encontrar comentarios por texto o título de tarea
    search_fields = ('comment', 'task__title')

    def short_comment(self, obj):
        return obj.comment[:30]
    short_comment.short_description = 'Comentario'

@admin.register(CommentStage)
class CommentStageAdmin(admin.ModelAdmin):
    list_display = ('stage', 'short_comment', 'uploaded_at')
    list_filter = ('uploaded_at', 'stage')
    search_fields = ('comment', 'stage__title')

    def short_comment(self, obj):
        return obj.comment[:30]
    short_comment.short_description = 'Comentario'