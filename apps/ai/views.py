from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    AIAssessmentInputSerializer,
    AIAssessmentOutputSerializer,
)
from .tasks import process_image_task
from .models import AIAssessment


class AIAssessmentFormDataAPIView(APIView):
    """
    Recebe form com imagem e dispara a task Celery.
    """
    def post(self, request, *args, **kwargs):
        ser = AIAssessmentInputSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        image_file = data['image']
        image_bytes = b''.join(chunk for chunk in image_file.chunks())
        image_name = image_file.name

        celery_task = process_image_task.delay(
            data['task_id'], data['item_id'], image_bytes, image_name
        )

        return Response(
            {"job_id": celery_task.id, "status": "PROCESSING"},
            status=status.HTTP_202_ACCEPTED,
        )


class AIAssessmentResultAPIView(RetrieveAPIView):
    """
    Retorna status e resultado de um AIAssessment.
    """
    queryset = AIAssessment.objects.all()
    serializer_class = AIAssessmentOutputSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'