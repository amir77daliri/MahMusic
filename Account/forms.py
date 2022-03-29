from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
import re

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'username', 'id': 'username', 'class': 'form-control'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'password', 'id': 'password', 'class': 'form-control'})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            self.user_cache = User.objects.filter(username=username).first()
            if self.user_cache is None:
                self.add_error('username', 'incorrect username')
            else:
                self.confirm_login_allowed(self.user_cache)
                if self.user_cache.check_password(password):
                    return self.cleaned_data
                else:
                    self.add_error('password', 'incorrect password')
                    if not self.user_cache.is_active:
                        self.add_error('password', 'user is not active')
        return self.cleaned_data


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'username', 'id': 'username', 'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'id': 'email', 'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'password', 'id': 'password1', 'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Confirm-Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'confirm-password', 'id': 'password2', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if validate_email(email):
            return email
        raise forms.ValidationError("Incorrect Email")


def validate_email(email):
    if re.match(r'^[a-zA-Z0-9\.\_]+@[a-zA-Z0-9]+\.[a-zA-Z]{3}$', email):
        return True
    return False
