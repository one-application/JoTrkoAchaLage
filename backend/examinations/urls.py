from django.urls import path
from .views import (
    exam_types, exam_schedules, register_exam, user_exam_registrations,
    user_exam_results, request_revaluation, user_revaluation_requests,
    question_papers, submit_answer_sheet, user_answer_sheets,
    mark_exam_attendance, user_exam_attendance, create_exam_schedule,
    publish_results, all_revaluation_requests, update_revaluation_status
)

urlpatterns = [
    # Exam type endpoints
    path('types/', exam_types, name='exam-types'),
    
    # Exam schedule endpoints
    path('schedules/', exam_schedules, name='exam-schedules'),
    path('schedules/create/', create_exam_schedule, name='create-exam-schedule'),
    path('schedules/<int:schedule_id>/register/', register_exam, name='register-exam'),
    path('schedules/<int:schedule_id>/results/publish/', publish_results, name='publish-results'),
    
    # Registration endpoints
    path('registrations/', user_exam_registrations, name='user-exam-registrations'),
    
    # Results endpoints
    path('results/', user_exam_results, name='user-exam-results'),
    
    # Revaluation endpoints
    path('results/<int:result_id>/revaluation/', request_revaluation, name='request-revaluation'),
    path('revaluations/', user_revaluation_requests, name='user-revaluation-requests'),
    path('revaluations/all/', all_revaluation_requests, name='all-revaluation-requests'),
    path('revaluations/<int:request_id>/status/', update_revaluation_status, name='update-revaluation-status'),
    
    # Question paper endpoints
    path('question-papers/', question_papers, name='question-papers'),
    
    # Answer sheet endpoints
    path('schedules/<int:schedule_id>/submit/', submit_answer_sheet, name='submit-answer-sheet'),
    path('answer-sheets/', user_answer_sheets, name='user-answer-sheets'),
    
    # Attendance endpoints
    path('schedules/<int:schedule_id>/attendance/', mark_exam_attendance, name='mark-exam-attendance'),
    path('attendance/', user_exam_attendance, name='user-exam-attendance'),
]
