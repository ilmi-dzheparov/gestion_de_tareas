from django.views.generic import CreateView, ListView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import CommentTask, CommentStage
from .forms import CommentTaskForm, CommentStageForm
from taskapp.models import Task, Stage


class CommentTaskCreateView(CreateView):
    model = CommentTask
    fields = ['comment']  # Solo mostramos el campo de texto
    template_name = 'comments/comment-create.html'

    def form_valid(self, form):
        # 1. Asignamos el usuario logueado (el estudiante)
        form.instance.user = self.request.user

        # 2. Capturamos la tarea desde el parámetro ?task=ID de la URL
        task_id = self.request.GET.get('task')
        if task_id:
            form.instance.task = Task.objects.get(id=task_id)

        return super().form_valid(form)

    def get_success_url(self):
        # Al terminar, volvemos al detalle de la tarea
        return reverse('taskapp:task_detail', kwargs={'pk': self.object.task.id})


class CommentTaskDeleteView(DeleteView):
    model = CommentTask
    template_name = ('comments/comment-delete.html')

    def get_success_url(self):
        # Al terminar, volvemos al detalle de la tarea
        return reverse('taskapp:task_detail', kwargs={'pk': self.object.task.id})
#
# class CommentTaskListView(ListView):
#     model = CommentTask
#     template_name = 'tasks/tasks-detail.html'
#     context_object_name = 'comments'
#     queryset = CommentTask.objects.filter(task.id)  # (.archived=False)
#     # permission_required = ['products.view_product']
#
#
# class CommentTaskCreateView(CreateView):
#     model = CommentTask
#     form_class = CommentTaskForm
#
#     def form_valid(self, form):
#         # Capturamos la tarea por el ID que vendrá en la URL
#         task_id = self.kwargs.get('task_id')
#         form.instance.task = Task.objects.get(id=task_id)
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         # Redirige de vuelta al detalle de la tarea
#         return reverse_lazy('task-detail', kwargs={'pk': self.kwargs.get('task_id')})