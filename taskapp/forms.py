from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Task, Stage

class TaskForm(forms.ModelForm):
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = Task
        fields = '__all__'

    # def form_valid(self, form):
    #     task = form.save(commit=False)
    #     if 'file' in self.request.FILES:
    #         contract.file = self.request.FILES['file']
    #     contract.save()
    #     return super().form_valid(form)

class StageForm(forms.ModelForm):
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = Stage
        fields = '__all__'