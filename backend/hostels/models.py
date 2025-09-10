from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Hostel(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    total_rooms = models.IntegerField()
    capacity_per_room = models.IntegerField()
    amenities = models.TextField(blank=True)
    warden_name = models.CharField(max_length=100)
    warden_contact = models.CharField(max_length=20)
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('quad', 'Quad'),
    ]
    
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    floor = models.IntegerField()
    is_available = models.BooleanField(default=True)
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

    class Meta:
        unique_together = ['hostel', 'room_number']
        ordering = ['hostel', 'room_number']


class HostelAllotment(models.Model):
    ALLOTMENT_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('terminated', 'Terminated'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hostel_allotments')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allotments')
    application_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ALLOTMENT_STATUS, default='pending')
    monthly_rent = models.DecimalField(max_digits=8, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.room}"

    class Meta:
        ordering = ['-application_date']


class Mess(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='messes')
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    manager_name = models.CharField(max_length=100)
    manager_contact = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.hostel.name} - {self.name}"

    class Meta:
        ordering = ['hostel', 'name']


class MessSubscription(models.Model):
    SUBSCRIPTION_STATUS = [
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mess_subscriptions')
    mess = models.ForeignKey(Mess, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=SUBSCRIPTION_STATUS, default='active')
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.student.username} - {self.mess}"

    class Meta:
        ordering = ['-start_date']


class MessMenu(models.Model):
    mess = models.ForeignKey(Mess, on_delete=models.CASCADE, related_name='menus')
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ])
    items = models.TextField()  # JSON string of menu items
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mess} - {self.date} - {self.meal_type}"

    class Meta:
        unique_together = ['mess', 'date', 'meal_type']
        ordering = ['-date', 'meal_type']


class HostelComplaint(models.Model):
    COMPLAINT_STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    COMPLAINT_TYPES = [
        ('maintenance', 'Maintenance'),
        ('cleaning', 'Cleaning'),
        ('security', 'Security'),
        ('mess', 'Mess'),
        ('other', 'Other'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hostel_complaints')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='complaints')
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=COMPLAINT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.username} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
