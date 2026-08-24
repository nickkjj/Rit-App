from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from table_administration_service.models.question_models import QuestionVersion
from table_administration_service.serializers.question_serializers import (
    QuestionVersionReadSerializer,
    QuestionVersionCreateSerializer
)

class QuestionVersionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = QuestionVersion.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionVersionCreateSerializer
        return QuestionVersionReadSerializer

    def _check_permission(self, request):
        allowed_positions = ['CEO', 'CTO', 'CFO']
        if request.user.position_name not in allowed_positions:
            return False
        return True

    def create(self, request, *args, **kwargs):
        if not self._check_permission(request):
            return Response({"detail": "Acesso Restrito. Apenas cargos de diretoria podem salvar configurações."}, status=403)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if not self._check_permission(request):
            return Response({"detail": "Acesso Restrito."}, status=403)
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def current(self, request):
        active_version = QuestionVersion.objects.filter(status=True).first()
        
        if not active_version:
            return Response({"detail": "Nenhuma versão ativa encontrada."}, status=404)
            
        serializer = self.get_serializer(active_version)
        return Response(serializer.data)
