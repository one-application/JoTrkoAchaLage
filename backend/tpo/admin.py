from django.contrib import admin
from .models import (
    Company, JobOpening, StudentProfile, JobApplication,
    PlacementDrive, DriveRegistration, TrainingProgram, TrainingRegistration
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'contact_person', 'is_verified', 'is_active']
    list_filter = ['is_verified', 'is_active', 'industry']
    search_fields = ['name', 'contact_person', 'contact_email']


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'job_type', 'experience_level', 'application_deadline', 'is_active']
    list_filter = ['job_type', 'experience_level', 'is_active', 'application_deadline']
    search_fields = ['title', 'company__name']


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['student', 'is_available_for_placement', 'updated_at']
    list_filter = ['is_available_for_placement', 'updated_at']
    search_fields = ['student__username', 'student__first_name', 'student__last_name']


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['student__username', 'job__title']


@admin.register(PlacementDrive)
class PlacementDriveAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'drive_date', 'status', 'total_positions']
    list_filter = ['status', 'drive_date']
    search_fields = ['title', 'company__name']


@admin.register(DriveRegistration)
class DriveRegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'drive', 'status', 'registered_at']
    list_filter = ['status', 'registered_at']
    search_fields = ['student__username', 'drive__title']


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ['title', 'program_type', 'instructor', 'start_date', 'is_active']
    list_filter = ['program_type', 'is_active', 'start_date']
    search_fields = ['title', 'instructor']


@admin.register(TrainingRegistration)
class TrainingRegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'program', 'registered_at', 'attendance_percentage']
    list_filter = ['registered_at', 'attendance_percentage']
    search_fields = ['student__username', 'program__title']
