(ifdd-ts-api-reference)=
# Reference

The template variables of this instance, with their values and meaning, are
in {ref}`ifdd-instances-ts-api`. This page lists what is not a template
variable.

## Environment (`.env`)

| Name | Here | Meaning |
|---|---|---|
| `API_TITLE` | `{{ cookiecutter.ifdd_ts_api_prj_name }}` | title of the OpenAPI document and the pages |
| `LOG_LEVEL` | `{{ cookiecutter.ifdd_ts_api_log_level.upper() }}` | log level |
| `WORKERS` | `{{ cookiecutter.ifdd_ts_api_max_workers }}` | uvicorn processes |
| `PORT` | `{{ cookiecutter.ifdd_ts_api_port }}` | internal port |
| `IFDD_TS_API_VERSION` | `{{ cookiecutter.ifdd_ts_api_version }}` | shown by `/version` |
| `IFDD_TS_API_PATH` | `{{ cookiecutter.ifdd_ts_api_path }}` | path prefix of every endpoint |
| `IFDD_TS_API_URL` | `{{ cookiecutter.ifdd_ts_api_url }}` | public URL, for people and scripts |
| `IFDD_TS_API_AUTH_ENABLED` | `true` | `false` only in development |
| `IFDD_OIDC_ISSUER` | `{{ cookiecutter.ifdd_oidc_realm }}` | required issuer |
| `IFDD_OIDC_JWKS_URL` | realm + `/protocol/openid-connect/certs` | signing keys |
| `IFDD_OIDC_TOKEN_URL` | realm + `/protocol/openid-connect/token` | shown in the API description |
| `IFDD_OIDC_JWKS_AUDIENCE` | `{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` | required audience, client of the roles |
| `IFDD_TS_ROLE_READ`, `IFDD_TS_ROLE_WRITE` | `{{ cookiecutter.ifdd_ts_api_role_read }}`, `{{ cookiecutter.ifdd_ts_api_role_write }}` | roles |
| `IFDD_CONTEXT_ROOT` | `{{ cookiecutter.ifdd_context_root }}` | store pattern of the development user |
| `IFDD_TS_VM_URL` | `{{ cookiecutter.ifdd_ts_api_vm_url }}` | VictoriaMetrics |
| `IFDD_TYPE_URL` | `{{ cookiecutter.ifdd_type_url }}` | type service |
| `IFDD_TS_MAX_ITEMS` | `{{ cookiecutter.ifdd_ts_api_max_items }}` | limit per request |

Further settings of `ifdd-ts-core` with their defaults (cache times,
timeouts, default time ranges) are listed in its README; set them in `.env`
when needed.

## Files

| Path | Content | `cruft update` |
|---|---|---|
| `.env` | configuration | skipped |
| `certs/` | CAs for the image | skipped |
| `app/settings.py` | own settings | skipped |
| `wheels/` | ts-core wheel while not on PyPI | – |
| `docs/` | this documentation | updated |

## Container

| | |
|---|---|
| Service | `api` |
| Networks | `{{ cookiecutter.ifdd_proxy_network }}`, `{{ cookiecutter.ifdd_ts_ingest_network }}` |
| Router | ``Host(`{{ cookiecutter.ifdd_ts_host }}`) && PathPrefix(`{{ cookiecutter.ifdd_ts_api_path }}`)``, middlewares `security-headers`, `csp-api-docs` |
| Health check | `http://127.0.0.1:<PORT>{{ cookiecutter.ifdd_ts_api_path }}/version` |
