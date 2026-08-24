from rest_framework.generics import ListCreateAPIView
from evaluation_service.models import Rating
from evaluation_service.serializers.rating_serializers import RatingCreateSerializer

class EvaluationCreateView(ListCreateAPIView):
    serializer_class = RatingCreateSerializer
    
    def get_queryset(self):
        leader = self.request.user
        
        return Rating.objects.filter(created_by=leader).prefetch_related('answers')
