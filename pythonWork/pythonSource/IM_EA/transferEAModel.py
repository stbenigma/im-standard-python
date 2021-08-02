import os
import re
import xml.etree.ElementTree as et
from datetime import datetime

import handleXML
from IM_DB import parameters, logmessages
from IM_OBJECTS import *
from IM_ODM import transferModel

"""Example XML of ea"""
"""<?xml version="1.0" encoding="windows-1252"?>
<Package name="riddle" guid="{68389B05-EBA4-4e57-954C-DFBC51443B65}">
	<Table name="t_package">
		<Row>
			<Column name="Package_ID" value="3"/>
			<Column name="Name" value="riddle"/>
			<Column name="Parent_ID" value="1"/>
			<Column name="CreatedDate" value="2021-06-29 17:32:29"/>
			<Column name="ModifiedDate" value="2021-06-29 17:32:29"/>
			<Column name="ea_guid" value="{68389B05-EBA4-4e57-954C-DFBC51443B65}"/>
			<Column name="IsControlled" value="FALSE"/>
			<Column name="Version" value="1.0"/>
			<Column name="Protected" value="FALSE"/>
			<Column name="UseDTD" value="FALSE"/>
			<Column name="LogXML" value="FALSE"/>
			<Column name="PackageFlags" value="isModel=1;VICON=3;"/>
			<Extension/>
		</Row>
	</Table>
	<Table name="t_object">
		<Row>
			<Column name="Object_ID" value="28"/>
			<Column name="Object_Type" value="Class"/>
			<Column name="Diagram_ID" value="0"/>
			<Column name="Name" value="Plane"/>
			<Column name="Author" value="bue"/>
			<Column name="Version" value="1.0"/>
			<Column name="Package_ID" value="3"/>
			<Column name="Stereotype" value="Entity"/>
			<Column name="NType" value="0"/>
			<Column name="Complexity" value="1"/>
			<Column name="Effort" value="0"/>
			<Column name="Backcolor" value="-1"/>
			<Column name="BorderStyle" value="0"/>
			<Column name="BorderWidth" value="2"/>
			<Column name="Fontcolor" value="-1"/>
			<Column name="Bordercolor" value="-1"/>
			<Column name="CreatedDate" value="2021-06-29 17:33:27"/>
			<Column name="ModifiedDate" value="2021-06-29 17:39:44"/>
			<Column name="Status" value="Proposed"/>
			<Column name="Abstract" value="0"/>
			<Column name="Tagged" value="0"/>
			<Column name="PDATA2" value="Java"/>
			<Column name="PDATA4" value="0"/>
			<Column name="GenType" value="Java"/>
			<Column name="Phase" value="1.0"/>
			<Column name="Scope" value="Public"/>
			<Column name="Classifier" value="0"/>
			<Column name="ea_guid" value="{15D14A8B-908A-4714-9424-DA0437161DF6}"/>
			<Column name="ParentID" value="0"/>
			<Column name="IsRoot" value="FALSE"/>
			<Column name="IsLeaf" value="FALSE"/>
			<Column name="IsSpec" value="FALSE"/>
			<Column name="IsActive" value="FALSE"/>
			<Extension Package_ID="{68389B05-EBA4-4e57-954C-DFBC51443B65}"/>
		</Row>
	</Table>
	<Table name="t_objectproperties">
		<Row>
			<Column name="PropertyID" value="17"/>
			<Column name="Object_ID" value="27"/>
			<Column name="Property" value="x_image"/>
			<Column name="Value" value="&lt;Image type=&quot;EAShapeScript 1.0&quot; xmlns:dt=&quot;urn:schemas-microsoft-com:datatypes&quot; dt:dt=&quot;bin.base64&quot;&gt;UEsDBBQAAAAIAJh1zlJKjJOkbwAAAKQAAAAHABEAc3RyLmRhdFVUDQAHPGvHYDxrx2A8a8dg&#xA;PY0xDoJAEEVfK4l3MFtBQqEVhfEwKARNFAiLsTDe3ccGLf7M3533ZyJXakZadjx0N3rebMnY&#xA;6AZimje6l8R"/>
			<Column name="Notes" value="Default: &lt;Image type=&quot;EAShapeScript 1.0&quot; xmlns:dt=&quot;urn:schemas-microsoft-com:datatypes&quot; dt:dt=&quot;bin.base64&quot;&gt;UEsDBBQAAAAIAJh1zlJKjJOkbwAAAKQAAAAHABEAc3RyLmRhdFVUDQAHPGvHYDxrx2A8a8dg&#xA;PY0xDoJAEEVfK4l3MFtBQqEVhfEwKARNFAiLsTDe3ccGLf7M3533ZyJXakZadjx0N3rebMnY&#xA;6AZimje6l8RJBWYmniYCx5WcfF38r8103NO2nD1l0sG69Mpa/DOjqeXaLN9LB6+0nN3c6X/c&#xA;R30BUEsBAhcLFAAAAAgAmHXOUkqMk6RvAAAApAAAAAcACQAAAAAAAAAAAACAAAAAAHN0ci5k&#xA;YXRVVAUABzxrx2BQSwUGAAAAAAEAAQA+AAAApQAAAAAA&lt;/Image&gt;&#xA;&#xA;"/>
			<Column name="ea_guid" value="{FA900ABA-C315-bec3-8A5A-B395CBF2C769}"/>
			<Extension Object_ID="{7AD59C4D-AA70-4019-9E4C-4F03A266D39D}"/>
		</Row>
	</Table>
	<Table name="t_attribute">
		<Row>
			<Column name="Object_ID" value="31"/>
			<Column name="Name" value="IATA Code"/>
			<Column name="Scope" value="Public"/>
			<Column name="Stereotype" value="Attribute"/>
			<Column name="Containment" value="Not Specified"/>
			<Column name="IsStatic" value="0"/>
			<Column name="IsCollection" value="0"/>
			<Column name="IsOrdered" value="0"/>
			<Column name="AllowDuplicates" value="0"/>
			<Column name="LowerBound" value="1"/>
			<Column name="UpperBound" value="1"/>
			<Column name="Derived" value="0"/>
			<Column name="ID" value="8"/>
			<Column name="Pos" value="0"/>
			<Column name="Length" value="0"/>
			<Column name="Const" value="0"/>
			<Column name="Classifier" value="29"/>
			<Column name="Type" value="Airport Codes"/>
			<Column name="ea_guid" value="{CB0F96CF-C29B-4f9a-8B72-FFE959450E46}"/>
			<Column name="StyleEx" value="volatile=0;union=0;"/>
			<Extension Object_ID="{1FDCDC17-0587-4f38-AFB1-3ED0159DA4A7}" Classifier="{7320D192-A2DF-463e-9FF6-A1E3A7987E33}"/>
		</Row>
	</Table>
	<Table name="t_connector">
		<Row>
			<Column name="Connector_ID" value="24"/>
			<Column name="Direction" value="Unspecified"/>
			<Column name="Connector_Type" value="Association"/>
			<Column name="SourceCard" value="*"/>
			<Column name="SourceAccess" value="Public"/>
			<Column name="DestCard" value="1"/>
			<Column name="DestAccess" value="Public"/>
			<Column name="SourceRole" value="land on"/>
			<Column name="SourceContainment" value="Unspecified"/>
			<Column name="SourceIsAggregate" value="0"/>
			<Column name="SourceIsOrdered" value="0"/>
			<Column name="DestContainment" value="Unspecified"/>
			<Column name="DestIsAggregate" value="0"/>
			<Column name="DestIsOrdered" value="0"/>
			<Column name="Start_Object_ID" value="30"/>
			<Column name="End_Object_ID" value="31"/>
			<Column name="Btm_Mid_Label" value=" &#xA;´Relationª"/>
			<Column name="Start_Edge" value="3"/>
			<Column name="End_Edge" value="1"/>
			<Column name="PtStartX" value="227"/>
			<Column name="PtStartY" value="-117"/>
			<Column name="PtEndX" value="236"/>
			<Column name="PtEndY" value="-211"/>
			<Column name="SeqNo" value="0"/>
			<Column name="HeadStyle" value="0"/>
			<Column name="LineStyle" value="0"/>
			<Column name="RouteStyle" value="1"/>
			<Column name="IsBold" value="0"/>
			<Column name="LineColor" value="-1"/>
			<Column name="Stereotype" value="Relation"/>
			<Column name="VirtualInheritance" value="0"/>
			<Column name="PDATA5" value="SX=-30;SY=6;EX=-43;EY=6;"/>
			<Column name="DiagramID" value="0"/>
			<Column name="ea_guid" value="{11649298-B3E9-4707-9447-F12045A7E622}"/>
			<Column name="SourceIsNavigable" value="FALSE"/>
			<Column name="DestIsNavigable" value="FALSE"/>
			<Column name="IsRoot" value="FALSE"/>
			<Column name="IsLeaf" value="FALSE"/>
			<Column name="IsSpec" value="FALSE"/>
			<Column name="SourceChangeable" value="none"/>
			<Column name="DestChangeable" value="none"/>
			<Column name="SourceTS" value="instance"/>
			<Column name="DestTS" value="instance"/>
			<Column name="IsSignal" value="FALSE"/>
			<Column name="IsStimulus" value="FALSE"/>
			<Column name="Target2" value="6619235"/>
			<Column name="SourceStyle" value="Union=0;Derived=0;AllowDuplicates=0;Owned=0;Navigable=Unspecified;"/>
			<Column name="DestStyle" value="Union=0;Derived=0;AllowDuplicates=0;Owned=0;Navigable=Unspecified;"/>
			<Extension Start_Object_ID="{17FB5FB5-9389-4852-A17F-69CC44782683}" End_Object_ID="{1FDCDC17-0587-4f38-AFB1-3ED0159DA4A7}"/>
		</Row>
	</Table>
	<Table name="t_diagram">
		<Row>
			<Column name="Diagram_ID" value="3"/>
			<Column name="Package_ID" value="3"/>
			<Column name="ParentID" value="0"/>
			<Column name="Diagram_Type" value="Logical"/>
			<Column name="Name" value="riddle"/>
			<Column name="Version" value="1.0"/>
			<Column name="Author" value="bue"/>
			<Column name="ShowDetails" value="0"/>
			<Column name="AttPub" value="TRUE"/>
			<Column name="AttPri" value="TRUE"/>
			<Column name="AttPro" value="TRUE"/>
			<Column name="Orientation" value="P"/>
			<Column name="cx" value="850"/>
			<Column name="cy" value="1098"/>
			<Column name="Scale" value="100"/>
			<Column name="CreatedDate" value="2021-06-29 17:33:03"/>
			<Column name="ModifiedDate" value="2021-06-30 11:29:19"/>
			<Column name="ShowForeign" value="TRUE"/>
			<Column name="ShowBorder" value="TRUE"/>
			<Column name="ShowPackageContents" value="TRUE"/>
			<Column name="PDATA" value="HideRel=0;ShowTags=0;ShowReqs=0;ShowCons=0;OpParams=1;ShowSN=0;ScalePI=0;PPgs.cx=0;PPgs.cy=0;PSize=1;ShowIcons=1;SuppCN=0;HideProps=0;HideParents=0;UseAlias=0;HideAtts=0;HideOps=1;HideStereo=1;HideEStereo=1;ShowRec=1;ShowRes=0;ShowShape=1;FormName=;"/>
			<Column name="Locked" value="FALSE"/>
			<Column name="ea_guid" value="{31F9B6EA-8455-42d6-9FDF-9D5F74D13FB4}"/>
			<Column name="Swimlanes" value="locked=false;orientation=0;width=0;inbar=false;names=false;color=-1;bold=false;fcol=0;tcol=-1;ofCol=-1;ufCol=-1;hl=1;ufh=0;hh=0;cls=0;bw=0;hli=0;bro=0;"/>
			<Column name="StyleEx" value="ExcludeRTF=0;DocAll=0;HideQuals=0;AttPkg=1;ShowTests=0;ShowMaint=0;SuppressFOC=1;MatrixActive=0;SwimlanesActive=1;KanbanActive=0;MatrixLineWidth=1;MatrixLineClr=0;MatrixLocked=0;TConnectorNotation=Information Engineering;TExplicitNavigability=0;AdvancedElementProps=1;AdvancedFeatureProps=1;AdvancedConnectorProps=1;m_bElementClassifier=1;SPT=1;MDGDgm=IM::Information Model View;STBLDgm=;ShowNotes=0;VisibleAttributeDetail=0;ShowOpRetType=1;SuppressBrackets=0;SuppConnectorLabels=0;PrintPageHeadFoot=0;ShowAsList=0;SuppressedCompartments=;Theme=:119;SaveTag=7405149A;"/>
			<Extension Package_ID="{68389B05-EBA4-4e57-954C-DFBC51443B65}"/>
		</Row>
	</Table>
	<Table name="t_diagramobjects">
		<Row>
			<Column name="Diagram_ID" value="3"/>
			<Column name="Object_ID" value="27"/>
			<Column name="RectTop" value="-240"/>
			<Column name="RectLeft" value="20"/>
			<Column name="RectRight" value="146"/>
			<Column name="RectBottom" value="-310"/>
			<Column name="Sequence" value="8"/>
			<Column name="ObjectStyle" value="DUID=4181B32B;HideIcon=0;LWth=2;"/>
			<Column name="Instance_ID" value="24"/>
			<Extension Diagram_ID="{31F9B6EA-8455-42d6-9FDF-9D5F74D13FB4}" Object_ID="{7AD59C4D-AA70-4019-9E4C-4F03A266D39D}"/>
		</Row>
	</Table>
	<Table name="t_diagramlinks">
		<Row>
			<Column name="DiagramID" value="3"/>
			<Column name="ConnectorID" value="21"/>
			<Column name="Geometry" value="SX=0;SY=0;EX=0;EY=0;EDGE=3;$LLB=CX=7:CY=15:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;LLT=CX=53:CY=14:OX=-9:OY=1:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;LMT=CX=75:CY=14:OX=0:OY=0:HDN=1:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;LMB=CX=47:CY=14:OX=0:OY=0:HDN=1:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;LRT=CX=27:CY=14:OX=84:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;LRB=CX=7:CY=15:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;IRHS=;ILHS=;"/>
			<Column name="Style" value="Mode=3;EOID=4181B32B;SOID=BEA48B85;Color=-1;LWidth=0;"/>
			<Column name="Hidden" value="FALSE"/>
			<Column name="Instance_ID" value="15"/>
			<Extension DiagramID="{31F9B6EA-8455-42d6-9FDF-9D5F74D13FB4}" ConnectorID="{8E978A5E-BA5C-4e3b-AFE6-44AEBBEB23EA}"/>
		</Row>
	</Table>
	<Table name="t_xref">
		<Row>
			<Column name="XrefID" value="{CB0C747D-2C31-4ad9-864A-81920056C3A0}"/>
			<Column name="Name" value="Stereotypes"/>
			<Column name="Type" value="connector property"/>
			<Column name="Visibility" value="Public"/>
			<Column name="Partition" value="0"/>
			<Column name="Description" value="@STEREO;Name=Relation;FQName=IM::Relation;@ENDSTEREO;"/>
			<Column name="Client" value="{11649298-B3E9-4707-9447-F12045A7E622}"/>
			<Column name="Supplier" value="&lt;none&gt;"/>
		</Row>
	</Table>
</Package>
"""

"""List of Relations 
   {relationguid: {"rela":, "srcentiguid": ,"dstentiguid","....":}}
"""
relations = dict()


def initDomains():
    daty_id = Datatype(pname="unknown"
                       , pbasetype=Datatype.STRING
                       , psrcname=Externalref.SOURCE_EAXML, pscrid="DATYunknown"
                       ).insert()

    doma = Domain(psrcname=Externalref.SOURCE_EAXML, psrcid="DOMAunknown")
    doma.doma_name = "unknown"
    doma.daty_id = daty_id
    doma.doma_type = Domain.TXT
    doma.doma_origin = Domain.DOMAIN
    doma.insert()
    return


def linetype(pidx, pmaxidx, psourcelt, ptargetlt):
    if (pidx < ((pmaxidx - 1) / 2)):
        return psourcelt
    else:
        return ptargetlt
    # fi


# linetype

def connector(pidx, pmaxidx, psource, ptarget):
    # ist kein Segment sondern in Punkt. es macht nur 1 oder M Sinn
    if (pidx == 0):
        return psource
    if (pidx == (pmaxidx - 1)):
        return ptarget
    return None


def doxmlfiles(pdirec, ptransfer, ppattern=r".*", pmandatorydirec=True):
    try:
        listdir = os.listdir(pdirec)
    except Exception as ex:
        if pmandatorydirec:
            logmessages.writelog('dosxmlfiles: directory "{}" not found.'.format(pdirec))
        return
    # try
    for file in listdir:
        if re.match(ppattern, file):
            ptransfer(pdirec + file)
        # fi
    # for


# doxmlfiles


def dosegfiles(pdirec, transferfiles, pmandatoryfile=True):
    try:
        listdir = os.listdir(pdirec)
    except Exception as ex:
        if pmandatoryfile:
            logmessages.writelog('dosSEGfiles: directory "{}" not found.'.format(pdirec))
        return
    # try
    for el in listdir:
        if re.match('seg_.*', el):
            doxmlfiles(pdirec=pdirec + el + '/'
                       , ptransfer=transferfiles
                       , ppattern=r'{}.xml'.format(GUIDPATTERN))
        # fi
    # for
    return


def do1entitydiag(pdiagxml):
    diagguid = handleXML.findColumn(pdiagxml, 'ea_guid')
    diag = Diagram(psrcname=Externalref.SOURCE_EAXML, psrcid=diagguid)
    diag.diag_name = handleXML.findColumn(pdiagxml, 'Name')
    diag.diag_diat_id = Diagramtype.getbyname(pname=Diagramtype.ENTITY).diat_id

    diag.diag_legendx = 0
    diag.diag_legendy = 0
    diag.diag_uc = handleXML.findColumn(pdiagxml, 'Author')
    diag.diag_dc = handleXML.findColumn(pdiagxml, 'CreatedDate')
    diag.diag_um = handleXML.findColumn(pdiagxml, 'ModifiedDate')
    diagid = diag.insert()
    return


def do1diaglink(pdiaglinkxml):
    diagguid = handleXML.findRefGuid(pdiaglinkxml, 'DiagramID')
    diag = Diagram().getbyEAref(psrcid=diagguid)
    if diag is None:
        logmessages.writelog("Diagram {} not found".format(diagguid))
        return
    objguid = handleXML.findRefGuid(pdiaglinkxml, 'ConnectorID')
    rela = Relation().getbyEAref(psrcid=objguid)
    if rela is None:
        logmessages.writelog("Object {} not found for diagram {}".format(objguid, diagguid))
        return

    linewidth = 3
    edge = lambda e: 'N' if (
                e == "0" or e == "1") else 'W' if e == "2" else 'S' if e == "3" else 'O' if e == "4" else 'x'

    relr = Relationrep()
    relr.relr_diag_id = diag.diag_id
    relr.relr_mode_id = rela.rela_id
    relr.relr_linewidth = linewidth
    relr.relr_linecolor = "ffffff"  # transferModel.int2hex(relations[objguid]["linecolor"])
    relr.relr_lineopacity = 100
    relr.relr_startedge = edge(relations[objguid]["Start_Edge"])
    relr.relr_startposition = None
    relr.relr_start_connector = rela.rela_maptype_to_from
    relr.relr_starttext_angle = None
    relr.relr_starttext_distance = None
    relr.relr_starttext_x = 0
    relr.relr_starttext_y = 10
    relr.relr_starttext_width = 30
    relr.relr_starttext_height = 5
    relr.relr_endedge = edge(relations[objguid]["End_Edge"])
    relr.relr_endposition = None
    relr.relr_end_connector = rela.rela_maptype_from_to
    relr.relr_endtext_angle = None
    relr.relr_endtext_distance = None
    relr.relr_endtext_x = 30
    relr.relr_endtext_y = 40
    relr.relr_endtext_width = 30
    relr.relr_endtext_height = 5
    relr.relr_fontcolor = "ffffff"
    relr.relr_fontsize = 10
    relr.relr_uc = "fillDBea"
    relr.relr_dc = datetime.today()
    relr.insert()

    geometry = handleXML.findColumn(pdiaglinkxml, "Geometry")
    nvlsearch = lambda x: x.group(0) if x is not None else None
    sx = nvlsearch(re.search("SX=(\d+);", geometry))
    sy = nvlsearch(re.search("SY=(\d+);", geometry))
    ex = nvlsearch(re.search("EX=(\d+);", geometry))
    ey = nvlsearch(re.search("EY=(\d+);", geometry))
    edge = nvlsearch(re.search("EDGE=(\d+);", geometry))
    print(rela.rela_name, relr.relr_startedge, sx, sy, ex, ey, edge)
    print(relations[objguid])
    print(geometry)
    return


def do1diagobj(pdiagobjxml):
    diagguid = handleXML.findRefGuid(pdiagobjxml, 'Diagram_ID')
    diag = Diagram().getbyEAref(psrcid=diagguid)
    if diag is None:
        logmessages.writelog("Diagram {} not found".format(diagguid))
        return
    objguid = handleXML.findRefGuid(pdiagobjxml, 'Object_ID')
    obj = Entity().getbyEAref(psrcid=objguid)
    if obj is None:
        logmessages.writelog("Object {} not found for diagram {}".format(objguid, diagguid))
        return

    # Diagram and Object found
    entix = int(handleXML.findColumn(pdiagobjxml, 'RectLeft'))
    entiy = -int(handleXML.findColumn(pdiagobjxml, 'RectTop'))
    r = int(handleXML.findColumn(pdiagobjxml, 'RectRight'))
    b = -int(handleXML.findColumn(pdiagobjxml, 'RectBottom'))
    entiwidth = r - entix
    entiheight = b - entiy
    eler = Elementrep()
    eler.eler_mode_id = obj.enti_id
    eler.eler_diag_id = diag.diag_id
    eler.eler_index = 0
    eler.eler_position_x = entix
    eler.eler_position_y = entiy
    eler.eler_width = entiwidth
    eler.eler_height = entiheight
    eler.eler_opacity = 100
    col = transferModel.getentity(objguid,"color")
    eler.eler_color = transferModel.int2hex(col.backgcolor)
    eler.eler_marginwidth = None
    eler.eler_marginopacity = 100
    eler.eler_margincolor = transferModel.int2hex(col.foregcolor)
    eler.eler_fontsize = col.fontsize
    eler.eler_fontcolor = transferModel.int2hex(col.fontcolor)
    eler.eler_uc = "fillDBea"
    eler.eler_dc = datetime.today()
    eler.insert()
    return


def transferobjtypes(proot, pobjtype, ptransferfunc, **restrictions):
    objs = proot.find(f"Table[@name='{pobjtype}']")
    for obj in objs:
        # check, that all restrictions for objecttype are met
        restrictionmet = True
        for type, value in restrictions.items():
            restrictionmet = restrictionmet and (handleXML.findColumn(obj, type) == value)
        if restrictionmet:
            ptransferfunc(obj)
    return


def findorcreateDomain(pattrname, pfathername, pdomatype, pattr, pintfid=None
                       , pdomguid=None, pstructdomguid=None, ptypeguid=None):
    return Domain().getunknown().doma_id


def do1Attribute(pattrxml):
    vaterguid = handleXML.findRefGuid(pattrxml, "Object_ID")
    vater = Entity().getbyEAref(psrcid=vaterguid)
    attrname = handleXML.findColumn(pattrxml, "Name")

    attr = Attribute(pname=transferModel.removeattrmeta(attrname), pentiid=vater.enti_id
                     , psrcname=Externalref.SOURCE_EAXML, psrcid=handleXML.findColumn(pattrxml, 'ea_guid'))
    if attr.attr_tech_name is None:
        attr.attr_tech_name = re.sub('[-,.()\[\]äöüèéàÄ~ÖÜ ]', '_', str.upper(attr.attr_displ_name))
    attr.attr_uc = "filldbea"
    attr.attr_dc = datetime.now()

    attr.attr_descr = handleXML.findText(pattrxml, 'Note')
    # attr.attr_displ_seq = plfnr
    attr.attr_is_descriptive = 'FALSE'
    attr.attr_is_mandatory = 'FALSE'  # Boolean.bool2str(handleXML.findText(pattrxml, 'nullsAllowed') != 'true')
    attr.attr_is_historicised = Boolean.bool2str(transferModel.is_historisized(attrname))
    attr.attr_is_repeated = Boolean.bool2str(transferModel.is_repeated(attrname))
    attr.attr_is_translated = Boolean.bool2str(transferModel.is_langdept(attrname))
    attr.attr_is_encrypted = 'FALSE'
    domaguid = handleXML.findRefGuid(pattrxml,"Classifier")
    if domaguid is not None:
        doma = Domain().getbyEAref(psrcid=domaguid)
        if doma is None:
            logmessages.writelog(f"Unknown domain {domaguid}")
            doma = Domain().getunknown()
    attr.attr_doma_id = doma.doma_id
    attrId = attr.insert()

    return


def fillKeys(p_enti, p_entiid):
    global schluessel
    allkeys = p_enti.find('identifiers')
    if allkeys is not None:
        for key in allkeys.findall('identifier'):
            kr = handleXML.findText(key, 'newElementsIDs')
            if (kr is not None):
                keyrefs = kr.split(',')
                # print(idx, handleXML.findField(enti,'name'), handleXML.findField(key,'id'), handleXML.findField(enti,'id'), keyrefs)
                keys = Key(psrcid=handleXML.findField(key, 'id'), psrcname=Externalref.SOURCE_ODM)
                keys.keys_name = handleXML.findField(key, 'name')
                keys.keys_uc = handleXML.findText(key, 'createdBy')
                keys.keys_dc = handleXML.findText(key, 'createdTime')
                keys.keys_enti_id = p_entiid
                keys.insert()

                schluessel.append([keys, keyrefs])
            # fi
        # rof
        # [Key, (listof attr and relationship guids)]
    # fi


def transferKeys():
    global schluessel
    # Schlüssel sind eingefügt es folgen die SchlüsselElemente, die ich jetzt alle haben sollte
    # schlüssel [[Key, (Liste der Referenzen)]]
    for schlentry in schluessel:
        key = schlentry[0]
        reflist = schlentry[1]
        # nun die Schlüsselelemente
        for ke in reflist:
            kele = Keyelement()
            kele.kele_keys_id = key.keys_id
            kele.kele_uc = key.keys_uc
            kele.kele_dc = key.keys_dc
            kele.kele_attr_id = Attribute().getIDbyODMref(psrcid=ke)
            if kele.kele_attr_id is None:
                kele.kele_rela_id = Relation().getIDbyODMref(psrcid=ke)
                kele.kele_attr_id = None
                if kele.kele_rela_id is None:
                    logmessages.writelog(
                        "key-element {} for key {} in entity {} is probably attribute group member and will be ignored ".format(
                            ke, key.keys_name, Entity().getbyid(key.keys_enti_id).getname()))
                    continue
            else:
                kele.kele_rela_id = None
            # if
            kele.insert()
        # for
    # for


def parseXML(pfilename):
    try:
        tree = et.parse(pfilename)
    except Exception as err:
        logmessages.writelog("File ({}) could not be handled".format(pfilename))
        print(pfilename)
        raise
    # try
    return tree

def handleSuperentities():
    global entities
    for entiguid,entiinfo in entities:
        if entiinfo["superentitityguid"] is None:
            continue

    #for
    return

def do1Entity(pentitiy):
    entiguid: str = handleXML.findColumn(pentitiy, 'ea_guid')
    enti = Entity(psrcname=Externalref.SOURCE_EAXML, psrcid=entiguid)
    enti.enti_name = handleXML.findColumn(pentitiy, "Name")
    enti.enti_descr = handleXML.findColumn(pentitiy, 'Note')
    enti.enti_uc = handleXML.findColumn(pentitiy, 'Author')
    enti.enti_dc = handleXML.findColumn(pentitiy, 'CreatedDate')
    enti.enti_dm = handleXML.findColumn(pentitiy, 'ModifiedDate')

    parentguid = handleXML.findRefGuid(pentitiy,"ParentID")

    entiId = enti.insert()

    color = transferModel.Color(foregcolor=transferModel.Color.WHITE
                                , backgcolor=transferModel.hex2int("c3f062")
                                , fontcolor=transferModel.Color.BLUE
                                , fontname=None
                                , fontsize=10
                                , fontstyle=None
                                )
    transferModel.setentity(entiguid,entity= enti, superentitityguid=parentguid,color=color
                            ,subentities=[], categoryguid=None)
    return


def do1LOV(plovvalue):
    deva = DefaultValue()
    deva.deva_value = handleXML.findColumn(plovvalue, "Name")
    deva.deva_descr = handleXML.findColumn(plovvalue, "Note")
    deva.deva_uc = "filldbea"
    deva.deva_dc = datetime.today()
    deva.deva_sort_order = handleXML.findColumn(plovvalue, "Pos")
    domaguid = handleXML.findRefGuid(plovvalue, "Object_ID")
    doma = Domain().getbyEAref(psrcid=domaguid)
    if doma is None:
        logmessages.writelog(f"Domain {domaguid}for domainvalue {deva.deva_name} not found")
    else:
        deva.deva_doma_id = doma.doma_id
        deva.insert()
    return


def do1Domain(pdomain):
    domaguid: str = handleXML.findColumn(pdomain, 'ea_guid')
    doma = Domain(psrcname=Externalref.SOURCE_EAXML, psrcid=domaguid)
    doma.doma_name = handleXML.findColumn(pdomain, "Name")
    doma.doma_origin = Domain.DOMAIN
    doma.doma_type = Domain.LOV
    doma.doma_descr = handleXML.findColumn(pdomain, 'Note')
    doma.doma_uc = handleXML.findColumn(pdomain, 'Author')
    doma.doma_dc = handleXML.findColumn(pdomain, 'CreatedDate')
    doma.doma_dm = handleXML.findColumn(pdomain, 'ModifiedDate')

    domaId = doma.insert()
    return


def do1Arc(parc):
    global relations
    arcguid: str = handleXML.findColumn(parc, 'ea_guid')
    arc = Arc(psrcname=Externalref.SOURCE_EAXML, psrcid=arcguid)
    arc.arcs_name = handleXML.findColumn(parc, "Name") + handleXML.findColumn(parc, "Object_ID")
    arc.arcs_uc = handleXML.findColumn(parc, 'Author')
    arc.arcs_dc = handleXML.findColumn(parc, 'CreatedDate')
    arc.arcs_dm = handleXML.findColumn(parc, 'ModifiedDate')

    arcbase = [(relaguid, rela) for relaguid, rela in relations.items() if
               (rela["isArc"] and (rela["srcentiguid"] == arcguid or rela["dstentiguid"] == arcguid))]
    if len(arcbase) != 1:
        logmessages.writelog(f"Arc {arcguid} has not exactly one arc-relationship")
        return
    # fi
    arcbase = arcbase[0]
    srcentiguid, dstentiguid = arcbase[1]["srcentiguid"], arcbase[1]["dstentiguid"]
    arcentiguid = srcentiguid if dstentiguid == arcguid else dstentiguid
    arcenti = Entity().getbyEAref(psrcid=arcentiguid)
    if arcenti is None:
        logmessages.writelog(f"Arc {arcguid} not connected to knwon entity {arcentiguid}")
        return

    arc.arcs_enti_id = arcenti.enti_id
    arcID = arc.insert()

    arcrelas = {relaguid: rela for relaguid, rela in relations.items() if
                (not rela["isArc"] and (rela["srcentiguid"] == arcguid or rela["dstentiguid"] == arcguid))}
    for relaguid, arcrela in arcrelas.items():
        srcentiguid, dstentiguid = arcrela["srcentiguid"], arcrela["dstentiguid"]
        otherentiguid = srcentiguid if dstentiguid == arcguid else dstentiguid
        otherenti = Entity().getbyEAref(psrcid=otherentiguid)
        if otherenti is None:
            logmessages.writelog(f"Arc {arcguid} not connected to known entity {otherentiguid}")
            continue

        rela = arcrela["rela"]
        rela.rela_arc_id_from = arcID if srcentiguid == arcguid else None
        rela.rela_arc_id_to = arcID if dstentiguid == arcguid else None
        rela.rela_enti_id_from = arcenti.enti_id if srcentiguid == arcguid else otherenti.enti_id
        rela.rela_enti_id_to = arcenti.enti_id if srcentiguid != arcguid else otherenti.enti_id
        rela.insert()
    return


def do1Relation(prelaxml):
    global relations
    relaguid = handleXML.findColumn(prelaxml, 'ea_guid')
    srcentiguid = handleXML.findRefGuid(prelaxml, "Start_Object_ID")
    srcenti = Entity().getbyEAref(psrcid=srcentiguid)
    dstentiguid = handleXML.findRefGuid(prelaxml, "End_Object_ID")
    dstenti = Entity().getbyEAref(psrcid=dstentiguid)
    relaname = "RELA-" + handleXML.findColumn(prelaxml, "Connector_ID")

    rela = Relation(psrcname=Externalref.SOURCE_EAXML, psrcid=relaguid)
    rela.rela_name = relaname
    rela.rela_assoc_from_to = handleXML.findColumn(prelaxml, 'SourceRole')
    rela.rela_hist_from_to = Boolean.bool2str(transferModel.is_historisized(rela.rela_assoc_from_to))
    rela.rela_assoc_to_from = handleXML.findColumn(prelaxml, 'DestRole')
    rela.rela_hist_to_from = Boolean.bool2str(transferModel.is_historisized(rela.rela_assoc_to_from))
    srccard = handleXML.findColumn(prelaxml, "SourceCard")
    dstcard = handleXML.findColumn(prelaxml, "DestCard")
    rela.rela_maptype_from_to = None if srccard is None else Relation.ONE if (
                srccard in ('1', '0..1')) else Relation.MANY
    rela.rela_maptype_to_from = None if dstcard is None else Relation.ONE if (
                dstcard in ('1', '0..1')) else Relation.MANY
    rela.rela_mandatory_from_to = Boolean.bool2str(srccard in ('1', '*'))
    rela.rela_mandatory_to_from = Boolean.bool2str(srccard in ('1', '*'))
    rela.rela_type = rela.simpleType()
    rela.rela_uc = "filldbea"
    rela.rela_dc = datetime.now()

    isArc = handleXML.findColumn(prelaxml, 'Stereotype') == "Arc"
    if not isArc and (srccard is None or dstcard is None):
        logmessages.writelog(
            f"Relationship from {srcenti.enti_name if srcenti is not None else 'Arc'} to {dstenti.enti_name if dstenti is not None else 'Arc'} must have cardinalities on both ends.")
        return

    # postpone relations to ARCS
    if srcenti is not None and dstenti is not None:
        rela.rela_enti_id_from = srcenti.enti_id
        rela.rela_enti_id_to = dstenti.enti_id
        rela.insert()
    # fi

    relations[relaguid] = {"rela": rela
        , "srcentiguid": srcentiguid, "dstentiguid": dstentiguid
        , "isArc": isArc
        , "linecolor": 0
        , "Start_Edge": handleXML.findColumn(prelaxml, "Start_Edge")
        , "End_Edge": handleXML.findColumn(prelaxml, "End_Edge")
        , "PtStartX": handleXML.findColumn(prelaxml, "PtStartX")
        , "PtStartY": handleXML.findColumn(prelaxml, "PtStartY")
        , "PtEndX": handleXML.findColumn(prelaxml, "PtEndX")
        , "PtEndY": handleXML.findColumn(prelaxml, "PtEndY")
                           }
    return


def filllanguages():
    Languagetext.insertlang_texts(pudpthema=None)
    # copy comma-list-synonym into synoyms
    Synonym.transfersynotransl()
    # fill all elements in default language
    Languagetext.filldefaulttext(parameters.dbDefaultLangID())
    Language.deleteunused()
    return


def transfer1project(pprojxml):
    defspra = parameters.dbDefaultLang()
    sprachen = parameters.dbLanguages()
    proj = Project()
    proj.proj_name = handleXML.findColumn(pprojxml, 'Name')
    proj.proj_uc = "fillDBea"
    proj.proj_dc = handleXML.findColumn(pprojxml, 'CreatedDate')
    proj.proj_dm = handleXML.findColumn(pprojxml, 'ModifiedDate')
    proj.proj_languages = sprachen
    proj.proj_curr_lang = defspra
    proj.insert()
    if defspra is not None:
        defspra = defspra.lower()
        defspraid = Language.spraidlookup(piso=defspra)
        # setze die Defaultsprache aus dem Modell
        if defspraid is None:
            raise Exception("Language '{}' does not exist".format(defspra))
        else:
            Language.setmodellang(pmodellang=defspra)
            Language.setallreplacementlang()
            parameters.dbDefaultLang(defspra)
            parameters.dbDefaultLangID(defspraid)
    # fi
    return


def transferEAModel(**kwargs):
    """überträgt das ganze EA Modell aus einem XML in die DB"""
    infile = handleXML.searchfile(pfilename=kwargs["pinput"], pdefaultdirec=parameters.baseDirec())
    eaxml = handleXML.parseXML(pfilename=infile)
    earoot = eaxml.getroot()

    transferModel.insertlanguages()
    initDomains()
    transferobjtypes(proot=earoot, pobjtype='t_package'
                     , ptransferfunc=transfer1project
                     )
    transferobjtypes(proot=earoot, pobjtype='t_object'
                     , ptransferfunc=do1Entity
                     , Object_Type="Class"
                     , Stereotype="Entity")
    transferModel.doSubentities()

    transferobjtypes(proot=earoot, pobjtype='t_object'
                     , ptransferfunc=do1Domain
                     , Stereotype="Domain")

    transferobjtypes(proot=earoot, pobjtype='t_attribute'
                     , ptransferfunc=do1LOV
                     , Stereotype="enum")

    transferobjtypes(proot=earoot, pobjtype='t_attribute'
                     , ptransferfunc=do1Attribute
                     , Stereotype="Attribute")

    transferobjtypes(proot=earoot, pobjtype='t_connector'
                     , ptransferfunc=do1Relation
                     , Stereotype="Relation")

    transferobjtypes(proot=earoot, pobjtype='t_connector'
                     , ptransferfunc=do1Relation
                     , Stereotype="Arc")

    transferobjtypes(proot=earoot, pobjtype='t_object'
                     , ptransferfunc=do1Arc
                     , Stereotype="Arc")

    filllanguages()

    transferobjtypes(proot=earoot, pobjtype='t_diagram'
                     , ptransferfunc=do1entitydiag
                     , Diagram_Type="Logical")

    transferobjtypes(proot=earoot, pobjtype='t_diagramobjects'
                     , ptransferfunc=do1diagobj
                     )

    transferobjtypes(proot=earoot, pobjtype='t_diagramlinks'
                     , ptransferfunc=do1diaglink
                     )

    # transferdiagattrs()

    return
# end transferEAModel
