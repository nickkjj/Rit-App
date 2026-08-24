from rest_framework.test import APITestCase
from rest_framework import status

from table_administration_service.models.employee_models import Employee
from table_administration_service.models.question_models import QuestionVersion



class QuestionVersionViewTest(APITestCase):

    def setUp(self):
        QuestionVersion.objects.all().delete()
        self.ceo = Employee.objects.create(
            name='Alice', 
            email='alice@monks.com', 
            position_name='CEO'
        )
        self.analyst = Employee.objects.create(
            name='Bob', 
            email='bob@monks.com', 
            position_name='System Analyst'
        )

        #simulando a request do front com "autenticação"
        self.client.credentials(HTTP_X_USER_EMAIL='alice@monks.com')

    def test_deve_criar_versao_como_ceo(self):
        url = '/api/questions/versions/'
        payload = {
            "questions": [
                {"title": "Entrega de Resultados", "weight": 100},
            ]
        }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_deve_retornar_403_ao_criar_versao_com_cargo_baixo(self):
        self.client.credentials(HTTP_X_USER_EMAIL='bob@monks.com')
        url = '/api/questions/versions/'
        payload = {
            "questions": [
                {"title": "Teste", "weight": 100},
            ]
        }
        response = self.client.post(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deve_retornar_401_se_nao_estiver_autenticado(self):
        self.client.credentials() 
        url = '/api/questions/versions/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deve_listar_historico_de_versoes_como_ceo(self):
        QuestionVersion.objects.create(created_by=self.ceo, status=True)
        url = '/api/questions/versions/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_deve_retornar_403_ao_listar_historico_com_cargo_baixo(self):
        self.client.credentials(HTTP_X_USER_EMAIL='bob@monks.com')
        url = '/api/questions/versions/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_deve_retornar_apenas_a_versao_atual_ativa_para_qualquer_cargo(self):
        self.client.credentials(HTTP_X_USER_EMAIL='bob@monks.com')
        QuestionVersion.objects.create(created_by=self.ceo, status=False)
        versao_ativa = QuestionVersion.objects.create(created_by=self.ceo, status=True)
        url = '/api/questions/versions/current/' 
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], versao_ativa.id)

