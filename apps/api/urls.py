from django.urls import path, include

app_name = 'api'

# Inclui URLs das versões da API
urlpatterns = [
    path('v1/', include('apps.api.v1.urls')),  # URLs da versão 1 da API
]
