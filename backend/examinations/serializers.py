from rest_framework import serializers
from .models import (
    ExamType, ExamSchedule, ExamRegistration, ExamResult,
    RevaluationRequest, QuestionPaper, AnswerSheet, ExamAttendance
)


class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = '__all__'


class ExamScheduleSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(source='course.code', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    exam_type_name = serializers.CharField(source='exam_type.name', read_only=True)
    
    class Meta:
        model = ExamSchedule
        fields = '__all__'


class ExamRegistrationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    exam_title = serializers.CharField(source='exam_schedule.title', read_only=True)
    
    class Meta:
        model = ExamRegistration
        fields = '__all__'


class ExamResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    exam_title = serializers.CharField(source='exam_schedule.title', read_only=True)
    course_code = serializers.CharField(source='exam_schedule.course.code', read_only=True)
    
    class Meta:
        model = ExamResult
        fields = '__all__'


class RevaluationRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    exam_title = serializers.CharField(source='exam_result.exam_schedule.title', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.get_full_name', read_only=True)
    
    class Meta:
        model = RevaluationRequest
        fields = '__all__'


class QuestionPaperSerializer(serializers.ModelSerializer):
    exam_title = serializers.CharField(source='exam_schedule.title', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = QuestionPaper
        fields = '__all__'


class AnswerSheetSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    exam_title = serializers.CharField(source='exam_schedule.title', read_only=True)
    
    class Meta:
        model = AnswerSheet
        fields = '__all__'


class ExamAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    exam_title = serializers.CharField(source='exam_schedule.title', read_only=True)
    
    class Meta:
        model = ExamAttendance
        fields = '__all__'
