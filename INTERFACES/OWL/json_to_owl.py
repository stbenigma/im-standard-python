#!/usr/bin/env python3
"""
json_to_owl.py
==============
Converts an IM-Standard information-model JSON file (dataspot / astronomie-schema
format) into an OWL ontology serialised as Turtle (.ttl).

Supported JSON top-level sections
  ModelInfo     → owl:Ontology header
  Categories    → skos:ConceptScheme hierarchy (ENTITY categories → abstract
                  super-classes; DOMAIN categories are noted as comments)
  Domains
      NumericDomain  → rdfs:Datatype with xsd restrictions + optional qudt:unit
      TextDomain     → rdfs:Datatype  (xsd:string base)
      DatetimeDomain → rdfs:Datatype  (xsd:dateTime / xsd:date base)
      BooleanDomain  → rdfs:Datatype  (xsd:boolean base)
      LOVDomain      → owl:Class + owl:oneOf enumeration
      GroupDomain    → owl:Class with DatatypeProperty / ObjectProperty members
  Entities      → owl:Class
                  - category membership  → rdfs:subClassOf (via ENTITY category tree)
                  - SUBTYPE relations    → rdfs:subClassOf
                  - synonyms             → skos:altLabel
  Relations
      SUBTYPE    → rdfs:subClassOf
      M:1 / M:M  → owl:ObjectProperty + optional cardinality restriction
  Attributes    → owl:DatatypeProperty or owl:ObjectProperty
                  (ObjectProperty when domainid points to a GroupDomain/LOVDomain)
  BusinessRules → rdfs:subClassOf [ owl:Restriction ] with rdfs:comment

Usage
-----
  python json_to_owl.py <input.json> [output.ttl]

If no output path is given the file is written next to the input with suffix
_OWL-Notation.ttl.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _lang(obj: Any, preferred: str = "de", fallback: str = "en") -> str:
    """Return text from a {lang: text} dict, trying preferred then fallback."""
    if isinstance(obj, str):
        return obj
    if not isinstance(obj, dict):
        return ""
    return obj.get(preferred) or obj.get(fallback) or next(iter(obj.values()), "")


def _escape(text: str) -> str:
    """Escape special characters for Turtle string literals."""
    return (text
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", ""))


def _local(name: str) -> str:
    """UpperCamelCase IRI local name: 'Galaktische Entfernung' → 'GalaktischeEntfernung'"""
    parts = re.split(r"[\s\-/().,;:\[\]]+", name)
    return "".join(p.capitalize() for p in parts if p)


def _prop_name(name: str) -> str:
    """lowerCamelCase property name: 'mittlerer Abstand' → 'mittlererAbstand'"""
    parts = [p for p in re.split(r"[\s\-/().,;:\[\]]+", name) if p]
    if not parts:
        return "prop"
    return parts[0][0].lower() + parts[0][1:] + "".join(p.capitalize() for p in parts[1:])


def _safe(s: str) -> str:
    """Remove characters illegal in IRI local names."""
    return re.sub(r"[^A-Za-z0-9_\-.]", "_", s)


# ─────────────────────────────────────────────────────────────────────────────
# Turtle document builder
# ─────────────────────────────────────────────────────────────────────────────

class TTL:
    def __init__(self):
        self._lines: list[str] = []

    def line(self, text: str = ""):
        self._lines.append(text)

    def comment(self, text: str):
        self._lines.append(f"# {text}")

    def sep(self, title: str = ""):
        self._lines.append("# " + "=" * 60)
        if title:
            self._lines.append(f"# {title}")
            self._lines.append("# " + "=" * 60)

    def block(self, subject: str, triples: list[str]):
        """Write a Turtle subject block from a list of 'pred  obj' strings."""
        if not triples:
            return
        if len(triples) == 1:
            self._lines.append(f"{subject} {triples[0]} .")
        else:
            self._lines.append(f"{subject} {triples[0]} ;")
            for t in triples[1:-1]:
                self._lines.append(f"    {t} ;")
            self._lines.append(f"    {triples[-1]} .")

    def render(self) -> str:
        return "\n".join(self._lines) + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# Converter
# ─────────────────────────────────────────────────────────────────────────────

class Converter:

    _BASE_XSD: dict[str, str] = {
        "NumericDomain":  "xsd:decimal",
        "TextDomain":     "xsd:string",
        "BooleanDomain":  "xsd:boolean",
        "DatetimeDomain": "xsd:dateTime",
    }
    _GRANULARITY_XSD: dict[str, str] = {
        "DAY":    "xsd:date",
        "MINUTE": "xsd:dateTime",
        "SECOND": "xsd:dateTime",
    }

    def __init__(self, data: dict):
        self.data = data
        info: dict = data.get("ModelInfo", {})

        self.main_lang: str      = info.get("mainLanguage", "de")
        self.extra_langs: list   = info.get("languages", [])
        self.info                = info

        slug = re.sub(r"[^a-z0-9]", "", info.get("modelName", "model").lower())
        self.base_iri = f"urn:imstd:org.eclipse.{slug}:1.0.0#"

        # ── index maps ────────────────────────────────────────────────────────
        self.categories = {c["elementId"]: c for c in data.get("Categories", [])}
        self.domains    = {d["elementId"]: d for d in data.get("Domains", [])}
        self.entities   = {e["elementId"]: e for e in data.get("Entities", [])}
        self.relations  = {r["elementId"]: r for r in data.get("Relations", [])}
        self.attributes: list[dict] = data.get("Attributes", [])
        self.biz_rules:  list[dict] = data.get("BusinessRules", [])

        # ── ENTITY category local IRIs ────────────────────────────────────────
        self.entity_cat_local: dict[str, str] = {}
        for cid, cat in self.categories.items():
            if cat.get("categoryType") == "ENTITY":
                label = _lang(cat["name"], self.main_lang)
                self.entity_cat_local[cid] = _safe(_local(label))

        # ── SUBTYPE parent map (child → parent entity id) ─────────────────────
        self.subtype_parent: dict[str, str] = {}
        for rel in self.relations.values():
            if rel.get("relationType") == "SUBTYPE":
                self.subtype_parent[rel["bwd"]["entityId"]] = rel["fwd"]["entityId"]

        # ── entity / domain local IRI maps ────────────────────────────────────
        self.entity_local: dict[str, str] = {
            eid: _safe(_local(_lang(e["name"], self.main_lang)))
            for eid, e in self.entities.items()
        }
        self.domain_local: dict[str, str] = {
            did: _safe(_local(_lang(d["name"], self.main_lang)))
            for did, d in self.domains.items()
        }

        # ── GroupDomain child attributes ──────────────────────────────────────
        self.group_attrs: dict[str, list[dict]] = {}
        for attr in self.attributes:
            pid = attr.get("parentId", "")
            if pid in self.domains and self.domains[pid].get("domainType") == "GroupDomain":
                self.group_attrs.setdefault(pid, []).append(attr)

        # relation-id → prop local IRI (filled during _write_object_properties)
        self._rel_prop_map: dict[str, str] = {}

        self.ttl = TTL()

    # ─────────────────────────────────────────────────────────────────────────
    # Public entry point
    # ─────────────────────────────────────────────────────────────────────────

    def convert(self) -> str:
        self._write_prefixes()
        self._write_header()
        self._write_entity_category_classes()
        self._write_scalar_domains()
        self._write_lov_domains()
        self._write_group_domains()
        self._write_entity_classes()
        self._write_object_properties()
        self._write_entity_attributes()
        self._write_restrictions()
        self._write_disjointness()
        return self.ttl.render()

    # ─────────────────────────────────────────────────────────────────────────
    # Sections
    # ─────────────────────────────────────────────────────────────────────────

    def _write_prefixes(self):
        t = self.ttl
        t.line(f"@prefix : <{self.base_iri}> .")
        t.line("@prefix owl: <http://www.w3.org/2002/07/owl#> .")
        t.line("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .")
        t.line("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .")
        t.line("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .")
        t.line("@prefix skos: <http://www.w3.org/2004/02/skos/core#> .")
        t.line("@prefix dcterms: <http://purl.org/dc/terms/> .")
        t.line("@prefix qudt: <http://qudt.org/schema/qudt/> .")
        t.line()

    def _write_header(self):
        t = self.ttl
        ml   = self.main_lang
        name = _escape(_lang(self.info.get("modelName", "Model"), ml))
        ver  = self.info.get("modelVersion", "0.0")
        t.sep("Ontologie-Header")
        t.line()
        t.line(": a owl:Ontology ;")
        t.line(f'    rdfs:label "{name}"@{ml} ;')
        t.line(f'    owl:versionInfo "{ver}" ;')
        t.line(f'    dcterms:language "{ml}" ;')
        t.line(f'    dcterms:description "Informationsmodell {name}"@{ml} .')
        t.line()
        t.line()

    # ── ENTITY categories → abstract owl:Class hierarchy ─────────────────────

    def _write_entity_category_classes(self):
        t = self.ttl
        items = [(cid, c) for cid, c in self.categories.items()
                 if c.get("categoryType") == "ENTITY"]
        if not items:
            return
        t.sep("Klassenhierarchie – Kategorien (ENTITY-Kategorien)")
        t.line()
        for cid, cat in items:
            local     = self.entity_cat_local[cid]
            descr     = _lang(cat.get("description", ""), self.main_lang)
            parent_id = cat.get("categoryId", "")
            triples   = ["a owl:Class"]
            triples  += self._label_triples(cat["name"])
            if parent_id in self.entity_cat_local:
                triples.append(f"rdfs:subClassOf :{self.entity_cat_local[parent_id]}")
            if descr:
                triples.append(f'rdfs:comment "{_escape(descr)}"@{self.main_lang}')
            t.comment(f"{cid} – {_lang(cat['name'], self.main_lang)}")
            t.block(f":{local}", triples)
            t.line()
        t.line()

    # ── Scalar domains (Numeric / Text / Datetime / Boolean) → rdfs:Datatype ─

    def _write_scalar_domains(self):
        t = self.ttl
        scalar = {"NumericDomain", "TextDomain", "DatetimeDomain", "BooleanDomain"}
        items  = [(did, d) for did, d in self.domains.items()
                  if d.get("domainType") in scalar]
        if not items:
            return
        t.sep("Datentypen / Datatypes (aus Domains)")
        t.line()
        for did, dom in items:
            local   = self.domain_local[did]
            dt      = dom.get("domainType", "TextDomain")
            descr   = _lang(dom.get("description", ""), self.main_lang)
            unit    = dom.get("unit", "")
            syntax  = dom.get("syntaxRule", "")

            if dt == "DatetimeDomain":
                base = self._GRANULARITY_XSD.get(dom.get("granularity", ""), "xsd:dateTime")
            else:
                base = self._BASE_XSD.get(dt, "xsd:string")

            triples  = ["a rdfs:Datatype"]
            triples += self._label_triples(dom["name"])
            if descr:
                triples.append(f'rdfs:comment "{_escape(descr)}"@{self.main_lang}')
            triples.append(f"owl:onDatatype {base}")

            # xsd restriction facets
            restr: list[str] = []
            if "minValue" in dom:
                restr.append(f'[ xsd:minInclusive "{dom["minValue"]}"^^{base} ]')
            if "maxValue" in dom:
                restr.append(f'[ xsd:maxInclusive "{dom["maxValue"]}"^^{base} ]')
            if "totalDigits" in dom:
                restr.append(f'[ xsd:totalDigits "{dom["totalDigits"]}"^^xsd:positiveInteger ]')
            if "fractDigits" in dom:
                restr.append(f'[ xsd:fractionDigits "{dom["fractDigits"]}"^^xsd:nonNegativeInteger ]')
            if syntax:
                restr.append(f'[ xsd:pattern "{_escape(syntax)}" ]')
            if restr:
                triples.append("owl:withRestrictions (\n        "
                               + "\n        ".join(restr) + "\n    )")
            if unit:
                triples.append(f'qudt:unit :{_safe(unit.replace(" ", "_").replace("^", "pow"))}')

            t.comment(f"--- {_lang(dom['name'], self.main_lang)} ({did}) ---")
            t.block(f":{local}", triples)
            t.line()
        t.line()

    # ── LOV domains → owl:Class + owl:oneOf + individuals ────────────────────

    def _write_lov_domains(self):
        t = self.ttl
        items = [(did, d) for did, d in self.domains.items()
                 if d.get("domainType") == "LOVDomain"]
        if not items:
            return
        t.sep("Enumerationen / List-of-Values (LOVDomain)")
        t.line()
        for did, dom in items:
            local  = self.domain_local[did]
            values = dom.get("values", [])
            descr  = _lang(dom.get("description", ""), self.main_lang)

            triples  = ["a owl:Class"]
            triples += self._label_triples(dom["name"])
            if descr:
                triples.append(f'rdfs:comment "{_escape(descr)}"@{self.main_lang}')
            if values:
                members = " ".join(f":{local}_{_safe(v['value'])}" for v in values)
                triples.append(f"owl:oneOf ( {members} )")

            t.comment(f"--- {_lang(dom['name'], self.main_lang)} ({did}) ---")
            t.block(f":{local}", triples)
            t.line()

            for v in values:
                val_local = f":{local}_{_safe(v['value'])}"
                inst      = [f"a :{local}", f'skos:notation "{_escape(v["value"])}"']
                inst     += self._label_triples(v.get("displayValue", {}))
                vd = _lang(v.get("description", ""), self.main_lang)
                if vd:
                    inst.append(f'rdfs:comment "{_escape(vd)}"@{self.main_lang}')
                t.block(val_local, inst)
            t.line()
        t.line()

    # ── Group domains → owl:Class + child properties ──────────────────────────

    def _write_group_domains(self):
        t = self.ttl
        items = [(did, d) for did, d in self.domains.items()
                 if d.get("domainType") == "GroupDomain"]
        if not items:
            return
        t.sep("Hilfsklassen für GroupDomains (strukturierte Wertebereiche)")
        t.line()
        for did, dom in items:
            local = self.domain_local[did]
            descr = _lang(dom.get("description", ""), self.main_lang)
            triples  = ["a owl:Class"]
            triples += self._label_triples(dom["name"])
            if descr:
                triples.append(f'rdfs:comment "{_escape(descr)}"@{self.main_lang}')
            t.comment(f"--- {_lang(dom['name'], self.main_lang)} ({did}) ---")
            t.block(f":{local}", triples)
            t.line()
            for attr in sorted(self.group_attrs.get(did, []),
                               key=lambda a: a.get("displaySeq", 999)):
                self._emit_attribute(attr, parent_local=local)
            t.line()
        t.line()

    # ── Entity classes ────────────────────────────────────────────────────────

    def _write_entity_classes(self):
        t = self.ttl
        if not self.entities:
            return
        t.sep("Entitätsklassen (Entities)")
        t.line()
        for eid, ent in self.entities.items():
            local    = self.entity_local[eid]
            cat_id   = ent.get("categoryId", "")
            parent_eid = self.subtype_parent.get(eid)
            descr    = _lang(ent.get("description") or ent.get("shortDescr", ""), self.main_lang)
            synonyms = ent.get("synonyms", [])

            triples = ["a owl:Class"]
            if parent_eid and parent_eid in self.entity_local:
                triples.append(f"rdfs:subClassOf :{self.entity_local[parent_eid]}")
            elif cat_id in self.entity_cat_local:
                triples.append(f"rdfs:subClassOf :{self.entity_cat_local[cat_id]}")
            triples += self._label_triples(ent["name"])
            for syn in synonyms:
                triples.append(f'skos:altLabel "{_escape(syn)}"@{self.main_lang}')
            if descr:
                triples.append(f'rdfs:comment "{_escape(descr)}"@{self.main_lang}')

            t.comment(f"{eid} – {_lang(ent['name'], self.main_lang)}")
            t.block(f":{local}", triples)
            t.line()
        t.line()

    # ── Object properties from M:1 / M:M relations ───────────────────────────

    def _write_object_properties(self):
        t = self.ttl
        assoc = [(rid, r) for rid, r in self.relations.items()
                 if r.get("relationType") != "SUBTYPE"]
        if not assoc:
            return
        t.sep("Object Properties – Relationen (aus Relations)")
        t.line()

        # detect a common "orbits" verb to build a super-property
        has_umkreist = any(
            "umkreist" in _lang(r.get("bwd", {}).get("assocText", ""), self.main_lang).lower()
            for _, r in assoc
        )
        if has_umkreist:
            t.comment("Allgemeine Orbit-Eigenschaft")
            t.block(":umkreist",
                    ["a owl:ObjectProperty",
                     'rdfs:label "umkreist"@de, "orbits"@en'])
            t.line()
            t.block(":umkreistVon",
                    ["a owl:ObjectProperty",
                     "owl:inverseOf :umkreist",
                     'rdfs:label "umkreist von"@de, "orbited by"@en'])
            t.line()

        for rid, rel in assoc:
            fwd = rel.get("fwd", {}); bwd = rel.get("bwd", {})
            from_eid = bwd.get("entityId", ""); to_eid = fwd.get("entityId", "")
            if from_eid not in self.entity_local or to_eid not in self.entity_local:
                continue
            from_local = self.entity_local[from_eid]
            to_local   = self.entity_local[to_eid]
            bwd_text   = _lang(bwd.get("assocText", {}), self.main_lang)
            prop_local = _safe(_prop_name(f"{from_local}_{bwd_text}_{to_local}"))
            self._rel_prop_map[rid] = prop_local

            triples = ["a owl:ObjectProperty"]
            if has_umkreist and "umkreist" in bwd_text.lower():
                triples.append("rdfs:subPropertyOf :umkreist")
            triples.append(f'rdfs:label "{_escape(bwd_text)}"@{self.main_lang}')
            triples.append(f"rdfs:domain :{from_local}")
            triples.append(f"rdfs:range :{to_local}")

            t.comment(f"{rid}: {_lang(self.entities[from_eid]['name'], self.main_lang)} "
                      f"{bwd_text} {_lang(self.entities[to_eid]['name'], self.main_lang)}")
            t.block(f":{prop_local}", triples)
            t.line()
        t.line()

    # ── Entity-level attributes → Datatype / Object properties ───────────────

    def _write_entity_attributes(self):
        t = self.ttl
        ent_attrs = [a for a in self.attributes
                     if a.get("parentId", "") in self.entities]
        if not ent_attrs:
            return
        t.sep("Datatype Properties – Attribute der Entitäten")
        t.line()
        cur_parent = None
        for attr in sorted(ent_attrs,
                           key=lambda a: (a.get("parentId", ""), a.get("displaySeq", 999))):
            pid = attr.get("parentId", "")
            if pid != cur_parent:
                t.comment(f"--- {_lang(self.entities[pid]['name'], self.main_lang)} ({pid}) ---")
                t.line()
                cur_parent = pid
            self._emit_attribute(attr)
        t.line()

    # ── Restrictions ──────────────────────────────────────────────────────────

    def _write_restrictions(self):
        t = self.ttl
        wrote_header = False

        def header():
            nonlocal wrote_header
            if not wrote_header:
                t.sep("Restriktionen (aus BusinessRules & Kardinalitäten)")
                t.line()
                wrote_header = True

        # Mandatory M:1 cardinalities
        for rid, rel in self.relations.items():
            if rel.get("relationType") == "SUBTYPE":
                continue
            fwd = rel.get("fwd", {}); bwd = rel.get("bwd", {})
            from_eid = bwd.get("entityId", ""); to_eid = fwd.get("entityId", "")
            if from_eid not in self.entity_local or to_eid not in self.entity_local:
                continue
            prop_local = self._rel_prop_map.get(rid)
            if not prop_local:
                continue
            if bwd.get("mandatory") and bwd.get("cardinality") == "1":
                header()
                from_local = self.entity_local[from_eid]
                to_local   = self.entity_local[to_eid]
                t.comment(f"{rid}: {from_local} umkreist genau einen {to_local} (mandatory)")
                t.line(f":{from_local} rdfs:subClassOf [")
                t.line( "    a owl:Restriction ;")
                t.line(f"    owl:onProperty :{prop_local} ;")
                t.line(f'    owl:qualifiedCardinality "1"^^xsd:nonNegativeInteger ;')
                t.line(f"    owl:onClass :{to_local}")
                t.line("] .")
                t.line()

        # Business rules
        for rule in self.biz_rules:
            descr    = _escape(rule.get("description", rule.get("rule", "")))
            elem_ids = rule.get("restrictedElements", [])
            for eid in elem_ids:
                if eid in self.entity_local:
                    header()
                    local = self.entity_local[eid]
                    t.comment(f"{rule['elementId']}: {descr}")
                    t.line(f":{local} rdfs:subClassOf [")
                    t.line( "    a owl:Restriction ;")
                    t.line(f'    rdfs:comment "{descr}"@{self.main_lang}')
                    t.line("] .")
                    t.line()

        if wrote_header:
            t.line()

    # ── Disjointness ──────────────────────────────────────────────────────────

    def _write_disjointness(self):
        t = self.ttl
        if len(self.entities) < 2:
            return
        t.sep("Disjunktheit der Entitätsklassen")
        t.line()
        members = " ".join(f":{v}" for v in self.entity_local.values())
        t.line("[] a owl:AllDisjointClasses ;")
        t.line(f"    owl:members ( {members} ) .")
        t.line()

    # ─────────────────────────────────────────────────────────────────────────
    # Shared helpers
    # ─────────────────────────────────────────────────────────────────────────

    def _label_triples(self, name_obj: Any) -> list[str]:
        """Build rdfs:label triples from a string or {lang: text} dict."""
        if isinstance(name_obj, str):
            return [f'rdfs:label "{_escape(name_obj)}"']
        if isinstance(name_obj, dict):
            return [f'rdfs:label "{_escape(txt)}"@{lang}'
                    for lang, txt in name_obj.items() if txt]
        return []

    def _emit_attribute(self, attr: dict, parent_local: str | None = None):
        """Emit one owl:DatatypeProperty or owl:ObjectProperty."""
        t       = self.ttl
        pid     = attr.get("parentId", "")
        did     = attr.get("domainId", "")
        mand    = attr.get("mandatory", False)
        descr   = _lang(attr.get("description") or attr.get("shortDescr", ""), self.main_lang)

        # parent class local IRI
        if parent_local:
            dom_local = parent_local
        elif pid in self.entity_local:
            dom_local = self.entity_local[pid]
        elif pid in self.domain_local:
            dom_local = self.domain_local[pid]
        else:
            dom_local = _safe(_local(pid))

        # range + property type
        dom_obj  = self.domains.get(did, {})
        dom_type = dom_obj.get("domainType", "")
        is_obj   = dom_type in ("LOVDomain", "GroupDomain")

        if did in self.domain_local:
            range_str = f":{self.domain_local[did]}"
        else:
            range_str = "xsd:string"

        prop_class = "owl:ObjectProperty" if is_obj else "owl:DatatypeProperty"

        attr_name  = _lang(attr.get("name", attr["elementId"]), self.main_lang)
        prop_local = _safe(_prop_name(f"{dom_local}_{attr_name}"))

        triples  = [f"a {prop_class}"]
        triples += self._label_triples(attr.get("name", attr["elementId"]))
        triples.append(f"rdfs:domain :{dom_local}")
        triples.append(f"rdfs:range {range_str}")
        if descr:
            triples.append(f'rdfs:comment "{_escape(descr)}"@{self.main_lang}')
        if mand:
            triples.append('skos:note "mandatory"')
        examples = [str(e) for e in attr.get("examples", []) if e is not None]
        if examples:
            triples.append("skos:example " + ", ".join(f'"{_escape(e)}"' for e in examples))

        t.block(f":{prop_local}", triples)
        t.line()


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: python json_to_owl.py <input.json> [output.ttl]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(sys.argv[2]) if len(sys.argv) >= 3 \
        else input_path.with_name(input_path.stem + "_OWL-Notation.ttl")

    with open(input_path, encoding="utf-8") as fh:
        data = json.load(fh)

    ttl = Converter(data).convert()

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(ttl)

    n = {
        "Datatype":       ttl.count("a rdfs:Datatype"),
        "Class":          ttl.count("a owl:Class"),
        "ObjectProp":     ttl.count("a owl:ObjectProperty"),
        "DatatypeProp":   ttl.count("a owl:DatatypeProperty"),
        "AllDisjoint":    ttl.count("a owl:AllDisjointClasses"),
    }
    print(f"✓  OWL/Turtle written to: {output_path}")
    print(f"   rdfs:Datatype {n['Datatype']}  |  owl:Class {n['Class']}  |"
          f"  owl:ObjectProperty {n['ObjectProp']}  |  owl:DatatypeProperty {n['DatatypeProp']}")


if __name__ == "__main__":
    main()
