from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ResearchArea(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ResearchProject(models.Model):
    PROJECT_STATUS = [
        ('proposed', 'Proposed'),
        ('approved', 'Approved'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ]
    
    PROJECT_TYPES = [
        ('funded', 'Funded'),
        ('unfunded', 'Unfunded'),
        ('collaborative', 'Collaborative'),
        ('student', 'Student Project'),
    ]
    
    title = models.CharField(max_length=300)
    description = models.TextField()
    research_area = models.ForeignKey(ResearchArea, on_delete=models.CASCADE, related_name='projects')
    principal_investigator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_projects')
    co_investigators = models.ManyToManyField(User, related_name='co_investigated_projects', blank=True)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS, default='proposed')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    funding_agency = models.CharField(max_length=200, blank=True)
    grant_number = models.CharField(max_length=100, blank=True)
    objectives = models.TextField()
    methodology = models.TextField()
    expected_outcomes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class ResearchGrant(models.Model):
    GRANT_STATUS = [
        ('applied', 'Applied'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    ]
    
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='grants')
    grant_title = models.CharField(max_length=300)
    funding_agency = models.CharField(max_length=200)
    grant_number = models.CharField(max_length=100, unique=True)
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    application_date = models.DateField()
    approval_date = models.DateField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=GRANT_STATUS, default='applied')
    application_document = models.FileField(upload_to='grant_applications/', blank=True, null=True)
    approval_document = models.FileField(upload_to='grant_approvals/', blank=True, null=True)

    def __str__(self):
        return f"{self.grant_title} - {self.funding_agency}"

    class Meta:
        ordering = ['-application_date']


class Publication(models.Model):
    PUBLICATION_TYPES = [
        ('journal', 'Journal Article'),
        ('conference', 'Conference Paper'),
        ('book', 'Book'),
        ('book_chapter', 'Book Chapter'),
        ('patent', 'Patent'),
        ('report', 'Technical Report'),
    ]
    
    title = models.CharField(max_length=500)
    authors = models.TextField(help_text="Comma-separated list of authors")
    publication_type = models.CharField(max_length=20, choices=PUBLICATION_TYPES)
    journal_name = models.CharField(max_length=300, blank=True)
    conference_name = models.CharField(max_length=300, blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    publication_date = models.DateField()
    volume = models.CharField(max_length=20, blank=True)
    issue = models.CharField(max_length=20, blank=True)
    pages = models.CharField(max_length=50, blank=True)
    doi = models.CharField(max_length=200, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    issn = models.CharField(max_length=20, blank=True)
    abstract = models.TextField()
    keywords = models.TextField(help_text="Comma-separated keywords")
    project = models.ForeignKey(ResearchProject, on_delete=models.SET_NULL, null=True, blank=True, related_name='publications')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_publications')
    document = models.FileField(upload_to='publications/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_date']


class ResearchCollaboration(models.Model):
    COLLABORATION_TYPES = [
        ('academic', 'Academic'),
        ('industry', 'Industry'),
        ('government', 'Government'),
        ('international', 'International'),
    ]
    
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='collaborations')
    collaborator_name = models.CharField(max_length=200)
    collaborator_type = models.CharField(max_length=20, choices=COLLABORATION_TYPES)
    institution = models.CharField(max_length=300)
    country = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=200)
    contact_email = models.EmailField()
    collaboration_start_date = models.DateField()
    collaboration_end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    agreement_document = models.FileField(upload_to='collaboration_agreements/', blank=True, null=True)

    def __str__(self):
        return f"{self.project.title} - {self.collaborator_name}"

    class Meta:
        ordering = ['-collaboration_start_date']


class ResearchEquipment(models.Model):
    EQUIPMENT_STATUS = [
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Under Maintenance'),
        ('out_of_order', 'Out of Order'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    model_number = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=200)
    purchase_date = models.DateField()
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=EQUIPMENT_STATUS, default='available')
    responsible_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_equipment')
    maintenance_schedule = models.TextField(blank=True)
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.model_number}"

    class Meta:
        ordering = ['name']


class ResearchStudent(models.Model):
    STUDENT_TYPES = [
        ('phd', 'PhD'),
        ('mtech', 'M.Tech'),
        ('msc', 'M.Sc'),
        ('btech', 'B.Tech'),
        ('intern', 'Intern'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='research_students')
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='research_students')
    student_type = models.CharField(max_length=10, choices=STUDENT_TYPES)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supervised_students')
    enrollment_date = models.DateField()
    expected_completion_date = models.DateField()
    actual_completion_date = models.DateField(null=True, blank=True)
    thesis_title = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, default='active')

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.project.title}"

    class Meta:
        unique_together = ['student', 'project']
        ordering = ['-enrollment_date']


class ResearchMilestone(models.Model):
    MILESTONE_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed'),
    ]
    
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=MILESTONE_STATUS, default='pending')
    responsible_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='responsible_milestones')
    deliverables = models.TextField(blank=True)

    def __str__(self):
        return f"{self.project.title} - {self.title}"

    class Meta:
        ordering = ['due_date']
