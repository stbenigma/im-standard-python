# -*- coding: latin-1 -*-
from pathlib import Path

from IM_DB import dbDDL

def applysqlscript(psqlfilepath):
    """
    creates the sqlite dbstructure out of psqlfilepath in the already open Databas
    """
    sqltxt = Path(psqlfilepath).read_text()
    dbDDL.execscript(psql=sqltxt)
    return
