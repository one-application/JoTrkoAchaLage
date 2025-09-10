from rest_framework import serializers
from .models import (
    ResearchArea, ResearchProject, ResearchGrant, Publication,
    ResearchCollaboration, ResearchEquipment, ResearchStudent, ResearchMilestone
)


class ResearchAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchArea
        fields = '__all__'


class ResearchProjectSerializer(serializers.ModelSerializer):
    principal_investigator_name = serializers.CharField(source='principal_investigator.get_full_name', read_only=True)
    research_area_name = serializers.CharField(source='research_area.name', read_only=True)
    co_investigators_names = serializers.StringRelatedField(source='co_investigators', many=True, read_only=True)
    
    class Meta:
        model = ResearchProject
        fields = '__all__'


class ResearchGrantSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    
    class Meta:
        model = ResearchGrant
        fields = '__all__'


class PublicationSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = Publication
        fields = '__all__'


class ResearchCollaborationSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    
    class Meta:
        model = ResearchCollaboration
        fields = '__all__'


class ResearchEquipmentSerializer(serializers.ModelSerializer):
    responsible_person_name = serializers.CharField(source='responsible_person.get_full_name', read_only=True)
    
    class Meta:
        model = ResearchEquipment
        fields = '__all__'


class ResearchStudentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    project_title = serializers.CharField(source='project.title', read_only=True)
    supervisor_name = serializers.CharField(source='supervisor.get_full_name', read_only=True)
    
    class Meta:
        model = ResearchStudent
        fields = '__all__'


class ResearchMilestoneSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    responsible_person_name = serializers.CharField(source='responsible_person.get_full_name', read_only=True)
    
    class Meta:
        model = ResearchMilestone
        fields = '__all__'
