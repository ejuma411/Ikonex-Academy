from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    """
    Custom User model
    """

    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('teacher', 'Teacher'),
        ('staff', 'Administrative Staff'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    staff_id = models.CharField(max_length=20, unique=True, blank=True, null=True)

    phone_number = models.CharField(max_length=15, blank=True, default='')
    address = models.TextField(blank=True, default='')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_users'
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_joined']

    def save(self, *args, **kwargs):
        if not self.staff_id:
            self.staff_id = self.generate_staff_id()
        super().save(*args, **kwargs)

    def generate_staff_id(self):
        prefix_map = {
            'teacher': 'TCH',
            'staff': 'STF',
            'superadmin': 'ADM',
        }

        prefix = prefix_map.get(self.role, 'USR')

        last_user = User.objects.filter(
            role=self.role,
            staff_id__startswith=prefix
        ).order_by('-id').first()

        if last_user and last_user.staff_id:
            try:
                last_num = int(last_user.staff_id.replace(prefix, ''))
                new_num = last_num + 1
            except ValueError:
                new_num = 1
        else:
            new_num = 1

        return f"{prefix}{new_num:04d}"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.staff_id})"


# -------------------------
# Teacher Profile
# -------------------------
class TeacherProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )

    qualification = models.CharField(max_length=200, blank=True, default='')
    specialization = models.CharField(max_length=100, blank=True, default='')
    hire_date = models.DateField(null=True, blank=True)
    employment_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user}"


# -------------------------
# Class Teacher Assignment
# -------------------------
class ClassTeacherAssignment(models.Model):
    """
    Safe FK design: no circular dependency issues
    """

    class_stream = models.ForeignKey(
        'classes.ClassStream',
        on_delete=models.CASCADE,
        related_name='class_teachers'
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='class_assignments'
    )

    academic_year = models.CharField(max_length=9)
    is_active = models.BooleanField(default=True)

    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_classes'
    )

    assigned_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('class_stream', 'teacher', 'academic_year')
        ordering = ['-academic_year']

    def __str__(self):
        return f"{self.class_stream} - {self.teacher}"