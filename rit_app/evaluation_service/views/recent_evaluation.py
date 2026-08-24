from rest_framework.decorators import api_view
from rest_framework.response import Response
from evaluation_service.models import Rating
from django.utils import timezone
import datetime

@api_view(['GET'])
def recent_evaluation(request):
    employee_id = request.query_params.get('employee_id')
    leader = request.user
    
    if not employee_id:
        return Response({'error': 'employee_id é obrigatório'}, status=400)
        
    # Busca a avaliação mais recente feita por esse líder para esse funcionário
    try:
        rating = Rating.objects.filter(
            created_by=leader,
            employee_id=employee_id
        ).order_by('-created_at').first()
        
        if not rating:
            return Response({'recent': False})
            
        # Calcular tempo restante para completar 7 dias
        now = timezone.now()
        days_passed = (now - rating.created_at).days
        
        if days_passed >= 7:
            return Response({'recent': False})
            
        # Calcula horas e dias restantes
        time_diff = rating.created_at + datetime.timedelta(days=7) - now
        total_seconds = int(time_diff.total_seconds())
        days_left = total_seconds // 86400
        hours_left = (total_seconds % 86400) // 3600
        
        answers_data = []
        for ans in rating.answers.all().select_related('question'):
            answers_data.append({
                'question_title': ans.question.title,
                'weight': ans.question.weight,
                'answer': ans.answer
            })
            
        return Response({
            'recent': True,
            'days_left': days_left,
            'hours_left': hours_left,
            'created_at': rating.created_at,
            'answers': answers_data
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)
