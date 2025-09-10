#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_erp.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import UserProfile
from academics.models import Program, Course
from hr.models import Department, Employee
from admissions.models import Applicant, Application

User = get_user_model()

def create_sample_data():
    # Create programs
    program1 = Program.objects.create(code='BTECH', name='Bachelor of Technology')
    program2 = Program.objects.create(code='MBA', name='Master of Business Administration')
    
    # Create courses
    course1 = Course.objects.create(code='CS101', title='Introduction to Computer Science', credits=3.0, program=program1)
    course2 = Course.objects.create(code='CS102', title='Data Structures', credits=4.0, program=program1)
    course3 = Course.objects.create(code='MBA101', title='Business Management', credits=3.0, program=program2)
    
    # Create departments
    dept1 = Department.objects.create(code='CS', name='Computer Science')
    dept2 = Department.objects.create(code='MBA', name='Business Administration')
    
    # Create users
    admin_user = User.objects.create_user(
        username='admin',
        email='admin@university.edu',
        password='admin123',
        first_name='Admin',
        last_name='User',
        role='Admin'
    )
    
    student_user = User.objects.create_user(
        username='student1',
        email='student1@university.edu',
        password='student123',
        first_name='John',
        last_name='Doe',
        role='Student'
    )
    
    faculty_user = User.objects.create_user(
        username='faculty1',
        email='faculty1@university.edu',
        password='faculty123',
        first_name='Jane',
        last_name='Smith',
        role='Faculty'
    )
    
    # Create user profiles
    UserProfile.objects.create(user=student_user, student_id='STU001')
    UserProfile.objects.create(user=faculty_user, employee_id='EMP001')
    
    # Create employee
    employee = Employee.objects.create(
        user=faculty_user,
        employee_code='EMP001',
        department=dept1,
        designation='Assistant Professor'
    )
    
    # Create applicant and application
    applicant = Applicant.objects.create(
        email='applicant1@email.com',
        phone='9876543210'
    )
    
    Application.objects.create(
        applicant=applicant,
        program=program1,
        stage='submitted',
        payment_status='paid'
    )
    
    print("Sample data created successfully!")
    print("Admin login: admin / admin123")
    print("Student login: student1 / student123")
    print("Faculty login: faculty1 / faculty123")

if __name__ == '__main__':
    create_sample_data()
