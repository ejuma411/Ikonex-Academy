from django.urls import path
from . import views

urlpatterns = [
    path('', views.assessment_list, name='assessment_list'),
    path('create/', views.assessment_create, name='assessment_create'),
    path('<int:pk>/', views.assessment_detail, name='assessment_detail'),
    path('<int:pk>/update/', views.assessment_update, name='assessment_update'),
    path('<int:pk>/delete/', views.assessment_delete, name='assessment_delete'),

    path('scores/', views.score_list, name='score_list'),
    path('scores/create/', views.score_create, name='score_create'),
    path('results/student/<int:pk>/', views.student_result_view, name='student_result'),
path('results/class/<int:class_id>/', views.class_result_view, name='class_result'),
]