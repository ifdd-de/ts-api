(ifdd-ts-api-security)=
# Sicherheit

## Wer was darf

Jede Anfrage außer `/version` und der Doku braucht ein Access-Token des
Realms `{{ cookiecutter.ifdd_oidc_realm }}` mit der Audience
`{{ cookiecutter.ifdd_ts_api_oidc_client_id }}`. Die API prüft Signatur,
Ablauf, Audience, Aussteller und dass es ein Access-Token ist, kein
ID-Token. Aufrufer sind Dienste mit dem Client-Credentials-Grant; die Rollen
des Clients `{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` bekommen nur
Service-Accounts, das Token einer Person hat also weder die Audience noch
eine Rolle.

| Prüfung | Antwort bei Fehlschlag |
|---|---|
| Token | 401 |
| Store-Name | 422 |
| Rolle `{{ cookiecutter.ifdd_ts_api_role_read }}` (lesen) oder `{{ cookiecutter.ifdd_ts_api_role_write }}` (schreiben) | 403 |
| ein Store-Muster des Clients passt auf den Store | 403 |

Lesen und Schreiben sind getrennt: Ein Schreiber kann nicht lesen, ein Leser
nicht schreiben. Ein fremder Store antwortet 403, nicht 404 (keine Security
by Obscurity); `/stores` lässt weg, was der Aufrufer nicht lesen darf.

Vom keycloak-Template eingerichtete Service-Accounts:

| Client | Rollen hier |
|---|---|
| `ifdd-ts-ingest` | schreiben, Wurzel `{{ cookiecutter.ifdd_context_root }}` |
| `ifdd-ct` | schreiben, Wurzel (Beispieldaten) |
| `ifdd-api-script` | lesen, Wurzel |

## Wie die Stores getrennt bleiben

Die API übergibt VictoriaMetrics bei jedem Lesen und Schreiben
`extra_label=ifdd_store=<store>`: VictoriaMetrics setzt das Label auf jedes
geschriebene Sample und filtert jedes Lesen danach. Ein Label `ifdd_store`
im Rumpf einer Anfrage ändert daran nichts.

## Was die API nicht schützt

- **Grafana** liest VictoriaMetrics direkt. Wer sich bei Grafana anmeldet,
  sieht die Reihen aller Stores.
- **Das Ingest-Netz** `{{ cookiecutter.ifdd_ts_ingest_network }}`: Jeder
  Container darin kann ohne Prüfung in VictoriaMetrics schreiben und löschen.
  Nur vertrauenswürdige Container anhängen; Dienste, die dieses Recht nicht
  bekommen sollen, nutzen die API.

Beides ist so entschieden (2026-10-21).

## Doku-Seiten

`{{ cookiecutter.ifdd_ts_api_path }}/docs`, `/redoc` und `/openapi.json` sind
offen: Sie beschreiben die API und geben keinen Zugang zu Daten. Swagger UI
nimmt unter „Authorize“ ein Bearer-Token und hält es im lokalen Speicher des
Browsers für diesen Host; eine Anmeldung über den Browser gibt es nicht.

## Container

Wurzeldateisystem nur lesend, `/tmp` als tmpfs, alle Capabilities entzogen,
`no-new-privileges`, Benutzer `tsapi` (uid 10001). In Produktion wird kein
Port veröffentlicht.

```{note}
Nicht getestet: die Härtung mit dem echten Image (`python:3.14-slim`).
```

## Token-Cache

Ein geprüftes Token bleibt je Prozess bis zu `IFDD_TOKEN_CACHE_TTL` Sekunden
(Standard 300) im Cache; sein Ablauf wird bei jeder Nutzung geprüft. Ein in
Keycloak widerrufenes Token wird bis zu seinem Ablauf weiter angenommen, wie
bei jedem Resource Server, der Tokens lokal prüft.
