from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Q
from .models import (
    ExamType, ExamSchedule, ExamRegistration, ExamResult,
    RevaluationRequest, QuestionPaper, AnswerSheet, ExamAttendance
)
from .serializers import (
    ExamTypeSerializer, ExamScheduleSerializer, ExamRegistrationSerializer,
    ExamResultSerializer, RevaluationRequestSerializer, QuestionPaperSerializer,
    AnswerSheetSerializer, ExamAttendanceSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exam_types(request):
    exam_types = ExamType.objects.filter(is_active=True)
    serializer = ExamTypeSerializer(exam_types, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exam_schedules(request):
    course_id = request.GET.get('course_id')
    exam_type_id = request.GET.get('exam_type_id')
    
    schedules = ExamSchedule.objects.all()
    
    if course_id:
        schedules = schedules.filter(course_id=course_id)
    if exam_type_id:
        schedules = schedules.filter(exam_type_id=exam_type_id)
    
    serializer = ExamScheduleSerializer(schedules, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_exam(request, schedule_id):
    try:
        schedule = ExamSchedule.objects.get(pk=schedule_id, status='scheduled')
    except ExamSchedule.DoesNotExist:
        return Response({'detail': 'Exam schedule not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if already registered
    existing_registration = ExamRegistration.objects.filter(
        student=request.user,
        exam_schedule=schedule
    ).exists()
    
    if existing_registration:
        return Response({'detail': 'You have already registered for this exam'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if registration deadline has passed (assuming 1 day before exam)
    registration_deadline = schedule.exam_date - timezone.timedelta(days=1)
    if timezone.now() > registration_deadline:
        return Response({'detail': 'Registration deadline has passed'}, status=status.HTTP_400_BAD_REQUEST)
    
    registration = ExamRegistration.objects.create(student=request.user, exam_schedule=schedule)
    serializer = ExamRegistrationSerializer(registration)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_exam_registrations(request):
    registrations = ExamRegistration.objects.filter(student=request.user)
    serializer = ExamRegistrationSerializer(registrations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_exam_results(request):
    results = ExamResult.objects.filter(student=request.user)
    serializer = ExamResultSerializer(results, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_revaluation(request, result_id):
    try:
        result = ExamResult.objects.get(pk=result_id, student=request.user)
    except ExamResult.DoesNotExist:
        return Response({'detail': 'Exam result not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if already requested revaluation
    existing_request = RevaluationRequest.objects.filter(
        student=request.user,
        exam_result=result
    ).exists()
    
    if existing_request:
        return Response({'detail': 'You have already requested revaluation for this exam'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = RevaluationRequestSerializer(data=request.data)
    if serializer.is_valid():
        revaluation = serializer.save(student=request.user, exam_result=result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_revaluation_requests(request):
    requests = RevaluationRequest.objects.filter(student=request.user)
    serializer = RevaluationRequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def question_papers(request):
    schedule_id = request.GET.get('schedule_id')
    
    papers = QuestionPaper.objects.filter(is_available=True)
    if schedule_id:
        papers = papers.filter(exam_schedule_id=schedule_id)
    
    serializer = QuestionPaperSerializer(papers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer_sheet(request, schedule_id):
    try:
        schedule = ExamSchedule.objects.get(pk=schedule_id)
    except ExamSchedule.DoesNotExist:
        return Response({'detail': 'Exam schedule not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if student is registered for this exam
    registration = ExamRegistration.objects.filter(
        student=request.user,
        exam_schedule=schedule
    ).first()
    
    if not registration:
        return Response({'detail': 'You are not registered for this exam'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if already submitted
    existing_submission = AnswerSheet.objects.filter(
        student=request.user,
        exam_schedule=schedule
    ).exists()
    
    if existing_submission:
        return Response({'detail': 'You have already submitted the answer sheet'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if exam is ongoing or completed
    if schedule.status not in ['ongoing', 'completed']:
        return Response({'detail': 'Exam is not currently active'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = AnswerSheetSerializer(data=request.data)
    if serializer.is_valid():
        # Check for late submission
        is_late = timezone.now() > schedule.exam_date + timezone.timedelta(minutes=schedule.duration_minutes)
        answer_sheet = serializer.save(student=request.user, exam_schedule=schedule, is_late_submission=is_late)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_answer_sheets(request):
    answer_sheets = AnswerSheet.objects.filter(student=request.user)
    serializer = AnswerSheetSerializer(answer_sheets, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_exam_attendance(request, schedule_id):
    try:
        schedule = ExamSchedule.objects.get(pk=schedule_id)
    except ExamSchedule.DoesNotExist:
        return Response({'detail': 'Exam schedule not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if student is registered for this exam
    registration = ExamRegistration.objects.filter(
        student=request.user,
        exam_schedule=schedule
    ).first()
    
    if not registration:
        return Response({'detail': 'You are not registered for this exam'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if attendance already marked
    existing_attendance = ExamAttendance.objects.filter(
        student=request.user,
        exam_schedule=schedule
    ).first()
    
    if existing_attendance:
        return Response({'detail': 'Attendance already marked'}, status=status.HTTP_400_BAD_REQUEST)
    
    attendance = ExamAttendance.objects.create(
        student=request.user,
        exam_schedule=schedule,
        is_present=True,
        check_in_time=timezone.now()
    )
    serializer = ExamAttendanceSerializer(attendance)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_exam_attendance(request):
    attendance = ExamAttendance.objects.filter(student=request.user)
    serializer = ExamAttendanceSerializer(attendance, many=True)
    return Response(serializer.data)


# Admin functions
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_exam_schedule(request):
    serializer = ExamScheduleSerializer(data=request.data)
    if serializer.is_valid():
        schedule = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def publish_results(request, schedule_id):
    try:
        schedule = ExamSchedule.objects.get(pk=schedule_id)
    except ExamSchedule.DoesNotExist:
        return Response({'detail': 'Exam schedule not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # This would typically involve processing answer sheets and calculating results
    # For now, we'll just return a success message
    return Response({'detail': 'Results published successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_revaluation_requests(request):
    # Admin view - all revaluation requests
    requests = RevaluationRequest.objects.all()
    serializer = RevaluationRequestSerializer(requests, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_revaluation_status(request, request_id):
    try:
        revaluation_request = RevaluationRequest.objects.get(pk=request_id)
    except RevaluationRequest.DoesNotExist:
        return Response({'detail': 'Revaluation request not found'}, status=status.HTTP_404_NOT_FOUND)
    
    status_value = request.data.get('status')
    review_remarks = request.data.get('review_remarks', '')
    
    if status_value:
        revaluation_request.status = status_value
        revaluation_request.reviewed_at = timezone.now()
        revaluation_request.reviewed_by = request.user
        revaluation_request.review_remarks = review_remarks
        revaluation_request.save()
    
    serializer = RevaluationRequestSerializer(revaluation_request)
    return Response(serializer.data)
