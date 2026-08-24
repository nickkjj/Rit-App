from rest_framework.test import APITestCase
from rest_framework import status
from table_administration_service.models.employee_models import Employee
from table_administration_service.models.question_models import QuestionVersion, Question
from evaluation_service.models import Rating, Answer
from django.utils import timezone
from datetime import timedelta

class RecentEvaluationViewTest(APITestCase):

    def setUp(self):
        self.leader = Employee.objects.create(name='Líder', email='lider@monks.com', position_name='CTO', is_authenticated=True)
        self.lead = Employee.objects.create(name='Liderado', email='lead@monks.com', position_name='Dev', is_authenticated=False)
        
        self.version = QuestionVersion.objects.create(created_by=self.leader, status=True)
        self.q1 = Question.objects.create(questions_version=self.version, title="Pergunta 1", weight=100)

        self.client.credentials(HTTP_X_USER_EMAIL='lider@monks.com')

    def test_deve_retornar_recent_false_se_nao_houver_avaliacao(self):
        url = f'/api/evaluations/recent/?employee_id={self.lead.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['recent'])

    def test_deve_retornar_recent_false_se_avaliacao_for_antiga(self):
        rating = Rating.objects.create(created_by=self.leader, employee=self.lead)
        # Força data de criação para 10 dias atrás
        rating.created_at = timezone.now() - timedelta(days=10)
        rating.save()

        url = f'/api/evaluations/recent/?employee_id={self.lead.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['recent'])

    def test_deve_retornar_recent_true_com_dados_se_for_recente(self):
        rating = Rating.objects.create(created_by=self.leader, employee=self.lead)
        # Data de criação: apenas 2 dias atrás
        rating.created_at = timezone.now() - timedelta(days=2)
        rating.save()
        Answer.objects.create(rating=rating, question=self.q1, answer=3)

        url = f'/api/evaluations/recent/?employee_id={self.lead.id}'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['recent'])
        self.assertEqual(response.data['days_left'], 4) # 7 - 2 = 5 mas dependendo das horas pode ser 4
        self.assertEqual(len(response.data['answers']), 1)
        self.assertEqual(response.data['answers'][0]['answer'], 3)

    def test_deve_retornar_400_se_nao_passar_employee_id(self):
        url = '/api/evaluations/recent/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
