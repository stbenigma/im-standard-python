"""Infrastructure for SSOT

Functionality usable in any other module: see python files

Version file of current release
- versions.json
"""

from .nvl import nvl, nvl2  # publish low level functions directly in Module
from .translateprompt import transl,settransldomain,resettransldomain
