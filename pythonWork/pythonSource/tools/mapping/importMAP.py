import sys,os
from SSOT_db.SQL_INFRA import  dbConnect
from SSOT_infra import parameters, logmessages
from SSOT_db.IM_OBJECTS import  Table,TablEntiMap,Column,ColAttrMap, Relation,Entity,Attribute,Interface,UniqueKeyException
from openpyxl import load_workbook

def importintf(pws):
    tabs = {}
    """copy excel-sheet into a json-structure"""
    """tabs= {<tabname>:{"entis":[(entitiy,None|DELMAP),],"cols":{<colname>:[(entity,attribute,None|DELMAP),]}}"""
    curtab = None
    for rowidx,row in enumerate(pws):
        if rowidx == 0:continue
        tab,col,ent,attr = row[0].value,row[1].value,row[2].value,row[3].value,
        crud = row[4].value if len (row)> 4 else None
        assert crud in (None,"DELMAP"), "illegal Value for CRUD '{}'".format(crud)
        if tab is not None:
            curtab = tab #use for empty tab-entry with columns
            if tab not in tabs: tabs[tab]={"entis":[],"cols":{},"crud":crud}
            if ent is not None:
                #add table mapping
                tabs[tab]["entis"].append((ent,crud))
        else:
            if curtab is None : continue
            #do columnmappings
            cols = tabs[curtab]["cols"]
            if col not in cols: cols[col]=[]
            cols[col].append((ent,attr,crud))
        #fi
    #for
    return tabs

def inserttablemap(ptabid,pentiid=None,prelaid=None):
    tema= TablEntiMap.getbyuk(tema_tabl_id=ptabid,tema_enti_id=pentiid)\
            if pentiid is not None else \
        TablEntiMap.getbyuk(tema_tabl_id=ptabid, tema_rela_id=prelaid)
    if tema is not None:
        retval = 0 #mapping exists, skip
    else:
        tema = TablEntiMap()
        tema.tema_tabl_id = ptabid
        tema.tema_enti_id = pentiid
        tema.tema_rela_id = prelaid
        try:
            tema.insert(pdoerrhdlng=False)
            retval= 1
        except Exception as e:
            if type(e) != UniqueKeyException:
                logmessages.writelog("could not insert table-map tabl_id={ptabid}, enti_id={pentiid}, rela_id={prelaid}")
            retval= 0
        #try
    return retval

def insertcolumap(pcoluid,pattrid):
    coam = ColAttrMap.getbyuk(coam_attr_id=pattrid,coam_colu_id=pcoluid,coam_direction = ColAttrMap.INBOUND,coam_seq = 1)
    if coam is not None:
        retval = 0 #mapping exists, skip
    else:
        coam = ColAttrMap()
        coam.coam_colu_id = pcoluid
        coam.coam_attr_id = pattrid
        coam.coam_direction = ColAttrMap.INBOUND
        coam.coam_seq = 1
        try:
            coam.insert(pdoerrhdlng=False)
            retval= 1
        except Exception as e:
            if type(e) != UniqueKeyException:
                logmessages.writelog(f"could not insert column_attr_map colu_id={pcoluid}, attr_id={pattrid}")
            retval= 0
        #try
    #fi
    return retval

def getmapid(pname):
    entiid,relaid = None,None
    enti = Entity.getbyuk(enti_name=pname)
    if enti is None:
        rela = Relation.getbyuk(rela_name=pname)
        if rela is None:
            logmessages.writelog("Entity or Relation {} not found.".format(pname))
        else:
            relaid = rela.rela_id
    else: entiid =enti.enti_id
    return entiid,relaid

def printstatline(pname,*args):
    l = pname.ljust(25)
    l += ''.join(str(a).ljust(12) for a in args)
    print (l)
    return

def mergeintodb(pintfname,ptabs):
    tablmapinsert,tablmapdelete,columapinsert,columapdelete = 0,0,0,0
    intf = Interface.getbyuk(intf_name=pintfname)
    if intf is None:
        logmessages.writelog(f"Interface {pintfname} not found.")
        return
    for tabname,tabmap in ptabs.items():
        #print (pintfname,tabname,tabmap)
        # search table in DB
        tabl = Table.getbyuk(tabl_name=tabname, tabl_intf_id=intf.intf_id)
        if tabl is None:
            logmessages.writelog(f"table {tabname} does not exists.")
            continue
            
        for map in tabmap["entis"]:
            mapname,enticrud = map[0],map[1]
            entiid,relaid = getmapid(pname=mapname)
            if entiid is not None or relaid is not None:
                if enticrud == 'DELMAP':
                    nvlnull=lambda x:x if x is not None else "NULL"
                    tablmapdelete += TablEntiMap.delete(
                        pwhere=f"""tema_tabl_id ={tabl.tabl_id} 
                                    and (tema_enti_id = {entiid} or tema_rela_id = {relaid})"""
                    )
                else:
                    tablmapinsert += inserttablemap(ptabid=tabl.tabl_id, pentiid=entiid,prelaid=relaid)
                #fi
            #fi
        #for

        for colname,colmap in tabmap["cols"].items():
            #print (pintfname,tabname,colname,colmap)
            col = Column.getbyuk(colu_tabl_id=tabl.tabl_id, colu_column_name=colname)
            if col is None:
                logmessages.writelog(f"column {tabname}.{colname} does not exists.")
                continue

            for attrmap in colmap:
                entiname, attrname, colcrud = attrmap[0],attrmap[1],attrmap[2]
                #print (colname,entiname, attrname, colcrud)
                if entiname is None and attrname is None:
                    continue
                enti = Entity.getbyuk(enti_name=entiname)
                entiid = enti.enti_id if enti is not None else None
                attr = Attribute.getbyuk(attr_displ_name=attrname, attr_enti_id=entiid)
                attrid = None
                if attr is None:
                    logmessages.writelog("Column {}.{}: unknown attribute {}.{}"
                                         .format(tabname,colname,entiname,attrname))
                    continue
                else:
                    if attr.attr_enti_id == entiid:
                        attrid = attr.attr_id
                    else:
                        logmessages.writelog("Attribute {} does not belong to entity {}".format(attrname, entiname))
                #fi
                if colcrud == "DELMAP":
                    #remove mapping to attribute
                    columapdelete += ColAttrMap.delete(
                        pwhere="coam_attr_id ={attrid} and coam_colu_id = {coluid}"
                            .format(attrid=attrid, coluid=col.colu_id))
                else:
                    columapinsert += insertcolumap(pattrid=attrid, pcoluid=col.colu_id)
            #for
        #for
    # for
    printstatline(pintfname,tablmapinsert,tablmapdelete,columapinsert,columapdelete)
    return

def main(param1,pxls):
    parameters.initparam(pparamfile=param1)
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
        dbConnect.openDB(pfilepath=parameters.dbFilePath(), pfks="ON")
        printstatline("Interface","tab-mapins","tab-mapdel","col-mapins","col-mapdel")
        for ws in workbook.worksheets:
            if ws.title == 'Overview': continue
            interface = importintf(ws)
            mergeintodb(pintfname=ws.title,ptabs=interface)
        #for
        dbConnect.getdbcon().commit()
        dbConnect.closeDB()
    except Exception as exp:
        print ("Merge-Exception:",exp)
        raise exp
    finally:
        print ("file {} imported into model {}".format(infile,filename))
        logmessages.showmessages()
        return

if __name__ == '__main__':
    main(param1=sys.argv[1],pxls = sys.argv[2])
