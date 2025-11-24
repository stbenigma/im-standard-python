def nvl(v,d=""):
    """
    returns value v if it is not None
    else retuns the default value d
    """
    return v if v is not None else d

from .jsonelements import *
from .myjsonschema import *
from .standardmodeljson import *
from .jsonvalidation import *


