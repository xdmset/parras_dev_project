# pendientes/forms.py
from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    """
    Formulario para la creación y edición de Pendientes.
    """
    class Meta:
        model = Todo
        fields = ['user_id', 'api_id', 'title', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'user_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'api_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'user_id': 'ID del Usuario (de la API)',
            'api_id': 'ID del Pendiente (de la API)',
            'title': 'Título del Pendiente',
            'completed': '¿Está completado?',
        }