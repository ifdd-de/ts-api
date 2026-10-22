(ifdd-ts-api-reference)=
# Referenz

Die Template-Variablen dieser Instanz mit Werten und Bedeutung stehen in
{ref}`ifdd-instances-ts-api`. Diese Seite nennt, was keine Template-Variable
ist.

## Umgebung (`.env`)

| Name | Hier | Bedeutung |
|---|---|---|
| `API_TITLE` | `{{ cookiecutter.ifdd_ts_api_prj_name }}` | Titel des OpenAPI-Dokuments und der Seiten |
| `LOG_LEVEL` | `{{ cookiecutter.ifdd_ts_api_log_level.upper() }}` | Log-Level |
| `WORKERS` | `{{ cookiecutter.ifdd_ts_api_max_workers }}` | uvicorn-Prozesse |
| `PORT` | `{{ cookiecutter.ifdd_ts_api_port }}` | interner Port |
| `IFDD_TS_API_VERSION` | `{{ cookiecutter.ifdd_ts_api_version }}` | von `/version` angezeigt |
| `IFDD_TS_API_PATH` | `{{ cookiecutter.ifdd_ts_api_path }}` | Pfadpräfix aller Endpunkte |
| `IFDD_TS_API_URL` | `{{ cookiecutter.ifdd_ts_api_url }}` | öffentliche URL, für Menschen und Skripte |
| `IFDD_TS_API_AUTH_ENABLED` | `true` | `false` nur in der Entwicklung |
| `IFDD_OIDC_ISSUER` | `{{ cookiecutter.ifdd_oidc_realm }}` | verlangter Aussteller |
| `IFDD_OIDC_JWKS_URL` | Realm + `/protocol/openid-connect/certs` | Signaturschlüssel |
| `IFDD_OIDC_TOKEN_URL` | Realm + `/protocol/openid-connect/token` | in der API-Beschreibung genannt |
| `IFDD_OIDC_JWKS_AUDIENCE` | `{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` | verlangte Audience, Client der Rollen |
| `IFDD_TS_ROLE_READ`, `IFDD_TS_ROLE_WRITE` | `{{ cookiecutter.ifdd_ts_api_role_read }}`, `{{ cookiecutter.ifdd_ts_api_role_write }}` | Rollen |
| `IFDD_CONTEXT_ROOT` | `{{ cookiecutter.ifdd_context_root }}` | Store-Muster des Entwicklungsbenutzers |
| `IFDD_TS_VM_URL` | `{{ cookiecutter.ifdd_ts_api_vm_url }}` | VictoriaMetrics |
| `IFDD_TYPE_URL` | `{{ cookiecutter.ifdd_type_url }}` | type-Dienst |
| `IFDD_TS_MAX_ITEMS` | `{{ cookiecutter.ifdd_ts_api_max_items }}` | Obergrenze je Anfrage |

Weitere Einstellungen von `ifdd-ts-core` mit ihren Standardwerten
(Cache-Zeiten, Timeouts, Standard-Zeiträume) nennt dessen README; bei Bedarf
in `.env` setzen.

## Dateien

| Pfad | Inhalt | `cruft update` |
|---|---|---|
| `.env` | Konfiguration | übersprungen |
| `certs/` | CAs für das Image | übersprungen |
| `app/settings.py` | eigene Einstellungen | übersprungen |
| `wheels/` | ts-core-Wheel, solange nicht auf PyPI | – |
| `docs/` | diese Doku | aktualisiert |

## Container

| | |
|---|---|
| Dienst | `api` |
| Netze | `{{ cookiecutter.ifdd_proxy_network }}`, `{{ cookiecutter.ifdd_ts_ingest_network }}` |
| Router | ``Host(`{{ cookiecutter.ifdd_ts_host }}`) && PathPrefix(`{{ cookiecutter.ifdd_ts_api_path }}`)``, Middlewares `security-headers`, `csp-api-docs` |
| Healthcheck | `http://127.0.0.1:<PORT>{{ cookiecutter.ifdd_ts_api_path }}/version` |
