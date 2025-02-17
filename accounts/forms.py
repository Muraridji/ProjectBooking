from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(label="Введіть нікнейм", widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(),
            'email': forms.EmailInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }