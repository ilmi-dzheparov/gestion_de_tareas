from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Task, Stage

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'end_date': 'Fecha de terminación',
        }

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
