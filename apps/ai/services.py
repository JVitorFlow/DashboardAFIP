import os
import tempfile
import logging
from django.db import transaction
from django.core.files.uploadedfile import UploadedFile
from .agent import analyze_image
from .models import AIAssessment, Task, Item

logger = logging.getLogger(__name__)


class AssessmentProcessingError(Exception):
    """Exceção customizada para erros no processamento de imagem."""

    pass


class AIAssessmentService:
    @staticmethod
    def process_image(
        task_id: int, item_id: int, image_file: UploadedFile
    ) -> AIAssessment:
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise AssessmentProcessingError(f"Task com id={task_id} não encontrada.")
        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            raise AssessmentProcessingError(f"Item com id={item_id} não encontrado.")

        # Salva em tempfile e registra o path para log
        suffix = os.path.splitext(image_file.name)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            for chunk in image_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        logger.debug("Imagem salva em %s, iniciando análise", tmp_path)

        try:
            result_data = analyze_image(tmp_path)
            logger.debug("Resultado raw do agente: %s", result_data)
        except Exception as e:
            raise AssessmentProcessingError(f"Falha na análise de imagem: {e}")
        finally:
            # Limpeza do arquivo temporário
            try:
                os.unlink(tmp_path)
            except OSError as e:
                logger.warning("Falha ao remover temp file %s: %s", tmp_path, e)

        # Verifica se houve erro na resposta
        if error := result_data.get("error"):
            raise AssessmentProcessingError(error)

        # Construção do dict de criação
        assessment_data = {
            "task": task,
            "item": item,
            "tipo_exame_histopatologico": result_data.get(
                "Tipo de Exame histopatológico", ""
            ),
            "apresenta_risco_elevado_para_cancer_de_mama": result_data.get(
                "Apresenta risco elevado para câncer de mama?", ""
            ),
            "gravida_ou_amamentando": result_data.get(
                "Você está grávida ou amamentando?", ""
            ),
            "tratamento_anterior_para_cancer": result_data.get(
                "Tratamento anterior para câncer de mama?", ""
            ),
            "deteccao_da_lesao": result_data.get("Detecção da lesão", ""),
            "mama": result_data.get("Característica da lesão", {}).get("mama", ""),
            "localizacao_lesiao": result_data.get("Característica da lesão", {}).get(
                "localização", ""
            ),
            "tamanho_lesao": result_data.get("Característica da lesão", {}).get(
                "tamanho", ""
            ),
            "material_enviado_procedente_de": ", ".join(
                result_data.get("Material enviado procedente de", [])
            ),
            "status": "COMPLETED",
        }

        # Cria o registro dentro de uma transação
        with transaction.atomic():
            ai_assessment = AIAssessment.objects.create(**assessment_data)

        return ai_assessment
