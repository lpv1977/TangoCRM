from django import forms
from .models import Student, Lesson

class LessonQuickForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['student','date','start_time','count','pay_source','note']
        widgets = {'date': forms.DateInput(attrs={'type':'date'}),
                   'start_time': forms.TimeInput(attrs={'type':'time'})}

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name','phone','email','note','price_single']
