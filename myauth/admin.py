from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


# 1. Create a form for the "Add User" page
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "name", "is_student", "is_tutor")

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
    list_display = ("email", "name", "last_name", "is_student", "is_tutor", "is_staff")
    list_filter = ("is_student", "is_tutor", "is_staff", "is_active")
    ordering = ("email",)

    # Forms for editing and creating students
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "last_name", "dni", "birthdate", "department")}),
        ("Roles", {"fields": ("is_student", "is_tutor")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas", {"fields": ("last_login", "date_joined")}),
    )
    # Fields shown when creating a user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password", "name", "is_student", "is_tutor"),
        }),
    )
    search_fields = ("email", "name", "last_name", "dni")
    readonly_fields = ("date_joined", "last_login")
