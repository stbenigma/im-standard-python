import sys,os

from IM_DB import parameters,logmessages,dbConnect
from IM_OBJECTS import Table,TablEntiMap,Column,ColAttrMap, Relation,Entity,Interface
from openpyxl import load_workbook

def importintf(pws):
    tabs = {}
    """tabs= {<tabname>:{"entis":[entitiy,],"cols":{<colname>:[(entity,attribute,None|DELMAP),]},"crud":None|NEW}}"""
    curtab = None
    for rowidx,row in enumerate(pws):
        if rowidx == 0:continue
        tab,col,ent,attr = row[0].value,row[1].value,row[2].value,row[3].value,
        crud = row[4].value if len (row)> 4 else None
        assert crud in (None,"NEW","DELMAP"), "illegal Value for CRUD '{}'".format(crud)
        if tab is not None:
            curtab = tab
            if tab not in tabs: tabs[tab]={"entis":[],"cols":{},"crud":crud}
            if  ent is not None:
                #add table mapping
                tabs[tab]["entis"].append(ent)
        else:
            if curtab is None : continue
            #do columnmappings
            cols = tabs[curtab]["cols"]
            if col not in cols: cols[col]=[]
            if attr is None or ent is None: continue
            cols[col].append((ent,attr,crud))
        #fi
    #for
    return tabs

def mergeintodb(pintfname,ptabs):
    intf = Interface.getbyuk(intf_name=pintfname)
    if not intf:
        logmessages.writelog("Interface {} not found.".format(pintfname))
        return
    for tabname,tabmap in ptabs.items():
        #print (pintfname,tabname,tabmap)
        if tabmap["crud"] == 'NEW':
            #insert new table into db
            tabl = Table()
        else:
            #search table in DB
            pass
        #fi
    #for
    return

def main(param1,pxls):
    parameters.initparam(p_callarg=param1)
    logmessages.initlog('importEXCEL')
    filename = parameters.odmModelName()
    filepath = parameters.dbDirect()
    if os.path.isfile(pxls):
        infile = pxls
    elif os.path.isfile(filepath + pxls):
        infile = filepath + pxls
    else:
        logmessages.showmessages("File {} not found".format(pxls))
        return
    #fi
    try:
        workbook = load_workbook(filename=infile)
        dbConnect.openDB(pfilepath=parameters.dbFilePath(),pfks="ON")
        for ws in workbook.worksheets:
            if ws.title== 'Overview': continue
            interface = importintf(ws)
            mergeintodb(pintfname=ws.title,ptabs=interface)
        #for
        dbConnect.closeDB()
    except Exception as exp:
        print (exp)
    finally:
        print ("file {} imported into model {}".format(infile,filename))
        return

if __name__ == '__main__':
    main(param1=sys.argv[1],pxls = sys.argv[2])
