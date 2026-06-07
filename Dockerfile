FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Устанавливаем pytest для тестов
RUN pip install --no-cache-dir pytest

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]