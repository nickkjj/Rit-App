from rest_framework.routers import DefaultRouter
from django.urls import path

from table_administration_service.views.question_views import QuestionVersionViewSet
from table_administration_service.views.login_views import session_login, login_users
from table_administration_service.views.employee_views import team_dashboard

router = DefaultRouter()

router.register(r'questions/versions', QuestionVersionViewSet, basename='question_version')

urlpatterns = [
    path('session/', session_login, name='session_login'),
    path('login-users/', login_users, name='login_users'),
    path('team/dashboard/', team_dashboard, name='team_dashboard'),
] + router.urls