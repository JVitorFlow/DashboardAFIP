from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import AIAssessment, Task, Item
from .agent import analyze_image
import os
import logging

logger = logging.getLogger(__name__)

class AIAssessmentFormDataAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Enviar imagem via form-data e processar com IA",
        manual_parameters=[
            openapi.Parameter(
                name="task_id",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                description="ID da Task",
                required=True
            ),
            openapi.Parameter(
                name="item_id",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                description="ID do Item",
                required=True
            ),
            openapi.Parameter(
                name="image",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Arquivo da Imagem (opcional)",
                required=False
            ),
        ],
        responses={201: "Imagem processada com sucesso"}
    )
    def post(self, request, *args, **kwargs):
        task_id = request.data.get('task_id')
        item_id = request.data.get('item_id')

        # Verifica se os IDs foram fornecidos corretamente
        if not task_id or not item_id:
            return Response({"error": "ID da Task e Item são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        # Valida se o Task e Item existem
        task = get_object_or_404(Task, id=task_id)
        item = get_object_or_404(Item, id=item_id)

        if 'image' in request.FILES:
            # Salva o arquivo temporariamente
            image = request.FILES.get('image')
            image_path = f'/tmp/{image.name}'
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
        else:
            return Response({"error": "Nenhuma imagem foi enviada."}, status=status.HTTP_400_BAD_REQUEST)

        # Processar a imagem usando IA
        result_data = analyze_image(image_path)

        if not result_data:
            return Response({"error": "Nenhum dado processado."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar se a resposta contém dados clínicos ou a mensagem de que não há informações
        dados_clinicos = result_data.get('dados_clinicos')

        if isinstance(dados_clinicos, str) and dados_clinicos == "Nenhuma informação encontrada.":
            # Caso não tenha informações, cria um registro com campos vazios e status 'PENDING'
            ai_assessment = AIAssessment.objects.create(
                task=task,
                item=item,
                status='PENDING',
            )
            return Response({
                "result": "Nenhuma informação encontrada na imagem",
                "dados_clinicos": dados_clinicos
            }, status=status.HTTP_201_CREATED)

        # Se houver dados clínicos, cria o registro normalmente
        ai_assessment = AIAssessment.objects.create(
            task=task,
            item=item,
            tipo_exame_histopatologico=dados_clinicos.get('Tipo de Exame histopatológico', ''),
            apresenta_risco_elevado_para_cancer_de_mama=dados_clinicos.get('Apresenta risco elevado para câncer de mama?', ''),
            gravida_ou_amamentando=dados_clinicos.get('Você está grávida ou amamentando?', ''),
            tratamento_anterior_para_cancer=dados_clinicos.get('Tratamento anterior para câncer de mama?', ''),
            deteccao_da_lesao=dados_clinicos.get('Detecção da lesão', ''),
            mama=dados_clinicos.get('Característica da lesão', {}).get('mama', ''),
            localizacao_lesao=dados_clinicos.get('Característica da lesão', {}).get('localização', ''),
            tamanho_lesao=dados_clinicos.get('Característica da lesão', {}).get('tamanho', ''),
            material_enviado_procedente_de=', '.join(dados_clinicos.get('Material enviado procedente de', [])),
            status='COMPLETED',
        )

        return Response({
            "result": "Imagem processada com sucesso",
            "dados_clinicos": dados_clinicos  # Inclui o resultado processado na resposta
        }, status=status.HTTP_201_CREATED)
