# Imagem base
FROM python:3.11-slim

# Configuração do diretório de trabalho
WORKDIR /app

# Definir variáveis de ambiente para otimização do Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependências do sistema (incluindo postgresql-client para pg_isready)
RUN apt-get update && apt-get install -y postgresql-client

# Copiar apenas requirements.txt para aproveitar o cache durante builds
COPY requirements.txt /app/

# Atualizar pip e instalar dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código para o diretório de trabalho
COPY . /app/

# Copiar o script de entrada e dar permissão de execução
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expor a porta que o Gunicorn usará
EXPOSE 8000

# Definir o entrypoint para esperar o banco de dados antes de iniciar o Django
ENTRYPOINT ["/app/entrypoint.sh"]

# Comando para iniciar o servidor Gunicorn
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "apps.core.wsgi:application"]
