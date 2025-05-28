import os
import base64
import json
from typing import Dict
from decouple import config
from langchain_openai import ChatOpenAI
from langchain.schema.messages import SystemMessage, HumanMessage

os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

chat = ChatOpenAI(
    model='gpt-4o',
    temperature=0,
    max_tokens=512,
    max_retries=2,
    timeout=None,
)


def encode_image(image_path: str) -> str:
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def analyze_image(image_path: str) -> Dict:
    system_prompt = (
        'Você é um assistente especialista em análise de formulários médicos. '
        "Sua tarefa é receber uma imagem de um formulário e extrair todas as marcações 'X' "
        "na seção 'dados clínicos'.\n\n"
        'PROCESSO (não deve aparecer na saída):\n'
        " 1. Localize a região 'dados clínicos'.\n"
        " 2. Para cada 'X', identifique o campo correspondente.\n"
        ' 3. Calcule a bounding box (x, y, width, height).\n\n'
        'SAÍDA (estritamente JSON):\n'
        '```json\n'
        '{\n'
        '  "marcacoes": [\n'
        '    {\n'
        '      "campo": "pressao_arterial",\n'
        '      "bbox": {"x": 123, "y": 456, "width": 20, "height": 20}\n'
        '    }\n'
        '  ]\n'
        '}\n'
        '```'
    )
    human_prompt = 'Aqui está a imagem do formulário em base64. Analise conforme o system prompt.'

    msgs = [
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=[
                {'type': 'text', 'text': human_prompt},
                {
                    'type': 'image',
                    'source_type': 'base64',
                    'mime_type': 'image/png',
                    'data': encode_image(image_path),
                },
            ]
        ),
    ]

    response = chat.invoke(msgs)
    raw = response.content

    cleaned = (
        raw.removeprefix('```json')
        .removeprefix('```')
        .removesuffix('```')
        .strip()
    )
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {
            'error': 'JSON parse failed',
            'message': str(e),
            'raw_response': raw,
        }
