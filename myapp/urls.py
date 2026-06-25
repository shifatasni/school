from django.urls import path
from .import views


urlpatterns = [
    
    path('', views.home, name='home'),
    path('attendance/', views.attendance_view, name='attendance'),
    path('attendance-list/', views.attendance_list, name='attendance_list'),
    path('marks/', views.marks_entry, name='marks'),
    path('view-marks/', views.view_marks, name='view_marks'),
    path('edit-student-marks/<int:student_id>/<str:exam_name>/', views.edit_student_marks, name='edit_student_marks'),
    path('delete-student-marks/<int:student_id>/<str:exam_name>/', views.delete_student_marks, name='delete_student_marks'),
    path('report/', views.report, name='report'),
    path('students/', views.students, name='students'), 
    path('monthly-attendance/', views.monthly_attendance, name='monthly_attendance'),
    path('student/edit/<int:id>/', views.edit_student, name='edit_student'),
    path('student/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('student/<int:id>/', views.student_detail, name='student_detail'),
    path('edit-subject/<int:subject_id>/', views.edit_subject, name='edit_subject'),
    path('delete-subject/<int:subject_id>/', views.delete_subject, name='delete_subject'),
    path('edit-remark/<int:id>/', views.edit_remark, name='edit_remark'),
    path('students/', views.student_list, name='student_list'),
]
