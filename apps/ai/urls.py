from django.urls import path
from .views import AIAssessmentFormDataAPIView, AIAssessmentResultAPIView

urlpatterns = [

    path("", AIAssessmentFormDataAPIView.as_view(), name="ai-upload"),
    path("<int:pk>/", AIAssessmentResultAPIView.as_view(), name="ai-result"),
]