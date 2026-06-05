from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .forms import StaffUserChangeForm, StaffUserCreationForm

User = get_user_model()

# Unregister the default User admin if already registered
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = StaffUserCreationForm
    form = StaffUserChangeForm
    model = User

    list_display = ("username", "first_name", "last_name", "email", "role", "staff_id", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email", "staff_id")
    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Information", {"fields": ("first_name", "last_name", "email", "phone_number", "address")}),
        ("Staff Information", {"fields": ("role", "staff_id", "profile_picture")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),  # Removed updated_at
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "role",
                    "staff_id",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        """Make staff_id read-only after creation"""
        if obj:  # Editing existing object
            return self.readonly_fields + ('staff_id',)
        return self.readonly_fields


from .models import TeacherProfile, ClassTeacherAssignment


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'qualification', 'specialization', 'hire_date', 'employment_number')
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'employment_number')
    list_filter = ()
    raw_id_fields = ('user',)


@admin.register(ClassTeacherAssignment)
class ClassTeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ('class_stream', 'teacher', 'academic_year', 'is_active')
    list_filter = ('academic_year', 'is_active')
    search_fields = ('class_stream__name', 'teacher__first_name', 'teacher__last_name')
    raw_id_fields = ('teacher', 'assigned_by')
    
    def save_model(self, request, obj, form, change):
        if not obj.assigned_by:
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)