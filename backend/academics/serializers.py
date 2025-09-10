from rest_framework import serializers
from .models import Program, Course, CourseRegistration, Attendance


class ProgramSerializer(serializers.ModelSerializer):
	class Meta:
		model = Program
		fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
	program = ProgramSerializer(read_only=True)
	program_id = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all(), write_only=True, source="program")

	class Meta:
		model = Course
		fields = ["id", "code", "title", "credits", "program", "program_id"]


class AttendanceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Attendance
		fields = "__all__" 