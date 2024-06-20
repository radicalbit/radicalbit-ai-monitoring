FROM python:3.11.8-slim AS build

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN pip install --no-cache-dir poetry==1.8.2 && \
    poetry export -f requirements.txt -o requirements.txt

FROM python:3.11.8-slim

ENV HTTP_INTERFACE=0.0.0.0
ENV HTTP_PORT=9000
ENV LOG_LEVEL=debug
ENV PYTHONUNBUFFERED 1

EXPOSE 9000

WORKDIR /app

COPY --from=build /app/requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev tini curl && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["tini", "-v", "--", "./entrypoint.sh"]