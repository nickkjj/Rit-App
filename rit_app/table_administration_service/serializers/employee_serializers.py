from django.db.models import fields_all
from rest_framework import serializers

from table_administration_service.models.employee_models import Employee

#Iremos apenas consumir o banco cadastrado, mas em caso contrario, os usuarios deveriam possuir serializers para post, put e delete.
class EmployeeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
