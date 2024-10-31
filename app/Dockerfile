# Usar uma imagem oficial do Python
FROM python:3.10-slim as builder

# Configurações de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Criar o diretório de trabalho no contêiner
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências do Python
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar o código da aplicação para a imagem de build
COPY /app/ /app/

# Usar a imagem de build como base
FROM builder as deploy

# Configurações de ambiente
ENV DJANGO_SETTINGS_MODULE=core.settings

# Executar migrações, testes e coleta de arquivos estáticos
WORKDIR /app

# Executar migrações, testes e coleta de arquivos estáticos antes de iniciar o servidor
CMD sh -c "python manage.py migrate && python manage.py test && python manage.py collectstatic --noinput && gunicorn --workers=3 --bind=0.0.0.0:8000 core.wsgi:application"
