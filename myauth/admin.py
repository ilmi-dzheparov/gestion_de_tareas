from os import path

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import User
from .forms import CSVImportForm


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
class MyUserAdmin(UserAdmin):
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

class UserAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    def import_csv(self, request: HttpRequest) -> HttpResponse:
        form = CSVImportForm()
        context = { "form": form, }
        return render(request, "admin/csv_form.html", context)

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                "import_users_csv/",
                self.import_csv,
                name='import_users_csv'
            )
        ]
