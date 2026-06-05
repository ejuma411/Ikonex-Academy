from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.core.cache import cache
from .forms import StaffLoginForm

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import ClassTeacherAssignment, TeacherProfile
from .forms import UserCreationForm, UserUpdateForm, TeacherAssignmentForm, SubjectAssignmentForm
from subjects.models import TeacherSubjectAssignment, ClassSubject
from classes.models import ClassStream

User = get_user_model()


def login_view(request):
    """Handle staff login with rate limiting and session security"""
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = StaffLoginForm(request.POST or None)

    # Rate limiting: max 5 attempts per IP in 15 minutes
    ip_address = request.META.get('REMOTE_ADDR')
    cache_key = f'login_attempts_{ip_address}'
    attempts = cache.get(cache_key, 0)
    
    if attempts >= 5:
        messages.error(request, "Too many failed login attempts. Please try again later.")
        return render(request, "registration/login.html", {"form": StaffLoginForm()})

    if request.method == "POST" and form.is_valid():
        staff_no = form.cleaned_data["staff_no"].strip()
        password = form.cleaned_data["password"]
        user = authenticate(request, username=staff_no, password=password)

        if user is not None and user.is_staff:
            # Reset failed attempts on successful login
            cache.delete(cache_key)
            
            # Login the user
            login(request, user)
            
            # Set session expiry to 5 minutes (300 seconds)
            request.session.set_expiry(300)
            request.session['last_activity'] = datetime.now().timestamp()
            
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect(request.GET.get("next") or "dashboard")

        # Increment failed attempts
        cache.set(cache_key, attempts + 1, 900)  # 15 minutes timeout
        messages.error(request, "Invalid staff number or password.")

    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    """Handle staff logout with session cleanup"""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been successfully logged out.")
    return redirect("login")



@staff_member_required
def superadmin_dashboard(request):
    """Superadmin dashboard for complete user management"""
    if not request.user.role == 'superadmin':
        messages.error(request, "Access denied. Superadmin privileges required.")
        return redirect('admin:index')
    
    context = {
        'total_teachers': User.objects.filter(role='teacher').count(),
        'total_staff': User.objects.filter(role='staff').count(),
        'total_classes': ClassStream.objects.count(),
        'total_class_assignments': ClassTeacherAssignment.objects.filter(is_active=True).count(),
        'total_subject_assignments': TeacherSubjectAssignment.objects.filter(is_active=True).count(),
        'recent_users': User.objects.order_by('-date_joined')[:10],
        'recent_class_assignments': ClassTeacherAssignment.objects.select_related('class_stream', 'teacher').order_by('-assigned_date')[:10],
        'recent_subject_assignments': TeacherSubjectAssignment.objects.select_related('class_subject__class_stream', 'class_subject__subject', 'teacher').order_by('-assigned_date')[:10],
    }
    return render(request, 'accounts/superadmin/dashboard.html', context)


@staff_member_required
def user_list(request):
    """List all users with filtering options"""
    if not request.user.role == 'superadmin':
        messages.error(request, "Access denied.")
        return redirect('admin:index')
    
    role_filter = request.GET.get('role', '')
    users = User.objects.all().order_by('-date_joined')
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    context = {
        'users': users,
        'current_role': role_filter,
        'role_choices': User.ROLE_CHOICES,
    }
    return render(request, 'accounts/superadmin/user_list.html', context)


@staff_member_required
def user_create(request):
    """Create a new user (teacher or staff)"""
    if not request.user.role == 'superadmin':
        messages.error(request, "Access denied.")
        return redirect('admin:index')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                
                # Create teacher profile if role is teacher
                if user.role == 'teacher':
                    TeacherProfile.objects.create(
                        user=user,
                        qualification=form.cleaned_data.get('qualification', ''),
                        specialization=form.cleaned_data.get('specialization', ''),
                        hire_date=form.cleaned_data.get('hire_date')
                    )
                
                messages.success(request, f"User {user.get_full_name()} created successfully!")
                return redirect('user_detail', user_id=user.id)
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/superadmin/user_form.html', {'form': form, 'title': 'Create User'})


@staff_member_required
def user_detail(request, user_id):
    """View user details and assignments"""
    if not request.user.role == 'superadmin':
        messages.error(request, "Access denied.")
        return redirect('admin:index')
    
    user = get_object_or_404(User, id=user_id)
    
    # Get assignments based on role
    class_assignments = ClassTeacherAssignment.objects.filter(teacher=user, is_active=True) if user.role == 'teacher' else []
    subject_assignments = TeacherSubjectAssignment.objects.filter(teacher=user, is_active=True) if user.role == 'teacher' else []
    
    context = {
        'user': user,
        'class_assignments': class_assignments,
        'subject_assignments': subject_assignments,
    }
    return render(request, 'accounts/superadmin/user_detail.html', context)


@staff_member_required
def user_edit(request, user_id):
    """Edit user information"""
    if not request.user.role == 'superadmin':
        messages.error(request, "Access denied.")
        return redirect('admin:index')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"User {user.get_full_name()} updated successfully!")
            return redirect('user_detail', user_id=user.id)
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'accounts/superadmin/user_form.html', {'form': form, 'title': 'Edit User', 'user': user})


@staff_member_required
def user_delete(request, user_id):
    """Delete a user (soft delete or permanent)"""
    if not request.user.role == 'superadmin':
        messages.error(request, "Access denied.")
        return redirect('admin:index')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        user_name = user.get_full_name()
        user.delete()
        messages.success(request, f"User {user_name} has been deleted.")
        return redirect('user_list')
    
    return render(request, 'accounts/superadmin/user_confirm_delete.html', {'user': user})


@staff_member_required
def assign_class_teacher(request, user_id=None):
    """Assign a teacher as class teacher"""
    if not request.user.is_superuser and request.user.role != 'superadmin':
        messages.error(request, "Access denied. Superadmin privileges required.")
        return redirect('superadmin_dashboard')
    
    # Initialize form
    form = TeacherAssignmentForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            # Get cleaned data (not calling as function)
            teacher = form.cleaned_data.get('teacher')
            class_stream = form.cleaned_data.get('class_stream')
            academic_year = form.cleaned_data.get('academic_year')
            
            # Create assignment
            assignment = ClassTeacherAssignment.objects.create(
                teacher=teacher,
                class_stream=class_stream,
                academic_year=academic_year,
                assigned_by=request.user
            )
            
            messages.success(
                request, 
                f"Teacher {teacher.get_full_name()} assigned to {class_stream.name} successfully!"
            )
            
            # Redirect to user detail if user_id provided, otherwise dashboard
            if user_id:
                return redirect('user_detail', user_id=user_id)
            return redirect('superadmin_dashboard')
    
    # Pre-select teacher if user_id provided
    if user_id:
        teacher = get_object_or_404(User, id=user_id)
        form = TeacherAssignmentForm(initial={'teacher': teacher})
    
    context = {
        'form': form,
        'title': 'Assign Class Teacher'
    }
    return render(request, 'accounts/superadmin/assign_class_teacher.html', context)


@staff_member_required
def assign_subject_teacher(request, user_id=None):
    """Assign a teacher to teach a subject"""
    if not request.user.is_superuser and request.user.role != 'superadmin':
        messages.error(request, "Access denied. Superadmin privileges required.")
        return redirect('superadmin_dashboard')
    
    # Initialize form
    form = SubjectAssignmentForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            # Get cleaned data (not calling as function)
            teacher = form.cleaned_data.get('teacher')
            class_subject = form.cleaned_data.get('class_subject')
            academic_year = form.cleaned_data.get('academic_year')
            
            # Create assignment
            assignment = TeacherSubjectAssignment.objects.create(
                teacher=teacher,
                class_subject=class_subject,
                academic_year=academic_year,
                assigned_by=request.user
            )
            
            messages.success(
                request, 
                f"Teacher {teacher.get_full_name()} assigned to {class_subject} successfully!"
            )
            
            # Redirect to user detail if user_id provided, otherwise dashboard
            if user_id:
                return redirect('user_detail', user_id=user_id)
            return redirect('superadmin_dashboard')
    
    # Pre-select teacher if user_id provided
    if user_id:
        teacher = get_object_or_404(User, id=user_id)
        form = SubjectAssignmentForm(initial={'teacher': teacher})
    
    context = {
        'form': form,
        'title': 'Assign Subject Teacher'
    }
    return render(request, 'accounts/superadmin/assign_subject_teacher.html', context)
    
