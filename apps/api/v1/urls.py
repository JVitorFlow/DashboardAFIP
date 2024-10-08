from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.robots.views import RobotViewSet
from apps.items.views import ItemViewSet
from apps.tasks.views import TaskViewSet
from apps.values.views import ShiftDataViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Cria um DefaultRouter e registra os ViewSets para a versão 1
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'robots', RobotViewSet, basename='robot')
router.register(r'items', ItemViewSet, basename='item')
router.register(r'shift-data', ShiftDataViewSet, basename='shift-data')

urlpatterns = [
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Inclui as URLs geradas pelo router
    path('', include(router.urls)),
]
