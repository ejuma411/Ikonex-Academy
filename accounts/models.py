from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom User model with roles for school management"""
    
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin (Principal/Deputy Principal)'),
        ('teacher', 'Teacher'),
        ('staff', 'Administrative Staff'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    staff_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, default='')
    address = models.TextField(blank=True, default='')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    # Tracking fields
    created_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='created_users'
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_joined']
        permissions = [
            ("can_assign_teachers", "Can assign teachers to classes"),
            ("can_view_all_reports", "Can view all system reports"),
        ]
    
    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return f"{full_name} ({self.get_role_display()})"
        return f"{self.username} ({self.get_role_display()})"
    
    def get_full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return ""
    
    def is_superadmin(self):
        return self.role == 'superadmin' or self.is_superuser
    
    def is_teacher(self):
        return self.role == 'teacher'
    
    def is_staff_member(self):
        return self.role == 'staff'


class TeacherProfile(models.Model):
    """Additional teacher-specific information"""
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='teacher_profile'
    )
    qualification = models.CharField(max_length=200, blank=True, default='')
    specialization = models.CharField(max_length=100, blank=True, default='')
    hire_date = models.DateField(null=True, blank=True)
    employment_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"Profile: {self.user.get_full_name() or self.user.username}"


class ClassTeacherAssignment(models.Model):
    """Assign a teacher as class teacher"""
    
    class_stream = models.ForeignKey(
        'classes.ClassStream', 
        on_delete=models.CASCADE, 
        related_name='class_teachers'
    )
    teacher = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='class_assignments'
    )
    academic_year = models.CharField(max_length=9)
    is_active = models.BooleanField(default=True)
    assigned_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='assigned_classes'
    )
    assigned_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['class_stream', 'teacher', 'academic_year']
    
    def __str__(self):
        return f"{self.class_stream.name} - {self.teacher.get_full_name() or self.teacher.username}"