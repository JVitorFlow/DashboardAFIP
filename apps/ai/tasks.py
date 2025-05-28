import logging
from celery import shared_task
from django.core.files.uploadedfile import SimpleUploadedFile

from .services import AIAssessmentService, AssessmentProcessingError

logger = logging.getLogger(__name__)

@shared_task(
    bind=True,
    name="ai.process_image",
    max_retries=3,
    default_retry_delay=10,
)
def process_image_task(self, task_id: int, item_id: int, image_bytes: bytes, image_name: str):

    uploaded = SimpleUploadedFile(name=image_name, content=image_bytes)

    try:
        ai_assessment = AIAssessmentService.process_image(
            task_id, item_id, uploaded
        )
        return ai_assessment.id

    except AssessmentProcessingError as e:
        logger.exception("Erro no processamento de IA")
        # Se for recuperável, faz retry; senão, a task falha
        raise self.retry(exc=e)