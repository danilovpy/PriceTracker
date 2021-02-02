from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, PasswordInput
from .models import Item


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input100', 'placeholder': 'Repeat your password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={'class': 'input100', 'placeholder': 'Username'}),
            'email': TextInput(attrs={'class': 'input100', 'placeholder': 'Email'}),
        }


class CreateTrackItem(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('url',)
