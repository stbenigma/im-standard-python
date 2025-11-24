import json


def generate_owl_turtle_from_im(im_data: dict,
                                base_uri: str = "http://ihre-firma.com/ontology/im#") -> str:
    """
    Transformiert ein Informationsmodell (JSON) in eine OWL-Turtle-Repräsentation.

    :param im_data: Das Informationsmodell als Python-Dictionary (aus JSON geladen).
    :param base_uri: Die Basis-URI für die Ontologie-Elemente.
    :return: Der generierte OWL-Turtle-String.
    """

    # 1. Präfixe und Ontologie-Header
    ttl_output = f"""
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix im: <{base_uri}> .

im:Informationsmodell a owl:Ontology ;
    rdfs:comment "Generiert aus dem Informationsmodell-JSON." @de .

#################################################################
#    2. Entitäten (Entities) -> owl:Class
#################################################################
"""

    # Helfer-Mapping für Domänen-IDs zu xsd:Datentypen
    DOMAIN_MAPPING = {
        "DOMA1": "xsd:string",  # Beschreibung (TextDomain)
        "DOMA2": "xsd:string",  # Kurzname (TextDomain)
        "DOMA3": "xsd:string",  # Name (TextDomain)
        "DOMA4": "xsd:boolean",  # Boolean
        "DOMA5": "xsd:date",  # Datum (DatetimeDomain)
        "DOMA6": "xsd:integer",  # Integer (NumericDomain)
        "DOMA7": "xsd:string",  # String (TextDomain)
        "DOMA8": "xsd:string",  # Text (TextDomain)
        "DOMA9": "xsd:integer",  # Reihenfolge Nummer (NumericDomain)
    }

    entity_map = {e['elementid']: e for e in im_data.get('Entities', [])}

    for entity in im_data.get('Entities', []):
        entity_id = entity['elementid']
        name_de = entity['name'].get('de', 'UnbekannteEntitaet')
        description_de = entity.get('description',{}).get('de', 'Keine Beschreibung verfügbar.').replace('"', '\\"')

        ttl_output += f"""
im:{entity_id} a owl:Class ;
    rdfs:label "{name_de}" @de ;
    rdfs:comment "{description_de}" @de .
"""

    ttl_output += """
#################################################################
#    3. Attribute (Attributes) -> owl:DatatypeProperty
#################################################################
"""

    for entity in im_data.get('Entities', []):
        attribute_data = entity.get('attributes', [])
        for attr in attribute_data:
            attr_id = attr['elementid']
            name_de = attr['name']#.get('de', 'UnbekanntesAttribut')
            parent_id = entity.get("elementid")#attr['parentid']
            domain_id = attr.get('domainid')
            description_de = attr.get('description')

            # Bestimme den Datentyp (rdfs:range)
            xsd_type = DOMAIN_MAPPING.get(domain_id, "xsd:string")

            ttl_output += f"""
    im:{attr_id} a owl:DatatypeProperty ;
        rdfs:label "{name_de}" @de ;
        rdfs:domain im:{parent_id} ;
        rdfs:range {xsd_type} ;
        rdfs:comment "{description_de}" @de .
    """
            # Behandlung von Schlüsseln (FunctionalProperty für Unique Keys)
            # Im JSON sind Schlüssel nur implizit oder über ENTI3/ENTI5 definiert.
            # Hier wird eine vereinfachte Annahme getroffen, basierend auf 'mandatory' + Eindeutigkeit.

            # Man könnte hier prüfen, ob ein Attribut Teil eines Schlüssels (ENTI3/ENTI5) ist
            # und dann owl:FunctionalProperty hinzufügen.
            if attr.get('mandatory') and name_de == "Name":
                ttl_output += f"im:{attr_id} a owl:FunctionalProperty . # Möglicher Natural Key\n"

    ttl_output += """
#################################################################
#    4. Beziehungen (Relations) -> owl:ObjectProperty
#################################################################
"""

    for rel in im_data.get('Relations', []):
        rel_id = rel['elementid']
        # Vorwärts-Richtung (fwd)
        fwd_entity_id = rel['fwd']['entityid']
        fwd_assoctext_de = rel['fwd']['assoctext'].get('de', f"{rel_id}_fwd")
        fwd_cardinality = rel['fwd']['cardinality']
        fwd_mandatory = rel['fwd']['mandatory']

        # Rückwärts-Richtung (bwd)
        bwd_entity_id = rel['bwd']['entityid']
        bwd_assoctext_de = rel['bwd']['assoctext'].get('de', f"{rel_id}_bwd")
        bwd_cardinality = rel['bwd']['cardinality']
        bwd_mandatory = rel['bwd']['mandatory']

        # Eigenschaft für die Vorwärtsrichtung
        ttl_output += f"""
im:{fwd_assoctext_de.replace(' ', '_')} a owl:ObjectProperty ;
    rdfs:label "{fwd_assoctext_de}" @de ;
    rdfs:domain im:{fwd_entity_id} ;
    rdfs:range im:{bwd_entity_id} ;
    rdfs:comment "Beziehung von {fwd_entity_id} nach {bwd_entity_id}" @de .

im:{bwd_assoctext_de.replace(' ', '_')} a owl:ObjectProperty ;
    rdfs:label "{bwd_assoctext_de}" @de ;
    rdfs:domain im:{bwd_entity_id} ;
    rdfs:range im:{fwd_entity_id} ;
    owl:inverseOf im:{fwd_assoctext_de.replace(' ', '_')} ;
    rdfs:comment "Umkehrung: Beziehung von {bwd_entity_id} nach {fwd_entity_id}" @de .
"""

        # 5. Kardinalität (Constraints) - Beschränkung auf die 'M'-Seite der 1:M/M:N Beziehung
        # Die Transformation der Kardinalität ist komplex, hier nur die Abbildung der Pflicht (minCardinality 1)
        if fwd_mandatory and fwd_cardinality != '1':
            ttl_output += f"""
im:{fwd_entity_id} rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty im:{fwd_assoctext_de.replace(' ', '_')} ;
    owl:minCardinality 1 ; # Entspricht Pflicht (zwingende Verbindung)
] .
"""

    return ttl_output