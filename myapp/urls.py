from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
     path('attendance/', views.attendance_view, name='attendance'),
   path('attendance-list/', views.attendance_list, name='attendance_list'),
    path('marks/', views.marks, name='marks'),
    path('report/', views.report, name='report'),
    path('students/', views.students, name='students'), 
   
    path('student/edit/<int:id>/', views.edit_student, name='edit_student'),
    path('student/delete/<int:id>/', views.delete_student, name='delete_student'),
]

