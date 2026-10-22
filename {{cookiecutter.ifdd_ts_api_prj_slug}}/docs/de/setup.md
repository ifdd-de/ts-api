(ifdd-ts-api-setup)=
# Einrichtung

## Voraussetzungen

| Was | Warum |
|---|---|
| Docker mit Compose | die API läuft als ein Container |
| die externen Netze `{{ cookiecutter.ifdd_proxy_network }}` und `{{ cookiecutter.ifdd_ts_ingest_network }}` | Route des Proxys und Aufrufe über den Proxy; VictoriaMetrics |
| eine laufende ifdd-ts-Instanz, deren VictoriaMetrics in `{{ cookiecutter.ifdd_ts_ingest_network }}` hängt | die API speichert selbst nichts |
| der Proxy führt `{{ cookiecutter.ifdd_ts_host }}`, den Keycloak-Host und den type-Host in `ifdd_proxy_internal_hosts` | im Container müssen diese Namen zu Traefik führen |
| ein Keycloak-Realm `{{ cookiecutter.ifdd_oidc_realm }}` mit dem Client `{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` und seinen Rollen | Rollen und Store-Muster der Aufrufer |
| eine type-Instanz unter `{{ cookiecutter.ifdd_type_url }}` | die Vokabulare, gegen die jedes Sample geprüft wird |
| das ts-core-Wheel in `wheels/`, solange `ifdd-ts-core` nicht auf PyPI ist | das Image installiert es von dort |
| das CA-Zertifikat des Proxys in `certs/` | das Image muss dem Zertifikat des Proxys vertrauen |

## Instanz anlegen

Meist legt das Meta-Repo alle Instanzen in einem Zug an
(`.adm_01_create_services.sh`): `cruft create` mit `.cookiecutter_all.yaml`,
das ts-core-Wheel nach `wheels/` und die CA des Proxys nach `certs/`. Von
Hand:

```bash
cruft create --no-input --config-file .cookiecutter_all.yaml \
  --skip .env --skip certs https://github.com/ifdd-de/ts-api
cp <ts-core>/dist/ifdd_ts_core-*.whl {{ cookiecutter.ifdd_ts_api_prj_slug }}/wheels/
cp proxy/certs/ca.crt {{ cookiecutter.ifdd_ts_api_prj_slug }}/certs/
```

Das Wheel aus dem aktuellen Quelltext von ts-core bauen und ältere Wheels
gleicher Version vorher entfernen: pip nimmt jedes Wheel mit passender
Version.

## Konfiguration

Der Post-Hook schreibt `.env` aus `dotenv.dist` (Modus 0600). Secrets stehen
darin nicht. Ein späteres `cruft update` überschreibt `.env` nicht; neue
Einträge aus `dotenv.dist` sind von Hand nachzutragen. Die Bedeutung jedes
Eintrags steht in {ref}`ifdd-ts-api-reference`.

## Realm

Der Client `{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` trägt die Rollen
und ist die Audience, die die API verlangt. Er hat keine eigene Anmeldung.
Seine Client-Rollen:

| Rolle | Bedeutung |
|---|---|
| `{{ cookiecutter.ifdd_ts_api_role_read }}` | lesen |
| `{{ cookiecutter.ifdd_ts_api_role_write }}` | schreiben |
| ein Name mit Punkt, z. B. `{{ cookiecutter.ifdd_context_root }}` | Store-Muster: öffnet den gleichnamigen Store und alle darunter |

Das keycloak-Template legt den Client, die Rollen und das Wurzelmuster
`{{ cookiecutter.ifdd_context_root }}` an und gibt sie Service-Accounts
(siehe {ref}`ifdd-ts-api-security`). Ein weiteres Muster, etwa für nur einen
Store, entsteht in der Admin-Konsole: Clients →
`{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` → Roles → Create role, dann
Clients → aufrufender Client → Service account roles → Assign role.

```{note}
Nicht getestet: die Konsolenschritte für ein weiteres Muster. Dieselben
Schritte über die Admin-REST-API wurden gegen Keycloak 26.8.0 getestet.
```

## Starten und prüfen

```bash
docker compose -f docker-compose-production.yml up -d --build
curl --cacert certs/ca.crt {{ cookiecutter.ifdd_ts_api_url }}/version
```

Mit einem Token eines Service-Accounts (hier `ifdd-ts-ingest`, Secret aus
`keycloak/.env`):

```bash
TOKEN=$(curl -s --cacert certs/ca.crt -d grant_type=client_credentials \
  -u "ifdd-ts-ingest:$SECRET" \
  {{ cookiecutter.ifdd_oidc_realm }}/protocol/openid-connect/token | jq -r .access_token)
curl -s --cacert certs/ca.crt -H "Authorization: Bearer $TOKEN" {{ cookiecutter.ifdd_ts_api_url }}/whoami
```

`/whoami` zeigt die Rollen und Store-Muster, die die API aus dem Token liest.

## Entwicklung

`docker-compose-development.yml` startet dasselbe Image ohne Tokenprüfung auf
`127.0.0.1:{{ cookiecutter.ifdd_ts_api_port }}`. Die ifdd-ts-Instanz muss
laufen (ihr VictoriaMetrics hängt in beiden Modi in
`{{ cookiecutter.ifdd_ts_ingest_network }}`). Der type-Dienst wird weiter über
den Proxy erreicht.
