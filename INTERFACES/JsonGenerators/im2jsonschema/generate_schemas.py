"""
generate_schemas.py
--------------------
Erzeugt JSON-Schema-Dateien (Draft 2020-12) aus einem dataspot-Modellexport
(CHEM-X-DMP.json: ModelInfo/Categories/Domains/Entities/Relations/Attributes/
BusinessRules/Derivations/Transformations).

WICHTIGE ANNAHME (siehe README): Die Quelldatei enthält den kompletten Modell-
stand zweimal (SOURCE-MODEL "MVP DMP" = alt/unvollständig vs "MVP-DMP" =
aktuell/vollständig). Es wird ausschließlich "MVP-DMP" verwendet.
"""
import json
import re
from pathlib import Path

SRC = Path(__file__).parent/"CHEM-X-DMP.json"
SRC = Path(__file__).parent/"CHEM-X-IM.json"
OUT = Path(__file__).parent / "dmp-json"
OUT = Path(__file__).parent / "dmp-im"
OUT.mkdir(parents=True, exist_ok=True)

data = json.loads(SRC.read_text(encoding="utf-8"))


def is_current(x):
    return x.get("additionalProps", {}).get("SOURCE-MODEL") == "MVP-DMP"


entities = [e for e in data["Entities"] if is_current(e)]
attributes = [a for a in data["Attributes"] if is_current(a)]
relations = [r for r in data["Relations"] if is_current(r)]
domains = {x["elementId"]: x for x in data["Domains"]}  # Domains sind nicht dupliziert

attrs_by_parent = {}
for a in data["Attributes"]:
    attrs_by_parent.setdefault(a["parentId"], []).append(a)

entities_by_id = {e["elementId"]: e for e in entities}
attrs_by_entity = {}
for a in attributes:
    attrs_by_entity.setdefault(a["parentId"], []).append(a)

# BusinessRules indiziert nach betroffenem Element (Domain- oder Attribut-ID)
rules_by_element = {}
for r in data["BusinessRules"]:
    for el in r.get("restrictedElements", []):
        rules_by_element.setdefault(el, []).append(r.get("description"))


def to_camel_case(name: str) -> str:
    name = re.sub(r"[^0-9a-zA-Z]+", " ", name).strip()
    parts = [p for p in name.split(" ") if p]
    if not parts:
        return name
    first, rest = parts[0], parts[1:]
    # Akronyme (z.B. "PCF", "CE", "EU") komplett kleinschreiben statt nur den ersten Buchstaben,
    # sonst entstehen haessliche Mischformen wie "pCFDeclaration".
    first_out = first.lower() if first.isupper() else (first[0].lower() + first[1:])
    return first_out + "".join(p[:1].upper() + p[1:] for p in rest if p)


def to_pascal_kebab(name: str) -> str:
    name = re.sub(r"[^0-9a-zA-Z]+", "-", name).strip("-")
    return name.lower()


TYPO_FIXES = {"Delaration": "Declaration"}


def clean_technical(name: str) -> str:
    for wrong, right in TYPO_FIXES.items():
        name = name.replace(wrong, right)
    return name


def numeric_fragment(dom):
    frag = {"type": "number"}
    if dom.get("fractDigits") == 0:
        frag["type"] = "integer"
    if "minValue" in dom:
        frag["minimum"] = dom["minValue"]
    if "maxValue" in dom:
        frag["maximum"] = dom["maxValue"]
    return frag


def text_fragment(dom):
    frag = {"type": "string"}
    if "maxLength" in dom:
        frag["maxLength"] = dom["maxLength"]
    if dom.get("syntaxRule"):
        frag["pattern"] = dom["syntaxRule"]
    return frag


def datetime_fragment(dom):
    gran = dom.get("granularity")
    if gran == "DAY":
        return {"type": "string", "format": "date"}
    return {"type": "string", "format": "date-time"}


def lov_fragment(dom):
    values = [v["value"] for v in dom.get("values", [])]
    frag = {"type": "string"}
    if values:
        frag["enum"] = values
    return frag


def find_group_child_by_name(group_domain_id, attr_name):
    """Namens-Fuzzy-Match: sucht im GroupDomain nach einem Kind-Attribut,
    dessen Name im Attributnamen enthalten ist (oder umgekehrt)."""
    children = attrs_by_parent.get(group_domain_id, [])
    norm = re.sub(r"[^a-z0-9]", "", attr_name.lower())
    best = None
    for c in children:
        cnorm = re.sub(r"[^a-z0-9]", "", c["name"].lower())
        if cnorm and (cnorm in norm or norm in cnorm):
            if best is None or len(cnorm) > len(re.sub(r"[^a-z0-9]", "", best["name"].lower())):
                best = c
    return best


def resolve_domain(domain_id, attr_name_hint=None, _depth=0):
    """Liefert (schema_fragment, notes[]) fuer eine domainid."""
    notes = []
    if domain_id is None:
        notes.append("Kein domainid im Quellmodell hinterlegt - Fallback auf 'string'.")
        return {"type": "string"}, notes
    dom = domains.get(domain_id)
    if dom is None:
        notes.append(f"domainid {domain_id} nicht in Domains-Liste gefunden - Fallback 'string'.")
        return {"type": "string"}, notes

    dt = dom["domainType"]
    if dt == "BooleanDomain":
        frag = {"type": "boolean"}
    elif dt == "BinaryDomain":
        frag = {"type": "string", "contentEncoding": "base64"}
    elif dt == "TextDomain":
        frag = text_fragment(dom)
    elif dt == "NumericDomain":
        frag = numeric_fragment(dom)
    elif dt == "DatetimeDomain":
        frag = datetime_fragment(dom)
    elif dt == "LOVDomain":
        frag = lov_fragment(dom)
    elif dt == "GroupDomain":
        # GroupDomain ist ein zusammengesetzter Typ. Referenzierende Entity-
        # Attribute in diesem Modell sind aber durchgehend FLACHE Skalare
        # (verifiziert gegen das Quellmodell), die jeweils NUR eines der
        # Group-Felder meinen. Wir versuchen per Namens-Fuzzy-Match das
        # gemeinte Feld zu finden und dessen konkreten Typ zu uebernehmen.
        match = find_group_child_by_name(domain_id, attr_name_hint or "") if attr_name_hint else None
        if match and _depth < 4:
            frag, sub_notes = resolve_domain(match.get("domainid"), match["name"], _depth + 1)
            notes.append(
                f"domainid {domain_id} ('{dom['name']}') ist eine Gruppe (GroupDomain). "
                f"Feld wurde per Namensabgleich auf Gruppenmitglied '{match['name']}' "
                f"({match['elementId']}) gemappt."
            )
            notes.extend(sub_notes)
        else:
            frag = {"type": "string"}
            notes.append(
                f"domainid {domain_id} ('{dom['name']}') ist eine Gruppe (GroupDomain) mit "
                f"mehreren Feldern; das Quellmodell spezifiziert nicht, welches Gruppenfeld "
                f"gemeint ist. Fallback auf 'string' - BITTE MANUELL PRUEFEN."
            )
    else:
        frag = {"type": "string"}
        notes.append(f"Unbekannter domaintype '{dt}' - Fallback 'string'.")

    if dom.get("description") and _depth == 0:
        frag = dict(frag)
        frag.setdefault("description", dom["description"].strip())

    if domain_id in rules_by_element:
        notes.extend(f"Business-Regel: {r}" for r in rules_by_element[domain_id])

    return frag, notes


def build_property(attr):
    frag, notes = resolve_domain(attr.get("domainid"), attr["name"])
    frag = dict(frag)

    title = attr["name"]
    frag["title"] = title

    descr_parts = []
    if attr.get("description"):
        descr_parts.append(attr["description"].strip())
    elif attr.get("shortDescr"):
        descr_parts.append(attr["shortDescr"].strip())
    if attr.get("examples"):
        descr_parts.append("Beispiel(e): " + ", ".join(str(e) for e in attr["examples"]))
    if descr_parts:
        frag["description"] = " | ".join(descr_parts)

    if attr["elementId"] in rules_by_element:
        notes.extend(f"Business-Regel: {r}" for r in rules_by_element[attr["elementId"]])

    if notes:
        frag["$comment"] = " / ".join(dict.fromkeys(notes))  # dedupe, Reihenfolge erhalten

    if attr.get("repeated"):
        frag = {"type": "array", "items": frag}

    return frag


def build_entity_schema(entity):
    attrs = sorted(
        attrs_by_entity.get(entity["elementId"], []),
        key=lambda a: a.get("displaySeq", 9999),
    )
    props = {}
    required = []
    tech_used = set()
    for a in attrs:
        tech = a.get("additionalProps", {}).get("TechnicalName") or to_camel_case(a["name"])
        tech = clean_technical(tech)
        if tech in tech_used:
            tech = tech + "_" + a["elementId"]
        tech_used.add(tech)
        props[tech] = build_property(a)
        if a.get("mandatory"):
            required.append(tech)

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://chem-x.de/models/mvp-dmp/{to_pascal_kebab(clean_technical(entity['name']))}.schema.json",
        "title": clean_technical(entity["name"]),
        "type": "object",
        "properties": props,
        "additionalProperties": False,
    }
    if entity.get("description"):
        schema["description"] = entity["description"]
    if required:
        schema["required"] = required
    return schema


# --- Sub-Entity-Schemas erzeugen ---
root_entity = next(e for e in entities if e["elementId"] not in
                    {r["bwd"]["entityId"] for r in relations})
sub_entities = [e for e in entities if e["elementId"] != root_entity["elementId"]]

schema_files = {}
for e in sub_entities:
    fname = to_pascal_kebab(clean_technical(e["name"])) + ".schema.json"
    schema_files[e["elementId"]] = fname
    schema = build_entity_schema(e)
    (OUT / fname).write_text(json.dumps(schema, indent=2, ensure_ascii=False), encoding="utf-8")

# --- Root-Schema (MVP-DMP) aus Relations ---
root_props = {}
root_required = []
root_notes = []
for r in relations:
    target_id = r["bwd"]["entityId"]
    target_entity = entities_by_id[target_id]
    prop_name = to_camel_case(clean_technical(target_entity["name"]))
    ref = {"$ref": schema_files[target_id]}
    is_array = r["bwd"]["cardinality"] not in ("1", "0..1")
    root_props[prop_name] = {"type": "array", "items": ref} if is_array else ref
    if r["fwd"].get("mandatory"):
        root_required.append(prop_name)
    root_notes.append(
        f"{prop_name}: Kardinalitaet lt. Relation {r['elementId']} = "
        f"{r['relationType']} (bwd cardinality='{r['bwd']['cardinality']}') "
        f"=> {'array' if is_array else 'single object'}."
    )

root_schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://chem-x.de/models/mvp-dmp/mvp-dmp.schema.json",
    "title": clean_technical(root_entity["name"]),
    "type": "object",
    "properties": root_props,
    "additionalProperties": False,
    "$comment": " / ".join(root_notes),
}
if root_required:
    root_schema["required"] = root_required

(OUT / "mvp-dmp.schema.json").write_text(
    json.dumps(root_schema, indent=2, ensure_ascii=False), encoding="utf-8"
)

print("Erzeugte Dateien:")
for f in sorted(OUT.glob("*.schema.json")):
    print(" -", f.name)
