from rest_framework.test import APITestCase
from rest_framework import status
from table_administration_service.models.employee_models import Employee, LeaderLead

from django.utils import timezone
from datetime import timedelta
from evaluation_service.models import Rating


class EmployeeBFFViewTest(APITestCase):

    def setUp(self):
        self.ceo = Employee.objects.create(name='CEO', email='ceo@teste.com', position_name='CEO')
        self.diretor = Employee.objects.create(name='Diretor', email='dir@teste.com', position_name='Diretor')
        self.gerente = Employee.objects.create(name='Gerente', email='ger@teste.com', position_name='Gerente')
        self.analista = Employee.objects.create(name='Analista', email='ana@teste.com', position_name='Analista')

        LeaderLead.objects.create(leader=self.ceo, lead=self.diretor)
        LeaderLead.objects.create(leader=self.diretor, lead=self.gerente)
        LeaderLead.objects.create(leader=self.gerente, lead=self.analista)

        self.client.credentials(HTTP_X_USER_EMAIL='dir@teste.com')

    def test_deve_retornar_apenas_subordinados_abaixo_na_arvore(self):
        url = '/api/team/dashboard/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), 2) # gerente e analista (2)
        
        nomes_retornados = [emp['name'] for emp in response.data]
        self.assertNotIn('CEO', nomes_retornados)
        self.assertIn('Gerente', nomes_retornados)
        self.assertIn('Analista', nomes_retornados)
        
    def test_deve_classificar_corretamente_direto_e_indireto(self):
        url = '/api/team/dashboard/'
        response = self.client.get(url)
        
        for funcionario in response.data:
            if funcionario['name'] == 'Gerente':
                gerente = funcionario
            elif funcionario['name'] == 'Analista':
                analista = funcionario
        
        self.assertEqual(gerente['relation'], 'direto')
        self.assertEqual(analista['relation'], 'indireto')

    def test_deve_retornar_status_como_pendente_se_nunca_foi_avaliado(self):
        url = '/api/team/dashboard/'
        response = self.client.get(url)
        
        gerente = next(e for e in response.data if e['name'] == 'Gerente')
        self.assertEqual(gerente['evaluation_status'], 'Pendente')

    def test_deve_retornar_dias_restantes_se_avaliado_recentemente(self):
        rating = Rating.objects.create(created_by=self.diretor, employee=self.gerente)
        
        dois_dias_atras = timezone.now() - timedelta(days=2)
        Rating.objects.filter(id=rating.id).update(created_at=dois_dias_atras)
        
        url = '/api/team/dashboard/'
        response = self.client.get(url)
        
        gerente = next(e for e in response.data if e['name'] == 'Gerente')
        self.assertEqual(gerente['evaluation_status'], 'Realizada - próx. em 5 dias')

