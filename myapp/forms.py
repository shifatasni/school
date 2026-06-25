from django import forms
from django.db import models

from .models import Student
from .models import Attendance

CLASS_CHOICES = [
    ('8', 'Class 8'),
    ('9', 'Class 9'),
    ('10', 'Class 10'),
    ('+1', 'Plus One'),
    ('+2', 'Plus Two'),
    ('ug1', 'Degree 1st Year'),
    ('ug2', 'Degree 2nd Year'),
    ('ug3', 'Degree 3rd Year'),
]

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'roll_no', 'school_class', 'parent_phone', 'address', 'photo']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status']



from django import forms
from .models import StudentNote

class NoteForm(forms.ModelForm):
    class Meta:
        model = StudentNote
        fields = ['exam_name', 'note']


from .models import School

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'background']