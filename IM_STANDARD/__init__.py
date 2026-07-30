def nvl(v,d=""):
    """
    returns value v if it is not None
    else retuns the default value d
    """
    return v if v is not None else d

def alwayslist(x):
        """
        :param x: element to be converted into list
        :return: [] if x is None
                x if type(x) is list
                list(x) else
        """
        if x is None:
            return []
        elif type(x) == list:
            return x
        else:
            return [x]

def version() -> dict:
    from pathlib import Path
    import yaml
    version_file = Path(__file__).parent / 'versions.yaml'
    assert version_file.is_file(), f"Cannot read version file {version_file}"
    with open(version_file, 'r') as src:
        ver = yaml.safe_load(src)
        return ver

__version__ = version()
from pathlib import Path
IMSTANDARDPATH = Path(__file__).parent.parent.parent / "Information-model-standard"

from IM_STANDARD.SQL import *
from .jsonelements import JsonElement,model2json
from .myjsonschema import ElementId,JsonSchema,StandardSchema,json2timestamp
from .standardmodeljson import StandardJsonModel, IMStandardJsonModel, DMStandardJsonModel, \
        normalize_booleans, remove_empty_values, remove_key_from_json

from .jsonvalidation import ValidateJsonModel, validateschema, validatestruct, ImStandardGithub
from .genjsonschema import generatejsonschema,JsonExample,Json2JsonSchema
from .sql2imstandard import Sql2IMowlschema,Sql2IMJson,Sql2IMJsonschema
from .imstandard2sql import Standardmodel2SQLdatabase




