"""
URL configuration for orchestrator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import login_view, logout_view
from apps.tasks.views import DashboardListView
from apps.items.views import ItemListView
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication


# Configuração do drf-yasg para gerar a documentação da API
schema_view = get_schema_view(
    openapi.Info(
        title="Documentação da API Orchestrator",
        default_version='v1',
        description="Documentação da API para o projeto Orchestrator RPA AFIP",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="joao.vitor@wtime.com.br"),
        license=openapi.License(name="Licença MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(JWTAuthentication,),
)



urlpatterns = [
    path(r'', DashboardListView.as_view(), name='tasks'),
    path(r'login/', login_view, name='login'),
    path(r'logout/', logout_view, name="logout"),
    path(r'admin/', admin.site.urls),
    path(r'tareas/<int:task_id>', ItemListView.as_view(), name='items'),
    path(r'api/', include('apps.api.urls')),

    # URLs da documentação gerada pelo drf-yasg
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
