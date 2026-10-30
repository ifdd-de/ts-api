# Changelog

The version scheme follows the other IFDD repositories: `YY.MM.N`.

## [26.10.3] - 2026-10-30

- `ifdd_ts_api_version` and `ifdd_ts_core_version` 26.10.3: ifdd-ts-core
  26.10.3 with FastAPI 0.162.0. The instance needs that release on PyPI or
  its wheel in `wheels/`.
- Documentation check: Sphinx 9.2.0 (`tests/docs/requirements.txt`).
- Upgrade: `cruft update`, then rebuild the image and recreate the container.

## [26.10.2] - 2026-10-22

First version.

- Template of the time series API on `ifdd-ts-core`: image `python:3.14-slim`
  as user `tsapi`, read-only container, route `Host && PathPrefix` on the host
  of Grafana with the proxy's security headers, networks of the proxy and of
  ingest.
- `.env` without secrets; pre-generation hook checks path, URL, roles (no
  dot), networks and realm.
- Documentation `docs/en`, `docs/de`.
