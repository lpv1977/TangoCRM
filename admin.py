from django.contrib import admin
from .models import Student, Lesson, Block, Payment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display=('name','phone','email','price_single')
    search_fields=('name','phone','email')

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display=('student','lessons_total','lessons_used','price','is_active','created_at','purchased_at')
    list_filter=('is_active',)
    search_fields=('student__name',)

    def save_model(self, request, obj, form, change):
        from .models import Payment
        is_create = not change
        super().save_model(request, obj, form, change)
        if is_create and obj.price and obj.price > 0:
            Payment.objects.create(
                student=obj.student,
                date=obj.purchased_at,
                amount=obj.price,
                method='cash',
                note=f'Оплата блока на {obj.lessons_total} урок(ов)'
                )

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display=('student','date','start_time','count','pay_source','status')
    list_filter=('status','pay_source','date')
    search_fields=('student__name',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=('student','date','amount','method')
    list_filter=('method',)
    search_fields=('student__name',)
