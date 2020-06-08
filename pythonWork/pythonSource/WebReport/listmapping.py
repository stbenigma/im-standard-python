# -*- coding: latin-1 -*-
import sys,os
sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+'/../IM_db')
from IM_DB import parameters,dbConnect,dbParam
from IM_OBJECTS import *

fileCSV = None
csvdirectory = 'Web/'
csventitableFilename = 'EntiTable.csv'
EOL:str='\n'
CSVSEP:str=';'
entities = {}
attributes = {}
tables = {}
columns = {}
schnittstellen = {}
mapping = {}
tabentimap = {}

def createFile(pfilename):
    global fileCSV
    csvfile = parameters.localbasedirec()+csvdirectory + pfilename
    if os.path.exists(csvfile):
        os.remove(csvfile)
    fileCSV = open(csvfile, 'w')
#createFile

def closefile():
    global fileCSV
    fileCSV.close()
#closefile

def write(*args,**kwargs):
    global fileCSV
    sep = kwargs['sep'] if 'sep' in kwargs else ''
    str =sep.join(arg for arg in args)
    fileCSV.write(str)

def writeln(*args,**kwargs):
    write(*args,**kwargs)
    write(EOL)

def listtabenti(plang):
    global entities
    global attributes
    global tables
    global schnittstellen
    global mapping
    global tabentimap

    createFile(pfilename=parameters.odmModelName()+'_tabenti.csv')
    write('\ufeff')
    topheader = 'Interface'+CSVSEP +'Table'+ CSVSEP + CSVSEP.join(e[0] for e in entities.values())
    writeln(topheader)
    #def matrixentry(ptablid,pentiid):
    #    if (ptablid in tabentimap) and (pentiid in tabentimap[ptablid]): return 'X'
    #    else: return ''
    for tkey,tval in tables.items():
        matentry = lambda tabid,entiid : 'X' if (tabid in tabentimap) and (entiid in tabentimap[tabid]) else ''
        maps = [matentry(tkey,e) for e in entities.keys()]
        tval.append(maps)
    #for
    for skey,sval in schnittstellen.items():
        for tkey,tval in sval.items():
            writeln(skey,tval[0],CSVSEP.join(tables[tkey][3]),sep=CSVSEP)
    print("Erstellt: {}".format(fileCSV.name))
    closefile()
#listtabenti

def listcolattr(plang):
    global entities
    global attributes
    global tables
    global schnittstellen
    global mapping
    global tabentimap

    createFile(pfilename=parameters.odmModelName()+'_colattr.csv')
    write('\ufeff')
    topheader = 'Interface'+CSVSEP +'Table'+ CSVSEP +'Column'+ CSVSEP + CSVSEP.join(e[0] for e in entities.values())
    writeln(topheader)
    for tkey,tval in tables.items():
        matentry = lambda tabid,entiid : 'X' if (tabid in tabentimap) and (entiid in tabentimap[tabid]) else ''
        maps = [matentry(tkey,e) for e in entities.keys()]
        tval.append(maps)
    #for
    return
    for skey,sval in schnittstellen.items():
        for tkey,tval in sval.items():
            for ckey,cval in tval[1].items():
                writeln(skey,tval[0],cval,CSVSEP.join(tables[tkey][3]),sep=CSVSEP)
    print("Erstellt: {}".format(fileCSV.name))
    closefile()
#listcolattr

def listentiintf(plang):
    createFile(pfilename=parameters.odmModelName()+'_entiintf.csv')
    write('\ufeff')
    scns = Schnittstelle.select()
    writeln('Information Model',CSVSEP.join(scn.schn_name for scn in scns),sep=CSVSEP)
    entis = Entitaet.select()
    for enti in entis:
        write(enti.getname(plang),CSVSEP)
        tem = TablEntiMap.tablelist(pentiid=enti.enti_id)
        for scn in scns:
            for t in tem:
                if scn.schn_name == t[0]:
                    write('"'+EOL.join(ta for ta in t[1].keys())+'"')
            write(CSVSEP)
        writeln()
    print("Erstellt: {}".format(fileCSV.name))
    closefile()
#listentiintf

def listentitable(plang):
    createFile(pfilename=parameters.odmModelName()+'_entitable.csv')
    write('\ufeff')
    topheader = 'Information Model' + CSVSEP
    subheader = 'Entity' + CSVSEP
    scns = Schnittstelle.select()
    for scn in scns:
        tabs = Tabelle.selectbyschnid(pschnid=scn.schn_id)
        topheader += scn.schn_name+ CSVSEP+ CSVSEP.join('' for ta in tabs)[:-1]
        subheader += CSVSEP.join(ta.tabl_name for ta in tabs)
    writeln(topheader)
    writeln(subheader)
    entis = Entitaet.select()
    for enti in entis:
        write(enti.getname(plang),CSVSEP)
        tem = TablEntiMap.tablelist(pentiid=enti.enti_id)
        temdict = {t[0]:t[1] for t in tem}
        """{schnname : {tablename: webanker}}"""
        #print (temdict)
        for scn in scns:
            tabs = Tabelle.selectbyschnid(pschnid=scn.schn_id)
            for t in tabs:
                if ((scn.schn_name in temdict)\
                    and (t.tabl_name in temdict[scn.schn_name])):
                    write('X')
                write(CSVSEP)
            #for
        #for
        writeln()
    print("Erstellt: {}".format(fileCSV.name))
    closefile()
#listentitable

def filllists(plang):
    global entities
    global attributes
    global tables
    global columns
    global schnittstellen
    global mapping
    global tabentimap
    entities = {enti.enti_id:[enti.enti_name
                                ,{tem[0]: [t for t in tem[1].keys()]
                                for tem in TablEntiMap.tablelist(pentiid=enti.enti_id)}
                              ,{attr.attr_id:[attr.attr_anzname,attr.attr_tech_name]
                                 for attr in enti.getattributes()}
                              ]
                for enti in Entitaet.select()}
    attributes = {attr.attr_id:[attr.attr_anzname,attr.attr_tech_name,attr.attr_enti_id,attr.attr_bezi_id] for attr in Attribut.select()}
    tables = {tabl.tabl_id:[tabl.tabl_name,Schnittstelle.getname(tabl.tabl_schn_id)
                                ,{c.scha_id:c.scha_column_name for c in tabl.getcolumns()}
                            ]
                  for tabl in Tabelle.select()}

    columns = {scha.scha_id:[scha.scha_column_name,scha.scha_tabl_id,scha.scha_fremdsystem_id] for scha in Schnittstelleattr.select()}
    schnittstellen = {schn.schn_name:
                              {tabl.tabl_id:[tabl.tabl_name
                                             ,{c.scha_id:[c.scha_column_name,c.scha_fremdsystem_id] for c in tabl.getcolumns()}
                                            ] for tabl in Tabelle.selectbyschnid(schn.schn_id)
                               }
                        for schn in Schnittstelle.select() }
    mapping = TablEntiMap.tablelist()
    tabentimap = TablEntiMap.tabentimap()
    print (len(entities),entities)
#    print(len(attributes),attributes)
    print (len(tables),tables)
#    print (len(schnittstellen),schnittstellen)
#    print (len(mapping),mapping)
#    print(len(tabentimap),tabentimap)
#filllists

def main(pdirec, plang):
    parameters.initparam(p_callarg=pdirec)

    print ("listmapping",parameters.odmBaseDirec(),parameters.odmModelName())

    dbConnect.openDB(p_filepath= parameters.dbFilePath());
    deflang = Sprache.liesdeflangiso2()
    if deflang is not None : parameters.dbDefaultLang(deflang)
    filllists(plang=plang)
    listentiintf(plang=plang)
    listentitable(plang=plang)
    listcolattr(plang=plang)
    dbConnect.myDbConn.close()
#main

if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv)>2) else None
    main(pdirec=direc, plang=lang)