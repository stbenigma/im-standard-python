import logging
import os
import json
from pathlib import Path
from jsonschema import Draft7Validator, RefResolver, validate, SchemaError,protocols

from IM_STANDARD import nvl

def purevalidate(tovalidatejs, validattionjs, resolver, verbose=True):
    """
    :param tovalidatejs: json struct to be validatd
    :param validattionjs:  json-schema to validate against
    :param resolver:  resolver path for referenced sub schemas
    :param verbose: True add source of problem to logging
    :return:  True if ok
            False if not ok  + errorlog if verbose
    """
    try:
        validator = Draft7Validator(schema=validattionjs,
                                               resolver=resolver)

        validator.validate(tovalidatejs)
    except protocols.ValidationError as ve:
        error = ve.message
        if verbose:
            fullstr = str(ve)
            error += '\n'
            error += fullstr[fullstr.find("On instance"):]
            logging.error(error)
        return False
        #
    except Exception as ex:
        try:
            error = ex.message
        except Exception:
            error = ex.args[0]

        logging.error(error)
        return False
    return True

def validate_json_as_schema(schema: dict):
    META_SCHEMA_URI = "https://json-schema.org/draft/2020-12/schema"
    """
    Prüft, ob eine gegebene JSON-Datei ein gültiges JSON Schema (Draft 2020-12) ist.
    """
    try:
        # 2. Lade das Meta-Schema (optional, da jsonschema die URI oft selbst auflösen kann)
        # In den meisten Umgebungen kann jsonschema das Meta-Schema über die URI abrufen.
        # Wenn Sie offline arbeiten, müssen Sie es möglicherweise manuell laden.

        # 3. Validierung des Dokuments gegen das Meta-Schema
        # Wir verwenden das Meta-Schema als Schema, um das Dokument (das Schema sein soll) zu prüfen.

        # Die 'validate'-Funktion verwendet automatisch das Meta-Schema, das im
        # '$schema'-Feld des Dokuments angegeben ist (oder die übergebene URI).
        validate(
            instance=schema,
            # Hier verwenden wir die URI des Meta-Schemas.
            schema={"$ref": META_SCHEMA_URI}
        )

    except json.JSONDecodeError as e:
        print(f"❌ Fehler: Ungültiges JSON-Format in der Datei: {e}")
        raise e
    except SchemaError as e:
        # Dies fängt Fehler ab, wenn das META_SCHEMA_URI selbst ungültig wäre (sehr unwahrscheinlich).
        print(f"❌ Interner Fehler: Das Meta-Schema ist selbst ungültig: {e}")
        raise e
    except Exception as e:
        # Dies fängt ValidationErrors ab, wenn das Dokument das Meta-Schema verletzt.
        print(f"❌  '{schema}' ist KEIN gültiges JSON Schema.")
        print(f"Validierungsfehler: {e}")
        raise e

    return

def validate_jsonfile_as_schema(json_file_path: str):
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            document_to_validate = json.load(f)
        validate_json_as_schema(schema=document_to_validate)

    except FileNotFoundError as ex:
        print(f"❌ Fehler: Datei nicht gefunden unter {json_file_path}")
        raise ex
    return

class ValidateJsonModel:
    """
    Validates a json schemafile of an information model against the definition of
    jsonschema of the information model
    """

    def __init__(self, referenceschemapath):
        self.referencefilepath = referenceschemapath
        self.refschemajs = self.readjsonfromfile(filepath=self.referencefilepath)
        # base uri for files referefencedin the refschemajs
        self.resolver = self.getresolver(basefile=str(self.referencefilepath),
                                         curjson=self.refschemajs,
                                         referencepath=self._schemareferences(self.referencefilepath.parent)
                                         )
        # jsonschema.validators.RefResolver(base_uri="file://" + str(self.referencefilepath),
        #                                            referrer=self.refschemajs,
        #                                            store=self.resolverschema(referencepath=referenceschemapath)
        #                                            )
        # check the refschema for errors
        protocols.Validator.check_schema(self.refschemajs)
        self.model = None
        return

    @staticmethod
    def getresolver(basefile, curjson, referencepath):
        """get the resolver for local file references for this json"""
        # base uri for files referefencedin the refschemajs
        base_uri = "file://" + str(basefile)
        return RefResolver(base_uri=base_uri,
                           referrer=curjson,
                           store=referencepath
                           )

    def _schemareferences(self, schemapath):
        retval = {}
        with os.scandir(schemapath) as schemata:
            for schema in schemata:
                if schema.name.endswith("-schema.json"):
                    with open(schema) as infile:
                        injson = json.load(infile)
                    retval[schema.name] = injson
        return retval

    @staticmethod
    def readjsonfromfile(filepath: Path):
        with open(filepath) as infile:
            myschemajs = json.load(fp=infile)
        return myschemajs

    def uniquenames(self, elements, verbose):
        def find_duplicates(input_list):
            duplicates = set()
            for item in input_list:
                if input_list.count(item) > 1:
                    duplicates.add(item)
            return list(duplicates)

        if self.model.modelismultilingual():
            for lang in self.model.languages:
                duplicates = find_duplicates([self.model.mlvalue(elem.get("name"), lang) for elem in nvl(elements, [])])
                if len(duplicates) > 0:
                    #if verbose: logging.error(f"Duplicate name (in any language) in {duplicates}")
                    return [f"Duplicate name (in any language) in {duplicates}"]
        else:
            duplicates = find_duplicates([elem.get("name") for elem in nvl(elements, [])])
            if len(duplicates) > 0:
                #if verbose: logging.error(f"Duplicate name in {duplicates}")
                return [f"Duplicate name in {duplicates}"]

        return []

    @staticmethod
    def listUnique(x):
        """True if sorted lists in list are unique"""
        seen = list()
        return not any(sorted(i) in seen or seen.append(sorted(i)) for i in x)

    def _checkadditionalrules(self, verbose=True):
        errors=[]
        # validate the additional rules, not covered by the model itself.
        myschema = self.model
        if self.model is None:
            return errors

        # model spanning rules
        relaids = [e["elementid"] for e in myschema.getelementinstances(elementname="Relations")]
        domainids = [e.get("elementid") for e in myschema.getelementinstances(elementname="Domains")]
        buruids = [e["elementid"] for e in myschema.getelementinstances(elementname="BusinessRules")]
        entityids = [e.get("elementid") for e in myschema.getelementinstances(elementname="Entities")]
        attrids = [e["elementid"] for e in myschema.getelementinstances(elementname="Attributes")]
        domaattrids = [e.get("elementid")
                       for elems in [doma.get("elements", [])
                                     for doma in myschema.getelementinstances(elementname="Domains")]
                       for e in elems]
        tableids = [e.get("elementid") for e in myschema.getelementinstances(elementname="Tables")]
        columnids = [e.get("elementid") for e in myschema.getelementinstances(elementname="Columns")]
        catgids = [e.get("elementid") for e in myschema.getelementinstances(elementname="Categories")]

        # Many  names must be unique in all languages
        errors += self.uniquenames(elements=myschema.getelementinstances(name="Entities"),
                                   verbose=verbose)

        # all businessrule id's must be unique over the model
        if len(buruids) > len(set(buruids)):
            #if verbose: logging.error(f"Duplicate businessrule-id's in model")
            errors.append(f"Duplicate businessrule-id's in model")

        # all entity id's must be unique over the model
        if len(entityids) > len(set(entityids)):
            #if verbose: logging.error(f"Duplicate entity-id's in model")
            errors.append(f"Duplicate entity-id's in model")

        # all attribute id's must be unique over all entities
        if len(attrids) > len(set(attrids)):
            #if verbose: logging.error(f"Duplicate attribute-id's in model")
            errors.append(f"Duplicate attribute-id's in model")

        # all column id's must be unique over all tables
        if len(columnids) > len(set(columnids)):
            #if verbose: logging.error(f"Duplicate Column-id's in model")
            errors.append(f"Duplicate Column-id's in model")

        # all relation id's must be unique
        if len(relaids) > len(set(relaids)):
            #if verbose: logging.error(f"Duplicate relation-id's in model")
            errors.append(f"Duplicate relation-id's in model")
            # relationships must be unique (assoc and entities)
            relationskeys = [[rela.get("fwd").get("entityid") + "-"
                              + rela.get("bwd").get("entityid") + "-"
                              + nvl(myschema.mlvalue(rela.get("fwd").get("assoctext")), lang)
                              for lang in myschema.languages
                              ]
                             for rela in myschema.getelementinstances(name="Relations")
                             ] + \
                            [[rela.get("bwd").get("entityid") + "-"
                              + rela.get("fwd").get("entityid") + "-"
                              + nvl(myschema.mlvalue(rela.get("bwd").get("assoctext")), lang)
                              for lang in myschema.languages
                              ]
                             for rela in myschema.getelementinstances(name="Relations")
                             ]
            if not self.listUnique(relationskeys):
                #if verbose: logging.error(f"Duplicate relations (enti-enti-multilangassoctext) in model")
                errors.append(f"Duplicate relations (enti-enti-multilangassoctext) in model")

        # rules within domains
        for doma in myschema.getelementinstances(name="Domains"):
            # categories exist
            if doma.get("categoryid") is not None and doma.get("categoryid") not in catgids:
                #if verbose: logging.error(f"Category-id {doma.get('categoryid')} not in categories")
                errors.append(f"Category-id {doma.get('categoryid')} not in categories")
            # all referenced domains (in groupdomains) must exist in the domainlist
            if doma.get("domaintype") == "GroupDomain":
                for elem in doma.get("elements", []):
                    domainid = elem.get("domainid")
                    if domainid is not None and domainid not in domainids:
                        #if verbose: logging.error(
                        #    f"Domain {elem.get('domainid')} of groupdomain {doma.get('elementid')} not found.")
                        errors.append(f"Domain {elem.get('domainid')} of groupdomain {doma.get('elementid')} not found.")

        # rules for categories
        if len(catgids) > len(set(catgids)):
            #if verbose: logging.error(f"Duplicate Category-id's in model")
            errors.append(f"Duplicate Category-id's in model")

        for catg in myschema.getelementinstances(name="Categories"):
            # name must have a value in the main mainlanguage
            if not (type(catg.get("name")) is str or myschema.mainlang in catg.get("name")):
                #if verbose: logging.error(f"No name in main language in category {catg.get('name')}")
                errors.append(f"No name in main language in category {catg.get('name')}")

        # rules within entities
        for enti in myschema.getelementinstances(name="Entities"):
            # categories exist
            if enti.get("categoryid") is not None and enti.get("categoryid") not in catgids:
                #if verbose: logging.error(f"Category-id {enti.get('categoryid')} not in categories")
                errors.append(f"Category-id {enti.get('categoryid')} not in categories")

            # name must have a value in the main mainlanguage
            if not (type(enti.get("name")) is str or myschema.mainlang in enti.get("name")):
                #if verbose: logging.error(f"No name in main language in entity {enti.get('name')}")
                errors.append(f"No name in main language in entity {enti.get('name')}")

            # rules for synonyms
            # all synonyms must have a value in the main mainlanguage
            synos = enti.get("synonyms", [])
            if not (all([(type(syno) == str or myschema.mainlang in syno) for syno in synos])):
                #if verbose: logging.error(f"Missing synonym name in main language in entity {enti.get('name')}")
                errors.append(f"Missing synonym name in main language in entity {enti.get('name')}")

            # synonyms names must be unique in all languages within an entity
            if self.model.modelismultilingual() and not self.listUnique([[myschema.mlvalue(syno, lang)
                                                                     for lang in myschema.languages
                                                                     ] for syno in synos
                                                                    ]):
                #if verbose: logging.error(f"Duplicate synonym in entity {enti.get('name')}")
                errors.append(f"Duplicate synonym in entity {enti.get('name')}")

            entyattrs = [attr for attr in myschema.getelementinstances(name="Attributes") if
                         attr.get("parentid") == enti.get("elementid")]
            # attribute names must be unique in all languages within an entity
            attrnames = [[myschema.mlvalue(attr.get("name"), lang)
                          for lang in myschema.languages
                          ] for attr in entyattrs
                         ]
            if not self.listUnique(attrnames):
                #if verbose: logging.error(f"Duplicate multimultilang attributename in entity {enti.get('name')}")
                errors.append(f"Duplicate multimultilang attributename in entity {enti.get('name')}")

        # rules for attributes
        for attr in myschema.getelementinstances(name="Attributes"):
            # attribute parent must be entity
            if attr.get("parentid") not in entityids:
                #if verbose: logging.error(
                #    f"Entity {attr.get('parentid')} in attribute {attr.get('elementid')} not found.")
                errors.append(f"Entity {attr.get('parentid')} in attribute {attr.get('elementid')} not found.")

            # all attributes must have a value in the main mainlanguage
            if not (type(attr.get("name")) == str or myschema.mainlang in attr.get("name")):
                #if verbose: logging.error(
                #    f"Missing attribute name {attr.get('name')} in main language in entity {enti.get('name')}")
                errors.append(f"Missing attribute name {attr.get('name')} in main language in entity {enti.get('name')}")

            # all referenced domains must exist in the domainlist
            domaid = attr.get("domainid")
            if domaid is not None and domaid not in domainids:
                #if verbose: logging.error(
                #    f"Domain {domaid} in attribute {attr.get('elementid')} not found.")
                errors.append(f"Domain {domaid} in attribute {attr.get('elementid')} not found.")

        # rules for relationships
        for rela in myschema.getelementinstances(name="Relations"):
            if myschema.modeltype == "Information model":
                # all referenced entities must exist
                if rela.get("fwd").get("entityid") not in entityids:
                    #if verbose: logging.error(
                    #    f"Entity {rela.get('fwd').get('entityid')} in relation {rela.get('elementid')} not found.")
                    errors.append(f"Entity {rela.get('fwd').get('entityid')} in relation {rela.get('elementid')} not found.")

                if rela.get("bwd").get("entityid") not in entityids:
                    #if verbose: logging.error(
                    #    f"Entity {rela.get('bwd').get('entityid')} in relation {rela.get('elementid')} not found.")
                    errors.append(f"Entity {rela.get('bwd').get('entityid')} in relation {rela.get('elementid')} not found.")

                # relationship types require specific end-properties
                if rela.get("relationtype") == "M:1" \
                        and (rela.get("fwd").get("cardinality")
                             == rela.get("bwd").get("cardinality")):
                    #if verbose: logging.error(
                    #    f"Functional relationship must have 1 at one end in relationship {rela.get('elementid')}")
                    errors.append(f"Functional relationship must have 1 at one end in relationship {rela.get('elementid')}")
                if rela.get("relationtype") == "M:N" \
                        and (rela.get("fwd").get("cardinality") == "1"
                             or rela.get("bwd").get("cardinality") == "1"):
                    #if verbose: logging.error(
                    #    f"M:N relationship must have M a both ends in relationship {rela.get('elementid')}")
                    errors.append(f"M:N relationship must have M a both ends in relationship {rela.get('elementid')}")
                if rela.get("relationtype") == "1:1" \
                        and (rela.get("fwd").get("cardinality") == "M"
                             or rela.get("bwd").get("cardinality") == "M"):
                    #if verbose: logging.error(
                    #    f"1:1 relationship must have 1 a both ends in relationship {rela.get('elementid')}")
                    errors.append(f"1:1 relationship must have 1 a both ends in relationship {rela.get('elementid')}")
                if rela.get("relationtype") == "ROLE" \
                        and (rela.get("fwd").get("cardinality") == "M"
                             or rela.get("bwd").get("cardinality") == "M"
                             or (rela.get("fwd").get("mandatory") ==
                                 rela.get("bwd").get("mandatory"))
                ):
                    #if verbose: logging.error(
                    #    f"ROLE relationship must have 1 a both ends in relationship {rela.get('elementid')}")
                    errors.append(f"ROLE relationship must have 1 a both ends in relationship {rela.get('elementid')}")
                if rela.get("relationtype") == "SUBTYPE" \
                        and (rela.get("fwd").get("cardinality") == "M"
                             or rela.get("bwd").get("cardinality") == "M"
                             or rela.get("fwd").get("mandatory") is False
                             or rela.get("bwd").get("mandatory") == False
                             or (rela.get("fwd").get("arcnumber") is None
                                 and rela.get("bwd").get("arcnumber") is None)
                ):
                    #if verbose: logging.error(
                    #    f"SUBTYPE relationship must have 1 a both ends in relationship {rela.get('elementid')}")
                    errors.append(f"SUBTYPE relationship must have 1 a both ends in relationship {rela.get('elementid')}")

            elif myschema.modeltype == "Data model":
                # all referenced entities must exist
                if rela.get("fwd").get("tableid") not in tableids:
                    #if verbose: logging.error(
                    #    f"Table {rela.get('fwd').get('tableid')} in relation {rela.get('elementid')} not found.")
                    errors.append(f"Table {rela.get('fwd').get('tableid')} in relation {rela.get('elementid')} not found.")
                if rela.get("bwd").get("tableid") not in tableids:
                    #if verbose: logging.error(
                    #    f"Table {rela.get('bwd').get('tableid')} in relation {rela.get('elementid')} not found.")
                    errors.append(f"Table {rela.get('bwd').get('tableid')} in relation {rela.get('elementid')} not found.")
                # all referenced columns must exist
                for direc in ("fwd", "bwd"):
                    for c in rela.get(direc).get("fkcolumns", []):
                        if c not in columnids:
                            #if verbose: logging.error(f"Column {c} in relation {rela.get('elementid')} not found.")
                            errors.append(f"Column {c} in relation {rela.get('elementid')} not found.")

        # rules for businessrules
        for buru in myschema.getelementinstances(name="BusinessRules"):
            # all referenced objects must exist
            for elem in buru.get("restrictedElements"):
                if elem not in domaattrids + attrids + relaids + entityids + domainids:
                    #if verbose: logging.error(f"ID {elem} in businessrule {buru.get('elementid')} not found.")
                    errors.append(f"ID {elem} in businessrule {buru.get('elementid')} not found.")

        return errors

    def purevalidate(self, tovalidatejs, validattionjs, resolver, verbose=True):
        """
        :param tovalidatejs: json struct to be validatd
        :param validattionjs:  json-schema to validate against
        :param resolver:  resolver path for referenced sub schemas
        :param verbose: True add source of problem to logging
        :return:  None if no errors
                errormessage else
        """
        error = []
        try:
            validator = Draft7Validator(schema=validattionjs,
                                                   resolver=resolver)

            validator.validate(tovalidatejs)
        except protocols.ValidationError as ve:
            errormsg = ve.message
            if verbose:
                fullstr = str(ve)
                errormsg += '\n'
                errormsg += fullstr[fullstr.find("On instance"):]
            error.append(errormsg)
        except Exception as ex:
            try:
                error.append(ex.message)
            except Exception:
                error.append(ex.args[0])
        return error

    def validateschemaonly(self, instance, verbose=False) -> int:
        """

        @param instance:
            dict or path to json file to be validated against my schemafile
        @return:
            errcnt: 0-> success
                    >0 -> errors
        """

        error = []
        jsmodel = instance if type(instance) is dict \
            else self.readjsonfromfile(filepath=Path(instance))


        error += self.purevalidate(tovalidatejs=jsmodel,
                                      validattionjs=self.refschemajs,
                                      resolver=self.resolver,
                                      verbose=verbose)
        return error

    def validatemodel(self, instance, verbose=False) -> int:
        """
        @param instance:
            dict or path to json file to be validated against my schemafile
        @return:
            [] : success
            []: failure
                   list of errors
        """
        # TODO errors with my own logging-instance
        errors = []
        errors += self.validateschemaonly(instance=instance, verbose=verbose)
        errors += self._checkadditionalrules(verbose=verbose)
        return errors

def validateschema(instance,
                   schemafile,
                   verbose=False,
                   schemaonly=False) -> bool:
    """
    validatemodel the instance of an informationmodel schemafile in a file against the json-schemafile of the informationmodel

    @param instance:
        filepath of jsonschema to be validated as Path object or as string
        or
        dict() object to be validated
    @param schemafile:
        filepath of reference schemafile to validatemodel the instance to
        default the version of the schemafile in this development environment
    @param schemaonly:
        True:   only check json-schema
        False:  check my additional rules as well
    @return:
        errors:  [] ok
        errors [xxx] nok
    """

    mymodel = ValidateJsonModel(referenceschemapath=schemafile)
    if schemaonly:
        errors = mymodel.validateschemaonly(instance=instance,
                                            verbose=verbose)
    else:
        errors = mymodel.validatemodel(instance=instance,
                                       verbose=verbose)

    return errors


def remove_key_from_json(obj, key_to_remove):
    if isinstance(obj, dict):
        return {
            key: remove_key_from_json(value, key_to_remove)
             for key, value in obj.items() if key != key_to_remove
        }
    elif isinstance(obj, list):
        return [remove_key_from_json(item, key_to_remove) for item in obj]
    else:
        return obj


if __name__ == '__main__':
    pass