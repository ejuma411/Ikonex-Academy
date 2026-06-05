from django.urls import path

from . import views

urlpatterns = [
    path("", views.report_list, name="report_list"),
    path("results/", views.result_list, name="result_list"),
    path('results/student/<int:student_id>/pdf/', views.student_report_pdf, name='student_report_pdf'),
    path("class/<int:class_id>/pdf/", views.class_report_pdf, name="class_report_pdf"),
    path('reports/class/<int:class_id>/pdf/', views.class_report_pdf, name='class_report_pdf'),
]
