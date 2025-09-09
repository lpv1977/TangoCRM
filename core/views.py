from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from .models import Student, Lesson, Payment, Block
from .forms import LessonQuickForm, StudentForm

def dashboard(request):
    today = timezone.localdate()
    lessons = Lesson.objects.filter(date=today).order_by('start_time')
    revenue_month = Payment.objects.filter(date__month=today.month, date__year=today.year).aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'dashboard.html', {'today_lessons': lessons, 'revenue_month': revenue_month})

def lesson_quick_create(request):
    if request.method == 'POST':
        form = LessonQuickForm(request.POST)
        if form.is_valid():
            form.save(); return redirect('dashboard')
    else:
        form = LessonQuickForm()
    return render(request, 'lesson_form.html', {'form': form})

def students(request):
    qs = Student.objects.all().order_by('name')
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save(); return redirect('core:students')
    else:
        form = StudentForm()
    return render(request, 'students.html', {'students': qs, 'form': form})
