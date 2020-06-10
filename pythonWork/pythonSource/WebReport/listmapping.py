# -*- coding: latin-1 -*-
import sys,os,re
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
tabentimap = {}
colattrmap = {}

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
    global tabentimap

    createFile(pfilename=parameters.odmModelName()+'_tabenti.csv')
    write('\ufeff')
    topheader = 'Interface'+CSVSEP +'Table'+ CSVSEP + CSVSEP.join(e[0] for e in entities.values())
    writeln(topheader)
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
    global tabentimap

    createFile(pfilename=parameters.odmModelName()+'_colattr.csv')
    write('\ufeff')
    topheader = CSVSEP + CSVSEP + 'Entity' + CSVSEP
    subheader = 'Interface'+CSVSEP +'Table'+ CSVSEP +'Column'+ CSVSEP
    for enti in entities.values():
        attrs = enti[2]
        topheader += enti[0] + CSVSEP+ CSVSEP.join('' for at in attrs)[:-1]
        subheader += CSVSEP+ CSVSEP.join(at[0] for at in attrs.values())
    writeln(topheader)
    writeln(subheader)
    for skey,sval in schnittstellen.items():
        for tkey,tval in sval.items():
            for ckey,cval in tval[1].items():
                writeln(skey,tval[0],cval[0],CSVSEP.join(columns[ckey][3]),sep=CSVSEP)
    print("Erstellt: {}".format(fileCSV.name))
    closefile()
#listcolattr
def istintabentimap(tabid,entiid):
    return (tabid in tabentimap) and (entiid in tabentimap[tabid])
#istintabentimap
def istincolattrmap(colid,attrid):
    return (colid in colattrmap) and (attrid in colattrmap[colid])
#istincolattrmap

def stripeol(str):
    retval = re.sub("\n+", "\n", str)
    retval = retval.strip(EOL)
    return retval
#stripeol

def listentiintf(plang):
    global tabentimap,schnittstellen,entities
    createFile(pfilename=parameters.odmModelName()+'_entiintf.csv')
    write('\ufeff')
    writeln('Information Model',CSVSEP.join(schn_name for schn_name in schnittstellen.keys()),sep=CSVSEP)
    for entiid,enti in entities.items():
        write(enti[0],CSVSEP)
        for schntabs in schnittstellen.values():
            entry = EOL.join(tab[0] if (istintabentimap(tabid,entiid)) else "" for tabid,tab in schntabs.items())
            entry = stripeol(entry)
            if (entry!= ""):
                write('"'+entry+'"')
            write(CSVSEP)
        writeln()
    print("Erstellt: {}".format(fileCSV.name))
    closefile()
#listentiintf

def listattrintf(plang):
    global tabentimap,schnittstellen,entities
    createFile(pfilename=parameters.odmModelName()+'_attrintf.csv')
    write('\ufeff')
    topheader = CSVSEP + CSVSEP
    subheader = 'Entity' + CSVSEP+ 'Attribute'
    for schn_name,tabs in schnittstellen.items():
        topheader += schn_name + CSVSEP + CSVSEP.join('' for ta in tabs)[:-1]
        subheader += CSVSEP+ CSVSEP.join(ta[0] for ta in tabs.values())
    writeln(topheader)
    writeln(subheader)
    for enti_id,enti in entities.items():
        for attrid,attr in enti[2].items():
            write(enti[0],CSVSEP,attr[0],CSVSEP)
            for schntabs in schnittstellen.values():
                entry = []
                for tab in schntabs.values():
                    colentry = EOL.join((tab[0]+'.'+col[0]) if (istincolattrmap(colid,attrid)) else "" for colid,col in tab[1].items())
                    colentry = stripeol(colentry)
                    if (colentry!= ""):
                        entry.append(colentry)
                #for
                entry = EOL.join(entry)
                entry = stripeol(entry)
            if (entry != ""):
                write('"' + entry + '"')
            write(CSVSEP)
            #for
        #for
        writeln()
    #for

    print("Erstellt: {}".format(fileCSV.name))
    closefile()
#listattrintf

def listentitable(plang):
    global entities
    global schnittstellen

    createFile(pfilename=parameters.odmModelName()+'_entitable.csv')
    write('\ufeff')
    topheader = 'Information Model' + CSVSEP
    subheader = 'Entity'
    for schn_name,tabs in schnittstellen.items():
        topheader += schn_name + CSVSEP+ CSVSEP.join('' for ta in tabs)[:-1]
        subheader += CSVSEP+ CSVSEP.join(ta[0] for ta in tabs.values())
    writeln(topheader)
    writeln(subheader)
    for enti in entities.values():
        writeln(enti[0],CSVSEP.join(enti[3]),sep=CSVSEP)
    print("Erstellt: {}".format(fileCSV.name))
    closefile()
#listentitable

def listtabenti(plang):
    global entities
    global schnittstellen

    createFile(pfilename=parameters.odmModelName()+'_tabenti.csv')
    write('\ufeff')
    topheader = 'Interface' + CSVSEP + 'Table' + CSVSEP + CSVSEP.join(enti[0] for enti in entities.values())
    writeln(topheader)
    for skey,sval in schnittstellen.items():
        for tkey,tval in sval.items():
            writeln(skey,tval[0],CSVSEP.join(tables[tkey][3]),sep=CSVSEP)
    print("Erstellt: {}".format(fileCSV.name))
    closefile()
#listtabenti

def filllists(plang):
    global entities
    global attributes
    global tables
    global columns
    global schnittstellen
    global tabentimap
    global colattrmap
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
    tabentimap = TablEntiMap.tabentimap()
    for tkey,tval in tables.items():
        matentry = lambda tabid,entiid : 'X' if (tabid in tabentimap) and (entiid in tabentimap[tabid]) else ''
        maps = [matentry(tkey,e) for e in entities.keys()]
        tval.append(maps)
    #for
    for ekey,eval in entities.items():
        matentry = lambda tabid,entiid : 'X' if (tabid in tabentimap) and (entiid in tabentimap[tabid]) else ''
        maps = [matentry(tkey,ekey) for tkey in tables.keys()]
        eval.append(maps)
    #for
    colattrmap = AttrTransf.colattrmap()
    for colid,cval in columns.items():
        matentry = lambda colid,attrid : 'X' if (colid in colattrmap) and (attrid in colattrmap[colid]) else ''
        maps = [matentry(colid,attrid) for attrid in attributes.keys()]
        cval.append(maps)
    #for
#    print (len(entities),entities)
#    print(len(attributes),attributes)
#    print (len(tables),tables)
#    print (len(schnittstellen),schnittstellen)
#    print (len(mapping),mapping)
#    print(len(colattrmap),colattrmap)
#filllists

def main(pdirec, plang):
    parameters.initparam(p_callarg=pdirec)

    print ("listmapping",parameters.odmBaseDirec(),parameters.odmModelName())

    dbConnect.openDB(p_filepath= parameters.dbFilePath());
    deflang = Sprache.liesdeflangiso2()
    if deflang is not None : parameters.dbDefaultLang(deflang)
    filllists(plang=plang)
    listentiintf(plang=plang)
    listattrintf(plang=plang)
    listentitable(plang=plang)
    listtabenti(plang=plang)
    listcolattr(plang=plang)
    dbConnect.myDbConn.close()
#main

if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv)>2) else None
    main(pdirec=direc, plang=lang)