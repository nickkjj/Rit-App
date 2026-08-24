from rest_framework.decorators import api_view
from rest_framework.response import Response
from evaluation_service.models import Rating
from django.utils import timezone
import datetime
from collections import defaultdict

@api_view(['GET'])
def team_history(request):
    leader = request.user
    
    now = timezone.now()
    months = []
    labels = []
    
    pt_months = {
        1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
        5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
        9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
    }
    
    # Calculate last 6 months natively
    current_month = now.month
    current_year = now.year
    
    for i in range(5, -1, -1):
        m = current_month - i
        y = current_year
        while m <= 0:
            m += 12
            y -= 1
        
        months.append(f"{y}-{m:02d}")
        labels.append(pt_months[m])
        
        if i == 5:
            six_months_ago = now.replace(year=y, month=m, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Buscar ratings do líder nos últimos 6 meses
    ratings = Rating.objects.filter(
        created_by=leader,
        created_at__gte=six_months_ago
    ).prefetch_related('answers__question')
    
    # Agrupar e calcular score
    month_scores = defaultdict(list)
    
    for rating in ratings:
        key = rating.created_at.strftime('%Y-%m')
        
        # Fórmula: Soma(Resposta * Peso_da_Questao) / 4
        # answer.answer é 1 a 4. question.weight é 0 a 100.
        score = 0
        for ans in rating.answers.all():
            score += (ans.answer * ans.question.weight)
            
        score = score / 4.0
        month_scores[key].append(score)
        
    # Construir array de dados alinhado aos 6 meses
    data = []
    for m in months:
        scores = month_scores.get(m, [])
        if scores:
            data.append(round(sum(scores) / len(scores), 1))
        else:
            data.append(0)
            
    return Response({
        "labels": labels,
        "data": data
    })
