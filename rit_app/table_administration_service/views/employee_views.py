from rest_framework.decorators import api_view
from rest_framework.response import Response
from table_administration_service.models.employee_models import Employee

# Novos imports para lidar com tempo e consultas avançadas
from django.utils import timezone
from evaluation_service.models import Rating
from django.db.models import Max

@api_view(['GET'])
def team_dashboard(request):
    
    leader_id = request.user.id
    
    #CTE
    query = """
    WITH RECURSIVE subordinates AS (
        SELECT 
            e.id, e.name, e.email, e.position_name, e.is_authenticated,
            'direto' AS relation
        FROM employee e
        INNER JOIN leader_lead ll ON e.id = ll.lead_id
        WHERE ll.leader_id = %s
        
        UNION ALL
        
        SELECT 
            e.id, e.name, e.email, e.position_name, e.is_authenticated,
            'indireto' AS relation
        FROM employee e
        INNER JOIN leader_lead ll ON e.id = ll.lead_id
        INNER JOIN subordinates s ON ll.leader_id = s.id
    )
    SELECT * FROM subordinates;
    """
    
    team_members = Employee.objects.raw(query, [leader_id])
    
    member_ids = [emp.id for emp in team_members]
    
    latest_ratings = Rating.objects.filter(
        created_by_id=leader_id,
        employee_id__in=member_ids
    ).values('employee_id').annotate(last_eval=Max('created_at'))
    
    rating_map = {item['employee_id']: item['last_eval'] for item in latest_ratings}
    
    now = timezone.now()
    result = []
    
    for emp in team_members:
        status = "Pendente"
        last_eval = rating_map.get(emp.id)
        
        if last_eval:
            days_since = (now - last_eval).days
            if days_since < 7:
                days_remaining = 7 - days_since
                status = f"Realizada - próx. em {days_remaining} dias"
                
        result.append({
            "id": emp.id,
            "name": emp.name,
            "position_name": emp.position_name,
            "relation": emp.relation,
            "evaluation_status": status
        })
        
    return Response(result)
