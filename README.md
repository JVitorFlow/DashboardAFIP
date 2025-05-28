Veja abaixo uma versão do **README.md** ajustada para usar **exclusivamente o Docker/entrypoint.sh**, sem comandos manuais de `manage.py` e com a URL correta do Swagger:

````markdown
# Orquestrador RPA

O **Orquestrador RPA** é uma plataforma desenvolvida para permitir que usuários enviem e gerenciem tarefas massivas a serem processadas por robôs de automação (RPA). Essa solução resolve o problema da necessidade de realizar tarefas repetitivas e múltiplas em sistemas que não suportam a entrada massiva de solicitações. O sistema também possui um orquestrador que distribui as tarefas de forma inteligente para o robô com menos itens sob sua responsabilidade.

---

## 🚀 Visão Geral do Projeto

Este projeto utiliza **Django REST Framework** para a API, **Celery** para gerenciamento de tarefas assíncronas, **RabbitMQ** como message broker e **PostgreSQL** como banco de dados principal. Além disso, utilizamos **Swagger** para documentação da API e **JWT (JSON Web Token)** para autenticação segura.

---

## 📌 Recursos Principais

- Interface gráfica responsiva e intuitiva.  
- Autenticação e gerenciamento de usuários.  
- Envio e processamento de tarefas massivas via CSV.  
- API REST para integração com robôs de automação.  
- Monitoramento de status dos robôs e atribuição dinâmica de tarefas.  
- Desconexão automática de robôs inativos.  
- Gerenciamento de tarefas assíncronas com Celery + RabbitMQ.  
- Documentação da API com Swagger e Redoc.  
- Autenticação via Simple JWT.  
- Automação completa do ambiente em produção via `entrypoint.sh`.

---

## 🔧 Configuração do Ambiente

Crie um arquivo `.env` na raiz do projeto com as variáveis abaixo:

```ini
SECRET_KEY='sua_chave_secreta'
POSTGRES_DB='nome_do_banco'
POSTGRES_USER='usuario_do_banco'
POSTGRES_PASSWORD='senha_do_banco'
DB_HOST='db'
DB_PORT='5432'
CELERY_BROKER_URL='amqp://guest:guest@rabbitmq:5672//'
DATABASE_URL='postgres://usuario:senha@db:5432/nome_do_banco'
OPENAI_API_KEY='sua_chave_openai'
NGROK_AUTHTOKEN='seu_token_ngrok'
DJANGO_SUPERUSER_USERNAME='admin'
DJANGO_SUPERUSER_EMAIL='admin@dominio.com'
DJANGO_SUPERUSER_PASSWORD='senha_admin'
````

---

## 🚀 Instalação e Inicialização via Docker

1. **Clone o repositório**

   ```bash
   git clone https://github.com/seu_usuario/orquestrador-rpa.git
   cd orquestrador-rpa
   ```

2. **Construa e suba os containers**
   O `entrypoint.sh` já faz:

   * Espera o banco de dados subir
   * Roda `makemigrations` e `migrate`
   * Cria o superusuário se não existir
   * Coleta arquivos estáticos
   * Inicia o Gunicorn

   Basta executar:

   ```bash
   docker-compose up --build -d
   ```

3. **Verifique os logs**

   ```bash
   docker logs -f <nome_do_container_web>
   ```

4. **Acesse a aplicação**

   * Front-end/API:

     ```
     http://localhost:8000/
     ```
   * Swagger UI:

     ```
     http://localhost:8000/swagger/v1/
     ```
   * Redoc:

     ```
     http://localhost:8000/redoc/v1/
     ```

5. **Parando tudo**

   ```bash
   docker-compose down
   ```

---

## 🔐 Autenticação com Simple JWT

Para obter o token de acesso, faça um `POST` em:

```http
POST /api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "senha_admin"
}
```

Resposta:

```json
{
  "refresh": "seu_token_refresh",
  "access":  "seu_token_access"
}
```

Use nos cabeçalhos:

```http
Authorization: Bearer seu_token_access
```

---

## 🛠 EntryPoint.sh

Esse script, rodando dentro do container web, automatiza toda a inicialização do Django:

```sh
#!/bin/sh
# entrypoint.sh

echo "🚀 Aguardando PostgreSQL..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER"; do
  sleep 1
done

echo "💾 Aplicando migrations e criando superusuário..."
python apps/manage.py makemigrations
python apps/manage.py migrate
python apps/manage.py createsuperuser --no-input || true
python apps/manage.py collectstatic --no-input

echo "🔥 Iniciando Gunicorn..."
exec gunicorn orchestrator.wsgi:application --bind 0.0.0.0:8000
```

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License**.

