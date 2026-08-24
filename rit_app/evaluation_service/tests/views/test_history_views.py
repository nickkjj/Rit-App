from rest_framework.test import APITestCase
from rest_framework import status
from table_administration_service.models.employee_models import Employee
from table_administration_service.models.question_models import QuestionVersion, Question
from evaluation_service.models import Rating, Answer
from datetime import timedelta
from django.utils import timezone

class TeamHistoryViewTest(APITestCase):

    def setUp(self):
        self.leader = Employee.objects.create(name='Líder', email='lider@monks.com', position_name='CTO', is_authenticated=True)
        self.lead1 = Employee.objects.create(name='Liderado 1', email='lead1@monks.com', position_name='Dev', is_authenticated=False)
        self.lead2 = Employee.objects.create(name='Liderado 2', email='lead2@monks.com', position_name='Dev', is_authenticated=False)
        
        self.version = QuestionVersion.objects.create(created_by=self.leader, status=True)
        self.q1 = Question.objects.create(questions_version=self.version, title="Pergunta 1", weight=50)
        self.q2 = Question.objects.create(questions_version=self.version, title="Pergunta 2", weight=50)

        self.client.credentials(HTTP_X_USER_EMAIL='lider@monks.com')

    def test_deve_retornar_historico_da_equipe(self):
        # Avaliação 1
        r1 = Rating.objects.create(created_by=self.leader, employee=self.lead1)
        r1.created_at = timezone.now() - timedelta(days=30)
        r1.save()
        Answer.objects.create(rating=r1, question=self.q1, answer=3) # 50% * 3 = 1.5
        Answer.objects.create(rating=r1, question=self.q2, answer=4) # 50% * 4 = 2.0 -> avg 3.5 -> (3.5/4)*100 = 87.5

        # Avaliação 2
        r2 = Rating.objects.create(created_by=self.leader, employee=self.lead2)
        r2.created_at = timezone.now() - timedelta(days=30)
        r2.save()
        Answer.objects.create(rating=r2, question=self.q1, answer=2) # 50% * 2 = 1.0
        Answer.objects.create(rating=r2, question=self.q2, answer=2) # 50% * 2 = 1.0 -> avg 2.0 -> (2.0/4)*100 = 50.0

        # Média da equipe no mês: (87.5 + 50.0) / 2 = 68.75

        url = '/api/team/history/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertIn('labels', response.data)
        self.assertTrue(len(response.data['data']) > 0)
        # O último item adicionado deve ter o score da média
        self.assertAlmostEqual(response.data['data'][-2], 68.8, places=1)

    def test_deve_retornar_401_se_nao_estiver_autenticado(self):
        self.client.credentials() 
        url = '/api/team/history/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
