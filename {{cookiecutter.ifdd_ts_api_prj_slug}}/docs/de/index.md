(ifdd-ts-api-index)=
# {{ cookiecutter.ifdd_ts_api_prj_name }} (ts-api)

Die REST-Schnittstelle der Zeitreihen eines IFDD-Knotens: Dienste lesen und
schreiben über sie Samples in VictoriaMetrics, mit einem Access-Token des
Realms und nur in den Stores, die ihre Rollen öffnen. Dieses Kapitel
beschreibt die Instanz `{{ cookiecutter.ifdd_ts_api_prj_slug }}`, erzeugt aus
dem Template `ifdd-de/ts-api`.

| | |
|---|---|
| Öffentliche URL | `{{ cookiecutter.ifdd_ts_api_url }}` (Host `{{ cookiecutter.ifdd_ts_host }}`, Pfad `{{ cookiecutter.ifdd_ts_api_path }}`, vom Proxy geroutet) |
| Interner Port | `{{ cookiecutter.ifdd_ts_api_port }}` (uvicorn, in Produktion nicht veröffentlicht) |
| Version der Instanz | `{{ cookiecutter.ifdd_ts_api_version }}` |
| Laufzeit | Paket `ifdd-ts-core` `~={{ cookiecutter.ifdd_ts_core_version }}` |
| Zeitreihen-Datenbank | VictoriaMetrics der ifdd-ts-Instanz, `{{ cookiecutter.ifdd_ts_api_vm_url }}` |
| Realm | `{{ cookiecutter.ifdd_oidc_realm }}`, Audience `{{ cookiecutter.ifdd_ts_api_oidc_client_id }}` |

## Was die Instanz enthält

Die Laufzeit (Token- und Store-Prüfung, Prüfung gegen die Vokabulare,
VictoriaMetrics, Doku-Seiten) ist das Paket `ifdd-ts-core`. Die Instanz
steuert Paketierung, Image, Compose-Dateien und Konfiguration (`.env`) bei.
Die API hat weder ein eigenes Secret noch eine eigene Datenbank.

## Architektur

```{uml}
@startuml
left to right direction
  rectangle "Dienste, Client Credentials" as S
  rectangle "proxy: Traefik" as P
  S --> P : HTTPS
  rectangle "ts-api: uvicorn" as API
  P --> API : {{ cookiecutter.ifdd_ts_host }}{{ cookiecutter.ifdd_ts_api_path }}
  rectangle "Grafana" as G
  P --> G : {{ cookiecutter.ifdd_ts_host }}, andere Pfade
  database "VictoriaMetrics" as VM
  API --> VM : {{ cookiecutter.ifdd_ts_ingest_network }}
  G --> VM
  API --> P : JWKS, Vokabulare
  rectangle "Keycloak" as KC
  P --> KC
  rectangle "type" as T
  P --> T
@enduml
```

Die API teilt sich den Host mit Grafana: Der Proxy schickt den Pfad
`{{ cookiecutter.ifdd_ts_api_path }}` an die API und alles andere an Grafana.
Sie ruft Keycloak (Signaturschlüssel) und den type-Dienst (Vokabulare) unter
ihren öffentlichen URLs über den Proxy auf und VictoriaMetrics direkt im
Ingest-Netz.

| Wer | ruft die API auf für |
|---|---|
| ct (Plugin `ts-post`) | Schreiben von Beispielreihen |
| eigene Dienste mit dem Client `ifdd-ts-ingest` oder einem eigenen Client | Schreiben von Messwerten |
| Skripte und Notebooks (`ifdd-api-script`) | Lesen |
| Personen | Swagger UI und ReDoc, mit einem von Hand geholten Token |

## Kapitel

```{toctree}
:maxdepth: 2

setup
build-release
operations
security
troubleshooting
reference
api
```

Die Werte der Variablen dieser Instanz stehen im Kapitel über die
Dienst-Instanzen ({ref}`ifdd-instances-ts-api`); das Paket beschreibt
{ref}`ifdd-ts-core-index`.
