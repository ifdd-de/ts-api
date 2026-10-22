(ifdd-ts-api-api)=
# API

Die API dokumentiert sich selbst:

| Seite | URL |
|---|---|
| Swagger UI | `{{ cookiecutter.ifdd_ts_api_url }}/docs` |
| ReDoc | `{{ cookiecutter.ifdd_ts_api_url }}/redoc` |
| OpenAPI-Dokument | `{{ cookiecutter.ifdd_ts_api_url }}/openapi.json` |

Dasselbe Dokument als Seite dieser Doku steht in
{ref}`ifdd-ts-core-api-http`.

## Endpunkte

| Methode und Pfad | Rolle | Zweck |
|---|---|---|
| `GET /version` | keine | Version |
| `GET /whoami` | gültiges Token | Rollen und Store-Muster aus dem Token |
| `GET /stores` | lesen | Stores, die der Aufrufer lesen darf |
| `GET /stores/{store}/series` | lesen + Muster | Reihen eines Stores |
| `GET /stores/{store}/samples` | lesen + Muster | letztes Sample zu oder vor `at` |
| `GET /stores/{store}/samples/range` | lesen + Muster | Rohwerte in `[start, end]` |
| `POST /stores/{store}/samples` | schreiben + Muster | ein Sample schreiben |
| `POST /stores/{store}/samples/batch` | schreiben + Muster | eine Liste schreiben |

Es gibt kein PUT und kein DELETE.

## Swagger UI

1. Ein Token mit den Client Credentials eines Service-Accounts holen (siehe
   {ref}`ifdd-ts-api-setup`).
2. `{{ cookiecutter.ifdd_ts_api_url }}/docs` öffnen, „Authorize“ klicken und
   das Token einfügen (ohne `Bearer`).
3. „Try it out“ schickt die Anfragen damit.

Das Token gilt so lange, wie der Realm es vorgibt (im IFDD-Realm 30 Minuten);
Swagger UI behält es über ein Neuladen hinweg.

## Reihenvertrag

Ein Sample benennt seine Reihe mit `name`, `ifdd_id`, `ifdd_property` und
`ifdd_unit` (volle IRIs); der Store ist der Pfad. Das ist der Reihenvertrag
von ifdd-ts plus das Label `ifdd_store`, das die API setzt.
