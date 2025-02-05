# Orquestrador RPA

O **Orquestrador RPA** é uma plataforma desenvolvida para permitir que usuários enviem e gerenciem tarefas massivas a serem processadas por robôs de automação (RPA). Essa solução resolve o problema da necessidade de realizar tarefas repetitivas e múltiplas em sistemas que não suportam a entrada massiva de solicitações. O sistema também possui um orquestrador que distribui as tarefas de forma inteligente para o robô com menos itens sob sua responsabilidade.

## 🚀 Visão Geral do Projeto

Este projeto utiliza **Django REST Framework** para a API, **Celery** para gerenciamento de tarefas assíncronas, **RabbitMQ** como message broker e **PostgreSQL** como banco de dados principal. Além disso, utilizamos **Swagger** para documentação da API e **JWT (JSON Web Token)** para autenticação segura.

## 📌 Recursos Principais

✅ Interface gráfica responsiva e intuitiva para os usuários.
✅ Autenticação e gerenciamento de usuários.
✅ Envio e processamento de tarefas massivas via CSV.
✅ API REST para integração com robôs de automação.
✅ Monitoramento de status dos robôs e atribuição dinâmica de tarefas.
✅ Desconexão automática de robôs inativos.
✅ Utilização de Celery para gerenciamento inteligente das tarefas.
✅ Documentação da API com Swagger.
✅ Autenticação via Simple JWT.
✅ Uso de `entrypoint.sh` para automação do ambiente em produção.

---

## 🔧 Configuração do Ambiente

### 📁 Criar Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto e preencha com os valores adequados:

```ini
SECRET_KEY='chave_secreta'
POSTGRES_DB='nome_do_banco'
POSTGRES_USER='usuario_do_banco'
POSTGRES_PASSWORD='senha_do_banco'
DB_HOST='db'
DB_PORT='5432'
CELERY_BROKER_URL='amqp://guest:guest@rabbitmq:5672//'
DATABASE_URL='postgres://usuario:senha@db:5432/nome_do_banco'
OPENAI_API_KEY='chave_api_openai'
NGROK_AUTHTOKEN='token_ngrok'
PG_ADMIN_EMAIL='admin@email.com'
PG_ADMIN_PASSWORD='senha_admin'
DJANGO_SUPERUSER_USERNAME='admin'
DJANGO_SUPERUSER_EMAIL='admin@email.com'
DJANGO_SUPERUSER_PASSWORD='senha_admin'
```

---

## 🚀 Instalação e Inicialização

### 1️⃣ Clonar o Repositório

```bash
git clone https://github.com/seu_usuario/orquestrador-rpa.git
cd orquestrador-rpa
```

### 2️⃣ Criar Ambiente Virtual e Instalar Dependências

```bash
python3 -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate    # Windows
pip install -r requirements.txt
```

### 3️⃣ Criar e Configurar o Banco de Dados

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4️⃣ Criar Superusuário

```bash
python manage.py createsuperuser
```

### 5️⃣ Executar o Servidor Django

```bash
python manage.py runserver
```

---

## 📜 Documentação da API com Swagger

A documentação da API pode ser acessada através do Swagger na URL:

📌 **http://localhost:8000/docs**

---

## 🔐 Autenticação com Simple JWT

A API utiliza autenticação via **JWT (JSON Web Token)**. Para obter um token de acesso, faça uma requisição `POST`:

```http
POST /api/token/
Content-Type: application/json
{
    "username": "seu_usuario",
    "password": "sua_senha"
}
```

Resposta:
```json
{
    "refresh": "token_refresh",
    "access": "token_access"
}
```

Use o token nos cabeçalhos das requisições autenticadas:

```http
Authorization: Bearer seu_token_access
```

---

## ⚙️ Execução no Docker

O projeto usa **Docker** para facilitar a implantação.

### 1️⃣ Construir e Iniciar os Containers

```bash
docker-compose up --build -d
```

### 2️⃣ Parar os Containers

```bash
docker-compose down
```

### 3️⃣ Visualizar Logs

```bash
docker logs nome_do_container -f
```

---

## 🔄 Uso do Celery e RabbitMQ

O Celery é utilizado para o processamento assíncrono de tarefas. Para iniciar um worker do Celery, execute:

```bash
celery -A orchestrator worker --loglevel=info
```

Para iniciar o **Celery Beat** (agendador de tarefas periódicas):

```bash
celery -A orchestrator beat --loglevel=info
```

---

## 📡 Exposição do Servidor com Ngrok

O **Ngrok** é utilizado para expor o servidor local para acessos externos.

### 1️⃣ Configurar o arquivo `ngrok.yml`

```yaml
version: "3"
agent:
  authtoken: ${NGROK_AUTHTOKEN}

tunnels:
  basic:
    proto: http
    addr: 80
```

### 2️⃣ Iniciar o Ngrok

```bash
docker-compose up ngrok -d
```

---

## 🛠 EntryPoint.sh

O projeto utiliza um **script de entrada (`entrypoint.sh`)** para automação do ambiente. Esse script:

✅ Aguarda o banco de dados ficar pronto antes de iniciar o Django.
✅ Aplica as migrações automaticamente.
✅ Cria o superusuário caso necessário.
✅ Coleta arquivos estáticos.
✅ Inicia o servidor Gunicorn.

Caso precise depurar, verifique os logs:

```bash
docker logs nome_do_container -f
```

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License**.

