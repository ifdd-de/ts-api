# Changelog

The version scheme follows the other IFDD repositories: `YY.MM.N`.

## [Unreleased]

- CI: GitHub Actions pinned to commit SHAs (version as comment),
  `persist-credentials: false` on every checkout; the same in the workflows of
  the instance.

## [26.11.2] - 2026-11-18

- Instance version 26.11.2; the instance still requires `ifdd-ts-core`
  26.11.1 (`ifdd_ts_core_version`), which has no changes.
- Documentation: `ifdd-ts-core` is on PyPI; `wheels/` is needed only for an
  unreleased build. The template CI comment says why it still installs
  ts-core from its `main` branch.

## [26.11.1] - 2026-11-14

- Documentation: the architecture diagram in `docs/en` and `docs/de` is
  PlantUML instead of Mermaid, so it also renders in PDF builds. The Sphinx
  project of the full documentation needs `sphinxcontrib-plantuml`, Java and
  Graphviz instead of `sphinxcontrib-mermaid`. `tests/docs/get_plantuml.sh`
  downloads the pinned PlantUML jar (1.2026.10) for `tests/check_docs.py`; the
  template CI installs Java and Graphviz.
- `ifdd_ts_api_version` and `ifdd_ts_core_version` 26.11.1.

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
