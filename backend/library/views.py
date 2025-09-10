from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import Book, BookLoan, BookReservation, Fine
from .serializers import BookSerializer, BookLoanSerializer, BookReservationSerializer, FineSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def books(request):
    if request.method == 'GET':
        search = request.GET.get('search', '')
        category = request.GET.get('category', '')
        
        books = Book.objects.all()
        if search:
            books = books.filter(title__icontains=search)
        if category:
            books = books.filter(category__icontains=category)
            
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def borrow_book(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if book.available_copies <= 0:
        return Response({'detail': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if user already has this book
    existing_loan = BookLoan.objects.filter(
        book=book, 
        borrower=request.user, 
        status='active'
    ).exists()
    
    if existing_loan:
        return Response({'detail': 'You already have this book'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create loan
    due_date = timezone.now() + timedelta(days=14)  # 14 days loan period
    loan = BookLoan.objects.create(
        book=book,
        borrower=request.user,
        due_date=due_date
    )
    
    # Update available copies
    book.available_copies -= 1
    book.save()
    
    serializer = BookLoanSerializer(loan)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_book(request, loan_id):
    try:
        loan = BookLoan.objects.get(pk=loan_id, borrower=request.user)
    except BookLoan.DoesNotExist:
        return Response({'detail': 'Loan not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if loan.status != 'active':
        return Response({'detail': 'Book already returned'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Update loan
    loan.return_date = timezone.now()
    loan.status = 'returned'
    loan.save()
    
    # Update available copies
    loan.book.available_copies += 1
    loan.book.save()
    
    # Check for overdue and calculate fine
    if loan.return_date > loan.due_date:
        days_overdue = (loan.return_date - loan.due_date).days
        fine_amount = days_overdue * 5.00  # $5 per day
        Fine.objects.create(
            loan=loan,
            amount=fine_amount,
            reason=f'Overdue return ({days_overdue} days)'
        )
    
    serializer = BookLoanSerializer(loan)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_loans(request):
    loans = BookLoan.objects.filter(borrower=request.user).order_by('-loan_date')
    serializer = BookLoanSerializer(loans, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reserve_book(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if already reserved by this user
    existing_reservation = BookReservation.objects.filter(
        book=book,
        user=request.user,
        status='pending'
    ).exists()
    
    if existing_reservation:
        return Response({'detail': 'You already have a pending reservation'}, status=status.HTTP_400_BAD_REQUEST)
    
    reservation = BookReservation.objects.create(book=book, user=request.user)
    serializer = BookReservationSerializer(reservation)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_reservations(request):
    reservations = BookReservation.objects.filter(user=request.user).order_by('-reservation_date')
    serializer = BookReservationSerializer(reservations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_fines(request):
    fines = Fine.objects.filter(loan__borrower=request.user).order_by('-created_at')
    serializer = FineSerializer(fines, many=True)
    return Response(serializer.data)
