#!/bin/sh

echo "🚀 Aguardando o PostgreSQL iniciar..."

# Espera o banco estar pronto antes de continuar
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER"; do
  echo "Aguardando banco de dados..."
  sleep 1
done

echo "Banco de dados está pronto!"

# Rodar migrações automaticamente em produção
echo "Aplicando migrações..."
python apps/manage.py check_and_migrate

# Criar superusuário automaticamente (opcional)
if [ "$CREATE_SUPERUSER" = "true" ]; then
  echo "Criando superusuário..."
  python apps/manage.py create_superuser || true
fi


# Coletar arquivos estáticos para produção
echo "Coletando arquivos estáticos..."
python apps/manage.py collectstatic --noinput

echo "Iniciando o Gunicorn..."
exec "$@"
