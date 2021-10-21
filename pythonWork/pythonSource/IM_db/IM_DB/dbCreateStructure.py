# -*- coding: latin-1 -*-
from IM_DB import dbDDL,dbConnect
from pathlib import Path

def applysqlscript(psqlfilepath):
    sqltxt = Path(psqlfilepath).read_text()
    dbDDL.execscript(psql=sqltxt)
    return
