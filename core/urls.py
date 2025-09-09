from django.urls import path
from . import views
app_name='core'
urlpatterns = [
    path('lessons/new/', views.lesson_quick_create, name='lesson_new'),
    path('students/', views.students, name='students'),
]
