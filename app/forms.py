from django.forms import ModelForm
from app.models import TODO
from django import forms


class TODOForm(ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'status', 'priority']

        # added styles for the form
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
