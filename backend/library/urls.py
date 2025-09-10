from django.urls import path
from .views import (
    books, book_detail, borrow_book, return_book, user_loans,
    reserve_book, user_reservations, user_fines
)

urlpatterns = [
    path('books/', books, name='books'),
    path('books/<int:pk>/', book_detail, name='book-detail'),
    path('books/<int:book_id>/borrow/', borrow_book, name='borrow-book'),
    path('loans/<int:loan_id>/return/', return_book, name='return-book'),
    path('loans/', user_loans, name='user-loans'),
    path('books/<int:book_id>/reserve/', reserve_book, name='reserve-book'),
    path('reservations/', user_reservations, name='user-reservations'),
    path('fines/', user_fines, name='user-fines'),
]
