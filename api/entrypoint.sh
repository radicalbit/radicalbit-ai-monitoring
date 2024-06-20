#!/bin/sh
exec uvicorn --host="$HTTP_INTERFACE" --port "$HTTP_PORT" --log-level "$LOG_LEVEL" app.main:app