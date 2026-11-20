FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --upgrade protobuf==4.25.3

COPY . .

EXPOSE 8000
EXPOSE 50051

CMD ["python", "-m", "app.main"]