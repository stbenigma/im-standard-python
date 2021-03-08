# -*- coding: latin-1 -*-
from IM_ODM import transferModel
from IM_DB import dbConnect, parameters, logmessages


# Main Programm

def filldbmain(pinmemory=False):
    if not pinmemory:
        dbConnect.openDB(parameters.dbFilePath(), fks='OFF')
        transferModel.loeschmodell()
        dbConnect.myDbConn.close()
        #print("filldbmain Constraints sollten auf ON stehen")
        dbConnect.openDB(parameters.dbFilePath(), fks='ON')
    #fi
    transferModel.insertBaseData()
    transferModel.transferODMModel();
    if not pinmemory: dbConnect.myDbConn.close()
# filldbmain


def buildid2uktranslate():
    import inspect
    g = vars(IM_OBJECTS).copy()
    """ db-Objects from Module IM_OBJECTS"""
    ALL_DBOBJECTS = [obj for name, obj in g.items()
                     if inspect.isclass(obj)
                     and name not in ('Baseobject', 'MultilangBaseobject', 'Boolean')
                     ]

    retval = {}
    for dbobj in ALL_DBOBJECTS:
        fklist = IM_db.dbDDL.getfklist(ptablename=dbobj._tablename)
        prefix = dbobj._prefix
        for row in dbobj().select():
            retval["{}{}".format(row._prefix,str(row.getid()))] = row.getukvaluepairs()
    return retval

    def translatefks(self,pid2uklist):
        """if a fk is not None: translate it via the UK-translation-table into the id of the row
            pid2uklist = {jsid : {colname:colvalue,}}
                 jsid = <modelelemtype>nnn "ENTI143" """
        fklist = dbDDL.getfklist(ptablename=self._tablename)



def filldbmain2(callarg):
    memoryfilepath = ":memory:"
    dbConnect.openDB(p_filepath=memoryfilepath,fks='ON');
    dbErstelleTables.erstelleInfra(parameters.sqlfilepath());
    transferModel.insertBaseData()
    transferModel.transferODMModel();
    odmjson = createJSON.jsonfromdb()
    id2uktranslate = buildid2uktranslate()
    dbConnect.closeDB()


    if True:
        IM_db.createDB(par1=callarg,pforcecreate=True)

    dbConnect.openDB(p_filepath=parameters.dbFilePath(),fks='ON');
    transferModel.insertBaseData()
    json2sql.fillsql(pmodel=odmjson)
    #dbjson = createJSON.jsonfromdb()
    #mergedbs.mergeodm2db(podmjson=odmjson,pdbjson=dbjson)
    dbConnect.closeDB()

def main(p_param1):
    """Main program for fillDB"""
    parameters.initparam(p_callarg=p_param1)
    logmessages.initlog('fillDB')

    try:
        filldbmain()
    finally:
        logmessages.showmessages("database {} for model {} filled with modeldata"
                                 .format(parameters.dbFilePath(),
                               parameters.odmModelName()))
#  main

if __name__ == '__main__':
    import sys
    main(p_param1=sys.argv[1])
