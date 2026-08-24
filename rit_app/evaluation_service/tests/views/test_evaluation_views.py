from rest_framework.test import APITestCase
from rest_framework import status
from table_administration_service.models.employee_models import Employee
from table_administration_service.models.question_models import QuestionVersion, Question
from evaluation_service.models import Rating, Answer

class EvaluationViewTest(APITestCase):

    def setUp(self):
        self.leader = Employee.objects.create(name='Líder', email='lider@monks.com', position_name='CTO', is_authenticated=True)
        self.lead = Employee.objects.create(name='Liderado', email='lead@monks.com', position_name='Dev', is_authenticated=False)
        
        # Pega a versão ativa criada pela migration (seed)
        self.version = QuestionVersion.objects.filter(status=True).first()
        self.q1 = self.version.questions.first() if self.version and self.version.questions.exists() else None
        
        if not self.version:
            self.version = QuestionVersion.objects.create(created_by=self.leader, status=True)
            self.q1 = Question.objects.create(questions_version=self.version, title="Pergunta 1", weight=100)

        self.rival = Employee.objects.create(name='Líder Rival', email='rival@monks.com', position_name='CTO', is_authenticated=True)
        Rating.objects.create(created_by=self.rival, employee=self.lead)


    def test_deve_receber_payload_e_criar_avaliacao_via_api(self):
        self.client.defaults['HTTP_X_USER_EMAIL'] = self.leader.email
        
        url = '/api/evaluations/' 
        
        payload = {
            "employee_id": self.lead.id,
            "answers": [
                {"question_id": self.q1.id, "answer": 4}
            ]
        }
        
        response = self.client.post(url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Rating.objects.filter(created_by=self.leader).count(), 1)
        self.assertEqual(Answer.objects.filter(rating__created_by=self.leader).count(), 1)

    def test_deve_retornar_apenas_avaliacoes_do_lider_logado(self):
        Rating.objects.create(created_by=self.leader, employee=self.lead)
        
        self.client.defaults['HTTP_X_USER_EMAIL'] = self.leader.email
        url = '/api/evaluations/'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_nao_deve_retornar_avaliacoes_se_o_lider_nao_fez_nenhuma(self):
        self.client.defaults['HTTP_X_USER_EMAIL'] = self.leader.email
        url = '/api/evaluations/'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_as_notas_answers_devem_vir_aninhadas_na_resposta_do_get(self):
        rating = Rating.objects.create(created_by=self.leader, employee=self.lead)
        Answer.objects.create(rating=rating, question=self.q1, answer=4)
        
        self.client.defaults['HTTP_X_USER_EMAIL'] = self.leader.email
        url = '/api/evaluations/'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        primeiro_item = response.data[0]
        self.assertIn('answers', primeiro_item)
        self.assertEqual(primeiro_item['answers'][0]['answer'], 4)
