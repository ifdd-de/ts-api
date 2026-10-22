(ifdd-ts-api-security)=
# Security

## Who may do what

Every request except `/version` and the documentation needs an access token
of the realm `{{ cookiecutter.ifdd_oidc_realm }}` with the audience
`{{ cookiecutter.ifdd_ts_api_oidc_client_id }}`. The API checks signature,
expiry, audience, issuer and that it is an access token, not an ID token.
Callers are services with the client credentials grant; the roles of the
client `{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` are given to service
accounts only, so a person's token has neither the audience nor a role.

| Check | Answer if it fails |
|---|---|
| token | 401 |
| store name | 422 |
| role `{{ cookiecutter.ifdd_ts_api_role_read }}` (read) or `{{ cookiecutter.ifdd_ts_api_role_write }}` (write) | 403 |
| a store pattern of the client matches the store | 403 |

Reading and writing are separate: a writer cannot read, a reader cannot
write. A foreign store answers 403, not 404 (no security by obscurity);
`/stores` leaves out what the caller may not read.

Service accounts set up by the keycloak template:

| Client | Roles here |
|---|---|
| `ifdd-ts-ingest` | write, root `{{ cookiecutter.ifdd_context_root }}` |
| `ifdd-ct` | write, root (example data) |
| `ifdd-api-script` | read, root |

## How stores are kept apart

The API passes `extra_label=ifdd_store=<store>` to VictoriaMetrics on every
read and write: VictoriaMetrics sets the label on every sample written and
filters every read by it. A label `ifdd_store` in a request body cannot
change that.

## What the API does not protect

- **Grafana** reads VictoriaMetrics directly. Everyone with a Grafana login
  sees the series of every store.
- **The ingest network** `{{ cookiecutter.ifdd_ts_ingest_network }}`: every
  container on it can write to and delete in VictoriaMetrics without any
  check. Attach only containers you trust; services that should not get
  that right use the API.

Both are deliberate (decisions of 2026-10-21).

## Documentation pages

`{{ cookiecutter.ifdd_ts_api_path }}/docs`, `/redoc` and `/openapi.json` are
open: they describe the API, they give no access to data. Swagger UI takes a
bearer token under "Authorize" and keeps it in the browser's local storage
of this host; there is no login through the browser.

## Container

Read-only root file system, `/tmp` as tmpfs, all capabilities dropped,
`no-new-privileges`, user `tsapi` (uid 10001). No port is published in
production.

```{note}
Not tested: the hardening with the real image (`python:3.14-slim`).
```

## Token cache

A validated token is kept up to `IFDD_TOKEN_CACHE_TTL` seconds (default 300)
per process; its expiry is checked on every use. A token revoked in Keycloak
is still accepted until it expires, as with every resource server that
checks tokens locally.
