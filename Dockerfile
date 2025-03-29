FROM python:3.12.1-slim-bullseye

# Отключаем буферизацию Python и запись .pyc файлов
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app


# Устанавливаем системные зависимости (если нужны для вашего проекта)
WORKDIR /app

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev \
    libpq-dev \
    nmap

# Устанавливаем Poetry
RUN pip install --upgrade pip && \
    pip install poetry

# Копируем только файлы зависимостей для кэширования слоя
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости проекта
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

# Копируем весь остальной код
COPY . /app/


CMD ["gunicorn", "app.project.wsgi:application", "--bind", "0.0.0.0:8000"]