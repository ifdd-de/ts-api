(ifdd-ts-api-troubleshooting)=
# Fehlersuche

| Symptom | Ursache und Abhilfe |
|---|---|
| 404 von Grafana für `{{ cookiecutter.ifdd_ts_api_path }}/...` | der Router der API fehlt: Läuft der Container und hängt er in `{{ cookiecutter.ifdd_proxy_network }}`? Das Traefik-Dashboard zeigt beide Router von `{{ cookiecutter.ifdd_ts_host }}` |
| 401 `Invalid token audience` | das Token gilt einem anderen Client: Der aufrufende Client braucht eine Rolle von `{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` (dann setzt Keycloak die Audience) |
| 401 `Unable to verify the token signature` mit `CERTIFICATE_VERIFY_FAILED` | die CA des Proxys fehlt in `certs/`, oder das Image wurde danach nicht neu gebaut |
| 403 `Role ... required` | dem Client fehlt `{{ cookiecutter.ifdd_ts_api_role_read }}` oder `{{ cookiecutter.ifdd_ts_api_role_write }}`; `/whoami` zeigt seine Rollen |
| 403 `no store pattern of this client matches` | keine Rolle mit Punkt des Clients passt auf den Store; `/whoami` zeigt seine Muster |
| 422 `... is not below the type service` | `ifdd_property` muss mit `{{ cookiecutter.ifdd_type_url }}/` beginnen |
| 422 `defines no property` | dem Vokabular dieses Namensraums im type-Dienst fehlt die Eigenschaft; nach einer Änderung gilt es noch `IFDD_TS_VOCABULARY_CACHE_TTL` Sekunden |
| 422 `unit ... is not applicable` | eine der `qudt:applicableUnit` der Eigenschaft verwenden |
| 422 `has no offset` / `finer than a millisecond` | ISO 8601 mit `Z` oder `+hh:mm` senden, höchstens drei Nachkommastellen |
| 502 `VictoriaMetrics ...` | VictoriaMetrics ist unter `{{ cookiecutter.ifdd_ts_api_vm_url }}` nicht erreichbar: Läuft die ifdd-ts-Instanz und hängt sie in `{{ cookiecutter.ifdd_ts_ingest_network }}`? |
| 502 `vocabulary ...` | der type-Dienst ist nicht erreichbar oder antwortet mit einem Fehler |
| ein zweimal geschriebener Wert zeigt den größeren | Deduplizierung von VictoriaMetrics (ifdd-ts); ein Sample wird nie ersetzt |
