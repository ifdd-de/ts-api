# Changelog

The version scheme follows the other IFDD repositories: `YY.MM.N`.

## [Unreleased]

First version (26.10.2).

- Template of the time series API on `ifdd-ts-core`: image `python:3.14-slim`
  as user `tsapi`, read-only container, route `Host && PathPrefix` on the host
  of Grafana with the proxy's security headers, networks of the proxy and of
  ingest.
- `.env` without secrets; pre-generation hook checks path, URL, roles (no
  dot), networks and realm.
- Documentation `docs/en`, `docs/de`.
