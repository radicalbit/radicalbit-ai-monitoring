FROM python:3.11.15-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev python3-dev git && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY poetry.lock pyproject.toml ./

RUN pip install --no-cache-dir --no-compile poetry==1.8.2 && \
    poetry export --without-hashes --with main -f requirements.txt -o requirements.txt && \
    pip install --no-cache-dir --no-compile -r requirements.txt && \
    pip uninstall -y poetry setuptools wheel pip && \
    rm -f requirements.txt poetry.lock pyproject.toml && \
    rm -rf /root/.cache

FROM python:3.11.15-slim

ENV HTTP_INTERFACE=0.0.0.0
ENV HTTP_PORT=9000
ENV LOG_LEVEL=debug
ENV PYTHONUNBUFFERED=1

EXPOSE 9000

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends tini libpq5 && \
    apt-get install -y --only-upgrade libcap2 libsystemd0 libudev1 && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN rm -rf /usr/local/lib/python3.11/site-packages/*
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

COPY ./app ./app
COPY ./entrypoint.sh .

RUN chmod +x ./entrypoint.sh && chown -R appuser:appuser /app

USER appuser

ENTRYPOINT ["tini", "-v", "--", "./entrypoint.sh"]
