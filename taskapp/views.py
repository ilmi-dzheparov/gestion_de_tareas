from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student
from .forms import StudentForm


# def task_index(request):
#     return HttpResponse("Hello world")

# список студентов
def students_list(request):
    students = Student.objects.all()
    return render(request, "taskapp/students_list.html", {"students": students})

# детали студента
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, "taskapp/student_detail.html", {"student": student})

# создание студента
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("students_list")
    else:
        form = StudentForm()

    return render(request, "taskapp/student_form.html", {"form": form})

# редактирование студента
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_detail", pk=pk)
    else:
        form = StudentForm(instance=student)

    return render(request, "taskapp/student_form.html", {"form": form})

# удаление студента
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect("students_list")

