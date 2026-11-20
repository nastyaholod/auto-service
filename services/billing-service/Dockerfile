FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Запускаем и API, и потребитель сообщений в одном контейнере (для простоты)
# В реальном проекте это могут быть разные процессы
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & python -m app.infrastructure.rmq.consumer"]