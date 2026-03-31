from django import forms
from .models import Holiday


class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['name', 'start_date', 'end_date', 'holiday_type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Aïd El Fitr'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'holiday_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description optionnelle...'}),
        }
