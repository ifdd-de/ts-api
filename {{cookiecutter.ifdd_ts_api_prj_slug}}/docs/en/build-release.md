(ifdd-ts-api-build-release)=
# Build and release

## Image

```bash
docker compose -f docker-compose-production.yml build
```

The image is `{{ cookiecutter.ifdd_registry_url }}/{{ cookiecutter.ifdd_ts_api_prj_slug }}:{{ cookiecutter.ifdd_ts_api_version }}`,
based on `python:3.14-slim`. It installs the instance with `ifdd-ts-core`
from `wheels/` (or PyPI), adds the CAs of `certs/` to the system trust store
and runs as user `tsapi` (uid 10001).

## Versions

| Value | Where |
|---|---|
| instance `{{ cookiecutter.ifdd_ts_api_version }}` | `pyproject.toml`, image tag, `IFDD_TS_API_VERSION` in `.env` |
| ts-core `~={{ cookiecutter.ifdd_ts_core_version }}` | `pyproject.toml` |

The scheme is `YY.MM.N`. A new ts-core in the same image needs a rebuild of
the image with the new wheel.

## Release

`.github/workflows/release.yml` builds the image and pushes it to ghcr.io
when a tag `v*` is pushed. Until `ifdd-ts-core` is on PyPI, that build only
works with the wheel in `wheels/`.

```{note}
Not tested: the image build and the release workflow (no container registry
was reachable when the template was written).
```
