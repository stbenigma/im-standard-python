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

from .jsonelements import JsonElement
from .myjsonschema import ElementId,JsonSchema
from .standardmodeljson import StandardJsonModel,IMStandardJsonModel
from .jsonvalidation import ValidateJsonModel,validateschema,remove_key_from_json


