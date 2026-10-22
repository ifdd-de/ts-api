(ifdd-ts-api-setup)=
# Setup

## Prerequisites

| What | Why |
|---|---|
| Docker with Compose | the API runs as one container |
| the external networks `{{ cookiecutter.ifdd_proxy_network }}` and `{{ cookiecutter.ifdd_ts_ingest_network }}` | proxy route and calls through the proxy; VictoriaMetrics |
| a running ifdd-ts instance whose VictoriaMetrics is on `{{ cookiecutter.ifdd_ts_ingest_network }}` | the API stores nothing itself |
| the proxy lists `{{ cookiecutter.ifdd_ts_host }}`, the Keycloak host and the type host in `ifdd_proxy_internal_hosts` | inside the container these names must lead to Traefik |
| a Keycloak realm `{{ cookiecutter.ifdd_oidc_realm }}` with the client `{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` and its roles | the roles and store patterns of the callers |
| a type instance below `{{ cookiecutter.ifdd_type_url }}` | the vocabularies every sample is checked against |
| the ts-core wheel in `wheels/` while `ifdd-ts-core` is not on PyPI | the image installs it from there |
| the CA certificate of the proxy in `certs/` | the image must trust the proxy's certificate |

## Create the instance

Usually the meta repository creates every instance in one go
(`.adm_01_create_services.sh`): `cruft create` with `.cookiecutter_all.yaml`,
the ts-core wheel into `wheels/` and the CA of the proxy into `certs/`. By
hand:

```bash
cruft create --no-input --config-file .cookiecutter_all.yaml \
  --skip .env --skip certs https://github.com/ifdd-de/ts-api
cp <ts-core>/dist/ifdd_ts_core-*.whl {{ cookiecutter.ifdd_ts_api_prj_slug }}/wheels/
cp proxy/certs/ca.crt {{ cookiecutter.ifdd_ts_api_prj_slug }}/certs/
```

Build the wheel from the current source of ts-core and remove older wheels
of the same version first: pip takes any wheel with a matching version.

## Configuration

The post-generation hook writes `.env` from `dotenv.dist` (mode 0600). There
are no secrets in it. `.env` is not overwritten by a later `cruft update`;
new entries of `dotenv.dist` have to be added by hand. The meaning of every
entry is in {ref}`ifdd-ts-api-reference`.

## Realm

The client `{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` carries the roles
and is the audience the API requires. It has no login of its own. Its
client roles:

| Role | Meaning |
|---|---|
| `{{ cookiecutter.ifdd_ts_api_role_read }}` | read |
| `{{ cookiecutter.ifdd_ts_api_role_write }}` | write |
| a name with a dot, e.g. `{{ cookiecutter.ifdd_context_root }}` | store pattern: opens the store of that name and every store below |

The keycloak template creates the client, the roles and the root pattern
`{{ cookiecutter.ifdd_context_root }}`, and gives them to service accounts
(see {ref}`ifdd-ts-api-security`). A further pattern, e.g. for one store
only, is created in the admin console: Clients →
`{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` → Roles → Create role, then
Clients → the calling client → Service account roles → Assign role.

```{note}
Not tested: the console steps for a further pattern. The same steps through
the admin REST API were tested against Keycloak 26.8.0.
```

## Start and check

```bash
docker compose -f docker-compose-production.yml up -d --build
curl --cacert certs/ca.crt {{ cookiecutter.ifdd_ts_api_url }}/version
```

With a token of a service account (here `ifdd-ts-ingest`, secret from
`keycloak/.env`):

```bash
TOKEN=$(curl -s --cacert certs/ca.crt -d grant_type=client_credentials \
  -u "ifdd-ts-ingest:$SECRET" \
  {{ cookiecutter.ifdd_oidc_realm }}/protocol/openid-connect/token | jq -r .access_token)
curl -s --cacert certs/ca.crt -H "Authorization: Bearer $TOKEN" {{ cookiecutter.ifdd_ts_api_url }}/whoami
```

`/whoami` shows the roles and store patterns the API reads from the token.

## Development

`docker-compose-development.yml` starts the same image without token checks
on `127.0.0.1:{{ cookiecutter.ifdd_ts_api_port }}`. The ifdd-ts instance must
run (its VictoriaMetrics joins `{{ cookiecutter.ifdd_ts_ingest_network }}` in
both modes). The type service is still reached through the proxy.
