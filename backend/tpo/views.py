from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import (
    Company, JobOpening, StudentProfile, JobApplication,
    PlacementDrive, DriveRegistration, TrainingProgram, TrainingRegistration
)
from .serializers import (
    CompanySerializer, JobOpeningSerializer, StudentProfileSerializer,
    JobApplicationSerializer, PlacementDriveSerializer, DriveRegistrationSerializer,
    TrainingProgramSerializer, TrainingRegistrationSerializer
)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def companies(request):
    if request.method == 'GET':
        companies = Company.objects.filter(is_active=True, is_verified=True)
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_openings(request):
    search = request.GET.get('search', '')
    job_type = request.GET.get('job_type', '')
    experience = request.GET.get('experience', '')
    
    jobs = JobOpening.objects.filter(is_active=True, application_deadline__gte=timezone.now().date())
    
    if search:
        jobs = jobs.filter(title__icontains=search)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if experience:
        jobs = jobs.filter(experience_level=experience)
    
    serializer = JobOpeningSerializer(jobs, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def student_profile(request):
    if request.method == 'GET':
        try:
            profile = StudentProfile.objects.get(student=request.user)
            serializer = StudentProfileSerializer(profile)
            return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'POST':
        serializer = StudentProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save(student=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        try:
            profile = StudentProfile.objects.get(student=request.user)
            serializer = StudentProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except StudentProfile.DoesNotExist:
            return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_job(request, job_id):
    try:
        job = JobOpening.objects.get(pk=job_id, is_active=True)
    except JobOpening.DoesNotExist:
        return Response({'detail': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if already applied
    existing_application = JobApplication.objects.filter(
        student=request.user,
        job=job
    ).exists()
    
    if existing_application:
        return Response({'detail': 'You have already applied for this job'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if application deadline has passed
    if job.application_deadline < timezone.now().date():
        return Response({'detail': 'Application deadline has passed'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = JobApplicationSerializer(data=request.data)
    if serializer.is_valid():
        application = serializer.save(student=request.user, job=job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_applications(request):
    applications = JobApplication.objects.filter(student=request.user)
    serializer = JobApplicationSerializer(applications, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def placement_drives(request):
    drives = PlacementDrive.objects.filter(status__in=['scheduled', 'ongoing'])
    serializer = PlacementDriveSerializer(drives, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_drive(request, drive_id):
    try:
        drive = PlacementDrive.objects.get(pk=drive_id, status='scheduled')
    except PlacementDrive.DoesNotExist:
        return Response({'detail': 'Drive not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if already registered
    existing_registration = DriveRegistration.objects.filter(
        student=request.user,
        drive=drive
    ).exists()
    
    if existing_registration:
        return Response({'detail': 'You have already registered for this drive'}, status=status.HTTP_400_BAD_REQUEST)
    
    registration = DriveRegistration.objects.create(student=request.user, drive=drive)
    serializer = DriveRegistrationSerializer(registration)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_drive_registrations(request):
    registrations = DriveRegistration.objects.filter(student=request.user)
    serializer = DriveRegistrationSerializer(registrations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def training_programs(request):
    programs = TrainingProgram.objects.filter(is_active=True)
    serializer = TrainingProgramSerializer(programs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_training(request, program_id):
    try:
        program = TrainingProgram.objects.get(pk=program_id, is_active=True)
    except TrainingProgram.DoesNotExist:
        return Response({'detail': 'Training program not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if already registered
    existing_registration = TrainingRegistration.objects.filter(
        student=request.user,
        program=program
    ).exists()
    
    if existing_registration:
        return Response({'detail': 'You have already registered for this program'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if program has started
    if program.start_date < timezone.now():
        return Response({'detail': 'Registration deadline has passed'}, status=status.HTTP_400_BAD_REQUEST)
    
    registration = TrainingRegistration.objects.create(student=request.user, program=program)
    serializer = TrainingRegistrationSerializer(registration)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_training_registrations(request):
    registrations = TrainingRegistration.objects.filter(student=request.user)
    serializer = TrainingRegistrationSerializer(registrations, many=True)
    return Response(serializer.data)
