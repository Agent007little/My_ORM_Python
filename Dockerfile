# Используем базовый образ Python
FROM python:3.10

WORKDIR /app

# Копируем исходный код приложения
COPY . /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python", "main.py"]