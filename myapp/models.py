from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class SchoolClass(models.Model):
    name = models.CharField(max_length=50)   # 8, 9, 10, Degree etc

    def __str__(self):
        return self.name


# STUDENT



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

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField()
    school_class = models.CharField(max_length=20)   # 👈 this is key
    parent_phone = models.CharField(max_length=15)
    address = models.TextField()

     
     
    def __str__(self):
        return self.name




class Attendance(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    status = models.CharField(
        max_length=10,
        choices=[
            ('Present', 'Present'),
            ('Absent', 'Absent'),
        ]
    )

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"





class ClassRoom(models.Model):
    name = models.CharField(max_length=50)  # e.g. 8A, 10B, Degree

    def __str__(self):
        return self.name


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

def get_teacher_class(request):
    return request.user.teacherprofile.classroom











