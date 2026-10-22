(ifdd-ts-api-api)=
# API

The API is documented by itself:

| Page | URL |
|---|---|
| Swagger UI | `{{ cookiecutter.ifdd_ts_api_url }}/docs` |
| ReDoc | `{{ cookiecutter.ifdd_ts_api_url }}/redoc` |
| OpenAPI document | `{{ cookiecutter.ifdd_ts_api_url }}/openapi.json` |

The same document as a page of this documentation is in
{ref}`ifdd-ts-core-api-http`.

## Endpoints

| Method and path | Role | Purpose |
|---|---|---|
| `GET /version` | none | version |
| `GET /whoami` | valid token | roles and store patterns from the token |
| `GET /stores` | read | stores the caller may read |
| `GET /stores/{store}/series` | read + pattern | series of a store |
| `GET /stores/{store}/samples` | read + pattern | latest sample at or before `at` |
| `GET /stores/{store}/samples/range` | read + pattern | raw samples in `[start, end]` |
| `POST /stores/{store}/samples` | write + pattern | write one sample |
| `POST /stores/{store}/samples/batch` | write + pattern | write a list |

There is no PUT and no DELETE.

## Swagger UI

1. Get a token with the client credentials of a service account (see
   {ref}`ifdd-ts-api-setup`).
2. Open `{{ cookiecutter.ifdd_ts_api_url }}/docs`, click "Authorize" and
   paste the token (without `Bearer`).
3. "Try it out" sends the requests with it.

The token lasts as long as the realm says (30 minutes in the IFDD realm);
Swagger UI keeps it across reloads.

## Series contract

A sample names its series with `name`, `ifdd_id`, `ifdd_property` and
`ifdd_unit` (full IRIs); the store is the path. This is the series contract
of ifdd-ts plus the label `ifdd_store`, which the API sets.
