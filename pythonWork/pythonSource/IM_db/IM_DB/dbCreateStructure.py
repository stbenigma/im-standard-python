# -*- coding: latin-1 -*-
from pathlib import Path

from IM_DB import dbDDL


def applysqlscript(psqlfilepath):
    sqltxt = Path(psqlfilepath).read_text()
    dbDDL.execscript(psql=sqltxt)
    return
