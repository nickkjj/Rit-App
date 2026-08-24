from django.db.models import ForeignKey
from django.db import models

from table_administration_service.models.employee_models import Employee

class QuestionVersion(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="versions")
    status = models.BooleanField(default=True)
    
    class Meta:
        db_table = "question_version"


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    questions_version = ForeignKey(QuestionVersion, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=500)
    weight = models.IntegerField()

    class Meta:
        db_table = "question"