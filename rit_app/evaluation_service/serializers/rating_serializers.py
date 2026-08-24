from rest_framework import serializers
from django.db import transaction

from evaluation_service.models import Rating, Answer
from table_administration_service.models.employee_models import Employee
from table_administration_service.models.question_models import Question

from django.utils import timezone
from datetime import timedelta

class AnswerCreateSerializer(serializers.ModelSerializer):
    question_id = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(), source='question'
    )
    answer = serializers.IntegerField(min_value=1, max_value=4)

    class Meta:
        model = Answer
        fields = ['question_id', 'answer']

class RatingCreateSerializer(serializers.ModelSerializer):
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source='employee'
    )
    answers = AnswerCreateSerializer(many=True)
    class Meta:
        model = Rating
        fields = ['employee_id', 'answers']
        
    def validate(self, data):
        leader = self.context['request'].user
        employee = data.get('employee')
        
        one_week_ago = timezone.now() - timedelta(days=7)
        
        recent_evaluation_exists = Rating.objects.filter(
            created_by=leader,
            employee=employee,
            created_at__gte=one_week_ago 
        ).exists()
        
        if recent_evaluation_exists:
            raise serializers.ValidationError("Você já avaliou este funcionário nos últimos 7 dias.")
            
        return data
        
    @transaction.atomic
    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        
        leader = self.context['request'].user
        
        rating = Rating.objects.create(
            created_by=leader,
            **validated_data
        )
        
        answers_to_create = []
        for answer_dict in answers_data:
            answers_to_create.append(Answer(
                rating=rating, 
                question=answer_dict['question'], 
                answer=answer_dict['answer']
            ))
            
        Answer.objects.bulk_create(answers_to_create)
        
        return rating
