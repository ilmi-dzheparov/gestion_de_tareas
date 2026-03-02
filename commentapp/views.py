from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from .models import CommentTask, CommentStage
from .forms import CommentTaskForm, CommentStageForm
from taskapp.models import Task, Stage


class CommentTaskCreateView(CreateView):
    model = CommentTask
    fields = ['comment']  # Solo mostramos el campo de texto
    template_name = 'comments/task-comment-create.html'

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
    template_name = ('comments/task-comment-delete.html')

    def get_success_url(self):
        # Al terminar, volvemos al detalle de la tarea
        return reverse('taskapp:task_detail', kwargs={'pk': self.object.task.id})

class CommentTaskEditView(UpdateView):
    model = CommentTask
    fields = ['comment']  # Solo mostramos el campo de texto
    template_name = 'comments/task-comment-edit.html'

    def form_valid(self, form):
        # 1. Asignamos el usuario logueado (el estudiante)
        form.instance.user = self.request.user

        # # 2. Capturamos la tarea desde el parámetro ?task=ID de la URL
        # task_id = self.request.GET.get('task')
        # if task_id:
        #     form.instance.task = Task.objects.get(id=task_id)

        return super().form_valid(form)

    def get_success_url(self):
        # Al terminar, volvemos al detalle de la tarea
        return reverse('taskapp:task_detail', kwargs={'pk': self.object.task.id})

class CommentStageCreateView(CreateView):
    model = CommentStage
    fields = ['comment']  # Solo mostramos el campo de texto
    template_name = 'comments/stage-comment-create.html'

    def form_valid(self, form):
        # 1. Asignamos el usuario logueado (el estudiante)
        form.instance.user = self.request.user

        # 2. Capturamos la etapa desde el parámetro ?stage=ID de la URL
        stage_id = self.request.GET.get('stage')
        if stage_id:
            form.instance.stage = Stage.objects.get(id=stage_id)

        return super().form_valid(form)

    def get_success_url(self):
        # Al terminar, volvemos al detalle de la tarea
        return reverse('taskapp:stage_detail', kwargs={'pk': self.object.stage.id})

class CommentStageDeleteView(DeleteView):
    model = CommentStage
    template_name = ('comments/stage-comment-delete.html')

    def get_success_url(self):
        # Al terminar, volvemos al detalle de la tarea
        return reverse('taskapp:stage_detail', kwargs={'pk': self.object.stage.id})

class CommentStageEditView(UpdateView):
    model = CommentTask
    fields = ['comment']  # Solo mostramos el campo de texto
    template_name = 'comments/stage-comment-edit.html'

    def form_valid(self, form):
        # 1. Asignamos el usuario logueado (el estudiante)
        form.instance.user = self.request.user

        # # 2. Capturamos la tarea desde el parámetro ?task=ID de la URL
        # task_id = self.request.GET.get('task')
        # if task_id:
        #     form.instance.task = Stage.objects.get(id=task_id)

        return super().form_valid(form)

    def get_success_url(self):
        # Al terminar, volvemos al detalle de la tarea
        return reverse('taskapp:stage_detail', kwargs={'pk': self.object.stage.id})

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