from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True)
    publication_year = models.IntegerField()
    category = models.CharField(max_length=100)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        ordering = ['title']


class BookLoan(models.Model):
    LOAN_STATUS_CHOICES = [
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_loans')
    loan_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default='active')
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.borrower.username} - {self.book.title}"

    class Meta:
        ordering = ['-loan_date']


class BookReservation(models.Model):
    RESERVATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS_CHOICES, default='pending')
    notification_sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    class Meta:
        ordering = ['-reservation_date']


class Fine(models.Model):
    FINE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('waived', 'Waived'),
    ]
    
    loan = models.ForeignKey(BookLoan, on_delete=models.CASCADE, related_name='fines')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=FINE_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Fine for {self.loan.borrower.username} - {self.amount}"

    class Meta:
        ordering = ['-created_at']
