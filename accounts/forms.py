from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class StaffLoginForm(forms.Form):
    staff_no = forms.CharField(
        label="Staff No",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter staff number"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"}),
    )


class StaffUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "is_staff", "is_superuser")
        labels = {
            "username": "Staff No",
            "is_staff": "Active Staff Account",
            "is_superuser": "Administrator Access",
        }


class StaffUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "is_staff", "is_superuser", "is_active")
        labels = {
            "username": "Staff No",
            "is_staff": "Active Staff Account",
            "is_superuser": "Administrator Access",
        }
