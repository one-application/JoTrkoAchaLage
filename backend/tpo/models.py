from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Company(models.Model):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    description = models.TextField()
    address = models.TextField()
    contact_person = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class JobOpening(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    ]
    
    EXPERIENCE_LEVELS = [
        ('fresher', 'Fresher'),
        ('0-1', '0-1 years'),
        ('1-3', '1-3 years'),
        ('3-5', '3-5 years'),
        ('5+', '5+ years'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_openings')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    experience_level = models.CharField(max_length=10, choices=EXPERIENCE_LEVELS)
    salary_range = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200)
    application_deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} - {self.title}"

    class Meta:
        ordering = ['-created_at']


class StudentProfile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, related_name='placement_profile')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    portfolio_website = models.URLField(blank=True)
    skills = models.TextField(help_text="Comma-separated list of skills")
    projects = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    expected_salary = models.CharField(max_length=100, blank=True)
    preferred_locations = models.TextField(blank=True)
    is_available_for_placement = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - Placement Profile"

    class Meta:
        ordering = ['-updated_at']


class JobApplication(models.Model):
    APPLICATION_STATUS = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('interviewed', 'Interviewed'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    job = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.job.title}"

    class Meta:
        unique_together = ['student', 'job']
        ordering = ['-applied_at']


class PlacementDrive(models.Model):
    DRIVE_STATUS = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='placement_drives')
    title = models.CharField(max_length=200)
    description = models.TextField()
    drive_date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    eligibility_criteria = models.TextField()
    selection_process = models.TextField()
    status = models.CharField(max_length=20, choices=DRIVE_STATUS, default='scheduled')
    total_positions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} - {self.title}"

    class Meta:
        ordering = ['-drive_date']


class DriveRegistration(models.Model):
    REGISTRATION_STATUS = [
        ('registered', 'Registered'),
        ('shortlisted', 'Shortlisted'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drive_registrations')
    drive = models.ForeignKey(PlacementDrive, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS, default='registered')
    registered_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.drive.title}"

    class Meta:
        unique_together = ['student', 'drive']
        ordering = ['-registered_at']


class TrainingProgram(models.Model):
    PROGRAM_TYPES = [
        ('technical', 'Technical'),
        ('soft_skills', 'Soft Skills'),
        ('aptitude', 'Aptitude'),
        ('interview_prep', 'Interview Preparation'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES)
    instructor = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    max_participants = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']


class TrainingRegistration(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_registrations')
    program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    completion_certificate = models.FileField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.program.title}"

    class Meta:
        unique_together = ['student', 'program']
        ordering = ['-registered_at']
