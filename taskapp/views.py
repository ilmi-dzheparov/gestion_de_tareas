from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from .models import Task, Stage
from .forms import TaskForm, StageForm
# from .utils import get_count


# class StatisticView(View):
#     def get(self, request):
#         context = {
#             'products_count': get_count(Product),
#         }
#         return render(request, 'products/index.html', context=context)

def task_index(request):
    return HttpResponse("Hello world")


class TasksListView(ListView): #(PermissionRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks-list.html'
    context_object_name = 'tasks'
    queryset = Task.objects.all #(.archived=False)
    # permission_required = ['products.view_product']

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task-detail.html'

class TaskCreateView(CreateView):
    model = Task
    template_name = 'tasks/task-create.html'
    form_class = TaskForm
    success_url = reverse_lazy('taskapp:tasks_list')

class TaskUpdateView(UpdateView):
    model = Task
    fields = "title", "description", "end_date"
    template_name = 'tasks/task-edit.html'
    def get_success_url(self):
        return reverse_lazy('taskapp:task_detail', kwargs={'pk': self.object.pk})

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
    queryset = Stage.objects.all #(.archived=False)
    # permission_required = ['products.view_product']

class StageDetailView(DetailView):
    model = Task
    template_name = 'stages/stage-detail.html'

class StageCreateView(CreateView):
    model = Stage
    template_name = 'tasks/stage-create.html'
    form_class = StageForm
    success_url = reverse_lazy('taskapp:tasks_list')

class StageUpdateView(UpdateView):
    model = Stage
    # fields = "title", "description", "end_date"
    template_name = 'stages/stage-edit.html'
    def get_success_url(self):
        return reverse_lazy('taskapp:stage_detail', kwargs={'pk': self.object.pk})


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

