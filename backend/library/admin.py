from django.contrib import admin
from .models import Book, BookLoan, BookReservation, Fine


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'available_copies', 'total_copies', 'category']
    list_filter = ['category', 'publication_year']
    search_fields = ['title', 'author', 'isbn']


@admin.register(BookLoan)
class BookLoanAdmin(admin.ModelAdmin):
    list_display = ['book', 'borrower', 'loan_date', 'due_date', 'status']
    list_filter = ['status', 'loan_date']
    search_fields = ['book__title', 'borrower__username']


@admin.register(BookReservation)
class BookReservationAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'reservation_date', 'status']
    list_filter = ['status', 'reservation_date']
    search_fields = ['book__title', 'user__username']


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ['loan', 'amount', 'reason', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['loan__book__title', 'loan__borrower__username']
