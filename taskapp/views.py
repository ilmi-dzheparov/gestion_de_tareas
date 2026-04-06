from django.utils import timezone

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse, request
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.views.generic.edit import FormMixin

from .models import Task, Stage
from .forms import TaskForm, StageForm, TaskFileFormSet, StageFileFormSet
from commentapp.models import CommentTask, CommentStage
# from .utils import get_count


class StatisticView(View):
    def get(self, request):
        user = request.user

        # Si el usuario es TUTOR, contamos donde sea el tutor asignado
        if user.is_tutor:
            tasks = Task.objects.filter(tutor=user, status=0)
            stages = Stage.objects.filter(task__tutor=user, task__status=0)
            tasks_completed = Task.objects.filter(tutor=user, status=1)
        # Si el usuario es ALUMNO, contamos donde esté en la lista de alumnos
        else:
            tasks = Task.objects.filter(students=user, status=0)
            stages = Stage.objects.filter(student=user, task__status=0)
            tasks_completed = Task.objects.filter(students=user, status=1)
        context = {
            'tasks_count': tasks.count(),
            'stages_count': stages.count(),
            'tasks_completed_count': tasks_completed.count(),
        }
        return render(request, 'tasks/index.html', context=context)

class TasksListView(ListView): #(PermissionRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks-list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        # Filtramos: tareas donde es tutor O tareas donde está en el ManyToMany de alumnos
        return Task.objects.filter(
            Q(tutor=user) | Q(students=user),
            status=False
        ).distinct()
    #(.archived=False)
    # permission_required = ['products.view_product']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Дополнительно передаем завершенные задачи в этот же шаблон
        context['completed_tasks'] = Task.objects.filter(
            Q(tutor=user) | Q(students=user),
            status=True
        ).distinct().order_by('-end_date')
        context['now'] = timezone.now()  # Передаем текущее время
        return context

class TasksCompletedListView(ListView): #(PermissionRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks-completed-list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        # Filtramos: tareas donde es tutor O tareas donde está en el ManyToMany de alumnos
        return Task.objects.filter(
            Q(tutor=user) | Q(students=user),
            status=True
        ).distinct()
    #(.archived=False)
    # permission_required = ['products.view_product']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['now'] = timezone.now()
        return context


class TaskDetailView(FormMixin, DetailView):
    model = Task
    template_name = 'tasks/task-detail.html'
    form_class = TaskForm

    def get_form_kwargs(self):
        """Passes the current user's group to the form."""
        kwargs = super(TaskDetailView, self).get_form_kwargs()

        # Get the group of the currently logged-in user (assuming the user creating
        # the task has a 'group' Foreign Key relationship)
        user_group = self.request.user.group

        kwargs['user_group'] = user_group
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Traemos la lista de comentarios para ESTA tarea
        context['comments'] = (CommentTask.objects.filter(task=self.object)
                               .select_related('user').order_by('-uploaded_at'))
        context['now'] = timezone.now()
        return context

class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/task-create.html'
    form_class = TaskForm
    success_url = reverse_lazy('taskapp:tasks_list')

    def get_form_kwargs(self):
        """Passes the current user's group to the form."""
        kwargs = super(TaskCreateView, self).get_form_kwargs()

        # Get the group of the currently logged-in user (assuming the user creating
        # the task has a 'group' Foreign Key relationship)
        user_group = self.request.user.group

        kwargs['user_group'] = user_group
        return kwargs

    def get_context_data(self, **kwargs):
        """Добавляет formset файлов в контекст шаблона."""
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            # Если отправка формы — заполняем данными
            data['file_formset'] = TaskFileFormSet(self.request.POST, self.request.FILES)
        else:
            # Если открытие страницы — пустая форма
            data['file_formset'] = TaskFileFormSet()
        return data

    def form_valid(self, form):
        """Сохраняет задачу и привязанные к ней файлы."""
        context = self.get_context_data()
        file_formset = context['file_formset']

        # Используем транзакцию: если файлы не валидны, задача не создастся
        with transaction.atomic():
            self.object = form.save()
            if file_formset.is_valid():
                file_formset.instance = self.object
                file_formset.save()
            else:
                # Если файлы не валидны — перерисовываем страницу с ошибками
                return self.render_to_response(self.get_context_data(form=form))

        return super().form_valid(form)

class TaskUpdateView(UpdateView):
    model = Task
    # fields = "title", "description", "end_date"
    template_name = 'tasks/task-edit.html'
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy('taskapp:task_detail', kwargs={'pk': self.object.pk})

    def get_form_kwargs(self):
        """Passes the current user's group to the form."""
        kwargs = super(TaskUpdateView, self).get_form_kwargs()

        # Get the group of the currently logged-in user (assuming the user creating
        # the task has a 'group' Foreign Key relationship)
        user_group = self.request.user.group

        kwargs['user_group'] = user_group
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            # Передаем self.get_object(), чтобы связать данные с текущей задачей
            data['file_formset'] = TaskFileFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.get_object()
            )
        else:
            # ВАЖНО: Передаем instance=self.get_object(),
            # чтобы в форме появились уже существующие файлы
            data['file_formset'] = TaskFileFormSet(instance=self.get_object())
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        file_formset = context['file_formset']

        if file_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                file_formset.instance = self.object
                file_formset.save()
            return super().form_valid(form)
        else:
            # Если файлы не валидны, возвращаем форму с ошибками формсета
            return self.render_to_response(self.get_context_data(form=form, file_formset=file_formset))

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task-delete.html'
    success_url = reverse_lazy('taskapp:tasks_list')

    # def form_valid(self, form):
    #     success_url = self.get_success_url()
    #     self.object.archived = True
    #     self.object.save()
    #     return HttpResponseRedirect(success_url)

class StagesListView(ListView): #(PermissionRequiredMixin, ListView):
    model = Stage
    template_name = ('stages/stages-list.html')
    context_object_name = 'stages'

    def get_queryset(self):
        user = self.request.user
        # Filtramos: stages donde es tutor O stages donde es alumno
        return Stage.objects.filter(
            Q(task__tutor=user) | Q(student=user),
            task__status=False,
            status=False
        ).distinct()
     #(.archived=False)
    # permission_required = ['products.view_product']

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        # Дополнительно передаем завершенные задачи в этот же шаблон
        context['completed_stages'] = Stage.objects.filter(
            Q(task__tutor=user) | Q(student=user),
            Q(status=True) | Q(task__status=True)
        ).distinct().order_by('-end_date')

        context['now'] = timezone.now()
        return context

class StageDetailView(DetailView):
    model = Stage
    template_name = 'stages/stage-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Traemos la lista de comentarios para ESTA tarea
        context['comments'] = (CommentStage.objects.filter(stage=self.object)
                               .select_related('user').order_by('-uploaded_at'))
        return context

class StageCreateView(CreateView):
    model = Stage
    template_name = 'stages/stage-create.html'
    form_class = StageForm

    def get_success_url(self):
        # self.object — это только что созданный объект Stage
        # Мы берем pk его задачи (task) и строим URL
        return reverse('taskapp:task_detail', kwargs={'pk': self.object.task.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        task_id = self.request.GET.get('task')
        if task_id:
            task = get_object_or_404(Task, id=task_id)
            kwargs['fixed_task'] = task

        return kwargs

    def get_context_data(self, **kwargs):
        """Добавляет formset файлов в контекст шаблона."""
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            # Если отправка формы — заполняем данными
            data['file_formset'] = StageFileFormSet(self.request.POST, self.request.FILES)
        else:
            # Если открытие страницы — пустая форма
            data['file_formset'] = StageFileFormSet()
        return data

    def form_valid(self, form):
        """Сохраняет задачу и привязанные к ней файлы."""
        context = self.get_context_data()
        file_formset = context['file_formset']

        # Используем транзакцию: если файлы не валидны, задача не создастся
        with transaction.atomic():
            self.object = form.save()
            if file_formset.is_valid():
                file_formset.instance = self.object
                file_formset.save()
            else:
                # Если файлы не валидны — перерисовываем страницу с ошибками
                return self.render_to_response(self.get_context_data(form=form))

        return super().form_valid(form)

class StageUpdateView(UpdateView):
    model = Stage
    # fields = "title", "description", "end_date", "status", "student"
    form_class = StageForm
    template_name = 'stages/stage-edit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Obtenemos la etapa actual y su tarea vinculada
        current_stage = self.get_object()
        kwargs['fixed_task'] = current_stage.task  # Esto activa tu lógica de filtrado en el form

        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            # Передаем self.get_object(), чтобы связать данные с текущей задачей
            data['file_formset'] = StageFileFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.get_object()
            )
        else:
            # ВАЖНО: Передаем instance=self.get_object(),
            # чтобы в форме появились уже существующие файлы
            data['file_formset'] = StageFileFormSet(instance=self.get_object())
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        file_formset = context['file_formset']

        if file_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                file_formset.instance = self.object
                file_formset.save()
            return super().form_valid(form)
        else:
            # Если файлы не валидны, возвращаем форму с ошибками формсета
            return self.render_to_response(self.get_context_data(form=form, file_formset=file_formset))

    def get_success_url(self):
        return reverse_lazy('taskapp:stage_detail', kwargs={'pk': self.object.pk})

class StageDeleteView(DeleteView):
    model = Stage
    template_name = 'stages/stage-delete.html'
    success_url = reverse_lazy('taskapp:stages_list')

    # def form_valid(self, form):
    #     success_url = self.get_success_url()
    #     self.object.archived = True
    #     self.object.save()
    #     return HttpResponseRedirect(success_url)


# список студентов
# def students_list(request):
#     students = Student.objects.all()
#     return render(request, "taskapp/students_list.html", {"students": students})
#
# # детали студента
# def student_detail(request, pk):
#     student = get_object_or_404(Student, pk=pk)
#     return render(request, "taskapp/student_detail.html", {"student": student})

# создание студента
# def student_create(request):
#     if request.method == "POST":
#         form = StudentForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("students_list")
#     else:
#         form = StudentForm()
#
#     return render(request, "taskapp/student_form.html", {"form": form})
#
# # редактирование студента
# def student_edit(request, pk):
#     student = get_object_or_404(Student, pk=pk)
#
#     if request.method == "POST":
#         form = StudentForm(request.POST, instance=student)
#         if form.is_valid():
#             form.save()
#             return redirect("student_detail", pk=pk)
#     else:
#         form = StudentForm(instance=student)
#
#     return render(request, "taskapp/student_form.html", {"form": form})
#
# # удаление студента
# def student_delete(request, pk):
#     student = get_object_or_404(Student, pk=pk)
#     student.delete()
#     return redirect("students_list")

