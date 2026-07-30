# JSON-Schema-Generierung aus CHEM-X-DMP.json (dataspot-Modellexport)

## Dateien
- `generate_schemas.py` – Generator (liest die Modelldefinition, schreibt die 5 Schema-Dateien)
- `schemas/mvp-dmp.schema.json` – Root-Schema
- `schemas/ce-declaration.schema.json`, `mixturesubstances.schema.json`,
  `pcf-declaration.schema.json`, `waterscarcity.schema.json` – Sub-Schemas

Alle 5 Dateien sind gegen den Draft-2020-12-Metaschema geprüft (`jsonschema.Draft202012Validator.check_schema`)
und eine Testinstanz validiert fehlerfrei gegen den `$ref`-Verbund.

## Befund 1: Die Quelldatei enthält das Modell zweimal
`CHEM-X-DMP.json` enthält jede Entity und jedes Attribut doppelt: einmal unter
`additionalProps.SOURCE-MODEL == "MVP DMP"` (Leerzeichen – älterer, unvollständiger
Stand ohne `domainid`/Beschreibungen) und einmal unter `"MVP-DMP"` (Bindestrich –
aktueller, vollständiger Stand). Der Generator verwendet **ausschließlich** die
`"MVP-DMP"`-Teilmenge (5 Entities, 37 Attribute, 4 Relationen – danach keine
Namenskollisionen mehr). Falls das nicht eurer Absicht entspricht: in
`generate_schemas.py` ist das die Funktion `is_current()`.

## Befund 2: Tippfehler im Quellmodell
Die Entity heißt im Modell "**PCF Delaration**" (fehlt das "c"). Der generierte
Titel wurde korrigiert ("PCF Declaration"), der technische Property-Name ist
`pcfDeclaration`.

## Mapping-Regeln Domain → JSON-Schema-Typ
| domaintype | JSON-Schema |
|---|---|
| `BooleanDomain` | `"type": "boolean"` |
| `BinaryDomain` | `"type": "string", "contentEncoding": "base64"` |
| `TextDomain` | `"type": "string"` + `maxLength` (aus `maxlength`) + `pattern` (aus `syntaxrule`) |
| `NumericDomain` | `"type": "number"` (oder `"integer"` bei `fractdigits == 0`) + `minimum`/`maximum` |
| `DatetimeDomain` | `format: "date"` bei `granularity: DAY`, sonst `"date-time"` |
| `LOVDomain` | `"type": "string", "enum": [...]` aus `values[].value` |
| `GroupDomain` | siehe unten – kein direktes Mapping möglich |

`mandatory: true` → Property landet in `required`. `repeated: true` → Property
wird zu `{"type": "array", "items": <fragment>}`.

## Befund 3: GroupDomain ist im Modell nicht eindeutig auf Entity-Attribute abgebildet
34 Domains sind vom Typ `GroupDomain` (z.B. "Concentration" mit den Feldern
Accuracy/Lower value/Upper value/Value/Unit, oder "EC Number" mit
EINECS/ELINCS/List Number/NLP). Das sind im Modell **eigene zusammengesetzte
Typen mit eigenen Kind-Attributen** – aber die Entity-Attribute, die per
`domainid` auf eine solche Gruppe verweisen, sind im Ist-Zustand des Modells
durchgehend **flache Skalare** (z.B. "Concentration accuracy" ist ein einzelnes
Attribut von `MixtureSubstances`, kein verschachteltes Objekt). Das Modell
spezifiziert nicht, welches der 4-5 Gruppenfelder mit einem solchen flachen
Attribut gemeint ist.

Der Generator versucht einen Namensabgleich (z.B. "Concentration unit of
measure" → Gruppenfeld "Concentration unit" → übernimmt dessen konkreten Typ,
hier ein `LOVDomain` mit Enum `["volume percentage","mass percentage","ppb","ppm"]`).
Wo das nicht eindeutig gelingt, steht **`"type": "string"` als Fallback** mit
einem `$comment: "... BITTE MANUELL PRÜFEN"` am Feld. Betroffen sind aktuell:

- `mixturesubstances.schema.json`: `indexNumber`, `hazardStatementsCode`,
  `concentrationMinimumGeq`, `concentrationMaximumLt`, `ecNumber`

Bei `concentrationMinimumGeq`/`concentrationMaximumLt` legen die Beispielwerte
im Modell ("0,1", "3") nahe, dass es sich um Zahlen handelt – ich habe das
**nicht automatisch als `number` gesetzt**, weil das eine Vermutung wäre, keine
Ableitung aus dem Modell. Bitte manuell entscheiden.

## Befund 4: Ungewöhnliche Kardinalität bei MixtureSubstances
Die Relation MVP-DMP→MixtureSubstances ist als `M:1` deklariert (eine DMP
enthält *genau ein* `MixtureSubstances`-Objekt), während MVP-DMP→CE-Declaration,
→PCF-Declaration und →WaterScarcity als `M:N` deklariert sind (Arrays). Das
Root-Schema bildet das entsprechend ab: `mixtureSubstances` ist ein einzelnes
Objekt, die anderen drei sind Arrays. Für eine reale Gemischbeschreibung mit
mehreren Substanzen wirkt "genau eine Substanz pro DMP" ungewöhnlich
einschränkend – das ist aber exakt das, was die Relation im Modell aussagt,
keine Interpretation meinerseits. Bitte gegenprüfen, ob im Quellmodell eigentlich
`M:N` gemeint war.

Ebenso sind alle 4 Relationen `fwd.mandatory: true` → alle 4 Top-Level-Properties
stehen in `required` von `mvp-dmp.schema.json`, inklusive `waterScarcity`. Falls
WaterScarcity in der Praxis optional sein soll, ist das im Quellmodell so nicht
hinterlegt.

## Befund 5: Domain/Beispiel-Inkonsistenz bei Datumsfeldern
`PCF Declaration.referencePeriodStart/End` und `WaterScarcity.referencePeriodStart/End`
nutzen die Domain "Date" (`granularity: DAY` → JSON-Schema `format: "date"`,
also `YYYY-MM-DD`), aber die im Modell hinterlegten Beispielwerte sind volle
Zeitstempel (`"2021-11-20T08:30:00.000Z"`). Ich habe die Domain-Definition
(`DAY`) befolgt, nicht das Beispiel – das Beispiel widerspricht der eigenen
Domain-Deklaration im Modell.

## BusinessRules
Die 7 `BusinessRules` aus dem Modell (meist Cross-Field-Constraints wie "at
least one of X/Y/Z must be filled") lassen sich nicht verlustfrei in
JSON-Schema-Validierungslogik (`oneOf`/`anyOf`/`dependentRequired`) übersetzen,
ohne Annahmen über die exakt gemeinten Felder zu treffen, die im Modell nicht
eindeutig sind. Sie sind daher als `$comment` an den betroffenen Properties
hinterlegt (durchsuchbar nach `"Business-Regel:"`), nicht als ausführbare
Schema-Constraints. Wer will, kann sie in einem zweiten Schritt manuell in
`oneOf`/`dependentRequired` übersetzen.

## Nutzung
```bash
python3 generate_schemas.py
```
Liest `/mnt/user-data/uploads/CHEM-X-DMP.json`, schreibt nach `schemas/`.
