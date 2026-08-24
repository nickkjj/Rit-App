from django.test import TestCase
from table_administration_service.serializers.question_serializers import QuestionVersionCreateSerializer
from table_administration_service.models.question_models import QuestionVersion, Question
from table_administration_service.models.employee_models import Employee

class QuestionVersionServiceTest(TestCase):

    def setUp(self):
        QuestionVersion.objects.all().delete()
        self.employee = Employee.objects.create(name='Nicolas', email='macielniiicolas@gmail.com', position_name='Software Analyst')
        self.versao_antiga = QuestionVersion.objects.create(created_by=self.employee, status=True)

    
    def test_deve_criar_versao_com_sucesso_e_desativar_versoes_antigas(self):

        #arrange
        payload = {
            "questions": [
                {"title": "Entrega de Resultados", "weight": 25},
                {"title": "Execução e Qualidade do Trabalho", "weight": 20},
                {"title": "Capacidade de Aprendizado e Desenvolvimento", "weight": 20},
                {"title": "Resolução de Problemas e Pensamento Crítico", "weight": 15},
                {"title": "Colaboração, Influência e Liderança", "weight": 10},
                {"title": "Visão Estratégica e Potencial de Crescimento", "weight": 10},
            ]
        }

        #act
        class MockRequest:
            user = self.employee

        serializer = QuestionVersionCreateSerializer(
            data=payload, 
            context={'request': MockRequest()}
        )

        serializer.is_valid(raise_exception=True)

        nova_versao = serializer.save()
       
        #assert  
        self.assertEqual(QuestionVersion.objects.count(), 2) #verificar se as duas versoes foram criadas
        self.assertEqual(Question.objects.count(), 6) #verficar se todas questoes foram criadas
        self.assertEqual(Question.objects.filter(questions_version=nova_versao).count(), 6) #verificar se as questoes foram vinculadas a versão correta
        self.assertTrue(nova_versao.status)
        self.assertEqual(nova_versao.created_by, self.employee)

        self.versao_antiga.refresh_from_db()
        self.assertFalse(self.versao_antiga.status)


    def test_deve_falhar_se_soma_dos_pesos_nao_for_100(self):

        payload = {
            "questions": [
                {"title": "Entrega de Resultados", "weight": 99},
                {"title": "Execução e Qualidade do Trabalho", "weight": 2}
            ]
        }

        class MockRequest:
            user = self.employee

        serializer = QuestionVersionCreateSerializer(
            data = payload,
            context = {'request': MockRequest()}
        )

        is_valid = serializer.is_valid()

        self.assertFalse(is_valid)
        
        self.assertIn('non_field_errors', serializer.errors)
        self.assertEqual(
            str(serializer.errors['non_field_errors'][0]), 
            "A soma dos pesos das questões tem que resultar em 100."
        )
        
                
