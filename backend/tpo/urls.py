from django.urls import path
from .views import (
    companies, job_openings, student_profile, apply_job, user_applications,
    placement_drives, register_drive, user_drive_registrations,
    training_programs, register_training, user_training_registrations
)

urlpatterns = [
    # Company endpoints
    path('companies/', companies, name='companies'),
    
    # Job endpoints
    path('jobs/', job_openings, name='job-openings'),
    path('jobs/<int:job_id>/apply/', apply_job, name='apply-job'),
    path('applications/', user_applications, name='user-applications'),
    
    # Student profile endpoints
    path('profile/', student_profile, name='student-profile'),
    
    # Placement drive endpoints
    path('drives/', placement_drives, name='placement-drives'),
    path('drives/<int:drive_id>/register/', register_drive, name='register-drive'),
    path('drive-registrations/', user_drive_registrations, name='user-drive-registrations'),
    
    # Training program endpoints
    path('training/', training_programs, name='training-programs'),
    path('training/<int:program_id>/register/', register_training, name='register-training'),
    path('training-registrations/', user_training_registrations, name='user-training-registrations'),
]
