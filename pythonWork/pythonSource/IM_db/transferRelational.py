import xml.etree.ElementTree as ET
import re,os
from datetime import date
from IM_DB import dbDML,dbLookup,dbConnect,parameters,dbParam,dbInserts
import math
from IM_OBJECTS import schnittstelle,tabelle
import transferModel

globalschnid:int = None

def do1table(pfilename):
    global globalschnid
    tablexml = ET.parse(pfilename).getroot()
    #print (tablexml.get('name'),tablexml.get('id'),sep=' | ')
    tabl = tabelle.tabelle()
    tabl.tabl_name = tablexml.get("name")
    tabl.tabl_odm_guid = tablexml.get("id")
    tabl.tabl_uc = transferModel.findText(tablexml,'createdBy')
    tabl.tabl_dc = transferModel.findText(tablexml,'createdTime')
    tabl.tabl_schn_id = globalschnid
    tabl.tabl_beschr = transferModel.findText(tablexml,"comment")
    tabl.tabl_id = tabelle.insert(tabl)
    lmodeId =dbInserts.insertModeTabl(tabl.tabl_id)

    documents = transferModel.getdokuref(tablexml)
    dbInserts.insertdokuref(documents = documents, modeid = lmodeId)

#do1table

def transfertables(pschndirec):
    tablesdirec = pschndirec\
                +'/' +parameters.odmtabledirec()
    transferModel.dosegfiles(pdirec=tablesdirec
                            ,transferfiles=do1table)
#transfertables

def do1schnittstelle(pfilename):
    global globalschnid
    schnxml = ET.parse(pfilename).getroot()
    schn=schnittstelle.schnittstelle()
    schn.schn_name = schnxml.get('name')
    schn.schn_odm_guid = schnxml.get('id')
    schn.schn_uc = transferModel.findText(schnxml,'createdBy')
    schn.schn_dc = transferModel.findText(schnxml,'createdTime')
    schn.schn_id = schnittstelle.insert(schn)
    lmodeId =dbInserts.insertModeSchn(schn.schn_id)

    #Dokumente an dieser Schnittstelle
    documents = transferModel.getdokuref(pelem=schnxml,pstruct=True)
    dbInserts.insertdokuref(documents = documents, modeid = lmodeId)
    #Tabellen
    filename, file_extension = os.path.splitext(pfilename)
    globalschnid = schn.schn_id #hässlich aber geht nicht über generische Funktionen
    transfertables(pschndirec=filename)
#do1schnittstelle

def transferschn():
    for el in os.listdir(parameters.odmreldirec()):
        transferModel.doGUIDfile(pdirec=parameters.odmreldirec()
                   , pfile=el
                   , transferfiles=do1schnittstelle)
    # endfor
#transferschn

def loeschmodell():
    tabelle.delete()
    schnittstelle.delete()
#loeschmodell


def transfer():
    transferschn()
#transfer