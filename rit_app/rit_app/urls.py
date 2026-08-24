from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    #path('admin/', admin.site.urls),

    path('api/', include('table_administration_service.urls')),
    path('api/', include('evaluation_service.urls')),
    
    # Rota para renderizar a documentação da api
    path('api/docs/', TemplateView.as_view(template_name='api_docs.html'), name='api-docs'),
]
