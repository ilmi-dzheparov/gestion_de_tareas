import csv
import io

from django.urls import path

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .models import User
from .forms import CSVImportForm
from .apps import ExportAsCSVMixin


# 1. Create a form for the "Add User" page
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "name", "last_name", "dni", "is_student", "is_tutor", "group")

    def clean(self):
        cleaned_data = super().clean()
        # Esta línea imprime los errores no relacionados con campos en tu consola de terminal
        if self.errors:
            print("ERRORES DEL FORMULARIO:", self.errors)
        return cleaned_data


# 2. Form for Editing Users
class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class MyUserAdmin(UserAdmin, ExportAsCSVMixin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm

    # Fields to display in the list view
    list_display = ("email", "name", "last_name", "is_student", "group", "is_tutor", "is_staff")
    list_filter = ("is_student", "is_tutor", "is_staff", "is_active", "group")
    ordering = ("email",)

    # Forms for editing and creating students
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "last_name", "dni", "birthdate", "group")}),
        ("Roles", {"fields": ("is_student", "is_tutor")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ('Important dates', {"fields": ("last_login", "date_joined")}),
    )

    # Fields shown when creating a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'email', 'password1', 'password2', 'dni', 'name', 'last_name', 'group', 'is_student', 'is_tutor')
        }),
    )
    search_fields = ("email", "name", "last_name", "dni", "group")
    readonly_fields = ("date_joined", "last_login")

    filter_horizontal = ('groups', 'user_permissions',)

    # Указываем кастомный шаблон (должен лежать в templates/admin/user_change_list.html)
    change_list_template = "admin/user_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import_users_csv/",
                self.admin_site.admin_view(self.import_csv),  # Защищаем админ-вьюхой
                name='import_users_csv'
            ),
        ]
        return new_urls + urls

    def changelist_view(self, request, extra_context=None):
        # Добавляем форму в контекст основной страницы списка
        extra_context = extra_context or {}
        extra_context['csv_import_form'] = CSVImportForm()
        return super().changelist_view(request, extra_context=extra_context)

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "POST":
            form = CSVImportForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES["csv_file"]

                try:
                    # Читаем и декодируем файл
                    data_set = csv_file.read().decode('UTF-8')
                    io_string = io.StringIO(data_set)
                    reader = csv.DictReader(io_string)

                    count = 0
                    for row in reader:
                        # 1. Создаем или обновляем основные данные
                        user, created = User.objects.update_or_create(
                            email=row['email'],
                            defaults={
                                'name': row.get('name', ''),
                                'last_name': row.get('last_name', ''),
                                'dni': row.get('dni', ''),
                                'is_student': str(row.get('is_student', '')).lower() == 'true',
                                'is_tutor': str(row.get('is_tutor', '')).lower() == 'true',
                                # Если нужно импортировать ID группы:
                                # 'group_id': row.get('group') if row.get('group') else None,
                            }
                        )

                        # 2. Обработка пароля
                        raw_password = row.get('password')
                        if raw_password:
                            user.set_password(raw_password)  # Хэшируем
                            user.save()
                        elif created:
                            # Для новых юзеров без пароля в CSV ставим дефолтный
                            user.set_password("Student123!")
                            user.save()

                        count += 1

                    messages.success(request, f"Успешно импортировано {count} пользователей.")
                except Exception as e:
                    messages.error(request, f"Ошибка при обработке файла: {e}")
            else:
                messages.error(request, "Некорректная форма загрузки.")

        return redirect("..")