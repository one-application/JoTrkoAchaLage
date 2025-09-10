#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_erp.settings')
django.setup()

from library.models import Book, BookLoan, BookReservation, Fine
from django.contrib.auth import get_user_model

User = get_user_model()

def add_library_data():
    # Create sample books
    books_data = [
        {
            'isbn': '9780134685991',
            'title': 'Effective Java',
            'author': 'Joshua Bloch',
            'publisher': 'Addison-Wesley',
            'publication_year': 2017,
            'category': 'Programming',
            'total_copies': 3,
            'available_copies': 3,
            'location': 'CS-001'
        },
        {
            'isbn': '9780132350884',
            'title': 'Clean Code',
            'author': 'Robert C. Martin',
            'publisher': 'Prentice Hall',
            'publication_year': 2008,
            'category': 'Programming',
            'total_copies': 2,
            'available_copies': 2,
            'location': 'CS-002'
        },
        {
            'isbn': '9780134685992',
            'title': 'Design Patterns',
            'author': 'Gang of Four',
            'publisher': 'Addison-Wesley',
            'publication_year': 1994,
            'category': 'Programming',
            'total_copies': 2,
            'available_copies': 1,
            'location': 'CS-003'
        },
        {
            'isbn': '9780132350885',
            'title': 'Introduction to Algorithms',
            'author': 'Thomas H. Cormen',
            'publisher': 'MIT Press',
            'publication_year': 2009,
            'category': 'Computer Science',
            'total_copies': 4,
            'available_copies': 4,
            'location': 'CS-004'
        },
        {
            'isbn': '9780134685993',
            'title': 'Database System Concepts',
            'author': 'Abraham Silberschatz',
            'publisher': 'McGraw-Hill',
            'publication_year': 2019,
            'category': 'Database',
            'total_copies': 3,
            'available_copies': 3,
            'location': 'CS-005'
        }
    ]
    
    for book_data in books_data:
        book, created = Book.objects.get_or_create(
            isbn=book_data['isbn'],
            defaults=book_data
        )
        if created:
            print(f"Created book: {book.title}")
    
    # Create a sample loan for student1
    try:
        student = User.objects.get(username='student1')
        book = Book.objects.get(title='Design Patterns')
        
        # Create a loan
        loan = BookLoan.objects.create(
            book=book,
            borrower=student,
            due_date=datetime.now() + timedelta(days=14)
        )
        
        # Update available copies
        book.available_copies -= 1
        book.save()
        
        print(f"Created loan: {student.username} borrowed {book.title}")
        
    except User.DoesNotExist:
        print("Student user not found")
    except Book.DoesNotExist:
        print("Book not found")
    
    print("Library sample data created successfully!")

if __name__ == '__main__':
    add_library_data()
