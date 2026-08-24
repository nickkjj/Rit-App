from django.test import TestCase

from table_administration_service.models.employee_models import Employee
from table_administration_service.models.question_models import QuestionVersion, Question
from evaluation_service.serializers.rating_serializers import RatingCreateSerializer

from evaluation_service.models import Rating, Answer

from datetime import timedelta
from django.utils import timezone

class RatingSerializerTest(TestCase):

    def setUp(self):
        self.leader = Employee.objects.create(name='Leader', email='ldr@monks.com', position_name='CTO')
        self.lead = Employee.objects.create(name='Lead', email='ld@monks.com', position_name='Dev')
        
        self.version = QuestionVersion.objects.create(created_by=self.leader, status=True)
        self.q1 = Question.objects.create(questions_version=self.version, title="Comunicação?", weight=50)
        self.q2 = Question.objects.create(questions_version=self.version, title="Proatividade?", weight=50)

    def test_deve_criar_rating_e_respostas_simultaneamente(self):
        payload = {
            "employee_id": self.lead.id,
            "answers": [
                {"question_id": self.q1.id, "answer": 3},
                {"question_id": self.q2.id, "answer": 4}
            ]
        }
        
        class MockRequest:
            user = self.leader
            
        serializer = RatingCreateSerializer(data=payload, context={'request': MockRequest()})
        
        self.assertTrue(serializer.is_valid(), serializer.errors)
        rating = serializer.save()
        
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Answer.objects.count(), 2)
        
        self.assertEqual(rating.created_by, self.leader)
        self.assertEqual(rating.employee, self.lead)

    
    def test_nao_deve_permitir_avaliacoes_do_mesmo_liderado_em_menos_de_7_dias(self):
        Rating.objects.create(created_by=self.leader, employee=self.lead)
        
        payload = {
            "employee_id": self.lead.id,
            "answers": [{"question_id": self.q1.id, "answer": 3}]
        }
        
        class MockRequest:
            user = self.leader
            
        serializer = RatingCreateSerializer(data=payload, context={'request': MockRequest()})
        
        self.assertFalse(serializer.is_valid())
        self.assertIn("Você já avaliou este funcionário nos últimos 7 dias", str(serializer.errors))

    def test_deve_permitir_se_ultima_avaliacao_for_mais_antiga_que_7_dias(self):
        old_rating = Rating.objects.create(created_by=self.leader, employee=self.lead)
        
        Rating.objects.filter(id=old_rating.id).update(created_at=timezone.now() - timedelta(days=8))
        
        payload = {
            "employee_id": self.lead.id,
            "answers": [{"question_id": self.q1.id, "answer": 3}]
        }
        
        class MockRequest:
            user = self.leader
            
        serializer = RatingCreateSerializer(data=payload, context={'request': MockRequest()})
        
        self.assertTrue(serializer.is_valid(), serializer.errors)

