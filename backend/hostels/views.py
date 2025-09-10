from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import (
    Hostel, Room, HostelAllotment, Mess, MessSubscription, 
    MessMenu, HostelComplaint
)
from .serializers import (
    HostelSerializer, RoomSerializer, HostelAllotmentSerializer,
    MessSerializer, MessSubscriptionSerializer, MessMenuSerializer,
    HostelComplaintSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hostels(request):
    hostels = Hostel.objects.filter(is_active=True)
    serializer = HostelSerializer(hostels, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_rooms(request, hostel_id):
    rooms = Room.objects.filter(hostel_id=hostel_id, is_available=True)
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_hostel(request):
    serializer = HostelAllotmentSerializer(data=request.data)
    if serializer.is_valid():
        # Check if student already has an active allotment
        existing_allotment = HostelAllotment.objects.filter(
            student=request.user,
            status__in=['pending', 'approved', 'active']
        ).exists()
        
        if existing_allotment:
            return Response(
                {'detail': 'You already have an active hostel application or allotment'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        allotment = serializer.save(student=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_allotments(request):
    allotments = HostelAllotment.objects.filter(student=request.user)
    serializer = HostelAllotmentSerializer(allotments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def messes(request):
    messes = Mess.objects.filter(is_active=True)
    serializer = MessSerializer(messes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_mess(request):
    serializer = MessSubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        # Check if student already has an active mess subscription
        existing_subscription = MessSubscription.objects.filter(
            student=request.user,
            status='active'
        ).exists()
        
        if existing_subscription:
            return Response(
                {'detail': 'You already have an active mess subscription'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        subscription = serializer.save(student=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_mess_subscriptions(request):
    subscriptions = MessSubscription.objects.filter(student=request.user)
    serializer = MessSubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mess_menu(request, mess_id):
    date = request.GET.get('date', timezone.now().date())
    menus = MessMenu.objects.filter(mess_id=mess_id, date=date)
    serializer = MessMenuSerializer(menus, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_complaint(request):
    serializer = HostelComplaintSerializer(data=request.data)
    if serializer.is_valid():
        complaint = serializer.save(student=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_complaints(request):
    complaints = HostelComplaint.objects.filter(student=request.user)
    serializer = HostelComplaintSerializer(complaints, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_complaints(request):
    # Admin view - all complaints
    complaints = HostelComplaint.objects.all()
    serializer = HostelComplaintSerializer(complaints, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_complaint_status(request, complaint_id):
    try:
        complaint = HostelComplaint.objects.get(pk=complaint_id)
    except HostelComplaint.DoesNotExist:
        return Response({'detail': 'Complaint not found'}, status=status.HTTP_404_NOT_FOUND)
    
    status_value = request.data.get('status')
    resolution = request.data.get('resolution', '')
    
    if status_value:
        complaint.status = status_value
        if status_value == 'resolved':
            complaint.resolved_at = timezone.now()
            complaint.resolution = resolution
    
    complaint.save()
    serializer = HostelComplaintSerializer(complaint)
    return Response(serializer.data)
