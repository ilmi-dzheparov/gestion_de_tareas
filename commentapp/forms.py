from django import forms
from .models import CommentTask, CommentStage

class CommentTaskForm(forms.ModelForm):
    class Meta:
        model = CommentTask
        fields = ['comment']  # Solo pedimos el texto, la tarea la asignamos internamente
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu comentario...'}),
        }


class CommentStageForm(forms.ModelForm):
    class Meta:
        model = CommentStage
        fields = ['comment']  # Solo pedimos el texto, la tarea la asignamos internamente
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe tu comentario...'}),
        }