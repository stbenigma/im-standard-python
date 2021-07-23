import dbDML
from IM_DB import parameters,logmessages,dbErstelleTables,dbConnect
from IM_ODM import transferModel,fillDB
import createDB
import sys,os,copy
import openpyxl

def excelfilename(pfilename):
    return pfilename + '.xlsx'

"""Base-data is omitted:
   MODELELEM_TYPE, DIAGRAMTYPES, 'MELT_DIATS'
   order is essential: FK-dependencies """
entitylist = ["PROJECTS","LANGUAGES"
              ,"MODELELEMENT", 'ENTITY_CATEGORIES','ELEMENT_UI'
            , 'LANG_TEXTS', 'EXTERNAL_REFS'
              ,"DATATYPES",'PHYSICAL_UNIT', 'STORAGE_FORMATS'
            , 'USER_DEFINED_PROPERTIES', 'UDP_VALUES', 'MODELEMTYPE_PROPERTIES'
             , 'DOCUMENTS', 'MODE_DOCU', 'ORGANISATIONALUNITS', 'MODE_ORGU'
            , 'INTERFACES'
            , 'DOMAINS', 'DOMAINGROUP_MEMBERS', 'DEFAULT_VALUES'
            , 'ENTITIES', 'SYNONYMS', 'ATTRIBUTES', 'ARCS',  'RELATIONS', 'KEYS', 'KEY_ELEMENTS'
              , 'TABLES', 'COLUMNS', 'COLU_ATTR_MAP', 'TABL_ENTI_MAPS'
            , 'BUSINESS_RULES', 'BUSINESSRULE_ELEMENTS'
              ,  'DIAGRAMS', 'ELEMENTREPS', 'RELATIONREPS', 'LINESEGMENTS']
manage = {}

def transfer1entity(pws,pentiname):
    global manage
    manage[pentiname] = {}
    headers = pws[1]
    collist =  [h.value for h in headers[1:]]
    lsql = "insert into {} ({}) values ({})".format(pentiname
                                                    , ', '.join(col for col in collist)
                                                    , ', '.join('?' for i in range(len(collist))))
    valueset = []
    for rowidx,row in enumerate(pws.values):
        crud = None

        if rowidx == 0: continue #skip headers
        values = []
        for colidx,val in enumerate(row):
            if colidx == 0:
                crud = val.upper() if type(val) == str else val
            elif colidx == 1:
                if crud not in ("I","D","U",None):
                    raise Exception("{}: first column-flag must be 'I','D','U' but is {}".format(pentiname,crud))
                manage[pentiname][val] = crud
                values.append(val)
            else:
                values.append(val)
            #fi
        #for
        valueset.append(tuple(values))
    #for
    """try to insert, if fk errors occur, repeat it with the rest of the list"""
    trycnt = 0
    while (trycnt < 10 and  len(valueset)>0):
        loopvalues = copy.copy(valueset)
        for vals in loopvalues:
            try:
                dbDML.insert(psql=lsql, rec=tuple(vals))
                valueset.remove(vals)
            except Exception as err:
                if (trycnt < 10) \
                    and str(err).startswith("FOREIGN KEY constraint failed"):
                    trycnt += 1
                else:
                    logmessages.writelog("Data error in excel, table={}".format(pentiname))
                    print("******* Data error in excel, table={}".format(pentiname))
                    print (str(err))
                    raise err
        #for
    #while
    return

def excel2db():
    global manage,workbook,entitylist
    manage = {}

    for entiname in entitylist:
        transfer1entity(pws=workbook[entiname] ,pentiname=entiname)
    #for
    return

workbook = None
def main(pparam1, pinfile):
    parameters.initparam(p_callarg=pparam1)
    logmessages.initlog('importEXCEL')
    filename = parameters.odmModelName()
    filepath = parameters.dbDirect()
    if os.path.isfile(pinfile):
        infile = pinfile
    elif os.path.isfile(filepath + pinfile):
        infile = filepath + pinfile
    else:
        logmessages.showmessages("File {} not found".format(pinfile))
        return
    #fi
    try:
        workbook = openpyxl.load_workbook(filename=infile)
        fillDB.fillmergedb(callarg=pparam1
                           , transferfunction=excel2db
                           , createnewdb=not createDB.existsDB(parameters.dbFilePath()))
    finally:
        logmessages.showmessages("XLSX file {} imported for model {}"
                                 .format(infile, parameters.odmModelName()))
    return

if __name__ == '__main__':
    main(pparam1=sys.argv[1], pinfile=sys.argv[2])
