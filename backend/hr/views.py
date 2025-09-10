from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, LeaveApplication
from .serializers import EmployeeSerializer, LeaveApplicationSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def employees(request):
    if request.method == 'GET':
        employees = Employee.objects.all().order_by('employee_code')
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def employee_detail(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({'detail': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def leaves(request):
    if request.method == 'GET':
        leaves = LeaveApplication.objects.all().order_by('-created_at')
        serializer = LeaveApplicationSerializer(leaves, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = LeaveApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def leave_detail(request, pk):
    try:
        leave = LeaveApplication.objects.get(pk=pk)
    except LeaveApplication.DoesNotExist:
        return Response({'detail': 'Leave application not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = LeaveApplicationSerializer(leave)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = LeaveApplicationSerializer(leave, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        leave.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
