from django import forms
from .models import Task, Stage
from myauth.models import User
from django.contrib.auth import get_user_model
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
    class Meta:
        model = Task
        fields = '__all__'
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
        # 1. Pop the custom argument 'user_group'
        user_group = kwargs.pop('user_group', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        # 2. Use the argument to filter the queryset for the 'students' field
        if user_group:
            self.fields['students'].queryset = User.objects.filter(
                group=user_group,
                is_student=True
            ).order_by('last_name')
        else:
            # Fallback for users without a group (e.g., superusers)
            self.fields['students'].queryset = User.objects.all()


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
