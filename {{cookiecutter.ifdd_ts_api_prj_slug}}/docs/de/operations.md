(ifdd-ts-api-operations)=
# Betrieb

## Starten, stoppen, Logs

```bash
docker compose -f docker-compose-production.yml up -d
docker compose -f docker-compose-production.yml logs -f api
docker compose -f docker-compose-production.yml down
```

Die API hält keinen Zustand: Tokens und Vokabulare liegen je Prozess im
Speicher und werden nach einem Neustart neu geholt. Nichts braucht ein
Backup; die Samples liegen in VictoriaMetrics (ifdd-ts).

## Zustand

`{{ cookiecutter.ifdd_ts_api_path }}/version` antwortet ohne Token; der
Healthcheck des Images ruft es auf. Es zeigt, dass der Prozess läuft, nicht,
dass VictoriaMetrics oder der type-Dienst erreichbar sind.

## Samples schreiben

Ein Sample:

```bash
curl -s --cacert certs/ca.crt -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  {{ cookiecutter.ifdd_ts_api_url }}/stores/temperature.ops.example.ifdd.de/samples -d '{
    "name": "temperature",
    "ifdd_id": "https://rest/products/<id>",
    "ifdd_property": "{{ cookiecutter.ifdd_type_url }}/climate.ops.example.ifdd.de/temperature",
    "ifdd_unit": "https://unit/v1/unit/DEG_C",
    "time": "2026-10-22T09:15:00+02:00",
    "value": 21.5}'
```

Store und IRIs oben sind Beispiele (Beispiel-Domäne `ops`). Eine Liste geht
als `{"samples": [...]}` an `.../samples/batch`, höchstens
`{{ cookiecutter.ifdd_ts_api_max_items }}` je Anfrage. Jedes Sample wird
gegen das Vokabular seiner Eigenschaft geprüft; ein fehlerhaftes Sample
weist die ganze Liste ab.

Schreiben hängt nur an. Ein Sample mit derselben Reihe und Zeit wie ein
gespeichertes ersetzt dieses nicht: Mit der Deduplizierung von ifdd-ts bleibt
der größere Wert. Einen Wert zu korrigieren, geht über diese API nicht.

## Samples lesen

| Anfrage | Antwort |
|---|---|
| `GET /stores` | Stores, die der Aufrufer lesen darf |
| `GET /stores/{store}/series?ifdd_id=...` | Reihen eines Stores |
| `GET /stores/{store}/samples?ifdd_id=...&ifdd_property=...[&at=...]` | letztes Sample zu oder vor `at` |
| `GET /stores/{store}/samples/range?ifdd_id=...&start=...[&end=...]` | Rohwerte im Zeitraum |

Alle Pfade liegen unter `{{ cookiecutter.ifdd_ts_api_url }}`; Einzelheiten in
{ref}`ifdd-ts-api-api`.

## Grafana

Grafana liest VictoriaMetrics direkt und zeigt die Reihen aller Stores
gemeinsam; der Store ist dort nur das Label `ifdd_store`. Ein Diagramm kann
deshalb Werte zweier Stores nebeneinander zeigen, etwa Temperatur und
Feuchte.
