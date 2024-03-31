# temp stage
FROM python:3.10-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN apt-get update && apt-get autoremove --purge -y && apt-get -y clean && rm -rf /var/lib/apt/lists/*

# Preparando o ambiente
COPY requirements.txt /app
# Instale as dependências do aplicativo
RUN python -m pip install --upgrade pip
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# final stage
FROM python:3.10-slim
EXPOSE 8000
WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt /app

# RUN pip install --no-cache /wheels/*
COPY src /app/src/

# Crie um usuário não privilegiado e o define para a app
RUN useradd -ms /bin/bash appuser && chown appuser /app/src
USER appuser

# Comando para executar a aplicação com o Uvicorn
CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--forwarded-allow-ips", "*" ]
