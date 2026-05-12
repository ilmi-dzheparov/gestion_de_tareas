import os

from django import forms
from .models import Task, Stage, TaskFile, StageFile, Group
from myauth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.dispatch import receiver

User = get_user_model()


class CustomCheckboxWidget(forms.CheckboxSelectMultiple):
    template_name = "django/forms/widgets/checkbox_select.html"  # Use the custom template

    # def __init__(self, *args, **kwargs):
    #     kwargs.setdefault('attrs', {})['class'] = 'students-columns'  # Add your custom class
    #     super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        # Call the parent render method to get the default rendering
        output = super().render(name, value, attrs, renderer)

        # Wrap the output with a div that has the id 'id_students'
        wrapper = f'<div id="id_students" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">{output}</div>'

        return wrapper


class TaskForm(forms.ModelForm):
    # Definimos el campo sin el atributo 'multiple' aquí
    # attachments = forms.FileField(
    #     widget=forms.ClearableFileInput(attrs={
    #         'class': 'form-control',
    #         'id': 'file-input'
    #     }),
    #     rsequired=False,
    #     label="Adjuntar archivos"
    # )
    # Campo extra que no está en el modelo Task
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        label="Seleccionar Grupo",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_group_select'})
    )

    class Meta:
        model = Task
        #fields = '__all__'
        exclude = ['author']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            # --- Widget para ManyToManyField ---
            'students': forms.CheckboxSelectMultiple(),
            # 'students': forms.SelectMultiple(attrs={'class': 'select2-multiple'}),
            # 'students': forms.CheckboxSelectMultiple(
            #     attrs={'class': 'students-columns'}
            # ),
        }
        labels = {
            'end_date': 'Fecha de terminación',
        }

    def __init__(self, *args, **kwargs):
        user_group = kwargs.pop('user_group', None)
        current_user = kwargs.pop('current_user', None)
        is_tutor = kwargs.pop('is_tutor', False)
        super(TaskForm, self).__init__(*args, **kwargs)

        # 1. Скрываем группу для обычных пользователей
        if not is_tutor:
            if 'group' in self.fields:
                self.fields.pop('group')


        # 2. Настройка списка студентов (ГЛАВНОЕ ИСПРАВЛЕНИЕ ТУТ)
        if 'students' in self.data:
            # Если форма отправлена (POST), разрешаем любых студентов,
            # чтобы AJAX-выбор прошел валидацию
            self.fields['students'].queryset = User.objects.all()

        elif user_group:
            # Если это обычный студент, видит только своих одногруппников
            self.fields['students'].queryset = User.objects.filter(
                group=user_group,
                is_student=True
            ).order_by('last_name')

        # 2. ЕСЛИ ЭТО РЕДАКТИРОВАНИЕ (есть объект в базе)
        elif self.instance.pk:
            # Показываем студентов, которые уже привязаны к этой задаче
            self.fields['students'].queryset = self.instance.students.all()
            # Также можно предустановить группу в селекторе, если она сохранена в задаче
            if hasattr(self.instance, 'group') and self.instance.group:
                self.initial['group'] = self.instance.group

        elif is_tutor:
            # Если это вход тьютора (первичная загрузка), список пуст до выбора группы через AJAX
            self.fields['students'].queryset = User.objects.none()
        else:
            self.fields['students'].queryset = User.objects.all()

        # 3. Настройка Тьютора
        if is_tutor and current_user:
            self.initial['tutor'] = current_user
            self.fields['tutor'].disabled = True

        # # Inyectamos el atributo 'multiple' manualmente para el HTML
        # # Esto engaña a Django y evita el ValueError
        # self.fields['attachments'].widget.attrs.update({'multiple': True})

# Создаем набор форм для файлов
TaskFileFormSet = forms.inlineformset_factory(
    Task, TaskFile,
    fields=('file',),
    extra=5,        # сколько пустых полей для файлов показать сразу
    can_delete=True, # позволит удалять уже загруженные файлы при редактировании
    widgets={
            'file': forms.FileInput(attrs={'class': 'form-control file-input-field'})
        }
)

# Создаем набор форм для файлов
StageFileFormSet = forms.inlineformset_factory(
    Stage, StageFile,
    fields=('file',),
    extra=5,        # сколько пустых полей для файлов показать сразу
    can_delete=True, # позволит удалять уже загруженные файлы при редактировании
    widgets={
            'file': forms.FileInput(attrs={'class': 'form-control file-input-field'})
        }
)

# СИГНАЛ: Удаление файла с диска после удаления записи из БД
@receiver(post_delete, sender=TaskFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Удаляет файл из файловой системы, когда объект TaskFile удаляется.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

class StageForm(forms.ModelForm):
    def __init__(self, *args, fixed_task=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Если этап создаётся из задачи
        if fixed_task:
            # 🔒 фиксируем задачу
            self.fields['task'].initial = fixed_task
            self.fields['task'].widget = forms.HiddenInput()

            # 🎯 ФИЛЬТРУЕМ ответственных
            self.fields['student'].queryset = fixed_task.students.all()
        elif self.instance and self.instance.pk and self.instance.task:
            self.fields['student'].queryset = self.instance.task.students.all()
        else:
            # Если этап создаётся отдельно — показываем всех студентов
            self.fields['student'].queryset = User.objects.all()

    class Meta:
        model = Stage
        fields = '__all__'
        exclude = ['count']
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'end_date': 'Fecha de terminación',
        }
