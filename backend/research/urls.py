from django.urls import path
from .views import (
    research_areas, research_projects, research_project_detail, user_projects,
    research_grants, publications, user_publications, research_collaborations,
    research_equipment, research_students, user_supervised_students,
    research_milestones, update_milestone_status
)

urlpatterns = [
    # Research area endpoints
    path('areas/', research_areas, name='research-areas'),
    
    # Research project endpoints
    path('projects/', research_projects, name='research-projects'),
    path('projects/<int:project_id>/', research_project_detail, name='research-project-detail'),
    path('projects/my/', user_projects, name='user-projects'),
    
    # Research grant endpoints
    path('grants/', research_grants, name='research-grants'),
    
    # Publication endpoints
    path('publications/', publications, name='publications'),
    path('publications/my/', user_publications, name='user-publications'),
    
    # Collaboration endpoints
    path('collaborations/', research_collaborations, name='research-collaborations'),
    
    # Equipment endpoints
    path('equipment/', research_equipment, name='research-equipment'),
    
    # Research student endpoints
    path('students/', research_students, name='research-students'),
    path('students/supervised/', user_supervised_students, name='user-supervised-students'),
    
    # Milestone endpoints
    path('milestones/', research_milestones, name='research-milestones'),
    path('milestones/<int:milestone_id>/status/', update_milestone_status, name='update-milestone-status'),
]
