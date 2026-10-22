# Image of the time series API: python:3.14-slim with ifdd-ts-core.
FROM python:3.14-slim

ENV PIP_ROOT_USER_ACTION=ignore \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Local wheels, e.g. a build of ifdd-ts-core that is not published yet. The
# directory is normally empty, in which case pip falls back to the index.
COPY wheels /tmp/wheels
COPY pyproject.toml /app/pyproject.toml
COPY ./app /app/app
COPY start.sh /app/start.sh

WORKDIR /app
RUN pip install --no-cache-dir --find-links /tmp/wheels . \
    && rm -rf /tmp/wheels

# Additional CA certificates from certs/ (*.crt, *.pem), e.g. the CA of the
# proxy, so that the API can reach Keycloak and the type service under their
# public https URLs. Without files there the trust store stays as it is.
COPY certs/ /tmp/ifdd-certs/
RUN set -eu; \
    mkdir -p /usr/local/share/ca-certificates; \
    for f in /tmp/ifdd-certs/*.crt /tmp/ifdd-certs/*.pem; do \
        [ -f "$f" ] || continue; \
        name=$(basename "$f"); \
        cp "$f" "/usr/local/share/ca-certificates/ifdd-${name%.*}.crt"; \
    done; \
    rm -rf /tmp/ifdd-certs; \
    update-ca-certificates

# ifdd-ts-core checks certificates against the system trust store (Python's
# ssl module, for the JWKS and for the type service).
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

# Run as the unprivileged user "tsapi" (uid/gid 10001), not as root. The code
# stays owned by root and is only readable for it; the API writes no files.
RUN groupadd --system --gid 10001 tsapi \
    && useradd --system --uid 10001 --gid tsapi --no-create-home \
       --home-dir /nonexistent --shell /usr/sbin/nologin tsapi \
    && chmod -R a+rX /app \
    && chmod a+rx /app/start.sh
USER tsapi

# Liveness probe without curl (not in this image). PORT and IFDD_TS_API_PATH
# come from .env.
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c "import os,sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:' + os.environ.get('PORT', '{{ cookiecutter.ifdd_ts_api_port }}') + os.environ.get('IFDD_TS_API_PATH', '{{ cookiecutter.ifdd_ts_api_path }}') + '/version', timeout=5).status == 200 else 1)"

CMD ["/app/start.sh"]
