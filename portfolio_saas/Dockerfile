# Usar uma imagem oficial do Python
FROM python:3.10-slim

# Configurações de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependências do Python
COPY requirements.txt /app/

# Criar o diretório de trabalho no contêiner
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar o código da aplicação
COPY /app/ /app/

# Executar o servidor Django
CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8000", "core.wsgi:application"]

