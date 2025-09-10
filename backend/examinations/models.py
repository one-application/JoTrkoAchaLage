from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ExamType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    weightage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weightage in percentage")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ExamSchedule(models.Model):
    EXAM_STATUS = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE, related_name='exam_schedules')
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='schedules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    exam_date = models.DateTimeField()
    duration_minutes = models.IntegerField()
    venue = models.CharField(max_length=200)
    max_marks = models.DecimalField(max_digits=6, decimal_places=2)
    passing_marks = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, choices=EXAM_STATUS, default='scheduled')
    instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.code} - {self.title}"

    class Meta:
        ordering = ['-exam_date']


class ExamRegistration(models.Model):
    REGISTRATION_STATUS = [
        ('registered', 'Registered'),
        ('absent', 'Absent'),
        ('present', 'Present'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_registrations')
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REGISTRATION_STATUS, default='registered')
    seat_number = models.CharField(max_length=20, blank=True)
    hall_ticket_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.exam_schedule.title}"

    class Meta:
        unique_together = ['student', 'exam_schedule']
        ordering = ['-registration_date']


class ExamResult(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+'),
        ('A', 'A'),
        ('B+', 'B+'),
        ('B', 'B'),
        ('C+', 'C+'),
        ('C', 'C'),
        ('D', 'D'),
        ('F', 'F'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_results')
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.DecimalField(max_digits=6, decimal_places=2)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    is_pass = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    published_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='published_results')

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.exam_schedule.title} - {self.marks_obtained}"

    class Meta:
        unique_together = ['student', 'exam_schedule']
        ordering = ['-published_at']


class RevaluationRequest(models.Model):
    REQUEST_STATUS = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='revaluation_requests')
    exam_result = models.ForeignKey(ExamResult, on_delete=models.CASCADE, related_name='revaluation_requests')
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=REQUEST_STATUS, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviewed_revaluations')
    review_remarks = models.TextField(blank=True)
    fee_paid = models.BooleanField(default=False)
    fee_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.exam_result.exam_schedule.title}"

    class Meta:
        ordering = ['-requested_at']


class QuestionPaper(models.Model):
    exam_schedule = models.OneToOneField(ExamSchedule, on_delete=models.CASCADE, related_name='question_paper')
    file = models.FileField(upload_to='question_papers/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_question_papers')
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return f"Question Paper - {self.exam_schedule.title}"

    class Meta:
        ordering = ['-uploaded_at']


class AnswerSheet(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_sheets')
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name='answer_sheets')
    file = models.FileField(upload_to='answer_sheets/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_late_submission = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.exam_schedule.title}"

    class Meta:
        unique_together = ['student', 'exam_schedule']
        ordering = ['-submitted_at']


class ExamAttendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_attendance')
    exam_schedule = models.ForeignKey(ExamSchedule, on_delete=models.CASCADE, related_name='attendance')
    is_present = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.exam_schedule.title}"

    class Meta:
        unique_together = ['student', 'exam_schedule']
        ordering = ['-check_in_time']
