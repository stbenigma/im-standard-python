import sys,os
from datetime import datetime
from IM_DB import parameters,logmessages,dbConnect
from IM_OBJECTS import Table,TablEntiMap,Column,ColAttrMap, Relation,Entity,Interface,UniqueKeyException
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
            if tab not in tabs: tabs[tab]={"entis":[],"cols":{},"crud":crud if crud == 'NEW' else None}
            if ent is not None:
                #add table mapping
                tabs[tab]["entis"].append((ent,crud if crud == "DELMAP" else None))
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

def inserttablemap(ptabid,pentiid=None,prelaid=None):
    tema = TablEntiMap()
    tema.tema_tabl_id = ptabid
    tema.tema_enti_id = pentiid
    tema.tema_rela_id = prelaid
    try:
        tema.insert(pdoerrhdlng=False)
        return 1
    except Exception as e:
        if type(e) != UniqueKeyException:
            logmessages.writelog("could not insert table-map tabl_id={}, enti_id={}, rela_id={}"
                                 .format(ptabid, pentiid, prelaid))
        return 0
    #try
    return

def printstatline(pname,*args):
    l = pname.ljust(25)
    l += ''.join(str(a).ljust(12) for a in args)
    print (l)
    return

def mergeintodb(pintfname,ptabs):
    tablinsert,tablmapinsert,tablmapdelete = 0,0,0
    intf = Interface.getbyuk(intf_name=pintfname)
    if not intf:
        logmessages.writelog("Interface {} not found.".format(pintfname))
        return
    for tabname,tabmap in ptabs.items():
        #print (pintfname,tabname,tabmap)
        if tabmap["crud"] == 'NEW':
            #insert new table into db
            tabl = Table()
            tabl.tabl_name = tabname
            tabl.tabl_intf_id = intf.intf_id
            tabl.tabl_dc = datetime.today()
            tabl.tabl_uc = "Excel-Map-Import"
            try:
                tabl.insert(pdoerrhdlng=False)
                tablinsert += 1
            except Exception as e:
                if e == UniqueKeyException:
                    print("NEW table {} already exists.".format(tabname))
                    logmessages.writelog("NEW table {} already exists.".format(tabname))
                else:
                    logmessages.writelog("table {} could not be created.".format(tabname))
                    logmessages.writelog("{}".format(e))

        else:
            #search table in DB
            tabl = Table.getbyuk(tabl_name=tabname,tabl_intf_id = intf.intf_id)
        #fi
        for map in tabmap["entis"]:
            mapname,crud = map[0],map[1]
            enti = Entity.getbyuk(enti_name=mapname)
            if enti is None:
                rela = Relation.getbyuk(rela_name =mapname)
                if rela is None:
                    logmessages.writelog("Entity {} .".format(mapname))
                else:
                    if crud == 'DELMAP':
                        tablmapdelete += TablEntiMap.delete(
                            pwhere="tema_tabl_id ={tablid} and tema_rela_id = {relaid}"
                            .format(tablid=tabl.tabl_id, relaid=rela.rela_id))
                    else:
                        tablmapinsert += inserttablemap(ptabid=tabl.tabl_id,prelaid=rela.rela_id)
            else:
                if crud == 'DELMAP':
                    tablmapdelete += TablEntiMap.delete(
                        pwhere="tema_tabl_id ={tablid} and tema_enti_id = {entiid}"
                        .format(tablid=tabl.tabl_id, entiid=enti.enti_id))
                else:
                    tablmapinsert += inserttablemap(ptabid=tabl.tabl_id, pentiid=enti.enti_id)
        #for
    # for
    printstatline(pintfname,tablinsert,tablmapinsert,tablmapdelete,0,0,0)
    return

def main(param1,pxls):
    parameters.initparam(p_callarg=param1)
    logmessages.initlog('importEXCEL')
    filename = parameters.modelName()
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
        printstatline("Interface","tab-insert","tab-mapins","tab-mapdel","col-ins","col-mapins","col-mapdel")
        for ws in workbook.worksheets:
            if ws.title== 'Overview': continue
            interface = importintf(ws)
            mergeintodb(pintfname=ws.title,ptabs=interface)
        #for
        dbConnect.getdbcon().commit()
        dbConnect.closeDB()
    except Exception as exp:
        print (exp)
    finally:
        print ("file {} imported into model {}".format(infile,filename))
        logmessages.showmessages()
        return

if __name__ == '__main__':
    main(param1=sys.argv[1],pxls = sys.argv[2])
