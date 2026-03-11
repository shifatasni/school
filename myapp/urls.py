from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('students',views.students,name='students'),
    path('attendance/', views.attendance, name='attendance'),
    path('marks/', views.marks, name='marks'),
    path('report/', views.report, name='report'),
    path('report/<int:student_id>/', views.view_report, name='view_report'),
]

