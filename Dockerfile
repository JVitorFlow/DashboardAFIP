# Imagem base
FROM python:3.11

# Configuração do diretório de trabalho
WORKDIR /app

# Definir variáveis de ambiente para otimização do Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copiar apenas requirements.txt para aproveitar o cache durante builds
COPY requirements.txt /app/

# Atualizar pip e instalar dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código para o diretório de trabalho
COPY . /app/

# Expor a porta que o Gunicorn usará
EXPOSE 8000

# Comando para iniciar o servidor Gunicorn
CMD ["gunicorn", "--chdir", "/app/orchestrator_rpa", "--config", "gunicorn-cfg.py", "orchestrator.orchestrator.wsgi"]
