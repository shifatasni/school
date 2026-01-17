from urllib import request, response
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render

# Create your views here.
def new(request):
    return render (request,'new.html')
def students(request):
    return render (request,'students.html')
