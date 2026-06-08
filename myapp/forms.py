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
    school_class = forms.ChoiceField(choices=CLASS_CHOICES)

    class Meta:
        model = Student
        fields = '__all__'


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['status']