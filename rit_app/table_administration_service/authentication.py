from table_administration_service.models import employee_models
from rest_framework import authentication
from rest_framework import exceptions
from table_administration_service.models.employee_models import Employee

class EmailAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):

        email = request.META.get('HTTP_X_USER_EMAIL') #vou mandar o email pelo header

        if not email:
            return None
        
        try:
            employee = Employee.objects.get(email=email)
            token = None #autenticação apenas por email
        except Employee.DoesNotExist:
            raise exceptions.AuthenticationFailed('Email inválido')


        return (employee, token)

    def authenticate_header(self, request): #como criei uma autenticação sem token, preciso retornar um header caso a autenticação falhe, para que o django saiba que a autenticação falhou, e não retorne 403.
        return 'Custom-Email'