from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SchoolClass(models.Model):
    name = models.CharField(max_length=50)   # 8, 9, 10, Degree etc

    def __str__(self):
        return self.name


# STUDENT
class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField()
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
    parent_phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name


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
    school_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    parent_phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name







