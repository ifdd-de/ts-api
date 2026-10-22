(ifdd-ts-api-index)=
# {{ cookiecutter.ifdd_ts_api_prj_name }} (ts-api)

The REST interface of the time series of an IFDD node: services read and
write samples in VictoriaMetrics through it, with an access token of the
realm and only in the stores their roles open. This chapter describes the
instance `{{ cookiecutter.ifdd_ts_api_prj_slug }}`, generated from the
template `ifdd-de/ts-api`.

| | |
|---|---|
| Public URL | `{{ cookiecutter.ifdd_ts_api_url }}` (host `{{ cookiecutter.ifdd_ts_host }}`, path `{{ cookiecutter.ifdd_ts_api_path }}`, routed by the proxy) |
| Internal port | `{{ cookiecutter.ifdd_ts_api_port }}` (uvicorn, not published in production) |
| Instance version | `{{ cookiecutter.ifdd_ts_api_version }}` |
| Runtime | package `ifdd-ts-core` `~={{ cookiecutter.ifdd_ts_core_version }}` |
| Time series database | VictoriaMetrics of the ifdd-ts instance, `{{ cookiecutter.ifdd_ts_api_vm_url }}` |
| Realm | `{{ cookiecutter.ifdd_oidc_realm }}`, audience `{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` |

## What the instance contains

The runtime (token and store checks, checks against the vocabularies,
VictoriaMetrics, documentation pages) is the package `ifdd-ts-core`. The
instance adds packaging, the image, the compose files and the configuration
(`.env`). The API has no secret and no database of its own.

## Architecture

```{mermaid}
flowchart LR
  S[services, client credentials] -->|HTTPS| P[proxy: Traefik]
  P -->|"{{ cookiecutter.ifdd_ts_host }}{{ cookiecutter.ifdd_ts_api_path }}"| API[ts-api: uvicorn]
  P -->|"{{ cookiecutter.ifdd_ts_host }}, other paths"| G[Grafana]
  API -->|"{{ cookiecutter.ifdd_ts_ingest_network }}"| VM[(VictoriaMetrics)]
  G --> VM
  API -->|JWKS, vocabularies| P
  P --> KC[Keycloak]
  P --> T[type]
```

The API shares the host of Grafana: the proxy sends the path
`{{ cookiecutter.ifdd_ts_api_path }}` to the API and everything else to
Grafana. It calls Keycloak (signing keys) and the type service (vocabularies)
under their public URLs through the proxy, and VictoriaMetrics directly on
the ingest network.

| Who | Calls the API for |
|---|---|
| ct (plugin `ts-post`) | writing example series |
| own services with the client `ifdd-ts-ingest` or an own client | writing measurements |
| scripts and notebooks (`ifdd-api-script`) | reading |
| people | Swagger UI and ReDoc, with a token got by hand |

## Chapters

```{toctree}
:maxdepth: 2

setup
build-release
operations
security
troubleshooting
reference
api
```

The values of the variables of this instance are listed in the chapter on
the service instances ({ref}`ifdd-instances-ts-api`); the package is
described in {ref}`ifdd-ts-core-index`.
