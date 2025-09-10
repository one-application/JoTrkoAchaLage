from django.contrib import admin
from .models import (
    ExamType, ExamSchedule, ExamRegistration, ExamResult,
    RevaluationRequest, QuestionPaper, AnswerSheet, ExamAttendance
)


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'weightage', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(ExamSchedule)
class ExamScheduleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'exam_type', 'exam_date', 'status', 'max_marks']
    list_filter = ['status', 'exam_date', 'exam_type']
    search_fields = ['title', 'course__code']


@admin.register(ExamRegistration)
class ExamRegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam_schedule', 'status', 'registration_date']
    list_filter = ['status', 'registration_date']
    search_fields = ['student__username', 'exam_schedule__title']


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam_schedule', 'marks_obtained', 'grade', 'is_pass', 'published_at']
    list_filter = ['is_pass', 'grade', 'published_at']
    search_fields = ['student__username', 'exam_schedule__title']


@admin.register(RevaluationRequest)
class RevaluationRequestAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam_result', 'status', 'requested_at', 'fee_paid']
    list_filter = ['status', 'fee_paid', 'requested_at']
    search_fields = ['student__username', 'exam_result__exam_schedule__title']


@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ['exam_schedule', 'uploaded_at', 'uploaded_by', 'is_available']
    list_filter = ['is_available', 'uploaded_at']
    search_fields = ['exam_schedule__title']


@admin.register(AnswerSheet)
class AnswerSheetAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam_schedule', 'submitted_at', 'is_late_submission']
    list_filter = ['is_late_submission', 'submitted_at']
    search_fields = ['student__username', 'exam_schedule__title']


@admin.register(ExamAttendance)
class ExamAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam_schedule', 'is_present', 'check_in_time']
    list_filter = ['is_present', 'check_in_time']
    search_fields = ['student__username', 'exam_schedule__title']
