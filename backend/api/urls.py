from django.urls import path
from users.views import register, login, profile, change_password
from academics.views import courses, course_detail, student_attendance, faculty_attendance_post
from admissions.views import applications, application_detail
from hr.views import employees, employee_detail, leaves, leave_detail
from finance.views import student_fees, create_payment, payments
from django.urls import include

urlpatterns = [
    # Auth endpoints
    path('auth/register/', register, name='register'),
    path('auth/token/', login, name='login'),
    path('users/profile/', profile, name='profile'),
    path('users/change-password/', change_password, name='change-password'),
    
    # Academics endpoints
    path('academics/courses/', courses, name='courses'),
    path('academics/courses/<int:pk>/', course_detail, name='course-detail'),
    path('academics/students/<int:student_id>/attendance/', student_attendance, name='student-attendance'),
    path('academics/faculty/<int:faculty_id>/attendance/', faculty_attendance_post, name='faculty-attendance-post'),
    
    # Admissions endpoints
    path('admissions/applications/', applications, name='applications'),
    path('admissions/applications/<int:pk>/', application_detail, name='application-detail'),
    
    # HR endpoints
    path('hr/employees/', employees, name='employees'),
    path('hr/employees/<int:pk>/', employee_detail, name='employee-detail'),
    path('hr/leaves/', leaves, name='leaves'),
    path('hr/leaves/<int:pk>/', leave_detail, name='leave-detail'),
    
    # Finance endpoints
    path('finance/students/<int:student_id>/fees/', student_fees, name='student-fees'),
    path('finance/payments/', create_payment, name='create-payment'),
    path('finance/payments/list/', payments, name='payments-list'),
    
    # Library endpoints
    path('library/', include('library.urls')),
    path('hostels/', include('hostels.urls')),
    path('tpo/', include('tpo.urls')),
    path('examinations/', include('examinations.urls')),
    path('research/', include('research.urls')),
]
