from django.urls import path
from .import views

urlpatterns = [
    path('',views.new,name='new'),
     path('students',views.new,name='students'),
]