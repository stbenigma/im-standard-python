import json
from copy import deepcopy
from pathlib import Path

from IM_STANDARD.jsonvalidation import  ImStandardGithub,validate_json_as_schema  # local due to recusrive import

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


class StandardJsonModel:
    DEFAULTLANGUAGE = "en"
    #SCHEMADEFPATH = IMSTANDARDPATH / "Model" / "im-standard-schema"

    def __init__(self, modeljson):
        self._schema = modeljson

    @staticmethod
    def dumpjsonfile(struct: dict | list | None,
                     outpath: Path,
                     verbose=False,
                     ensure_ascii=False):
        """
        writes a json to file
        :param struct: json-strcture
        :param outpath: path to write
        :param verbose: print success-message with path
        :param ensure_ascii: True: make sure all special characters are escaped Ü = \u00dc
                             False: write Ü
        :return:
        """
        with open(outpath, "w", encoding='utf-8') as outfile:
            json.dump(struct, outfile, indent=2,ensure_ascii=ensure_ascii)
            if verbose:
                print(f"json written to: '{outpath}'")
        return

    @property
    def schema(self):
        return self._schema

    # Standard functions for json-schema-handling
    def inschema(self, componentname: str) -> bool:
        """
        :param componentname: name of object to find
        :return: true if component is schemas main object (according to $id
                        or if component is in "$defs"
                false: else
        """
        return ((self.schema.get("$id", "").startswith(componentname + "-schema"))
                or (componentname in self.schema.get("$defs", dict())))

    def getcomponent(self, componentname) -> dict:
        """

        :param self: the schema to search
        :param componentname:  name of the component (object) to return
        :return: component with this name (top level, in components/schemas or  in components/$defs
                None if component was not found
        """
        if self.schema.get("$id", "").startswith(componentname + "-schema"):
            # component is top level object
            comp = self.schema
        else:
            comp = self.schema.get("$defs", dict()).get(componentname, dict())
        return comp

    def getproperties(self, componentname) -> dict:
        """
        :param componentname:
        :return: "properties of component
                empty dict if component was not found
        """
        if self.inschema(componentname):
            return self.getcomponent(componentname).get("properties", dict())
        else:
            return dict()


class IMStandardJsonModel(StandardJsonModel):
    #IMDEFINITIONFILEPATH = StandardJsonModel.SCHEMADEFPATH / "InformationModel" / "InformationModel-schema.json"

    def __init__(self):
        super().__init__(modeljson=ImStandardGithub.getimstdschema())
        # make sure, my reference is a correct json-schema
        validate_json_as_schema(schema=super().schema)


class DMStandardJsonModel(StandardJsonModel):
    #DMDEFINITIONFILEPATH = StandardJsonModel.SCHEMADEFPATH / "DataModel" / "DataModel-schema.json"

    def __init__(self):
        super().__init__(modeljson=ImStandardGithub.getdmstdschema())
        # make sure, my reference is a correct json-schema
        validate_json_as_schema(schema=super().schema)


