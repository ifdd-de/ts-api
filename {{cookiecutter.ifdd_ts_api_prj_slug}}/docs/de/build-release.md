(ifdd-ts-api-build-release)=
# Bauen und Freigeben

## Image

```bash
docker compose -f docker-compose-production.yml build
```

Das Image heißt `{{ cookiecutter.ifdd_registry_url }}/{{ cookiecutter.ifdd_ts_api_prj_slug }}:{{ cookiecutter.ifdd_ts_api_version }}`
und beruht auf `python:3.14-slim`. Es installiert die Instanz mit
`ifdd-ts-core` aus `wheels/` (oder von PyPI), übernimmt die CAs aus `certs/`
in den System-Speicher und läuft als Benutzer `tsapi` (uid 10001).

## Versionen

| Wert | Wo |
|---|---|
| Instanz `{{ cookiecutter.ifdd_ts_api_version }}` | `pyproject.toml`, Image-Tag, `IFDD_TS_API_VERSION` in `.env` |
| ts-core `~={{ cookiecutter.ifdd_ts_core_version }}` | `pyproject.toml` |

Das Schema ist `JJ.MM.N`. Ein neues ts-core im selben Image verlangt einen
Neubau des Images mit dem neuen Wheel.

## Freigabe

`.github/workflows/release.yml` baut das Image beim Push eines Tags `v*` und
schiebt es nach ghcr.io. Solange `ifdd-ts-core` nicht auf PyPI ist, gelingt
dieser Bau nur mit dem Wheel in `wheels/`.

```{note}
Nicht getestet: der Image-Bau und der Release-Workflow (beim Schreiben des
Templates war keine Container-Registry erreichbar).
```
