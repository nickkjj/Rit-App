from django.db import models

from table_administration_service.models import Question, Employee

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="evaluations_given")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="evaluations_received")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rating"

from django.core.validators import MinValueValidator, MaxValueValidator

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name="answers")
    answer = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])

    class Meta:
        db_table = "answer"    