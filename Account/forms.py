from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordResetForm
)
import re

User = get_user_model()


def validate_email(email):
    if re.match(r'^[a-zA-Z0-9\.\_]+@[a-zA-Z0-9]+\.[a-zA-Z]{3}$', email):
        return True
    return False


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


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
                   'first_name': forms.TextInput(attrs={'placeholder': 'first_name'}),
                   'last_name': forms.TextInput(attrs={'placeholder': 'last_name'})
                   }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if validate_email(email):
            check_email_exist = User.objects.filter(email=email).exclude(email=self.user.email).exists()
            if check_email_exist:
                raise forms.ValidationError("This email has been used by others")
            return email
        raise forms.ValidationError("Incorrect Email")

class SetNewResetPasswordForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetNewResetPasswordForm, self).__init__(*args, **kwargs)

    new_password1 = forms.CharField(
        label="new-password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'new-password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="confirm new-password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'placeholder': 'confirm-password'}),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data['new_password1']
        password2 = self.cleaned_data['new_password2']
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("New passwords dose not match")
        return password2

    def save(self, commit=True):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class ChangePasswordForm(SetNewResetPasswordForm):
    old_password = forms.CharField(
        label= "old_password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'placeholder': 'old-password', 'autofocus': True}),
    )
    """
    Validate that the old_password field is correct.
    """
    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError("Wrong old password- Try again")
        return old_password


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'placeholder': 'email'})
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if validate_email(email):
            return email
        raise forms.ValidationError("wrong email syntax! Try again")


