from rest_framework import serializers
from .models import Book, BookLoan, BookReservation, Fine


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookLoanSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    borrower_name = serializers.CharField(source='borrower.get_full_name', read_only=True)
    
    class Meta:
        model = BookLoan
        fields = '__all__'


class BookReservationSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = BookReservation
        fields = '__all__'


class FineSerializer(serializers.ModelSerializer):
    loan_info = serializers.CharField(source='loan.book.title', read_only=True)
    borrower_name = serializers.CharField(source='loan.borrower.get_full_name', read_only=True)
    
    class Meta:
        model = Fine
        fields = '__all__'
