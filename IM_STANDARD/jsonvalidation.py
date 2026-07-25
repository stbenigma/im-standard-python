import json
import logging
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

from IM_STANDARD import nvl


def validate_json_as_schema(schema: dict):
    """
    Prüft, ob eine gegebene JSON-Datei ein gültiges JSON Schema (Draft 2020-12) ist.
    """
    validatorclass = validator_for(schema)

    try:
        validatorclass.check_schema(schema)
    except json.JSONDecodeError as e:
        logging.error(f"❌ Fehler: Ungültiges JSON-Format in der Datei: {e}")
        raise e
    except SchemaError as e:
        logging.error(f"❌ Interner Fehler: Das Meta-Schema ist selbst ungültig: {e}")
        raise e
    except Exception as e:
        # Dies fängt ValidationErrors ab, wenn das Dokument das Meta-Schema verletzt.
        logging.error(f"❌  '{schema}' ist KEIN gültiges JSON Schema.")
        logging.error(f"Validierungsfehler: {e}")
        raise e
    return


def validate_jsonfile_as_schema(json_file_path: str):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        document_to_validate = json.load(f)
    validate_json_as_schema(schema=document_to_validate)
    return


class ValidateJsonModel:
    """
    Validates additional rules for a json schemafile of an information
    """

    def __init__(self, referenceschemapath):
        self.referencefilepath = referenceschemapath
        self.refschemajs = self.readjsonfromfile(filepath=self.referencefilepath)
        self.model = None
        return

    @staticmethod
    def readjsonfromfile(filepath: str | Path):
        with open(Path(filepath).resolve(), 'r', encoding='utf-8') as infile:
            myschemajs = json.load(fp=infile)
        return myschemajs

    def uniquenames(self, elements):
        def find_duplicates(input_list):
            ukduplicates = set()
            for item in input_list:
                if input_list.count(item) > 1:
                    ukduplicates.add(item)
            return list(ukduplicates)

        if self.model.modelismultilingual():
            for lang in self.model.languages:
                duplicates = find_duplicates([self.model.mlvalue(elem.get("name"), lang) for elem in nvl(elements, [])])
                if len(duplicates) > 0:
                    # if verbose: logging.error(f"Duplicate name (in any language) in {ukduplicates}")
                    return [f"Duplicate name (in any language) in {duplicates}"]
        else:
            duplicates = find_duplicates([elem.get("name") for elem in nvl(elements, [])])
            if len(duplicates) > 0:
                # if verbose: logging.error(f"Duplicate name in {ukduplicates}")
                return [f"Duplicate name in {duplicates}"]
        return []

    @staticmethod
    def listunique(x):
        """True if sorted lists in list are unique"""
        seen = list()
        return not any(sorted(i) in seen or seen.append(sorted(i)) for i in x)

    def _checkadditionalrules(self):
        errors = []
        # validate the additional rules, not covered by the model itself.
        myschema = self.model
        if self.model is None:
            return errors

        # model spanning rules
        relaids = [e["elementId"] for e in myschema.getelementinstances(elementname="Relations")]
        domainids = [e.get("elementId") for e in myschema.getelementinstances(elementname="Domains")]
        buruids = [e["elementId"] for e in myschema.getelementinstances(elementname="BusinessRules")]
        entityids = [e.get("elementId") for e in myschema.getelementinstances(elementname="Entities")]
        attrids = [e["elementId"] for e in myschema.getelementinstances(elementname="Attributes")]
        domaattrids = [e.get("elementId")
                       for elems in [doma.get("elements", [])
                                     for doma in myschema.getelementinstances(elementname="Domains")]
                       for e in elems]
        tableids = [e.get("elementId") for e in myschema.getelementinstances(elementname="Tables")]
        columnids = [e.get("elementId") for e in myschema.getelementinstances(elementname="Columns")]
        catgids = [e.get("elementId") for e in myschema.getelementinstances(elementname="Categories")]

        # Many  names must be unique in all languages
        errors += self.uniquenames(elements=myschema.getelementinstances(name="Entities"))

        # all businessrule id's must be unique over the model
        if len(buruids) > len(set(buruids)):
            # if verbose: logging.error(f"Duplicate businessrule-id's in model")
            errors.append(f"Duplicate businessrule-id's in model")

        # all entity id's must be unique over the model
        if len(entityids) > len(set(entityids)):
            # if verbose: logging.error(f"Duplicate entity-id's in model")
            errors.append(f"Duplicate entity-id's in model")

        # all attribute id's must be unique over all entities
        if len(attrids) > len(set(attrids)):
            # if verbose: logging.error(f"Duplicate attribute-id's in model")
            errors.append(f"Duplicate attribute-id's in model")

        # all column id's must be unique over all tables
        if len(columnids) > len(set(columnids)):
            # if verbose: logging.error(f"Duplicate Column-id's in model")
            errors.append(f"Duplicate Column-id's in model")

        # all relation id's must be unique
        if len(relaids) > len(set(relaids)):
            # if verbose: logging.error(f"Duplicate relation-id's in model")
            errors.append(f"Duplicate relation-id's in model")
            # relationships must be unique (assoc and entities)
            relationskeys = [[rela.get("fwd").get("entityId") + "-"
                              + rela.get("bwd").get("entityId") + "-"
                              + nvl(myschema.mlvalue(rela.get("fwd").get("assocText")), lang)
                              for lang in myschema.languages
                              ]
                             for rela in myschema.getelementinstances(name="Relations")
                             ] + \
                            [[rela.get("bwd").get("entityId") + "-"
                              + rela.get("fwd").get("entityId") + "-"
                              + nvl(myschema.mlvalue(rela.get("bwd").get("assocText")), lang)
                              for lang in myschema.languages
                              ]
                             for rela in myschema.getelementinstances(name="Relations")
                             ]
            if not self.listunique(relationskeys):
                # if verbose: logging.error(f"Duplicate relations (enti-enti-multilangassoctext) in model")
                errors.append(f"Duplicate relations (enti-enti-multilangassoctext) in model")

        # rules within domains
        for doma in myschema.getelementinstances(name="Domains"):
            # categories exist
            if doma.get("categoryId") is not None and doma.get("categoryId") not in catgids:
                # if verbose: logging.error(f"Category-id {doma.get('categoryId')} not in categories")
                errors.append(f"Category-id {doma.get('categoryId')} not in categories")
            # all referenced domains (in groupdomains) must exist in the domainlist
            if doma.get("domainType") == "GroupDomain":
                for elem in doma.get("elements", []):
                    domainid = elem.get("domainId")
                    if domainid is not None and domainid not in domainids:
                        # if verbose: logging.error(
                        #    f"Domain {elem.get('domainId')} of groupdomain {doma.get('elementId')} not found.")
                        errors.append(
                            f"Domain {elem.get('domainId')} of groupdomain {doma.get('elementId')} not found.")

        # rules for categories
        if len(catgids) > len(set(catgids)):
            # if verbose: logging.error(f"Duplicate Category-id's in model")
            errors.append(f"Duplicate Category-id's in model")

        for catg in myschema.getelementinstances(name="Categories"):
            # name must have a value in the main mainlanguage
            if not (type(catg.get("name")) is str or myschema.mainlang in catg.get("name")):
                # if verbose: logging.error(f"No name in main language in category {catg.get('name')}")
                errors.append(f"No name in main language in category {catg.get('name')}")

        # rules within entities
        for enti in myschema.getelementinstances(name="Entities"):
            # categories exist
            if enti.get("categoryId") is not None and enti.get("categoryId") not in catgids:
                # if verbose: logging.error(f"Category-id {enti.get('categoryId')} not in categories")
                errors.append(f"Category-id {enti.get('categoryId')} not in categories")

            # name must have a value in the main mainlanguage
            if not (type(enti.get("name")) is str or myschema.mainlang in enti.get("name")):
                # if verbose: logging.error(f"No name in main language in entity {enti.get('name')}")
                errors.append(f"No name in main language in entity {enti.get('name')}")

            # rules for synonyms
            # all synonyms must have a value in the main mainlanguage
            synos = enti.get("synonyms", [])
            if not (all([(type(syno) == str or myschema.mainlang in syno) for syno in synos])):
                # if verbose: logging.error(f"Missing synonym name in main language in entity {enti.get('name')}")
                errors.append(f"Missing synonym name in main language in entity {enti.get('name')}")

            # synonyms names must be unique in all languages within an entity
            if self.model.modelismultilingual() and not self.listunique([[myschema.mlvalue(syno, lang)
                                                                          for lang in myschema.languages
                                                                          ] for syno in synos
                                                                         ]):
                # if verbose: logging.error(f"Duplicate synonym in entity {enti.get('name')}")
                errors.append(f"Duplicate synonym in entity {enti.get('name')}")

            entyattrs = [attr for attr in myschema.getelementinstances(name="Attributes") if
                         attr.get("parentId") == enti.get("elementId")]
            # attribute names must be unique in all languages within an entity
            attrnames = [[myschema.mlvalue(attr.get("name"), lang)
                          for lang in myschema.languages
                          ] for attr in entyattrs
                         ]
            if not self.listunique(attrnames):
                # if verbose: logging.error(f"Duplicate multimultilang attributename in entity {enti.get('name')}")
                errors.append(f"Duplicate multimultilang attributename in entity {enti.get('name')}")

        # rules for attributes
        for attr in myschema.getelementinstances(name="Attributes"):
            # attribute parent must be entity
            if attr.get("parentId") not in entityids:
                # if verbose: logging.error(
                #    f"Entity {attr.get('parentId')} in attribute {attr.get('elementId')} not found.")
                errors.append(f"Entity {attr.get('parentId')} in attribute {attr.get('elementId')} not found.")

            # all attributes must have a value in the main mainlanguage
            if not (type(attr.get("name")) == str or myschema.mainlang in attr.get("name")):
                # if verbose: logging.error(
                errors.append(
                    f"Missing attribute name {attr.get('name')} in main language in entity {attr.get('parentId')}")

            # all referenced domains must exist in the domainlist
            domaid = attr.get("domainId")
            if domaid is not None and domaid not in domainids:
                # if verbose: logging.error(
                #    f"Domain {domaid} in attribute {attr.get('elementId')} not found.")
                errors.append(f"Domain {domaid} in attribute {attr.get('elementId')} not found.")

        # rules for relationships
        for rela in myschema.getelementinstances(name="Relations"):
            if myschema.modeltype == "Information model":
                # all referenced entities must exist
                if rela.get("fwd").get("entityId") not in entityids:
                    # if verbose: logging.error(
                    #    f"Entity {rela.get('fwd').get('entityId')} in relation {rela.get('elementId')} not found.")
                    errors.append(
                        f"Entity {rela.get('fwd').get('entityId')} in relation {rela.get('elementId')} not found.")

                if rela.get("bwd").get("entityId") not in entityids:
                    # if verbose: logging.error(
                    #    f"Entity {rela.get('bwd').get('entityId')} in relation {rela.get('elementId')} not found.")
                    errors.append(
                        f"Entity {rela.get('bwd').get('entityId')} in relation {rela.get('elementId')} not found.")

                # relationship types require specific end-properties
                if (rela.get("relationType") == "M:1"
                        and (rela.get("fwd").get("cardinality")
                             == rela.get("bwd").get("cardinality"))):
                    # if verbose: logging.error(
                    #    f"Functional relationship must have 1 at one end in relationship {rela.get('elementId')}")
                    errors.append(
                        f"Functional relationship must have 1 at one end in relationship {rela.get('elementId')}")
                if (rela.get("relationType") == "M:N"
                        and (rela.get("fwd").get("cardinality") == "1"
                             or rela.get("bwd").get("cardinality") == "1")):
                    # if verbose: logging.error(
                    #    f"M:N relationship must have M a both ends in relationship {rela.get('elementId')}")
                    errors.append(f"M:N relationship must have M a both ends in relationship {rela.get('elementId')}")
                if (rela.get("relationType") == "1:1"
                        and (rela.get("fwd").get("cardinality") == "M"
                             or rela.get("bwd").get("cardinality") == "M")):
                    # if verbose: logging.error(
                    #    f"1:1 relationship must have 1 a both ends in relationship {rela.get('elementId')}")
                    errors.append(f"1:1 relationship must have 1 a both ends in relationship {rela.get('elementId')}")
                if (rela.get("relationType") == "ROLE"
                        and (rela.get("fwd").get("cardinality") == "M"
                             or rela.get("bwd").get("cardinality") == "M"
                             or (rela.get("fwd").get("mandatory") ==
                                 rela.get("bwd").get("mandatory"))
                             )
                    ):
                    # if verbose: logging.error(
                    #    f"ROLE relationship must have 1 a both ends in relationship {rela.get('elementId')}")
                    errors.append(f"ROLE relationship must have 1 a both ends in relationship {rela.get('elementId')}")
                if (rela.get("relationType") == "SUBTYPE"
                        and (rela.get("fwd").get("cardinality") == "M"
                             or rela.get("bwd").get("cardinality") == "M"
                             or not rela.get("fwd").get("mandatory")
                             or not rela.get("bwd").get("mandatory")
                             or (rela.get("fwd").get("arcNumber") is None
                                 and rela.get("bwd").get("arcNumber") is None)
                        )):
                    # if verbose: logging.error(
                    #    f"SUBTYPE relationship must have 1 a both ends in relationship {rela.get('elementId')}")
                    errors.append(
                        f"SUBTYPE relationship must have 1 a both ends in relationship {rela.get('elementId')}")

            elif myschema.modeltype == "Data model":
                # all referenced entities must exist
                if rela.get("fwd").get("tableid") not in tableids:
                    # if verbose: logging.error(
                    #    f"Table {rela.get('fwd').get('tableid')} in relation {rela.get('elementId')} not found.")
                    errors.append(
                        f"Table {rela.get('fwd').get('tableid')} in relation {rela.get('elementId')} not found.")
                if rela.get("bwd").get("tableid") not in tableids:
                    # if verbose: logging.error(
                    #    f"Table {rela.get('bwd').get('tableid')} in relation {rela.get('elementId')} not found.")
                    errors.append(
                        f"Table {rela.get('bwd').get('tableid')} in relation {rela.get('elementId')} not found.")
                # all referenced columns must exist
                for direc in ("fwd", "bwd"):
                    for c in rela.get(direc).get("fkcolumns", []):
                        if c not in columnids:
                            # if verbose: logging.error(f"Column {c} in relation {rela.get('elementId')} not found.")
                            errors.append(f"Column {c} in relation {rela.get('elementId')} not found.")

        # rules for businessrules
        for buru in myschema.getelementinstances(name="BusinessRules"):
            # all referenced objects must exist
            for elem in buru.get("restrictedElements"):
                if elem not in domaattrids + attrids + relaids + entityids + domainids:
                    # if verbose: logging.error(f"ID {elem} in businessrule {buru.get('elementId')} not found.")
                    errors.append(f"ID {elem} in businessrule {buru.get('elementId')} not found.")

        return errors

    def validatemodel(self) -> list:
        """
        @param instance:
            dict or path to json file to be validated against my schemafile
        @return:
            [] : success
            []: failure
                   list of errors
        """
        # TODO errors with my own logging-instance
        errors = self._checkadditionalrules()
        return errors


def validatestruct(struct: dict, basepath: str | Path, startschemafile: str | Path) -> list:
    """
    Validates a json structure against all json schemas found in basepath and subdirectories.

    :param struct:    json structure to validate
    :param basepath:  root directory containing all schema files in subdirectories
    :param schemafile:  path to the schema to validate against (absolute or relative to basepath)
    :return:          list of error messages, empty list if valid
    """

    basepath = Path(basepath).resolve()

    startschemafile = Path(startschemafile)
    if not startschemafile.is_absolute():
        startschemafile = basepath / startschemafile
    startschemafile = startschemafile.resolve()

    # Registry aufbauen — alle Schemas mit absoluter file-URI registrieren
    resources = []
    for schemafile in basepath.rglob("*-schema.json"):
        try:
            schema = json.loads(schemafile.read_text(encoding="utf-8"))
        except Exception as e:
            return [f"Cannot read schema {schemafile}: {e}"]

        uri = schemafile.resolve().as_uri()
        schema["$id"] = uri  # $id auf absolute URI setzen damit relative $ref auflösbar sind
        resources.append((uri, Resource.from_contents(schema,
                                                      default_specification=DRAFT202012)))

    registry = Registry().with_resources(resources)

    # Zielschema laden
    target_uri = startschemafile.as_uri()
    try:
        resolved = registry.resolver().lookup(target_uri)
        target_schema = resolved.contents
    except Exception as e:
        return [f"Cannot resolve schema '{target_uri}': {e}"]

    # Validieren
    errors = []
    try:
        validator = Draft202012Validator(schema=target_schema, registry=registry)
        for error in validator.iter_errors(struct):
            errors.append(f"{error.message}\n  at: {' -> '.join(str(p) for p in error.absolute_path)}")
    except Exception as e:
        errors.append(f"Validation error: {e}")

    return errors


def validateschema(instance: dict | Path | str,
                    schemafile: str | Path,
                   schemaonly=False) -> list:
    """
    validatemodel the instance of a schemafile in a file against the reference IM-schema

    @param instance:
        filepath of jsonschema to be validated as Path object or as string
        or
        dict() object to be validated
    @param schemafile:
        filepath of reference schemafile to validatemodel against
    @param schemaonly:
        True:   only check json-schema
        False:  check my additional rules as well
    @return:
        errors:  [] ok
        errors [xxx] nok
    """

    if isinstance(instance,dict):
        locinstance=instance
    else:
        locinstance=ValidateJsonModel.readjsonfromfile(instance)

    locschemafile = Path(schemafile).resolve()

    errors = validatestruct(struct=locinstance,
                            startschemafile=locschemafile,
                            basepath=locschemafile.parent.parent)
    if not schemaonly:
        print(f"***** additional checks for json not yet implemented")

    return errors

def normalize_booleans(data):
    """
    changes the obj with all string values "TRUE" "FALSE" in all cases change to True, False
    :param obj: json with all boolean
    :return:
    """
    if isinstance(data, dict):
        return {k: normalize_booleans(v) for k, v in data.items()}
    elif isinstance(data, list):
        # Recursively apply to list items
        return [normalize_booleans(item) for item in data]
    elif isinstance(data, str):
        # Convert string representations to actual Python booleans
        if data.upper() == "TRUE":
            return True
        elif data.upper() == "FALSE":
            return False
    return data

def remove_empty_values(obj):
    """
    removes all empty values (None,'',[],{}) removed from all elements in a json structure

    :param obj: json to be cleansed
    :return: None: passed json object changed
    """
    if isinstance(obj, dict):
        return {
            key: remove_empty_values(value) for key, value in obj.items() if value not in ('', None, [], {})
        }
    elif isinstance(obj, list):
        return [remove_empty_values(item) for item in obj]
    else:
        return obj

def remove_key_from_json(obj, key_to_remove):
    """
    returns a copy of obj with  keys from key_to_remove removed from all elements in a json structure
    the original json structure will not be changed

    :param obj: json to be cleansed
    :param key_to_remove:  name of key to remove
    :return: json object with removed key
    """
    locobj = deepcopy(obj)
    if isinstance(locobj, dict):
        return {
            key: remove_key_from_json(value, key_to_remove)
            for key, value in locobj.items() if key != key_to_remove
        }
    elif isinstance(obj, list):
        return [remove_key_from_json(item, key_to_remove) for item in locobj]
    else:
        return locobj


if __name__ == '__main__':
    pass
