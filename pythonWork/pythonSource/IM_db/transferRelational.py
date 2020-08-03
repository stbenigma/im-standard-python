import os
import xml.etree.ElementTree as ET

import transferModel
from IM_DB import dbLookup, parameters, dbInserts,logging
from IM_OBJECTS import *

globalschnid:int = None

def do1column(plfnr, pcolxml, ptablid):
    #print(plfnr,ptablid,pcolxml)
    """
<Column name="MARQUE" id="A1AE8C02-F47A-47C5-8AB7-11F0F616DB99">
<createdBy>stb</createdBy>
<createdTime>2020-01-17 14:39:32 UTC</createdTime>
<comment><![CDATA[Name of the marketing brand of the reference. Is equal, by default, to MANUFACTURER]]></comment>
<ownerDesignName>IM_GEBERIT</ownerDesignName>
<shouldEngineer>false</shouldEngineer>
<useDomainConstraints>false</useDomainConstraints>
<use>1</use>
<logicalDatatype>A3A3C77D-0366-9768-FF89-1C25E56881C8</logicalDatatype>
<dataTypeSize>50</dataTypeSize>
<ownDataTypeParameters>50,,</ownDataTypeParameters>
<autoIncrementCycle>false</autoIncrementCycle>
<propertyMap>
<property name="EXT_ATTR_ID" value="."/>
<property name="EXT_SORT_ORDER" value="108.0"/>
</propertyMap>
</Column>
"""
    scha = Schnittstelleattr()
    scha.scha_column_name = transferModel.findField(pcolxml,'name')
    scha.scha_odm_guid = transferModel.findField(pcolxml,'id')
    scha.scha_format = None
    scha.scha_beschr = transferModel.findText(pcolxml,'comment')
    scha.scha_tabl_id = ptablid
    scha.scha_uc = transferModel.findText(pcolxml,'createdBy')
    scha.scha_dc = transferModel.findText(pcolxml, 'createdTime')
    scha.scha_fremdsystem_id = None
    daty_odm = transferModel.findText(pcolxml, 'logicalDatatype')
    if (daty_odm is not None and daty_odm != ''):
        scha.scha_daty_id = Datatype().getbyguid(daty_odm).daty_id
    daty_wrtb_odm = transferModel.findText(pcolxml, 'domain')
    scha.scha_wrtb_id = transferModel.findeOderErstelleDom(pdomguid=daty_wrtb_odm
                                                           ,pstructdomguid=None
                                                               ,ptypeguid=daty_odm
                                                               , pattrname=scha.scha_column_name
                                                               , pvatername=Tabelle().getbyid(ptablid).tabl_name
                                                               , pattrxml=pcolxml)
    if scha.scha_daty_id is None:
        scha.scha_daty_id = Datatype.getunknown().daty_id
    scha.insert()


    lmodeId= Modellelement.insertmode(pschaid=scha.scha_id)
    dbInserts.insertUdpColumn(pschaId=scha.scha_id)
    transferModel.updateUDP(pmodeid=lmodeId, pobj=pcolxml)
    documents = transferModel.getdokuref(pelem= pcolxml)
    ModelelemDoku.insertdokuref(pdocguidlist=documents, pmodeid=lmodeId)

#do1column

def do1table(pfilename):
    global globalschnid
    tablexml = ET.parse(pfilename).getroot()
    #print (tablexml.get('name'),tablexml.get('id'),sep=' | ')
    tabl = tabelle.Tabelle()
    tabl.tabl_name = transferModel.findField(tablexml,"name")
    tabl.tabl_odm_guid = transferModel.findField(tablexml,"id")
    tabl.tabl_uc = transferModel.findText(tablexml,'createdBy')
    tabl.tabl_dc = transferModel.findText(tablexml,'createdTime')
    tabl.tabl_schn_id = globalschnid
    tabl.tabl_beschr = transferModel.findText(tablexml,"comment")
    tabl.insert()
    lmodeId = Modellelement.insertmode(ptablid=tabl.tabl_id)

    dbInserts.insertUdpTable(ptablId=tabl.tabl_id)

    documents = transferModel.getdokuref(tablexml)
    ModelelemDoku.insertdokuref(pdocguidlist=documents, pmodeid=lmodeId)

    """<columns itemClass="oracle.dbtools.crest.model.design.relational.Column">"""
    cols= tablexml.find('columns')
    if cols is not None:
        for idx,col in enumerate(cols,start=1):
            do1column(plfnr=idx, pcolxml=col, ptablid=tabl.tabl_id)
        #rof
    #fi

    transferModel.updateUDP(pmodeid=lmodeId, pobj=tablexml)

#do1table

def transfertables(pschndirec):
    tablesdirec = pschndirec +'/' +parameters.odmtabledirec()
    transferModel.dosegfiles(pdirec=tablesdirec
                            ,transferfiles=do1table)
#transfertables

def do1schnittstelle(pfilename):
    global globalschnid
    schnxml = ET.parse(pfilename).getroot()
    schn=schnittstelle.Schnittstelle()
    schn.schn_name = transferModel.findField(schnxml,'name')
    schn.schn_odm_guid = transferModel.findField(schnxml,'id')
    schn.schn_uc = transferModel.findText(schnxml,'createdBy')
    schn.schn_dc = transferModel.findText(schnxml,'createdTime')
    schn.insert()
    lmodeId = Modellelement.insertmode(pschnid=schn.schn_id)

    #Dokumente an dieser Schnittstelle
    documents = transferModel.getdokuref(pelem=schnxml,pstruct=True)
    ModelelemDoku.insertdokuref(pdocguidlist= documents, pmodeid= lmodeId)
    #Tabellen
    filename, file_extension = os.path.splitext(pfilename)
    globalschnid = schn.schn_id #hässlich aber geht schlecht über generische Funktionen
    transfertables(pschndirec=filename)
#do1schnittstelle

def transferschn():
    transferModel.doxmlfiles(pdirec=parameters.odmreldirec()
               ,ptransfer=do1schnittstelle
               ,ppattern=r'{}.xml'.format(transferModel.GUIDPATTERN))
#    for el in os.listdir(parameters.odmreldirec()):
#        transferModel.doGUIDfile(pdirec=parameters.odmreldirec()
#                   , pfile=el
#                   , transferfiles=do1schnittstelle)
#    # endfor
#transferschn

def loeschmodell():
    AttrTransf.delete()
    TablEntiMap.delete()
    Schnittstelleattr().delete()
    Tabelle().delete()
    Schnittstelle().delete()
#loeschmodell

class Odmmapping:
    ENTITYPE = 0
    COLTYPE = 5
    TABLETYPE = 4
    ATTRTYPE = 1
    RELATYPE = 3 # (source ent, targ ent)
    FKTYPE = 8
    INHERITTYPE = 9
    RELARCTYPE = 13
    LOGARCTYPE = 14
    """
    <CM id="43D673EB-E3DCB674F0CEBE86A026-88057DB0AEEE" lID="43D673EB-E9B4-6636-072A-E3DCB674F0CE" lT="0" rID="BE86A026-2DB5-7C03-0A73-88057DB0AEEE" rT="4">
    <attributesSelection>61138C28-07E5-0E0E-C192-206CA0708A77,7F3CDF26-54F3-142A-4FC1-63D2DBE22319,1FAF93B9-B4A0-C357-3C10-77335807489F</attributesSelection>
    <columnsSelection>024E6C4F-98BE-457E-D328-26290EA427D2,CCDF613E-7A7B-E502-755B-3F7C49523709,B2D67599-36F9-5CC8-F1D4-95DC14F8962A,A4E9C571-618E-B2BA-9DFD-57C65FC78B11,3B5E88F5-85E3-CE20-3AC4-89A781FC4DFC,620B6F5B-685E-BE90-CA27-9EA94B910782,0D7E59F1-9E8F-B757-4AF2-2AD85AA1F67E,1884E90F-4FD9-B7DD-0AB8-41EF59A5DE04,52245329-FCD7-F424-625A-B4BE49ABB41C,66CECCD4-3319-3E35-C742-234B0D2B5130,430308E9-5649-FE59-030E-F0E34665DB81,A93025B9-A7DD-3B06-5119-CDE3FE4E33BF</columnsSelection>
    <keysSelection>69ED2946-947B-FF56-5526-76517C8A34B8</keysSelection>
    <containedMappings itemClass="oracle.dbtools.crest.model.xtdmapping.RelMapping">
    <Mg id="7F3CDF26-63D2DBE22319A93025B9-CDE3FE4E33BF" lID="7F3CDF26-54F3-142A-4FC1-63D2DBE22319" rID="A93025B9-A7DD-3B06-5119-CDE3FE4E33BF">
    </Mg>
    """

    def __init__(self,cmxml):
        self.mapid = transferModel.findField(cmxml,'id')
        self.logid = transferModel.findField(cmxml,'lID')
        self.logtype = int(transferModel.findField(cmxml, 'lT'))
        self.relid = transferModel.findField(cmxml,'rID')
        self.reltype = int(transferModel.findField(cmxml, 'rT'))
        self.columnselection = Odmmapping.selections(cmxml,'columnsSelection')
        self.attrselection = Odmmapping.selections(cmxml, 'attributesSelection')
        self.keyselection = Odmmapping.selections(cmxml, 'keysSelection')
        self.indexselection = Odmmapping.selections(cmxml, 'indexesSelections')

        cntmapxml = cmxml.find('containedMappings')
        self.cntmappings = []
        if cntmapxml is not None:
            for mg in cntmapxml:
                self.cntmappings.append({'id': transferModel.findField(mg,'id')
                                     ,'lID' :transferModel.findField(mg,'lID')
                                     ,'rID' :transferModel.findField(mg,'rID')
                                     })


    @staticmethod
    def selections(pxml,pname):
        sel = transferModel.findText(pxml, pname)
        return sel.split(',') if sel is not None else []
    #selections

#Odmmapping

def doattrmapping(pcolmappings):
    for colmap in pcolmappings:
        scha = Schnittstelleattr().getbyguid(transferModel.findField(colmap,'rID'))
        schaid = None if scha is None else scha.scha_id
        attrid = Attribut().getID (pguid=transferModel.findField(colmap,'lID'))
        attf = AttrTransf()
        attf.attf_laufnr =1
        attf.attf_richtung = AttrTransf.INBOUND
        #attf.attf_transf_formel
        #attf.attf_ausloeseart
        #attf.attf_ausloeseperiod
        attf.attf_scha_id = schaid
        attf.attf_attr_id = attrid
        attf.insert()
#doattrmapping

def do1mapping(pfilename):
    mapxml = ET.parse(pfilename).getroot()
    """
    <?xml version = '1.0' encoding = 'UTF-8'?>
    <RMExtendedMap class="oracle.dbtools.crest.model.xtdmapping.RMExtendedMap">
    <mappings itemClass="oracle.dbtools.crest.model.xtdmapping.ContainerMapping">
    <CM ...> 
        <containedMappings itemClass="oracle.dbtools.crest.model.xtdmapping.RelMapping">
        <Mg id="00270901-9EFE73A100CA28444027-8D9902F67F79" lID="00270901-6B61-7CF2-AD55-9EFE73A100CA" rID="28444027-9E42-3F66-F90F-8D9902F67F79">
        </Mg>
        ...
    </CM>
"""
    mapxml= mapxml.find('mappings')
    if mapxml is None: return
    for cmxml in mapxml:
        odmmap = Odmmapping(cmxml)
        #print (odmmap.__dict__)
        tabentimap = TablEntiMap()
        try:
            tabentimap.tema_enti_id = Entitaet().getID(odmmap.logid) if odmmap.logtype == odmmap.ENTITYPE else None
            tabentimap.tema_bezi_id = dbLookup.beziID(odmmap.logid) if odmmap.logtype == odmmap.RELATYPE else None
            tabentimap.tema_tabl_id = Tabelle().getID(odmmap.relid) if odmmap.reltype == odmmap.TABLETYPE else None
            #colattrmap.tema_tabl_id = Tabelle().getidbyfk(odmmap.relid) if odmmap.reltype == odmmap.FKTYPE else None
            tabentimap.insert(pdoerrhdlng=False)
        except:
            pass
            if odmmap.logtype == Odmmapping.ENTITYPE:
                 logging.writelog( 'Mapping funktioniert nicht Entity vermutlich gelöscht: '
                   + 'Logic: type = {}   guid = {}'.format(odmmap.logtype,odmmap.logid)
                   + '     relational: type = {}   guid = {}'.format(odmmap.reltype, odmmap.relid)
                    )
            elif odmmap.logtype == Odmmapping.FKTYPE:
                logging.writelog ( 'Mapping funktioniert nicht FK noch nicht behandelt:  '
                   + 'Logic: type = {}   guid = {} '.format(odmmap.logtype,odmmap.logid)
                   + '     relational: type = {}   guid = {}'.format(odmmap.reltype, odmmap.relid)
                    )
            else:
                logging.writelog( 'Mapping funktioniert nicht.:   '
                     + 'Logic: type = {}   guid = {}'.format(odmmap.logtype,odmmap.logid)
                     + '    relational: type = {}   guid = {}'.format(odmmap.reltype, odmmap.relid)
                    )

        #try
        doattrmapping(pcolmappings=odmmap.cntmappings)
    #for

#do1mapping

def transfermappings():
    transferModel.doxmlfiles(pdirec=parameters.odmmappingdirec(), ptransfer=do1mapping
                             ,ppattern=r'ExtendedMap_RM{}.xml'.format(transferModel.GUIDPATTERN))

#transfermappings


def transfer():
    transferschn()
    transfermappings()
#transfer