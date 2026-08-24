from rest_framework.test import APITestCase
from rest_framework import status
from table_administration_service.models.employee_models import Employee

class LoginViewTest(APITestCase):

    def setUp(self):
        Employee.objects.all().delete()
        self.employee = Employee.objects.create(
            name='Nicolas',
            email='macielniiicolas@gmail.com',
            position_name='System Analyst'
        )

    def test_deve_retornar_200_com_dados_do_usuario_se_email_existir(self):
        url = '/api/session/'
        payload = {"email": "macielniiicolas@gmail.com"}
        
        response = self.client.post(url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'macielniiicolas@gmail.com')
        self.assertEqual(response.data['name'], 'Nicolas')

    def test_deve_retornar_404_se_tentar_logar_com_email_inexistente(self):
        url = '/api/session/'
        payload = {"email": " sem@cadastro.com"}
        
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deve_retornar_lista_de_usuarios_para_login(self):
        url = '/api/login-users/'
        
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        self.assertTrue(len(response.data) >= 1)
        
        # Encontra o Nicolas na lista (pode ter seeds)
        nicolas = next((user for user in response.data if user['email'] == 'macielniiicolas@gmail.com'), None)
        self.assertIsNotNone(nicolas)
