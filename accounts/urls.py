from django.urls import path
from . import views

# app_name = 'accounts'

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
    # Superadmin user management
    path('superadmin/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('superadmin/users/', views.user_list, name='user_list'),
    path('superadmin/users/create/', views.user_create, name='user_create'),
    path('superadmin/users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('superadmin/users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('superadmin/users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    
    # Assignment management
    path('superadmin/assign-class-teacher/', views.assign_class_teacher, name='assign_class_teacher'),
    path('superadmin/assign-class-teacher/<int:user_id>/', views.assign_class_teacher, name='assign_class_teacher_to_user'),
    path('superadmin/assign-subject-teacher/', views.assign_subject_teacher, name='assign_subject_teacher'),
    path('superadmin/assign-subject-teacher/<int:user_id>/', views.assign_subject_teacher, name='assign_subject_teacher_to_user'),
]
