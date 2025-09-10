from django.contrib import admin
from .models import (
    ResearchArea, ResearchProject, ResearchGrant, Publication,
    ResearchCollaboration, ResearchEquipment, ResearchStudent, ResearchMilestone
)


@admin.register(ResearchArea)
class ResearchAreaAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'principal_investigator', 'research_area', 'status', 'start_date', 'budget']
    list_filter = ['status', 'project_type', 'start_date', 'research_area']
    search_fields = ['title', 'principal_investigator__username']
    filter_horizontal = ['co_investigators']


@admin.register(ResearchGrant)
class ResearchGrantAdmin(admin.ModelAdmin):
    list_display = ['grant_title', 'project', 'funding_agency', 'amount_approved', 'status']
    list_filter = ['status', 'application_date', 'funding_agency']
    search_fields = ['grant_title', 'grant_number', 'funding_agency']


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_type', 'journal_name', 'publication_date', 'is_verified']
    list_filter = ['publication_type', 'is_verified', 'publication_date']
    search_fields = ['title', 'authors', 'journal_name']


@admin.register(ResearchCollaboration)
class ResearchCollaborationAdmin(admin.ModelAdmin):
    list_display = ['collaborator_name', 'project', 'collaborator_type', 'institution', 'country']
    list_filter = ['collaborator_type', 'country']
    search_fields = ['collaborator_name', 'institution', 'project__title']


@admin.register(ResearchEquipment)
class ResearchEquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_number', 'manufacturer', 'status', 'location', 'responsible_person']
    list_filter = ['status', 'manufacturer', 'purchase_date']
    search_fields = ['name', 'model_number', 'manufacturer']


@admin.register(ResearchStudent)
class ResearchStudentAdmin(admin.ModelAdmin):
    list_display = ['student', 'project', 'student_type', 'supervisor', 'enrollment_date', 'status']
    list_filter = ['student_type', 'status', 'enrollment_date']
    search_fields = ['student__username', 'project__title', 'supervisor__username']


@admin.register(ResearchMilestone)
class ResearchMilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'due_date', 'status', 'responsible_person']
    list_filter = ['status', 'due_date']
    search_fields = ['title', 'project__title']
