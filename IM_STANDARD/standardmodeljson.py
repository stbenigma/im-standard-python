import json
from pathlib import Path

from IM_STANDARD import IMSTANDARDPATH
from IM_STANDARD.jsonvalidation import validate_jsonfile_as_schema  # local due to recusrive import


class StandardJsonModel:
    DEFAULTLANGUAGE = "en"
    SCHEMADEFPATH = IMSTANDARDPATH / "Model" / "im-standard-schema"

    def __init__(self, modelfilepath):
        self._schema = self.loadjsonfile(path=modelfilepath)

    @staticmethod
    def loadjsonfile(path: Path):
        with open(path, "r", encoding="utf-8") as infile:
            return json.load(infile)

    @staticmethod
    def dumpjsonfile(struct: dict | list | None,
                     path: Path,
                     verbose=False,
                     ensure_ascii=False):
        """
        writes a json to file
        :param struct: json-strcture
        :param path: path to write
        :param verbose: print success-message with path
        :param ensure_ascii: True: make sure all special characters are escaped Ü = \u00dc
                             False: write Ü
        :return:
        """
        with open(path, "w", encoding='utf-8') as outfile:
            json.dump(struct, outfile, indent=2,ensure_ascii=ensure_ascii)
            if verbose:
                print(f"json written to: '{path}'")

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
    IMDEFINITIONFILEPATH = StandardJsonModel.SCHEMADEFPATH / "InformationModel" / "InformationModel-schema.json"

    def __init__(self):
        super().__init__(modelfilepath=self.IMDEFINITIONFILEPATH)
        # make sure, my reference is a correct json-schema
        validate_jsonfile_as_schema(json_file_path=str(self.IMDEFINITIONFILEPATH))


class DMStandardJsonModel(StandardJsonModel):
    DMDEFINITIONFILEPATH = StandardJsonModel.SCHEMADEFPATH / "DataModel" / "DataModel-schema.json"

    def __init__(self):
        super().__init__(modelfilepath=self.DMDEFINITIONFILEPATH)
        # make sure, my reference is a correct json-schema
        validate_jsonfile_as_schema(json_file_path=str(self.DMDEFINITIONFILEPATH))
