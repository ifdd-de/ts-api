# ts-api

Cookiecutter template of the REST interface of the IFDD time series: services
read and write samples in VictoriaMetrics (template `ifdd-de/ts`) through it,
with access tokens of the realm and only in the stores their roles open. The
runtime is the package [`ifdd-ts-core`](https://github.com/ifdd-de/ts-core);
this template is the frame around it: packaging, image, compose files,
configuration and documentation.

## Generate an instance

```bash
cruft create --no-input --config-file .cookiecutter_all.yaml \
  --skip .env --skip certs https://github.com/ifdd-de/ts-api
```

Usually the meta repository does this together with every other instance.
The documentation of the generated instance is in `docs/en` and `docs/de`;
the meaning of every variable is in the instance chapter of the meta
repository.

## Variables

| Variable | Default | Meaning |
|---|---|---|
| `ifdd_ts_api_prj_name`, `ifdd_ts_api_prj_slug` | `IFDD TS API`, derived | name and directory |
| `ifdd_ts_api_version`, `ifdd_ts_core_version` | `26.10.2` | instance version, required ts-core |
| `ifdd_ts_api_path` | `/tsapi` | path prefix on the host of Grafana |
| `ifdd_ts_api_url` | `https://ts.example.org/tsapi` | public URL; must be `https://` + `ifdd_ts_host` + `ifdd_ts_api_path` (checked) |
| `ifdd_ts_api_port`, `ifdd_ts_api_max_workers`, `ifdd_ts_api_log_level` | `8093`, `2`, `info` | uvicorn |
| `ifdd_ts_api_max_items` | `10000` | limit per request |
| `ifdd_ts_api_vm_url` | `http://victoriametrics:8428` | VictoriaMetrics on the ingest network |
| `ifdd_ts_api_oidc_client_id` | `ifdd-ts-api` | audience and client of the roles (shared with keycloak) |
| `ifdd_ts_api_role_read`, `ifdd_ts_api_role_write` | `ifdd_ts_ro`, `ifdd_ts_rw` | roles (shared with keycloak) |
| `ifdd_ts_host`, `ifdd_ts_ingest_network` | | shared with ts |
| `ifdd_proxy_network`, `ifdd_oidc_realm`, `ifdd_type_url`, `ifdd_context_root`, `ifdd_registry_url` | | shared |

The pre-generation hook rejects values that would render but not work.

## Template tests

```bash
cookiecutter --no-input --config-file tests/fixtures/custom.yaml -o /tmp/out .
cd /tmp/out/grid-ts-api && pip install -e '.[dev]' && pytest
python tests/check_image.py /tmp/out/grid-ts-api
python tests/check_docs.py /tmp/out/grid-ts-api --prefix ifdd-ts-api- --external ifdd-ts-core-
```

The CI (`.github/workflows/template-test.yml`) does this for both fixtures,
and `template-update-test.yml` checks `cruft update` from the last tag.

## AI assistance

Parts of this repository, especially tests, test data and documentation,
were developed or improved with the help of large language models. The
maintainer reviewed and approved every change.

## License

BSD-3-Clause, see [LICENSE](LICENSE).
