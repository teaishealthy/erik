FROM python:3.8-slim-buster

WORKDIR /app

# Install poetry
RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --only main

COPY . .

CMD ["poetry", "run", "python", "erik.py"]