from django.contrib import admin
from .models import (
    Salon,
    Client,
    Specialist,
    Category,
    Service,
    Order,
    TimeSlot,
    WorkDay
)


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    fields = ('name', 'address', 'work_time','image')
    list_display = ('name', 'address', 'work_time', )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', )


class WorkDayInline(admin.TabularInline):
    model = Specialist.workdays.through
    extra = 0


@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    fields = ('name', 'specialization', 'salon', 'foto', 'experience', )
    list_display = ('name', 'specialization', 'salon', 'foto', 'experience',)
    inlines = [WorkDayInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    fields = ('name', 'category', 'descriptions', 'image', 'price')
    list_display = ('name', 'category', 'descriptions', 'image', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = ('client', 'procedure', 'salon', 'specialist', 'order_hour', 'payment_method', 'payment_status', )
    list_display = ('client', 'procedure', 'salon', 'specialist', 'order_hour', 'payment_method', 'payment_status', )


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    fields = ('start_time', 'date', 'specialist', 'is_available')


@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    pass



