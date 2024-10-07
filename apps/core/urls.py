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
schema_view_v1 = get_schema_view(
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
    patterns=[path('api/v1/', include('apps.api.v1.urls'))]
)

urlpatterns = [
    path('', DashboardListView.as_view(), name='tasks'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name="logout"),
    path('admin/', admin.site.urls),
    path('tareas/<int:task_id>/', ItemListView.as_view(), name='items'),
    path('api/', include('apps.api.urls')),

    # URLs da documentação gerada pelo drf-yasg
    re_path(r'^swagger/v1(?P<format>\.json|\.yaml)$', schema_view_v1.without_ui(cache_timeout=0), name='schema-json-v1'),
    path('swagger/v1/', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-v1'),
    path('redoc/v1/', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
]
