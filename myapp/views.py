
from datetime import date, datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import  Student,Attendance
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Student, Attendance, TeacherProfile

def home(request):
    return render(request, 'home.html')
def attendance(request):
    return render(request, 'attendance.html')
def marks(request):
    return render(request, 'marks.html')
def report(request):
    return render(request, 'report.html')


def students(request):
    selected_class = request.GET.get('class')

    # ✅ FILTER + ORDER
    if selected_class:
        students = Student.objects.filter(
            school_class=selected_class
        ).order_by('roll_no')
    else:
        students = Student.objects.all().order_by('school_class', 'roll_no')

    # ✅ ADD STUDENT (POST)
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = StudentForm()

    # ✅ GET ALL CLASSES FOR DROPDOWN
    classes = Student.objects.values_list('school_class', flat=True).distinct()

    return render(request, 'students.html', {
        'students': students,
        'form': form,
        'classes': classes,
        'selected_class': selected_class
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


from datetime import datetime, date

def attendance_view(request):

    selected_class = request.GET.get('class')
    selected_date = request.GET.get('date')

    if selected_date:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        selected_date = date.today()

    students = Student.objects.all()

    if selected_class:
        students = students.filter(school_class=selected_class)

    students = students.order_by('school_class', 'roll_no')

    # ✅ SAVE ATTENDANCE
    if request.method == "POST":
        student_ids = request.POST.getlist('student_ids')

        for sid in student_ids:
            status = request.POST.get(f'status_{sid}')

            if status:  # only if selected
                Attendance.objects.update_or_create(
                    student_id=sid,
                    date=selected_date,
                    defaults={'status': status}
                )

        return redirect(f'/attendance/?class={selected_class}&date={selected_date}')

    classes = Student.objects.values_list('school_class', flat=True).distinct()

    return render(request, 'attendance.html', {
        'students': students,
        'classes': classes,
        'selected_class': selected_class,
        'selected_date': selected_date,
    })

from .models import Attendance

from collections import defaultdict

def attendance_list(request):
    selected_class = request.GET.get('class')

    records = Attendance.objects.select_related('student')

    if selected_class:
        records = records.filter(student__school_class=selected_class)

    records = records.order_by('student__school_class', 'student__roll_no', '-date')

    grouped_records = defaultdict(list)

    for r in records:
        grouped_records[r.student.school_class].append(r)

    classes = Student.objects.values_list('school_class', flat=True).distinct()

    return render(request, 'attendance_list.html', {
        'grouped_records': dict(grouped_records),
        'classes': classes,
        'selected_class': selected_class
    })

   
def class_students_list(request):

    selected_class = request.GET.get('class')

    students = Student.objects.filter(
        school_class=selected_class
    ).order_by('roll_no')   # ⭐ THIS IS THE FIX

    return render(request, 'class_students_list.html', {
        'students': students,
        'selected_class': selected_class
    })  