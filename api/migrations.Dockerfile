FROM python:3.11.8-slim

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev tini && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    pip install --no-cache-dir poetry==1.8.2 && \
    poetry export -f requirements.txt -o requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

COPY ./alembic /app/alembic
COPY alembic.ini /app/alembic.ini
COPY ./app /app/app

CMD [ "alembic", "upgrade", "head" ]