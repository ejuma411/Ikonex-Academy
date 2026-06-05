from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import ClassTeacherAssignment
from classes.models import ClassStream
from subjects.models import ClassSubject

User = get_user_model()


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




class UserCreationForm(forms.ModelForm):
    """Form for superadmin to create new users"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        validators=[validate_password]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )
    
    # Teacher-specific fields
    qualification = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    specialization = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    hire_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'staff_id', 'phone_number', 'address']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'staff_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Form for superadmin to edit users"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'staff_id', 'phone_number', 'address', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'staff_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TeacherAssignmentForm(forms.Form):
    """Form for assigning class teacher"""
    teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(role='teacher'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Teacher"
    )
    class_stream = forms.ModelChoiceField(
        queryset=ClassStream.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Class Stream"
    )
    academic_year = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2024/2025'}),
        label="Academic Year"
    )


class SubjectAssignmentForm(forms.Form):
    """Form for assigning subject teacher"""
    teacher = forms.ModelChoiceField(
        queryset=User.objects.filter(role='teacher'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Teacher"
    )
    class_subject = forms.ModelChoiceField(
        queryset=ClassSubject.objects.select_related('class_stream', 'subject'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Class & Subject"
    )
    academic_year = forms.CharField(
        max_length=9,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2024/2025'}),
        label="Academic Year"
    )