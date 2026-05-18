
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm


def home(request):
    return render(request, 'home.html')

def attendance(request):
    return render(request, 'attendance.html')
def marks(request):
    return render(request, 'marks.html')
def report(request):
    return render(request, 'report.html')


# ✅ STUDENTS PAGE + ADD
def students(request):
    students = Student.objects.all()

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = StudentForm()

    return render(request, 'students.html', {
        'students': students,
        'form': form
    })


# ✅ EDIT STUDENT
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = StudentForm(instance=student)

    return render(request, 'edit_student.html', {
        'form': form,
        'student': student
    })


# ✅ DELETE (SAFE)
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()

    return redirect('students')