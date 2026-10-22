# {{ cookiecutter.ifdd_ts_api_prj_name }}

The REST interface of the time series of an IFDD node, generated from the
template `ifdd-de/ts-api`. The runtime is the package `ifdd-ts-core`; this
repository holds the frame: packaging, image, compose files and
configuration (`.env`).

## Quick start

```bash
cp <ts-core>/dist/ifdd_ts_core-*.whl wheels/   # while ifdd-ts-core is not on PyPI
cp <proxy instance>/certs/ca.crt certs/         # trust the proxy's certificate
docker compose -f docker-compose-production.yml up -d --build
curl --cacert certs/ca.crt {{ cookiecutter.ifdd_ts_api_url }}/version
```

The API is documented at `{{ cookiecutter.ifdd_ts_api_url }}/docs` (Swagger
UI) and `{{ cookiecutter.ifdd_ts_api_url }}/redoc`. Callers need an access
token of the client credentials grant with a role of the client
`{{ cookiecutter.ifdd_ts_api_oidc_client_id }}`.

## Documentation

Setup, build and release, operations, security, troubleshooting, reference
and API of this instance:

- English: [docs/en/index.md](docs/en/index.md)
- Deutsch: [docs/de/index.md](docs/de/index.md)

## AI assistance

Parts of this repository, especially tests, test data and documentation,
were developed or improved with the help of large language models. The
maintainer reviewed and approved every change.

## License

BSD-3-Clause, see [LICENSE](LICENSE).
