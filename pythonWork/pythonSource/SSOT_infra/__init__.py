"""Infrastructure for SSOT

Functionality usable in any other module: see python files

Version file of current release
- versions.json
"""

from .nvl import nvl, nvl2  # _publishable low level functions directly in Module
from .translateprompt import transl, settransldomain, resettransldomain
from .hex import hex2int,int2hex
