from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class SchoolClass(models.Model):
    name = models.CharField(max_length=50)   # 8, 9, 10, Degree etc

    def __str__(self):
        return self.name


# STUDENT



class Student(models.Model):

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

    name = models.CharField(max_length=100)
    roll_no = models.IntegerField()
    
    school_class = models.CharField(
        max_length=20,
        choices=CLASS_CHOICES
    )

    parent_phone = models.CharField(max_length=15)
    address = models.TextField()
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({self.get_school_class_display()})"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)  # Present / Absent





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







# Each subject mark stored separately
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=50)

    subject = models.CharField(max_length=50)
    marks = models.IntegerField(default=0)

    

    def __str__(self):
        return f"{self.student.name} - {self.subject}"

    # ✅ ADD THIS
    @staticmethod
    def calculate_total(student, exam_name):
        return sum(
            m.marks for m in Marks.objects.filter(
                student=student,
                exam_name=exam_name
            )
        )

    # ✅ ADD THIS
    @staticmethod
    def calculate_grade(total):
        if total >= 270:
            return "A+"
        elif total >= 240:
            return "A"
        elif total >= 210:
            return "B"
        elif total >= 180:
            return "C"
        else:
            return "Fail"



class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class StudentNote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=50)
    note = models.TextField()   



class StudentRemark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=50)
    remark = models.TextField()

    def __str__(self):
        return f"{self.student.name} - {self.exam_name}"
    


class School(models.Model):
    name = models.CharField(max_length=100)
    background = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name