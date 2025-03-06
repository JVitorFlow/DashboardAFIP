from django.urls import path
from apps.alerts.views import RobotAlertCreateAPIView, RobotAlertListAPIView

urlpatterns = [
    path('create/', RobotAlertCreateAPIView.as_view(), name='alert-create'),
    path('list/', RobotAlertListAPIView.as_view(), name='alert-list'),
]
