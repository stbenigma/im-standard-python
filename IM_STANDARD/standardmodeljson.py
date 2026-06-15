import json
from pathlib import Path

from IM_STANDARD.jsonvalidation import validate_jsonfile_as_schema  # local due to recusrive import
from IM_STANDARD import StandardSqlModel


class StandardJsonModel:

    def __init__(self, modelfilepath):
        self._schema = self._loadjsonfile(path=modelfilepath)

    @staticmethod
    def _loadjsonfile(path: Path):
        with open(path) as infile:
            return json.load(infile)

    @property
    def schema(self):
        return self._schema

    # Standard functions for json-schema-handling
    def inschema(self, componentname: str) -> bool:
        """
        :param componentname: name of component object to find
        :return: true if component is schemas main object (according to $id
                        or if component is in "components/schemas"
                        or if component is in "components/$defs"
                false: else
        """
        components = self.schema.get("components", dict())
        return ((self.schema.get("$id", "").startswith(componentname + "-schema"))
                or (componentname in components.get("schemas", dict()))
                or (componentname in components.get("$defs", dict())))

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
            comps = self.schema.get("components", dict())
            comp = comps.get("schemas", dict()).get(componentname)
            if comp is None:
                comp = comps.get("$defs", dict()).get(componentname)
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
    DEFAULTLANGUAGE = "en"
    IMDEFINITIONFILEPATH =StandardSqlModel.SCHEMADEFPATH /"Model"/"im-standard-schema" /"InformationModel" / "InformationModel-schema.json"

    def __init__(self):
        super().__init__(modelfilepath=self.IMDEFINITIONFILEPATH)
        # make sure, my reference is a correct json-schema
        validate_jsonfile_as_schema(json_file_path=str(self.IMDEFINITIONFILEPATH))


class DMStandardJsonModel(StandardJsonModel):
    DEFAULTLANGUAGE = "en"
    DMDEFINITIONFILEPATH = StandardSqlModel.SCHEMADEFPATH /"Model"/"im-standard-schema" / "DataModel" / "DataModel-schema.json"

    def __init__(self):
        super().__init__(modelfilepath=self.DMDEFINITIONFILEPATH)
        # make sure, my reference is a correct json-schema
        validate_jsonfile_as_schema(json_file_path=str(self.DMDEFINITIONFILEPATH))

