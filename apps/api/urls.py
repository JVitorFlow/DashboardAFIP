from django.urls import path
from apps.robots.views import RobotAPIView
from apps.tasks.views import TaskAPIView
from apps.items.views import ItemAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('robots/<int:robot_id>/', RobotAPIView.as_view(), name='robot'),
    path('tasks/<int:robot_id>/', TaskAPIView.as_view(), name='task_list'),
    path('tasks/<int:robot_id>/<int:task_id>/', TaskAPIView.as_view(), name='task_detail'),
    path(r'items', ItemAPIView.as_view(), name='item'),
]
