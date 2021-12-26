from _datetime import datetime
import os
import sys

import openpyxl

from IM_db.IM_DB import  openDB, closeDB
from SSOT_infra import parameters, logmessages
from IM_db.IM_OBJECTS import  Interface, Table,Column,Domain,Boolean

SOURCENAME = "IMPORTXLS"


def readtabl(pintfid,ptabname):
    tabl = Table.getbyuk(tabl_intf_id = pintfid,tabl_name=ptabname)
    return tabl

def readcolumn(ptablid, pname):
    colu = Column.getbyuk(colu_tabl_id = ptablid,colu_column_name=pname)
    return colu


def inserttab(ptabname,pintfid, pdescr):
    tabl = Table()
    tabl.tabl_name = ptabname
    tabl.tabl_intf_id = pintfid
    tabl.tabl_descr = pdescr
    tabl.tabl_uc = SOURCENAME
    tabl.tabl_dc = datetime.today()
    tabl.insert()
    return

def insertcolumn(ptabid,pname,pid, pdescr):
    colu = Column()
    colu.colu_column_name = pname
    colu.colu_mandatory = Boolean.FALSE
    colu.colu_descr = pdescr
    colu.colu_doma_id = Domain.getunknown().doma_id
    colu.colu_tabl_id = ptabid
    colu.colu_ext_system_id = pid
    colu.colu_uc = SOURCENAME
    colu.colu_dc = datetime.today()
    colu.insert()
    return

def getintf(pname):
    intf = Interface.getbyuk(intf_name=pname)
    if intf is None:
        logmessages.writelog(f"Interface {pname} not found")
        print(f"Interface {pname} not found")
    return intf


def transfercolumns(pws):
    for rowidx, row in enumerate(pws.values):
        if rowidx == 0:
            intf = getintf(pname=row[0])
            if intf is None: return
        elif rowidx == 1:
            pass  # skip headers
        else:
            if len(row) < 2: continue
            tabname = row[0]
            colname = row[1]
            colid = row[2]
            coldescr = row[3]
            if tabname is None or colname is None:continue
            tabl = readtabl(pintfid=intf.intf_id,ptabname=tabname)
            if tabl is None:
                print(f"Interface {intf.intf_name}, Table {tabname} does not exist")
                continue
            elif readcolumn(ptablid=tabl.tabl_id,pname=colname) is not None:
                continue
            else:
                try:
                    insertcolumn(ptabid=tabl.tabl_id, pname=colname,pid=colid, pdescr=coldescr)
                    print(f"Interface {intf.intf_name}, Table {tabname}, Column {colname} inserted")
                except Exception as exp:
                    logmessages.writelog(f"Table {tabname}, column {colname} could not be inserted")
                    logmessages.writelog(exp)
            #fi
        # fi
    # for
    return

def transfertables(pws):
    for rowidx, row in enumerate(pws.values):
        if rowidx == 0:
            intf = getintf(pname=row[0])
            if intf is None: return
        elif rowidx == 1:
            pass  # skip headers
        else:
            if len(row) < 2: continue
            tabname = row[0]
            tabdescr = row[1]
            if tabname is None :continue
            if readtabl(pintfid=intf.intf_id,ptabname=tabname) is not None:
                continue
            else:
                try:
                    inserttab(ptabname=tabname,pintfid=intf.intf_id, pdescr=tabdescr)
                    print(f"Interface {intf.intf_name}, Table {tabname} inserted")
                except Exception as exp:
                    logmessages.writelog(f"Interface {intf.intf_name}, Table {tabname} could not be inserted")
                    logmessages.writelog(exp)
        # fi
    # for
    return


def excel2db(pwb):
    for ws in pwb.worksheets:
        if ws.title == "Tables":
            transfertables(pws=ws)
        elif ws.title == "Columns":
            transfercolumns(pws=ws)
        else:
            logmessages.writelog(f"Worksheet {ws.title}  ignroed: not in (Tables,Columns)")
            print(f"Worksheet {ws.title}  ignroed: not in (Tables,Columns)")
    return


def main(pparam1, pinfile):
    global workbook
    parameters.initparam(p_callarg=pparam1)
    logmessages.initlog('importDMxls')
    filedirec = parameters.dbDirect()
    if os.path.isfile(pinfile):
        infile = pinfile
    elif os.path.isfile(filedirec + pinfile):
        infile = filedirec + pinfile
    else:
        logmessages.showmessages("File {} not found".format(pinfile))
        return
    # fi
    try:
        workbook = openpyxl.load_workbook(filename=infile)
        openDB(pfilepath=parameters.dbFilePath(), pfks=True)
        excel2db(pwb=workbook)
        closeDB()
    finally:
        logmessages.showmessages(f"XLSX file {infile} imported for model {parameters.modelName()}")
    return


if __name__ == '__main__':
    main(pparam1=sys.argv[1], pinfile=sys.argv[2])
