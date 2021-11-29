import os
import xml.etree.ElementTree as ET

from IM_OBJECTS import *
from IM_ODM import transferModel,handleXML
from SSOT_infra import parameters, logmessages,nvl

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
    colu = Column(psrcname=Externalref.SOURCE_ODM, psrcid=handleXML.findField(pcolxml, 'id'))
    colu.colu_column_name = handleXML.findField(pcolxml, 'name')
    colu.colu_format = None
    colu.colu_mandatory = Boolean.bool2str(not Boolean.str2bool(
        nvl(handleXML.findText(pcolxml, 'nullsAllowed'), 'true')))
    colu.colu_descr = handleXML.findText(pcolxml, 'comment')
    colu.colu_tabl_id = ptablid
    colu.colu_uc = handleXML.findText(pcolxml, 'createdBy')
    colu.colu_dc = handleXML.findText(pcolxml, 'createdTime')
    colu.colu_ext_system_id = None
    daty_odm = handleXML.findText(pcolxml, 'logicalDatatype')
    daty_wrtb_odm = handleXML.findText(pcolxml, 'domain')
    tabl = Table().getbyid(ptablid)
    colu.colu_doma_id = \
        transferModel.findorcreateDomain(pdomguid=daty_wrtb_odm
                                         , pstructdomguid=None
                                         , ptypeguid=daty_odm
                                         , pattrname=colu.colu_column_name
                                         , pfathername=Interface().getbyid(tabl.tabl_intf_id).intf_name
                                                       +'.' + tabl.tabl_name
                                         , pdomatype=Domain.DERIVED
                                         ,pintfid = tabl.tabl_intf_id
                                         , pattrxml=pcolxml)
    if colu.colu_doma_id is not None:
        colu.colu_type_string = Domain().getbyid(colu.colu_doma_id).typestring()
    colu.insert()

    Userdefpropvalue.fillallvalues(pcoluid=colu.colu_id)
    transferModel.updateUDP(pmodeid=colu.colu_id, pobj=pcolxml)
    colu.fillextid()
    documents = transferModel.getdokuref(pelem= pcolxml)
    ModelelemDocu.insertdocuref(pdocguidlist=documents, pmodeid=colu.colu_id)
    ModelelemOrgu.insertorguref(porguidlist=transferModel.getpartyref(pelem=pcolxml), pmodeid=colu.colu_id)
#do1column

def do1table(pfilename):
    global globalschnid
    tablexml = ET.parse(pfilename).getroot()
    #print (tablexml.get('name'),tablexml.get('id'),sep=' | ')
    tabl = table.Table(psrcname=Externalref.SOURCE_ODM, psrcid=handleXML.findField(tablexml, "id"))
    tabl.tabl_name = handleXML.findField(tablexml, "name")
    tabl.tabl_uc = handleXML.findText(tablexml, 'createdBy')
    tabl.tabl_dc = handleXML.findText(tablexml, 'createdTime')
    tabl.tabl_intf_id = globalschnid
    tabl.tabl_descr = handleXML.findText(tablexml, "comment")
    tabl.insert()

    Userdefpropvalue.fillallvalues(ptablid=tabl.tabl_id)

    documents = transferModel.getdokuref(tablexml)
    ModelelemDocu.insertdocuref(pdocguidlist=documents, pmodeid=tabl.tabl_id)
    ModelelemOrgu.insertorguref(porguidlist=transferModel.getpartyref(pelem=tablexml), pmodeid=tabl.tabl_id)

    """<columns itemClass="oracle.dbtools.crest.model.design.relational.Column">"""
    cols= tablexml.find('columns')
    if cols is not None:
        for idx,col in enumerate(cols,start=1):
            do1column(plfnr=idx, pcolxml=col, ptablid=tabl.tabl_id)
        #rof
    #fi

    transferModel.updateUDP(pmodeid=tabl.tabl_id, pobj=tablexml)

#do1table

def transfertables(pschndirec):
    tablesdirec = pschndirec +'/' + parameters.odmtabledirec()
    transferModel.dosegfiles(pdirec=tablesdirec
                             , transferfiles=do1table)
#transfertables

def do1interface(pfilename):
    global globalschnid
    intfxml = ET.parse(pfilename).getroot()
    intf = interface.Interface(psrcname=Externalref.SOURCE_ODM, psrcid=handleXML.findField(intfxml, 'id'))
    intf.intf_name = handleXML.findField(intfxml, 'name')
    intf.intf_descr = handleXML.findText(intfxml, 'comment')
    intf.intf_uc = handleXML.findText(intfxml, 'createdBy')
    intf.intf_dc = handleXML.findText(intfxml, 'createdTime')
    intf.insert()

    #Dokumente an dieser Interface
    ModelelemDocu.insertdocuref(pdocguidlist= transferModel.getdokuref(pelem=intfxml, pstruct=True), pmodeid    = intf.intf_id)
    ModelelemOrgu.insertorguref(porguidlist=transferModel.getpartyref(pelem=intfxml), pmodeid=intf.intf_id)
    #Tabellen
    filename, file_extension = os.path.splitext(pfilename)
    globalschnid = intf.intf_id #hässlich aber geht schlecht über generische Funktionen
    transfertables(pschndirec=filename)
#do1interface

def transferinterface():
    transferModel.doxmlfiles(pdirec=parameters.odmreldirec()
                             , ptransfer=do1interface
                             , ppattern=r'{}.xml'.format(transferModel.GUIDPATTERN))
#transferinterface

def loeschmodell():
    ColAttrMap.delete()
    TablEntiMap.delete()
    Column().delete()
    Table().delete()
    Interface().delete()
#loeschmodell

noneint = lambda elem : None if elem is None else int(elem)

class Odmmapping:
    ENTITYPE = 0
    ATTRTYPE = 1
    KEYTYPE = 2
    RELATYPE = 3 # (source ent, targ ent)
    TABLETYPE = 4
    COLTYPE = 5
    FKTYPE = 8
    INHERITTYPE = 9
    RELARCTYPE = 13
    LOGARCTYPE = 14
    RELKEYTYPE = 6
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
        self.mapid = handleXML.findField(cmxml, 'id')
        self.itype = noneint(handleXML.findField(cmxml, 'iT')) #weiss noch nicht, was das ist
        self.logid = handleXML.findField(cmxml, 'lID')
        self.logtype = noneint(handleXML.findField(cmxml, 'lT'))
        self.relid = handleXML.findField(cmxml, 'rID')
        self.reltype = noneint(handleXML.findField(cmxml, 'rT'))
        self.columnselection = Odmmapping.selections(cmxml,'columnsSelection')
        self.attrselection = Odmmapping.selections(cmxml, 'attributesSelection')
        self.keyselection = Odmmapping.selections(cmxml, 'keysSelection')
        self.indexselection = Odmmapping.selections(cmxml, 'indexesSelections')

        cntmapxml = cmxml.find('containedMappings')
        self.cntmappings = []
        if cntmapxml is not None:
            self.cntmappings = [{'id': handleXML.findField(mg, 'id')
                                , 'itype': noneint(handleXML.findField(mg, 'iT'))
                                , 'lID': handleXML.findField(mg, 'lID')
                                , 'ltype': noneint(handleXML.findField(mg, 'lT'))
                                , 'rID': handleXML.findField(mg, 'rID')
                                , 'rtype': noneint (handleXML.findField(mg, 'rT'))
                                 }
                                for mg in cntmapxml]
        # fi

    @staticmethod
    def selections(pxml,pname):
        sel = handleXML.findText(pxml, pname)
        return sel.split(',') if sel is not None else []
    #selections

#Odmmapping

def doattrmapping(pcolmappings):
    for colmap in pcolmappings:
        """        if cntmapxml is not None:
            self.cntmappings = [{'id': handleXML.findField(mg, 'id')
                                , 'itype': noneint(handleXML.findField(mg, 'iT'))
                                , 'lID': handleXML.findField(mg, 'lID')
                                , 'ltype': noneint(handleXML.findField(mg, 'lT'))
                                , 'rID': handleXML.findField(mg, 'rID')
                                , 'rtype': noneint (handleXML.findField(mg, 'rT'))
                                 }
                                for mg in cntmapxml]"""
        if (colmap["rtype"] ==  Odmmapping.RELKEYTYPE and colmap['ltype'] == Odmmapping.KEYTYPE):
            continue
        attrid = Externalref.getODMmodeid (psrcid=colmap['lID'])
        colu = Externalref.getODMmodeid(psrcid=colmap['rID'])
        if ((colu is None) or (attrid is None)):
            logmessages.writelog ("Column-Reference ({}:{}) or Attribute Reference ({}:{}) not found"
                                  .format(colmap['rtype'],colmap['rID'],colmap['ltype'],colmap['lID']))
            continue
        #fi

        colmap = ColAttrMap()
        colmap.coam_seq =1
        colmap.coam_direction = ColAttrMap.INBOUND
        colmap.coam_colu_id = colu
        colmap.coam_attr_id = attrid
        colmap.insert()
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
        tabentimap = TablEntiMap()
        if not (odmmap.logtype in (Odmmapping.ENTITYPE,Odmmapping.RELATYPE)
                and odmmap.reltype in (Odmmapping.TABLETYPE,)
                and odmmap.itype in (None,2,3) # hierachical mappings
                ):
            continue #only Entity/Relation to Table mappings are handled
        tabentimap.tema_enti_id = Externalref.getODMmodeid(psrcid=odmmap.logid) if odmmap.logtype == odmmap.ENTITYPE else None
        tabentimap.tema_rela_id = Externalref.getODMmodeid(psrcid=odmmap.logid) if odmmap.logtype == odmmap.RELATYPE else None
        tabentimap.tema_tabl_id = Externalref.getODMmodeid(psrcid=odmmap.relid) if odmmap.reltype == odmmap.TABLETYPE else None
        if (odmmap.logtype == Odmmapping.ENTITYPE and tabentimap.tema_enti_id is None):
            element = 'Entity fehlt'
        elif (odmmap.reltype == Odmmapping.TABLETYPE and tabentimap.tema_tabl_id is None):
            element = 'Table fehlt'
        elif (odmmap.logtype == Odmmapping.RELATYPE and tabentimap.tema_rela_id is None):
            element = 'Relation fehlt'
        else:
            element = None
        #fi
        if element is None:
            tabentimap.insert(pdoerrhdlng=False)
            if odmmap.logtype == Odmmapping.ENTITYPE:
                """for existing entites, consider column Mappings"""
                doattrmapping(pcolmappings=odmmap.cntmappings)
        else:
            logmessages.writelog('Mapping funktioniert nicht. ({}) :   '.format(element)
                                 + 'Logic: type = {}   guid = {}'.format(odmmap.logtype, odmmap.logid)
                                 + '    relational: type = {}   guid = {}'.format(odmmap.reltype, odmmap.relid)
                                 + '    file: {}'.format(pfilename)
                                 )
    #for
#do1mapping

def transfermappings():
    transferModel.doxmlfiles(pdirec=parameters.odmmappingdirec(), ptransfer=do1mapping
                             , ppattern=r'ExtendedMap_RM{}.xml'.format(transferModel.GUIDPATTERN))

#transfermappings


def transfer():
    transferinterface()
    transfermappings()
#transfer