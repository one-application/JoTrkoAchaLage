from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Q
from .models import (
    ResearchArea, ResearchProject, ResearchGrant, Publication,
    ResearchCollaboration, ResearchEquipment, ResearchStudent, ResearchMilestone
)
from .serializers import (
    ResearchAreaSerializer, ResearchProjectSerializer, ResearchGrantSerializer,
    PublicationSerializer, ResearchCollaborationSerializer, ResearchEquipmentSerializer,
    ResearchStudentSerializer, ResearchMilestoneSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def research_areas(request):
    areas = ResearchArea.objects.filter(is_active=True)
    serializer = ResearchAreaSerializer(areas, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def research_projects(request):
    if request.method == 'GET':
        search = request.GET.get('search', '')
        status_filter = request.GET.get('status', '')
        area_id = request.GET.get('area_id', '')
        
        projects = ResearchProject.objects.all()
        
        if search:
            projects = projects.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(principal_investigator__first_name__icontains=search) |
                Q(principal_investigator__last_name__icontains=search)
            )
        if status_filter:
            projects = projects.filter(status=status_filter)
        if area_id:
            projects = projects.filter(research_area_id=area_id)
        
        serializer = ResearchProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ResearchProjectSerializer(data=request.data)
        if serializer.is_valid():
            project = serializer.save(principal_investigator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def research_project_detail(request, project_id):
    try:
        project = ResearchProject.objects.get(pk=project_id)
    except ResearchProject.DoesNotExist:
        return Response({'detail': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ResearchProjectSerializer(project)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Only PI or co-investigators can update
        if request.user not in [project.principal_investigator] + list(project.co_investigators.all()):
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ResearchProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Only PI can delete
        if request.user != project.principal_investigator:
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_projects(request):
    # Projects where user is PI or co-investigator
    projects = ResearchProject.objects.filter(
        Q(principal_investigator=request.user) | 
        Q(co_investigators=request.user)
    ).distinct()
    
    serializer = ResearchProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def research_grants(request):
    if request.method == 'GET':
        project_id = request.GET.get('project_id', '')
        grants = ResearchGrant.objects.all()
        
        if project_id:
            grants = grants.filter(project_id=project_id)
        
        serializer = ResearchGrantSerializer(grants, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ResearchGrantSerializer(data=request.data)
        if serializer.is_valid():
            grant = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def publications(request):
    if request.method == 'GET':
        search = request.GET.get('search', '')
        pub_type = request.GET.get('type', '')
        project_id = request.GET.get('project_id', '')
        
        publications = Publication.objects.filter(is_verified=True)
        
        if search:
            publications = publications.filter(
                Q(title__icontains=search) | 
                Q(authors__icontains=search) |
                Q(journal_name__icontains=search)
            )
        if pub_type:
            publications = publications.filter(publication_type=pub_type)
        if project_id:
            publications = publications.filter(project_id=project_id)
        
        serializer = PublicationSerializer(publications, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PublicationSerializer(data=request.data)
        if serializer.is_valid():
            publication = serializer.save(uploaded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_publications(request):
    publications = Publication.objects.filter(uploaded_by=request.user)
    serializer = PublicationSerializer(publications, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def research_collaborations(request):
    if request.method == 'GET':
        project_id = request.GET.get('project_id', '')
        collaborations = ResearchCollaboration.objects.all()
        
        if project_id:
            collaborations = collaborations.filter(project_id=project_id)
        
        serializer = ResearchCollaborationSerializer(collaborations, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ResearchCollaborationSerializer(data=request.data)
        if serializer.is_valid():
            collaboration = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def research_equipment(request):
    if request.method == 'GET':
        status_filter = request.GET.get('status', '')
        equipment = ResearchEquipment.objects.all()
        
        if status_filter:
            equipment = equipment.filter(status=status_filter)
        
        serializer = ResearchEquipmentSerializer(equipment, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ResearchEquipmentSerializer(data=request.data)
        if serializer.is_valid():
            equipment = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def research_students(request):
    if request.method == 'GET':
        project_id = request.GET.get('project_id', '')
        student_type = request.GET.get('type', '')
        
        students = ResearchStudent.objects.all()
        
        if project_id:
            students = students.filter(project_id=project_id)
        if student_type:
            students = students.filter(student_type=student_type)
        
        serializer = ResearchStudentSerializer(students, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ResearchStudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_supervised_students(request):
    students = ResearchStudent.objects.filter(supervisor=request.user)
    serializer = ResearchStudentSerializer(students, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def research_milestones(request):
    if request.method == 'GET':
        project_id = request.GET.get('project_id', '')
        status_filter = request.GET.get('status', '')
        
        milestones = ResearchMilestone.objects.all()
        
        if project_id:
            milestones = milestones.filter(project_id=project_id)
        if status_filter:
            milestones = milestones.filter(status=status_filter)
        
        serializer = ResearchMilestoneSerializer(milestones, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ResearchMilestoneSerializer(data=request.data)
        if serializer.is_valid():
            milestone = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_milestone_status(request, milestone_id):
    try:
        milestone = ResearchMilestone.objects.get(pk=milestone_id)
    except ResearchMilestone.DoesNotExist:
        return Response({'detail': 'Milestone not found'}, status=status.HTTP_404_NOT_FOUND)
    
    status_value = request.data.get('status')
    completed_date = request.data.get('completed_date')
    
    if status_value:
        milestone.status = status_value
        if status_value == 'completed' and completed_date:
            milestone.completed_date = completed_date
        milestone.save()
    
    serializer = ResearchMilestoneSerializer(milestone)
    return Response(serializer.data)
