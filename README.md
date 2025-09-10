# University Enterprise Management System

A comprehensive ERP system for universities built with Django REST Framework backend and React frontend.

## 🏗️ Architecture

- **Backend**: Django + Django REST Framework with functional-based views
- **Frontend**: React + TypeScript + Bootstrap (plain HTML with Bootstrap classes)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT tokens with role-based access control

## 🎯 Features Implemented

### ✅ Core Modules Completed (10/15)

#### 1. **Authentication & User Management** ✅
- JWT-based authentication with token refresh
- Role-based access control (Student, Faculty, Admin, etc.)
- User registration and profile management
- Password reset functionality

#### 2. **Academics Management** ✅
- Program and course management
- Course registration system
- Student attendance tracking
- Faculty attendance logging

#### 3. **Admissions Management** ✅
- Applicant registration and management
- Multi-stage application process
- Application status tracking
- Document upload system

#### 4. **HR Management** ✅
- Employee directory and management
- Leave application system
- Department and designation management
- Employee profile management

#### 5. **Finance & Accounts** ✅
- Student fee management
- Payment processing
- Invoice generation
- Financial reporting

#### 6. **Library Management** 📚
- Book catalog and inventory
- Book borrowing and return system
- Reservation system
- Fine management for overdue books
- Search and filtering capabilities

#### 7. **Hostels & Mess Management** 🏠
- Hostel and room management
- Student allotment system
- Mess subscription management
- Menu planning and management
- Complaint system for hostel issues

#### 8. **Training & Placement Office (TPO)** 💼
- Company registration and management
- Job opening posting and management
- Student placement profiles
- Job application tracking
- Placement drive management
- Training program registration
- Drive registration system

#### 9. **Examinations Management** 📝
- Exam type and schedule management
- Student exam registration
- Result publishing and grade calculation
- Revaluation request system
- Question paper and answer sheet management
- Exam attendance tracking
- Hall ticket generation

#### 10. **Research & Development** 🔬
- Research project management
- Grant application and tracking
- Publication management
- Research collaboration tracking
- Equipment management
- Research student supervision
- Milestone tracking

### 🔄 Remaining Modules (5/15)

#### 11. **Learning Management System (LMS)**
- Course content management
- Assignment submission
- Online assessments
- Discussion forums

#### 12. **Stores & Procurement**
- Inventory management
- Purchase order system
- Vendor management
- Asset tracking

#### 13. **Estate Office**
- Infrastructure management
- Maintenance requests
- Asset management
- Space allocation

#### 14. **Laboratory Management**
- Lab equipment tracking
- Lab booking system
- Safety compliance
- Equipment maintenance

#### 15. **Co-curricular Activities**
- Event management
- Club and society management
- Activity registration
- Achievement tracking

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python create_sample_data.py
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🔐 Sample Login Credentials

- **Admin**: admin / admin123
- **Student**: student1 / student123
- **Faculty**: faculty1 / faculty123

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/token/` - Login (get JWT tokens)
- `POST /api/v1/auth/refresh/` - Refresh JWT token
- `GET /api/v1/users/profile/` - Get user profile

### Academics
- `GET /api/v1/academics/courses/` - List courses
- `GET /api/v1/academics/students/{id}/attendance/` - Student attendance
- `POST /api/v1/academics/faculty/{id}/attendance/` - Mark attendance

### Admissions
- `GET /api/v1/admissions/applications/` - List applications
- `POST /api/v1/admissions/applications/` - Create application

### HR
- `GET /api/v1/hr/employees/` - List employees
- `GET /api/v1/hr/leaves/` - List leave applications
- `POST /api/v1/hr/leaves/` - Apply for leave

### Finance
- `GET /api/v1/finance/students/{id}/fees/` - Student fees
- `POST /api/v1/finance/payments/` - Create payment

### Library
- `GET /api/v1/library/books/` - List books
- `POST /api/v1/library/books/{id}/borrow/` - Borrow book
- `POST /api/v1/library/loans/{id}/return/` - Return book
- `GET /api/v1/library/loans/` - User's loans
- `POST /api/v1/library/books/{id}/reserve/` - Reserve book
- `GET /api/v1/library/fines/` - User's fines

### Hostels
- `GET /api/v1/hostels/hostels/` - List hostels
- `GET /api/v1/hostels/hostels/{id}/rooms/` - Available rooms
- `POST /api/v1/hostels/allotments/apply/` - Apply for hostel
- `GET /api/v1/hostels/messes/` - List messes
- `POST /api/v1/hostels/mess/subscribe/` - Subscribe to mess
- `GET /api/v1/hostels/mess/{id}/menu/` - Mess menu
- `POST /api/v1/hostels/complaints/` - Create complaint

### TPO (Training & Placement)
- `GET /api/v1/tpo/companies/` - List companies
- `GET /api/v1/tpo/jobs/` - List job openings
- `POST /api/v1/tpo/jobs/{id}/apply/` - Apply for job
- `GET /api/v1/tpo/profile/` - Student placement profile
- `GET /api/v1/tpo/drives/` - List placement drives
- `POST /api/v1/tpo/drives/{id}/register/` - Register for drive
- `GET /api/v1/tpo/training/` - List training programs
- `POST /api/v1/tpo/training/{id}/register/` - Register for training

### Examinations
- `GET /api/v1/examinations/types/` - List exam types
- `GET /api/v1/examinations/schedules/` - List exam schedules
- `POST /api/v1/examinations/schedules/{id}/register/` - Register for exam
- `GET /api/v1/examinations/results/` - User's exam results
- `POST /api/v1/examinations/results/{id}/revaluation/` - Request revaluation
- `GET /api/v1/examinations/question-papers/` - List question papers
- `POST /api/v1/examinations/schedules/{id}/submit/` - Submit answer sheet
- `POST /api/v1/examinations/schedules/{id}/attendance/` - Mark exam attendance

### Research & Development
- `GET /api/v1/research/areas/` - List research areas
- `GET /api/v1/research/projects/` - List research projects
- `POST /api/v1/research/projects/` - Create research project
- `GET /api/v1/research/projects/my/` - User's projects
- `GET /api/v1/research/grants/` - List research grants
- `GET /api/v1/research/publications/` - List publications
- `POST /api/v1/research/publications/` - Add publication
- `GET /api/v1/research/equipment/` - List research equipment
- `GET /api/v1/research/students/` - List research students
- `GET /api/v1/research/milestones/` - List research milestones

## �� Frontend Features

- **Role-based Dashboards**: Different interfaces for Students, Faculty, and Admin
- **Responsive Design**: Bootstrap-based responsive UI
- **Authentication Flow**: Login/logout with JWT tokens
- **Protected Routes**: Role-based access control
- **Modern UI**: Clean, intuitive interface using Bootstrap components

## 🛠️ Technology Stack

- **Backend**: Django 5.0.6, Django REST Framework 3.15.1
- **Frontend**: React 18, TypeScript, Bootstrap 5
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Authentication**: JWT with SimpleJWT
- **API**: RESTful APIs with functional-based views

## 📊 Database Schema

The system uses a modular database design with separate models for each major functionality:

- **Users**: Custom user model with roles
- **Academics**: Programs, courses, registrations, attendance
- **Admissions**: Applicants, applications
- **HR**: Employees, departments, leaves
- **Finance**: Fee plans, invoices, payments
- **Library**: Books, loans, reservations, fines
- **Hostels**: Hostels, rooms, allotments, mess, complaints
- **TPO**: Companies, jobs, profiles, applications, drives, training
- **Examinations**: Exam types, schedules, results, revaluation, attendance
- **Research**: Projects, grants, publications, collaborations, equipment, students

## 🔄 Development Status

### ✅ Completed (10/15 modules - 67% Complete)
1. Authentication & User Management
2. Academics Management
3. Admissions Management
4. HR Management
5. Finance & Accounts
6. Library Management
7. Hostels & Mess Management
8. Training & Placement Office
9. Examinations Management
10. Research & Development

### 🚧 In Progress
- Continuing with remaining 5 modules

### 📋 Next Steps
1. Learning Management System (LMS)
2. Stores & Procurement
3. Estate Office
4. Laboratory Management
5. Co-curricular Activities

## 🎯 Key Achievements

- **67% Complete**: 10 out of 15 major modules fully functional
- **Functional-based Views**: All modules use Django functional views as requested
- **Plain HTML + Bootstrap**: Frontend uses standard HTML with Bootstrap classes
- **RESTful APIs**: Complete API endpoints for all modules
- **Role-based Access**: Different dashboards and permissions for each user type
- **Database Integration**: All modules properly integrated with migrations
- **Sample Data**: Test data created for all modules

## 🤝 Contributing

This is a comprehensive university ERP system designed to handle all major university operations. Each module is built with functional-based Django views and follows RESTful API principles.

## 📝 License

This project is developed for educational and demonstration purposes.
