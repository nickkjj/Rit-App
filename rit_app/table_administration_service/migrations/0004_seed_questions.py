from django.db import migrations

def populate_questions(apps, schema_editor):
    QuestionVersion = apps.get_model('table_administration_service', 'QuestionVersion')
    Question = apps.get_model('table_administration_service', 'Question')
    Employee = apps.get_model('table_administration_service', 'Employee')
    
    # We need a creator for the QuestionVersion. Alice (CEO) will be the creator.
    alice = Employee.objects.filter(email='alice.hartman@company.com').first()
    if not alice:
        return
        
    version = QuestionVersion.objects.create(created_by=alice, status=True)
    
    questions_data = [
        ("Entrega de Resultados", 25),
        ("Execução e Qualidade do Trabalho", 20),
        ("Capacidade de Aprendizado e Desenvolvimento", 20),
        ("Resolução de Problemas e Pensamento Crítico", 15),
        ("Colaboração, Influência e Liderança", 10),
        ("Visão Estratégica e Potencial de Crescimento", 10)
    ]
    
    for title, weight in questions_data:
        Question.objects.create(
            questions_version=version,
            title=title,
            weight=weight
        )

class Migration(migrations.Migration):

    dependencies = [
        ('table_administration_service', '0003_seed_employees'),
    ]

    operations = [
        migrations.RunPython(populate_questions),
    ]

"""
Questão Peso
Entrega de Resultados 25
Execução e Qualidade do Trabalho 20
Capacidade de Aprendizado e Desenvolvimento 20
Resolução de Problemas e Pensamento Crítico 15
Colaboração, Influência e Liderança 10
Visão Estratégica e Potencial de Crescimento 10
"""
