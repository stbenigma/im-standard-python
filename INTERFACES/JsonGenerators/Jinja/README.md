# DMP-JSON-Generierung mit Jinja2

## Dateien
- `dmp_template.j2` – Einstiegspunkt, rendert das Top-Level-DMP-Objekt.
- `_macros.j2` – Makros für die Teile mit echter struktureller Wiederholung/Rekursion.
- `render.py` – Beispiel-Kontext (Python-dict) + Aufruf, inkl. JSON-Parse-Check.
- `rendered_example.json` – Ergebnis von `render.py`, validiert 0 Fehler gegen das (korrigierte) Schema.

## Architekturentscheidung
`dmp_dereferenced_schema.json` hat >150 Felder, tief verschachtelt, mit `oneOf`
und `additionalProperties: false` überall. Zwei Wege:

1. Jedes Feld einzeln in Jinja mit manueller Komma-/Anführungszeichen-Logik
   nachbauen → bei dieser Größe garantiert fehleranfällig (vergessene
   optionale Felder, kaputte Kommas, `additionalProperties`-Verstöße).
2. Jinja nur für die Stellen einsetzen, an denen es einen echten Job hat
   (Strukturentscheidung, Rekursion, Wiederholung), und flache Datenblöcke
   als vorbereitete Python-dicts per `| tojson` durchreichen.

Ich habe (2) gebaut. Konkret übernimmt Jinja:
- die Komponenten-Liste (`components[]`),
- die `oneOf`-Entscheidung `substance` vs. `mixture`,
- die Rekursion `substance.impurities[].substance` (⟲ Substanz in Substanz)
  und `mixture.constituents[].mixture` (⟲ Mischung in Mischung),
- wiederkehrende Objektmuster (`Language dependant value`, Hazard-Statement-Objekte).

Alles andere (PCF-Kennzahlen, Geography, Checksum, `identifiers`/`regulatory`)
wird als fertiger Python-dict übergeben und per `tojson` ausgegeben. Das ist
keine Verlegenheitslösung, sondern die robustere Wahl: diese Blöcke haben
keine strukturelle Variation, die eine Template-Sprache abbilden müsste –
nur viele optionale Skalarfelder, für die `tojson` schlicht nie ein falsches
Komma produziert.

Wer will, kann für `sustainability`/PCF nachträglich eigene Makros ergänzen
(z. B. um Pflichtfeld-Defaults zu erzwingen) – die Struktur dafür (ein Makro
pro Submodel, aufgerufen aus `component()`) ist bereits angelegt.

## Gefundener Schema-Bug (nicht mein Template)
In `dmp_dereferenced_schema.json` zeigen drei `"$ref": "#"`
(bei `substance.impurities[].substance` und zweimal bei
`mixture.constituents[].mixture` / `.substance.impurities[].substance`)
auf das **Root-Objekt der Datei** – und Root ist hier der komplette
DMP-Wrapper (verlangt `dmpId`, `nameplate`, `components`). Damit ist
jede rekursive Substanz-/Mischungsangabe im Ist-Zustand nicht valide:
die Validierung verlangt an diesen Stellen fälschlich die drei
Top-Level-Pflichtfelder.

Vermutliche Ursache: Im ursprünglichen `substance.schema.json` (eigene
Datei, eigene `$id`) bedeutete `$ref: "#"` korrekt "diese Datei selbst".
Beim Zusammenführen in ein einziges dereferenziertes Dokument wurde diese
Selbstreferenz nicht auf den neuen internen Pfad umgeschrieben.

Fix (JSON-Pointer statt `"#"`):
```
substance.impurities[].substance  → "$ref": "#/properties/components/items/properties/materialDeclaration/properties/materialDeclaration/properties/substance"
mixture.constituents[].mixture    → "$ref": "#/properties/components/items/properties/materialDeclaration/properties/materialDeclaration/properties/mixture"
```
Erst mit diesem Fix validiert `rendered_example.json` fehlerfrei (getestet
mit `jsonschema` Draft 2020-12 Validator).

## Nutzung
```bash
pip install jinja2 --break-system-packages
python3 render.py
```
Kontext in `render.py` anpassen oder aus eigener Datenquelle befüllen
und `env.get_template("dmp_template.j2").render(**context)` aufrufen.
