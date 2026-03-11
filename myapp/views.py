
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.

def students(request):
    return render (request,'students.html')
def home(request):
    return render (request,'home.html')
def attendance(request):
    return render (request,'attendance.html')
def marks(request):
    return render (request,'marks.html')
def report(request):
    return render (request,'report.html')
def view_report(request):
    return render (request,'view_report.html')
