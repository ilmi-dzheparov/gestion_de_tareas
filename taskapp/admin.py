from django.contrib import admin
from .models import Department, Course, Student, Tutor, Task

admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Task)
