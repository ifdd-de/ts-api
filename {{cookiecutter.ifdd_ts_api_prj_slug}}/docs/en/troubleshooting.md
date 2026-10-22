(ifdd-ts-api-troubleshooting)=
# Troubleshooting

| Symptom | Cause and remedy |
|---|---|
| 404 from Grafana for `{{ cookiecutter.ifdd_ts_api_path }}/...` | the router of the API is missing: is the container running and on `{{ cookiecutter.ifdd_proxy_network }}`? Traefik's dashboard lists both routers of `{{ cookiecutter.ifdd_ts_host }}` |
| 401 `Invalid token audience` | the token was issued for another client: the calling client needs a role of `{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` (Keycloak adds the audience then) |
| 401 `Unable to verify the token signature` with `CERTIFICATE_VERIFY_FAILED` | the CA of the proxy is not in `certs/`, or the image was not rebuilt after adding it |
| 403 `Role ... required` | the client lacks `{{ cookiecutter.ifdd_ts_api_role_read }}` or `{{ cookiecutter.ifdd_ts_api_role_write }}`; `/whoami` shows its roles |
| 403 `no store pattern of this client matches` | no role with a dot of the client matches the store; `/whoami` shows its patterns |
| 422 `... is not below the type service` | `ifdd_property` must start with `{{ cookiecutter.ifdd_type_url }}/` |
| 422 `defines no property` | the vocabulary of that namespace in the type service lacks the property; it is kept for `IFDD_TS_VOCABULARY_CACHE_TTL` seconds after a change |
| 422 `unit ... is not applicable` | use one of the `qudt:applicableUnit` of the property |
| 422 `has no offset` / `finer than a millisecond` | send ISO 8601 with `Z` or `+hh:mm`, at most three decimals |
| 502 `VictoriaMetrics ...` | VictoriaMetrics is not reachable at `{{ cookiecutter.ifdd_ts_api_vm_url }}`: is the ifdd-ts instance running and on `{{ cookiecutter.ifdd_ts_ingest_network }}`? |
| 502 `vocabulary ...` | the type service is not reachable or answers with an error |
| a value written twice shows the larger one | deduplication of VictoriaMetrics (ifdd-ts); a sample is never replaced |
