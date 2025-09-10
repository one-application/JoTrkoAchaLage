from django.contrib import admin
from .models import (
    Hostel, Room, HostelAllotment, Mess, MessSubscription, 
    MessMenu, HostelComplaint
)


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ['name', 'total_rooms', 'monthly_rent', 'warden_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'warden_name']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['hostel', 'room_number', 'room_type', 'floor', 'is_available', 'monthly_rent']
    list_filter = ['hostel', 'room_type', 'is_available']
    search_fields = ['room_number', 'hostel__name']


@admin.register(HostelAllotment)
class HostelAllotmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'room', 'status', 'start_date', 'monthly_rent']
    list_filter = ['status', 'start_date']
    search_fields = ['student__username', 'room__room_number']


@admin.register(Mess)
class MessAdmin(admin.ModelAdmin):
    list_display = ['name', 'hostel', 'capacity', 'monthly_fee', 'is_active']
    list_filter = ['is_active', 'hostel']
    search_fields = ['name', 'hostel__name']


@admin.register(MessSubscription)
class MessSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['student', 'mess', 'status', 'start_date', 'monthly_fee']
    list_filter = ['status', 'start_date']
    search_fields = ['student__username', 'mess__name']


@admin.register(MessMenu)
class MessMenuAdmin(admin.ModelAdmin):
    list_display = ['mess', 'date', 'meal_type']
    list_filter = ['date', 'meal_type', 'mess']
    search_fields = ['mess__name']


@admin.register(HostelComplaint)
class HostelComplaintAdmin(admin.ModelAdmin):
    list_display = ['student', 'hostel', 'complaint_type', 'status', 'created_at']
    list_filter = ['status', 'complaint_type', 'created_at']
    search_fields = ['student__username', 'subject', 'hostel__name']
