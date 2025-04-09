from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm,
    AuthenticationForm, AdminPasswordChangeForm
)

from users.models import User
from .constants import USER_EMAIL_EXIST_ERR

QUser = get_user_model()


class AddUserForm(UserCreationForm):

    def clean_email(self):
        email = self.cleaned_data["email"]
        users = QUser.objects.filter(email__iexact=email)
        if users.exists():
            raise forms.ValidationError(USER_EMAIL_EXIST_ERR)
        return email.lower()


class ChangeUserForm(UserChangeForm):

    def clean_email(self):
        email = self.cleaned_data["email"]
        if self.instance.id:
            users = QUser.objects.filter(email__iexact=email).exclude(
                id=self.instance.id)
        else:
            users = QUser.objects.filter(email__iexact=email)
        if users.exists():
            raise forms.ValidationError(USER_EMAIL_EXIST_ERR)
        return email.lower()


class ChangeAdminPasswordForm(AdminPasswordChangeForm):

    def save(self, commit=True):
        """
        Saves the new password.
        """
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
            self.user.generate_secure_token()
        return self.user


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email.lower()).exists():
            raise ValidationError(USER_EMAIL_EXIST_ERR)
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            raise ValidationError("Passwords do not match.")
        return cleaned_data
