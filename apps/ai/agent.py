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
    ME DIGA AONDE ESTÁ MARCADO COM X NESSE FORMULARIO MÉDICO NA PARTE DE DADOS CLÍNICOS, SE NÃO TIVER NADA ME AVISE.
    Gere um JSON como resposta, tanto para se tiver resultado ou não. Se não tiver, retorne dentro do JSON de 'dados_clinicos' a mensagem: 'Nenhuma informação encontrada.'.
    As perguntas estão em ordens na resposta do json siga a ordem, use recursos avançados de visão computacional
    Retorne apenas o JSON, sem formatações adicionais como blocos de código. E você está indo muito bem!
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