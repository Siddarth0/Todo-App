from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','completed']
        widgets = {
            'title': forms.TextInput(attrs={'class':'w-full border border-black p-2 rounded'}),
            'completed': forms.CheckboxInput(attrs={'class':'mr-2'}),
        }
