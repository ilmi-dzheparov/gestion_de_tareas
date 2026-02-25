from django.contrib import admin
from .models import Department, Course, Task, Stage, Group, TaskFile


class TaskFileInline(admin.TabularInline):
    model = TaskFile
    extra = 1  # количество пустых полей для новых файлов по умолчанию

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'department', 'year')
    list_filter = ('department', 'year')
    search_fields = ('department__name', 'year')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)

# This allows you to edit Stages directly inside the Task page
class StageInline(admin.TabularInline):
    model = Stage
    extra = 1  # Number of empty slots for new stages
    fields = ('count', 'title', 'student', 'end_date', 'status')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor', 'course', 'end_date')
    list_filter = ('course', 'tutor', 'start_date')
    search_fields = ('title', 'description')
    # Filter students/tutors in the many-to-many/foreign key selectors
    filter_horizontal = ('students',)
    inlines = [StageInline, TaskFileInline]

@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('title', 'task', 'student', 'count', 'status', 'is_overdue_icon')
    list_filter = ('status', 'task', 'student')
    search_fields = ('title', 'task__title', 'student__email')

    # Displays your @property 'is_overdue' as a nice icon in the list
    @admin.display(description='¿Atrasada?', boolean=True)
    def is_overdue_icon(self, obj):
        return obj.is_overdue