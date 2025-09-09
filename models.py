from django.utils import timezone
from django.db import models

LESSON_DURATION_MIN = 45

class Student(models.Model):
    name = models.CharField('Имя', max_length=120)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True)
    email = models.EmailField('Email', blank=True, null=True)
    note = models.TextField('Заметки', blank=True, null=True)
    price_single = models.DecimalField('Цена разового', max_digits=10, decimal_places=2, default=0)
    class Meta: ordering=['name']; verbose_name='Ученик'; verbose_name_plural='Ученики'
    def __str__(self): return self.name

class Block(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='blocks', verbose_name='Ученик')
    lessons_total = models.PositiveIntegerField('Уроков в блоке')
    price = models.DecimalField('Цена блока', max_digits=10, decimal_places=2)
    purchased_at = models.DateField('Дата покупки' , default=timezone.localdate)
    lessons_used = models.PositiveIntegerField('Списано', default=0)
    created_at = models.DateField('Создан', auto_now_add=True)
    is_active = models.BooleanField('Активный', default=True)
    class Meta: verbose_name='Блок'; verbose_name_plural='Блоки'
    @property
    def lessons_left(self): return max(0, self.lessons_total - self.lessons_used)

class Lesson(models.Model):
    STATUS=[('hold','бронь'),('done','проведён'),('canceled','отменён')]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lessons', verbose_name='Ученик')
    date = models.DateField('Дата')
    start_time = models.TimeField('Начало')
    count = models.PositiveIntegerField('Кол-во уроков', default=1)
    pay_source = models.CharField('Оплата', max_length=10, choices=[('single','разовая'),('block','с блока')], default='single')
    status = models.CharField('Статус', max_length=10, choices=STATUS, default='hold')
    note = models.TextField('Заметка', blank=True, null=True)
    class Meta: ordering=['-date','-start_time']; verbose_name='Урок'; verbose_name_plural='Уроки'

class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments', verbose_name='Ученик')
    date = models.DateField('Дата', default=timezone.localdate)
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    method = models.CharField('Метод', max_length=20, choices=[('cash','наличные'),('transfer','перевод')], default='cash')
    note = models.TextField('Заметка', blank=True, null=True)
    class Meta: ordering=['-date']; verbose_name='Платёж'; verbose_name_plural='Платежи'
