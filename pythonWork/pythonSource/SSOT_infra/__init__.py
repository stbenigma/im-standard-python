"""Infrastructure for SSOT

Functionality usable in any other module: see python files

Version file of current release
- versions.json
"""

from .nvl import nvl, nvl2  # _publishable low level functions directly in Module
from .translateprompt import transl, settransldomain, resettransldomain
from .hex import hex2int,int2hex
from .mydatetime import DEFAULTDATETIMEFORMAT,todatetime
from .parameters import Parameter,parameter


def version() -> dict:
    from pathlib import Path
    import json
    version_file = Path(Path(__file__).parent, 'versions.json')
    assert version_file.is_file(), f"Cannot read version file {version_file}"
    with open(version_file, 'r') as src:
        ver = json.load(src)
        return ver


__version__ = version()
