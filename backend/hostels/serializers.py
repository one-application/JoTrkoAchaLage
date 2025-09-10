from rest_framework import serializers
from .models import (
    Hostel, Room, HostelAllotment, Mess, MessSubscription, 
    MessMenu, HostelComplaint
)


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    
    class Meta:
        model = Room
        fields = '__all__'


class HostelAllotmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    room_info = serializers.CharField(source='room.__str__', read_only=True)
    
    class Meta:
        model = HostelAllotment
        fields = '__all__'


class MessSerializer(serializers.ModelSerializer):
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    
    class Meta:
        model = Mess
        fields = '__all__'


class MessSubscriptionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    mess_name = serializers.CharField(source='mess.name', read_only=True)
    
    class Meta:
        model = MessSubscription
        fields = '__all__'


class MessMenuSerializer(serializers.ModelSerializer):
    mess_name = serializers.CharField(source='mess.name', read_only=True)
    
    class Meta:
        model = MessMenu
        fields = '__all__'


class HostelComplaintSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    hostel_name = serializers.CharField(source='hostel.name', read_only=True)
    
    class Meta:
        model = HostelComplaint
        fields = '__all__'
