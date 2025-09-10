from rest_framework import serializers
from .models import (
    Company, JobOpening, StudentProfile, JobApplication,
    PlacementDrive, DriveRegistration, TrainingProgram, TrainingRegistration
)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class JobOpeningSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = JobOpening
        fields = '__all__'


class StudentProfileSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = '__all__'


class JobApplicationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.CharField(source='job.company.name', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = '__all__'


class PlacementDriveSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    
    class Meta:
        model = PlacementDrive
        fields = '__all__'


class DriveRegistrationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    drive_title = serializers.CharField(source='drive.title', read_only=True)
    
    class Meta:
        model = DriveRegistration
        fields = '__all__'


class TrainingProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = '__all__'


class TrainingRegistrationSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    program_title = serializers.CharField(source='program.title', read_only=True)
    
    class Meta:
        model = TrainingRegistration
        fields = '__all__'
