from django import forms
from .models import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_id', 'department_name', 'head_of_department', 'start_date', 'no_of_students']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'department_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Informatique'}),
            # Ajoute d'autres widgets pour le style si nécessaire
        }