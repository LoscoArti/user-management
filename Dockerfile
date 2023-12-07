FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry==1.7.0

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . ./

RUN chmod +x ./entrypoint.sh
