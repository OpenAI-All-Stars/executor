FROM python:3.11-buster

WORKDIR /app/

ENV POETRY_VIRTUALENVS_CREATE false
RUN pip install poetry

COPY . .

RUN poetry install --no-dev

EXPOSE 8000

CMD ["sh", "-c", "executor server"]
