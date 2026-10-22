#!/bin/sh
# Entrypoint of the image: uvicorn with WORKERS processes on PORT (both from
# .env). The application serves its own path prefix (IFDD_TS_API_PATH), so
# the proxy passes the path unchanged. POSIX sh.
set -e

exec uvicorn app.main:app \
    --host "${HOST:-0.0.0.0}" \
    --port "${PORT:-{{ cookiecutter.ifdd_ts_api_port }}}" \
    --workers "${WORKERS:-{{ cookiecutter.ifdd_ts_api_max_workers }}}" \
    --proxy-headers --forwarded-allow-ips "*" \
    --no-server-header
