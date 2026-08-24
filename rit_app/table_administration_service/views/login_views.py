from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from table_administration_service.models.employee_models import Employee

@api_view(['POST'])
@permission_classes([AllowAny])
def session_login(request):
    
    email = request.data.get('email')
    
    try:
        employee = Employee.objects.get(email=email)
        
        return Response({
            "id": employee.id,
            "name": employee.name,
            "email": employee.email,
            "position_name": employee.position_name
        }, status=status.HTTP_200_OK)
        
    except Employee.DoesNotExist:
        return Response({"detail": "E-mail não encontrado."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def login_users(request):
    employees = Employee.objects.all().order_by('name')
    data = [
        {
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "position_name": emp.position_name
        } for emp in employees
    ]
    return Response(data, status=status.HTTP_200_OK)
