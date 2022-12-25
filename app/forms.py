from django.forms import ModelForm
from app.models import TODO
from django import forms


class TODOForm(ModelForm):
    class Meta:
        model = TODO
        fields = ['title', 'status', 'priority']
