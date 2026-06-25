
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, datetime


from .models import  School, Student,Attendance, StudentNote, StudentRemark
from .forms import StudentForm

from django.shortcuts import render
from .models import Student, Attendance 

from datetime import date

def home(request):

    total_students = Student.objects.count()
    today_attendance = Attendance.objects.filter(date=date.today()).count()

    school = School.objects.first()

    if not school:
        school = School.objects.create(name="My School")

    # ✅ HANDLE BACKGROUND CHANGE (FIXED)
    if request.method == "POST":

        # 👉 BACKGROUND CHANGE
        bg = request.POST.get('bg')
        if bg:
            school.background = bg
            school.save()
            return redirect('home')

        # 👉 STUDENT FORM
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = StudentForm()

    context = {
        'total_students': total_students,
        'today_attendance': today_attendance,
        'form': form,
        'school': school,
    }

    return render(request, 'home.html', context)

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def attendance(request):
    return render(request, 'attendance.html')

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
        form = StudentForm(request.POST, request.FILES)
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
        form = StudentForm(request.POST, request.FILES, instance=student)  # ✅ FIXED
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
from django.shortcuts import render, redirect
from .models import Student, Attendance

def attendance_view(request):

    # ✅ GET or POST (IMPORTANT FIX)
    selected_class = request.GET.get('class') or request.POST.get('class')
    selected_date = request.GET.get('date') or request.POST.get('date')

    # ✅ Convert date
    if selected_date:
        selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        selected_date = date.today()

    students = Student.objects.all()

    if selected_class:
        students = students.filter(school_class=selected_class)

    students = students.order_by('school_class', 'roll_no')

    # ✅ LOAD EXISTING ATTENDANCE (for edit)
    for student in students:
        record = Attendance.objects.filter(
            student=student,
            date=selected_date
        ).first()

        student.attendance_status = record.status if record else None

    # ✅ SAVE ATTENDANCE
    if request.method == "POST":
        student_ids = request.POST.getlist('student_ids')

        for sid in student_ids:
            status = request.POST.get(f'status_{sid}')

            if status:
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

from calendar import monthrange
from datetime import datetime
from .models import Attendance, Student

def attendance_list(request):
    selected_class = request.GET.get('class')
    selected_month = request.GET.get('month')

    students = Student.objects.all()

    if selected_class:
        students = students.filter(school_class=selected_class)

    # ✅ Default month (current)
    if not selected_month:
        today = datetime.today()
        year = today.year
        month = today.month
        selected_month = f"{year}-{month:02d}"
    else:
        year, month = map(int, selected_month.split('-'))

    # ✅ Get total days in month
    total_days = monthrange(year, month)[1]
    days = list(range(1, total_days + 1))

    # ✅ Get attendance records
    records = Attendance.objects.filter(
        date__year=year,
        date__month=month
    )

    # ✅ Create dictionary: {(student_id, day): status}
    attendance_dict = {}
    for r in records:
        attendance_dict[(r.student_id, r.date.day)] = r.status

    classes = Student.objects.values_list('school_class', flat=True).distinct()

    return render(request, 'attendance_list.html', {
        'students': students,
        'days': days,
        'attendance_dict': attendance_dict,
        'selected_month': selected_month,
        'selected_class': selected_class,
        'classes': classes
    })

from django.http import HttpResponse

from django.shortcuts import render
from .models import Attendance, Student
from django.db.models import Count
import calendar

def monthly_attendance(request):
    selected_class = request.GET.get('class')
    selected_month = request.GET.get('month')  # format: 2026-06

    students = Student.objects.all()

    if selected_class:
        students = students.filter(school_class=selected_class)

    attendance_data = {}

    if selected_month:
        year, month = map(int, selected_month.split('-'))

        # get all days in month
        num_days = calendar.monthrange(year, month)[1]
        days = list(range(1, num_days + 1))

        for student in students:
            student_attendance = []

            for day in days:
                record = Attendance.objects.filter(
                    student=student,
                    date__year=year,
                    date__month=month,
                    date__day=day
                ).first()

                if record:
                    student_attendance.append(record.status)
                else:
                    student_attendance.append('-')

            attendance_data[student] = student_attendance
    else:
        days = []

    classes = Student.objects.values_list('school_class', flat=True).distinct()

    return render(request, 'monthly_attendance.html', {
        'attendance_data': attendance_data,
        'days': days,
        'classes': classes,
        'selected_class': selected_class,
        'selected_month': selected_month,
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










from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Marks
from django.db.models import Q
from django.contrib import messages


from .models import Student, Marks, Subject
from django.contrib import messages

def marks_entry(request):
    selected_class = request.GET.get('class')

    if selected_class:
        students = Student.objects.filter(school_class=selected_class)
    else:
        students = Student.objects.all()

    subjects = Subject.objects.all()

    # ================= ADD SUBJECT =================
    if request.method == "POST" and 'add_subject' in request.POST:
        new_subject = request.POST.get('new_subject')

        if new_subject:
            Subject.objects.get_or_create(
                name=new_subject.strip().title()
            )

        return redirect('marks')

    # ================= SAVE MARKS + REMARK =================
    if request.method == "POST" and 'save_marks' in request.POST:
        exam_name = request.POST.get('exam_name')

        for student in students:

            # ✅ SAVE REMARK (ONE PER STUDENT)
            remark = request.POST.get(f"remark_{student.id}")
            if remark:
                StudentRemark.objects.update_or_create(
                    student=student,
                    exam_name=exam_name,
                    defaults={'remark': remark}
                )

            # ✅ SAVE MARKS
            for subject in subjects:
                key = f"{student.id}_{subject.id}"
                mark = request.POST.get(key)

                if mark not in [None, ""]:
                    Marks.objects.update_or_create(
                        student=student,
                        exam_name=exam_name,
                        subject=subject.name,
                        defaults={
                            'marks': int(mark)
                        }
                    )

        messages.success(request, "Marks & remarks saved successfully!")
        return redirect('marks')

    # ================= PAGE LOAD =================
    return render(request, 'marks.html', {
        'students': students,
        'subjects': subjects,
        'selected_class': selected_class
    })



from .models import Student, Marks, Subject
def view_marks(request):
    selected_class = request.GET.get('class')
    exam_name = request.GET.get('exam', 'Mid Term')

    if selected_class:
        students = Student.objects.filter(school_class=selected_class)
    else:
        students = Student.objects.all()

    subjects = Subject.objects.all()   # ✅ FIXED

    marks = Marks.objects.filter(exam_name=exam_name)

    table_data = []

    for student in students:
        row = {
            'student': student,
            'marks': [],
            'total': 0
        }

        total = 0

        for subject in subjects:
            mark_obj = marks.filter(
                student=student,
                subject=subject   # ✅ must be object
            ).first()

            if mark_obj:
                mark = mark_obj.marks
                total += mark
            else:
                mark = "-"

            row['marks'].append(mark)

        row['total'] = total
        row['grade'] = Marks.calculate_grade(total)

        table_data.append(row)

    remarks = StudentRemark.objects.filter(exam_name=exam_name)



    return render(request, 'view_marks.html', {
        'subjects': subjects,
        'table_data': table_data,
        'exam_name': exam_name,
         'remarks': remarks,
    })

def edit_student_marks(request, student_id, exam_name):
    student = get_object_or_404(Student, id=student_id)
    subjects = Subject.objects.all()

    marks_qs = Marks.objects.filter(student=student, exam_name=exam_name)

    # create dictionary {subject: marks}
    marks_dict = {m.subject: m.marks for m in marks_qs}

    if request.method == "POST":
        for subject in subjects:
            mark = request.POST.get(subject.name)

            Marks.objects.update_or_create(
    student=student,
    exam_name=exam_name,
    subject=subject,   # ✅ CORRECT
                defaults={
                    'marks': int(mark) if mark else 0
                }
            )

        return redirect('view_marks')

    return render(request,  'edit_marks.html', {
        'student': student,
        'subjects': subjects,
        'marks_dict': marks_dict,
        'exam_name': exam_name
    })


def delete_student_marks(request, student_id, exam_name):
    student = get_object_or_404(Student, id=student_id)

    Marks.objects.filter(
        student=student,
        exam_name=exam_name
    ).delete()

    return redirect('view_marks')






from calendar import monthrange
from datetime import date
from django.shortcuts import render, get_object_or_404
from .models import Student, Attendance, Marks
from collections import defaultdict


from datetime import date
import calendar
from calendar import monthrange
from collections import defaultdict

def student_detail(request, id):
    student = get_object_or_404(Student, id=id)

    today = date.today()

    # ✅ DEFINE FIRST (IMPORTANT)
    try:
        month = int(request.GET.get('month', today.month))
        year = int(request.GET.get('year', today.year))
    except:
        month = today.month
        year = today.year

    # ✅ Attendance filter
    attendance = Attendance.objects.filter(
        student=student,
        date__year=year,
        date__month=month
    )

    attendance_dict = {a.date.day: a.status for a in attendance}

    total_days = monthrange(year, month)[1]

    calendar_days = []
    for d in range(1, total_days + 1):
        calendar_days.append({
            'day': d,
            'status': attendance_dict.get(d)
        })

    # ✅ calendar
    cal = calendar.monthcalendar(year, month)

    # ✅ dropdown lists
    months = list(range(1, 13))
    years = list(range(2026, 2031))

    # ✅ MARKS
    marks = Marks.objects.filter(student=student)

    subjects = list(set(m.subject for m in marks))

    exam_data = defaultdict(dict)

    for m in marks:
        exam_data[m.exam_name][m.subject] = m.marks

    exam_list = []

    for exam, sub_marks in exam_data.items():
        marks_list = []
        total = 0
        count = 0

        for sub in subjects:
            mark = sub_marks.get(sub)

            if mark is not None:
                total += mark
                count += 1

            marks_list.append(mark)

        avg = total / count if count > 0 else 0

        if avg >= 90:
            grade = "A+"
        elif avg >= 75:
            grade = "A"
        elif avg >= 60:
            grade = "B"
        elif avg >= 50:
            grade = "C"
        else:
            grade = "Fail"

        exam_list.append({
            'exam': exam,
            'marks': marks_list,
            'total': total,
            'grade': grade
        })

    remarks = StudentRemark.objects.filter(student=student)

    return render(request, 'student_detail.html', {
        'student': student,
        'calendar_days': calendar_days,
        'calendar_weeks': cal,
        'month': month,
        'year': year,
        'month_name': calendar.month_name[month],
        'subjects': subjects,
        'exam_list': exam_list,
        'months': months,
        'years': years,
        'remarks': remarks,
        
    })





def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == "POST":
        new_name = request.POST.get("name")

        if new_name:
            subject.name = new_name.strip().title()
            subject.save()

        return redirect('marks')

    return render(request, "edit_subject.html", {
        "subject": subject
    })


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == "POST":
        subject.delete()
        return redirect('marks')


from .forms import NoteForm

def add_note(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.student = student
            note.save()
            return redirect('student_detail', id=student.id)
    else:
        form = NoteForm()

    return render(request, 'add_note.html', {
        'form': form,
        'student': student
    })



def edit_remark(request, id):
    remark = StudentRemark.objects.get(id=id)

    if request.method == "POST":
        remark.remark = request.POST.get('remark')
        remark.save()
        return redirect('view_marks')

    return render(request, 'edit_remark.html', {'remark': remark})





