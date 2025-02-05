import os
import base64
from decouple import config 
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage
import json

os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

# Inicializar o modelo GPT-4 Vision
chat = ChatOpenAI(model='gpt-4o', max_tokens=512)

def encode_image(image_path):
    """
    Função para codificar a imagem em base64
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_image(image_path):
    """
    Função principal que usa GPT-4 Vision para processar a imagem e retornar as respostas.
    """
    base64_image = encode_image(image_path)

    prompt = """
    Analise a imagem do formulário médico anexado e identifique precisamente as áreas que estão marcadas com 'X' na seção de 'dados clínicos'. Utilize técnicas avançadas de visão computacional para detectar essas marcações e gerar uma resposta organizada
    """

    human_message = [
        HumanMessage(content=prompt),
        HumanMessage(
            content=[
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64_image, "detail": "auto"}}
            ]
        )
    ]

    output = chat.invoke(human_message)

    # Processar a saída para remover blocos indesejados
    result_data = output.content.strip("```json").strip("```").strip()

    # Tentar carregar o resultado como JSON
    try:
        json_result = json.loads(result_data)
    except json.JSONDecodeError:
        json_result = {"erro": "Falha ao processar o JSON retornado"}

    return json_result