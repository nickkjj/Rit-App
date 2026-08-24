from django.urls import path
from evaluation_service.views.evaluation_views import EvaluationCreateView
from evaluation_service.views.history_views import team_history
from evaluation_service.views.recent_evaluation import recent_evaluation

urlpatterns = [
    path('evaluations/', EvaluationCreateView.as_view(), name='evaluations-create'),
    path('evaluations/recent/', recent_evaluation, name='evaluations-recent'),
    path('team/history/', team_history, name='team-history'),
]
