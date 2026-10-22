(ifdd-ts-api-operations)=
# Operations

## Start, stop, logs

```bash
docker compose -f docker-compose-production.yml up -d
docker compose -f docker-compose-production.yml logs -f api
docker compose -f docker-compose-production.yml down
```

The API keeps no state: tokens and vocabularies are cached in memory per
process and are fetched again after a restart. Nothing needs a backup; the
samples are in VictoriaMetrics (ifdd-ts).

## Health

`{{ cookiecutter.ifdd_ts_api_path }}/version` answers without a token; the
image's health check calls it. It shows that the process runs, not that
VictoriaMetrics or the type service can be reached.

## Writing samples

One sample:

```bash
curl -s --cacert certs/ca.crt -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  {{ cookiecutter.ifdd_ts_api_url }}/stores/temperature.ops.example.ifdd.de/samples -d '{
    "name": "temperature",
    "ifdd_id": "https://rest/products/<id>",
    "ifdd_property": "{{ cookiecutter.ifdd_type_url }}/climate.ops.example.ifdd.de/temperature",
    "ifdd_unit": "https://unit/v1/unit/DEG_C",
    "time": "2026-10-22T09:15:00+02:00",
    "value": 21.5}'
```

The store and the IRIs above are examples (the example domain `ops`). A list
goes to `.../samples/batch` as `{"samples": [...]}`, at most
`{{ cookiecutter.ifdd_ts_api_max_items }}` per request. Every sample is
checked against the vocabulary of its property; one bad sample refuses the
whole list.

Writes only append. A sample with the same series and time as a stored one
does not replace it: with the deduplication of ifdd-ts the larger value
stays. To correct a value, there is no way through this API.

## Reading samples

| Request | Answer |
|---|---|
| `GET /stores` | stores the caller may read |
| `GET /stores/{store}/series?ifdd_id=...` | series of a store |
| `GET /stores/{store}/samples?ifdd_id=...&ifdd_property=...[&at=...]` | latest sample at or before `at` |
| `GET /stores/{store}/samples/range?ifdd_id=...&start=...[&end=...]` | raw samples in the range |

All paths are below `{{ cookiecutter.ifdd_ts_api_url }}`; details in
{ref}`ifdd-ts-api-api`.

## Grafana

Grafana reads VictoriaMetrics directly and shows the series of all stores
together; the store is only a label `ifdd_store` there. A diagram can
therefore show values of two stores, e.g. temperature and humidity, side by
side.
