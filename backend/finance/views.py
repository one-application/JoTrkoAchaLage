from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice, Payment
from .serializers import InvoiceSerializer, PaymentSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_fees(request, student_id):
    invoices = Invoice.objects.filter(student__id=student_id).order_by('-created_at')
    serializer = InvoiceSerializer(invoices, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        payment = serializer.save()
        # Update invoice status to paid
        invoice = payment.invoice
        invoice.status = 'paid'
        invoice.save(update_fields=['status'])
        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payments(request):
    payments = Payment.objects.all().order_by('-created_at')
    serializer = PaymentSerializer(payments, many=True)
    return Response(serializer.data)
