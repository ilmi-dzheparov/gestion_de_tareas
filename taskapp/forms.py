from django import forms
from .models import Task, Stage
from django.contrib.auth import get_user_model
User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            # --- Widget para ManyToManyField ---
            # 'students': forms.CheckboxSelectMultiple(),
            'students': forms.SelectMultiple(attrs={'class': 'select2-multiple'}),
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

    # Opcional: Puedes personalizar el queryset aquí para asegurarte de que solo
    # se muestren los usuarios que son estudiantes, aunque limit_choices_to
    # en el modelo ya debería ocuparse de ello.
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['assigned_to'].queryset = settings.AUTH_USER_MODEL.objects.filter(is_student=True)


    # def form_valid(self, form):
    #     task = form.save(commit=False)
    #     if 'file' in self.request.FILES:
    #         contract.file = self.request.FILES['file']
    #     contract.save()
    #     return super().form_valid(form)

class StageForm(forms.ModelForm):

    class Meta:
        model = Stage
        fields = '__all__'
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'end_date': 'Fecha de terminación',
        }
