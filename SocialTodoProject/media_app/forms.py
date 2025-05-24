from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class':'w-full border border-black p-2 rounded','rows':4})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class':'w-full border border-black p-2 rounded','rows':3})
        }

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        widgets = {
            'content': forms.Textarea(attrs={'class':'w-full border border-black p-2 rounded','rows':3})
        }
