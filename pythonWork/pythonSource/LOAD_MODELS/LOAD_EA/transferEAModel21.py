import math
import os
import re
import xml.etree.ElementTree as et
from datetime import datetime

import handleXML
from SSOT_infra import parameters, logmessages,int2hex
from SSOT_db.IM_OBJECTS import  *
from LOAD_MODELS.LOAD_ODM import transferModel

XMIVERSION = "2.1"
XMIPREFIX = f"{{http://schema.omg.org/spec/XMI/{XMIVERSION}}}"
SOURCE_EAXMI: str = 'EAXMI'

"""List of Relations 
   {relationguid: {"rela":, "srcentiguid": ,"dstentiguid","....":}}
"""
relations = dict()
def getrelationkeys():
    global relations
    return relations.keys()
def setrelation(pguid,**kwargs):
    global relations
    if pguid not in relations: relations[pguid]={}
    for key,val in kwargs.items():
        relations[pguid][key]=val
def getrelation(pguid,pvalue=None):
    global relations
    if pvalue is None:
        return relations[pguid]
    else:
        return relations[pguid][pvalue]


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

def movediaglegend():
    """move the legend to the lower left if it overlaps any element"""
    return


def inslineseg(prelrid,pseq,px,py,pmandatory,pangle):
    lineseg = Linesegment()
    lineseg.lise_relr_id = prelrid
    lineseg.lise_seq = pseq
    lineseg.lise_x = px
    lineseg.lise_y = py
    lineseg.lise_linetype = Linesegment.SOLID if pmandatory else Linesegment.DASHED
    lineseg.lise_angle = pangle
    lineseg.insert()
    return

def do1diaglink(pdiaglinkxml):
    diagguid = handleXML.findRefGuid(pdiaglinkxml, 'DiagramID')
    diag = Diagram().getbyextref(psrcid=diagguid,psrcname=SOURCE_EAXMI)
    if diag is None:
        logmessages.writelog("Diagram {} not found".format(diagguid))
        return
    objguid = handleXML.findRefGuid(pdiaglinkxml, 'ConnectorID')
    rela = Relation().getbyextref(psrcid=objguid,psrcname=SOURCE_EAXMI)
    if rela is None:
        logmessages.writelog("Object {} not found for diagram {}".format(objguid, diagguid))
        return

    linewidth = 3
    edge = lambda e: Linesegment.NORTH if (e == Linesegment.EAST or e == "1") \
                    else Linesegment.WEST if e == "2" \
                        else Linesegment.SOUTH if e == "3"\
                        else Linesegment.EAST if e == "4" \
                            else 'x'

    relr = Relationrep()
    relr.relr_diag_id = diag.diag_id
    relr.relr_mode_id = rela.rela_id
    relr.relr_linewidth = linewidth
    relr.relr_linecolor = "ffffff"  # int2hex(getrelation(objguid,"linecolor"))
    relr.relr_lineopacity = 100
    relr.relr_startedge = edge(getrelation(objguid,"Start_Edge"))
    relr.relr_startposition = None
    relr.relr_start_connector = rela.rela_maptype_to_from
    relr.relr_starttext_angle = None
    relr.relr_starttext_distance = None
    relr.relr_starttext_x = 0
    relr.relr_starttext_y = 10
    relr.relr_starttext_width = 30
    relr.relr_starttext_height = 5
    relr.relr_endedge = edge(getrelation(objguid,"End_Edge"))
    relr.relr_endposition = None
    relr.relr_end_connector = rela.rela_maptype_from_to
    relr.relr_endtext_angle = None
    relr.relr_endtext_distance = None
    relr.relr_endtext_x = 30
    relr.relr_endtext_y = 40
    relr.relr_endtext_width = 30
    relr.relr_endtext_height = 5
    relr.relr_fontcolor = "000000"
    relr.relr_fontsize = 10
    relr.relr_uc = "fillDBea"
    relr.relr_dc = datetime.today()
    relrID= relr.insert()


    seqNr =0
    entirefft = Elementrep().getbyuk(eler_diag_id=diag.diag_id,eler_mode_id=Relation().getbyid(relr.relr_mode_id).rela_enti_id_from)
    entireftf = Elementrep().getbyuk(eler_diag_id=diag.diag_id,eler_mode_id=Relation().getbyid(relr.relr_mode_id).rela_enti_id_to)
    #geometry = handleXML.findColumn(pdiaglinkxml, "Geometry")
    # nvlsearch = lambda x: x.group(1) if x is not None else None
    # sx = int(nvlsearch(re.search("SX=([\d-]+);", geometry)))
    # sy = int(nvlsearch(re.search("SY=([\d-]+);", geometry)))
    # ex = int(nvlsearch(re.search("EX=([\d-]+);", geometry)))
    # ey = int(nvlsearch(re.search("EY=([\d-]+);", geometry)))
    # edge = nvlsearch(re.search("EDGE=(\d+);", geometry))

    startX = entirefft.eler_position_x + (entirefft.eler_width/2 if relr.relr_startedge in (Linesegment.SOUTH,Linesegment.NORTH)\
                                         else entirefft.eler_width  if relr.relr_startedge in (Relationrep.EAST)\
                                         else 0)
    startY=entirefft.eler_position_y + (entirefft.eler_height/2 if relr.relr_startedge in (Linesegment.EAST,Linesegment.WEST)\
                                         else entirefft.eler_height  if relr.relr_startedge in (Relationrep.SOUTH)\
                                        else 0)
    endX= entireftf.eler_position_x + (entireftf.eler_width/2 if relr.relr_endedge in (Linesegment.SOUTH,Linesegment.NORTH)\
                                         else entireftf.eler_width  if relr.relr_endedge in (Relationrep.EAST)\
                                         else 0)
    endY=entireftf.eler_position_y + (entireftf.eler_height/2 if relr.relr_endedge in (Linesegment.EAST,Linesegment.WEST)\
                                         else entireftf.eler_height  if relr.relr_endedge in (Relationrep.SOUTH)\
                                        else 0)

    inslineseg(prelrid=relrID,pseq=seqNr,px=startX
               ,py=startY
               ,pmandatory=rela.getmandatorytofrom(),pangle=math.pi / 2)
    seqNr+=1
    inslineseg(prelrid=relrID,pseq=seqNr,px=startX + (endX-startX)/2
               ,py=startY + (endY-startY)/2
               ,pmandatory=rela.getmandatoryfromto(),pangle=math.pi / 2)
    seqNr+=1
    inslineseg(prelrid=relrID,pseq=seqNr,px=endX
               ,py=endY
               ,pmandatory=rela.getmandatoryfromto(),pangle=math.pi / 2)

    return


def do1diagobj(pdiagobjxml):
    diagguid = handleXML.findRefGuid(pdiagobjxml, 'Diagram_ID')
    diag = Diagram().getbyextref(psrcid=diagguid,psrcname=SOURCE_EAXMI)
    if diag is None:
        logmessages.writelog("Diagram {} not found".format(diagguid))
        return
    objguid = handleXML.findRefGuid(pdiagobjxml, 'Object_ID')
    obj = Entity().getbyextref(psrcid=objguid,psrcname=SOURCE_EAXMI)
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
    col = transferModel.getentity(objguid, "color")
    eler.eler_color = int2hex(col.backgcolor)
    eler.eler_marginwidth = None
    eler.eler_marginopacity = 100
    eler.eler_margincolor = int2hex(col.foregcolor)
    eler.eler_fontsize = col.fontsize
    eler.eler_fontcolor = int2hex(col.fontcolor)
    eler.eler_uc = "fillDBea"
    eler.eler_dc = datetime.today()
    eler.insert()
    return


def transferobjtypes(proot, ptransferfunc, **restrictions):
    objs = proot.find("elements")
    for obj in objs:
        # check, that all restrictions for objecttype are met
        restrictionmet = True
        for type, value in restrictions.items():
            restrictionmet = restrictionmet and (handleXML.findField(obj, XMIPREFIX+"type") == f"uml:{value}")
        if restrictionmet:
            ptransferfunc(obj)
    return


def findorcreateDomain(pattrname, pfathername, pdomatype, pattr, pintfid=None
                       , pdomguid=None, pstructdomguid=None, ptypeguid=None):
    return Domain().getunknown().doma_id


def do1Attribute(pattrxml):
    vaterguid = handleXML.findRefGuid(pattrxml, "Object_ID")
    vater = Entity().getbyextref(psrcid=vaterguid,psrcname=SOURCE_EAXMI)
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
        doma = Domain().getbyextref(psrcid=domaguid,psrcname=SOURCE_EAXMI)
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
                keys = Key(psrcid=handleXML.findField(key, 'id'), psrcname=SOURCE_EAXMI)
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
            kele.kele_attr_id = Attribute().getIDbyextref(psrcid=ke,psrcname=SOURCE_EAXMI)
            if kele.kele_attr_id is None:
                kele.kele_rela_id = Relation().getIDbyextref(psrcid=ke,psrcname=SOURCE_EAXMI)
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
    transferModel.setentity(entiguid, entity= enti, superentitityguid=parentguid, color=color
                            , subentities=[], categoryguid=None)
    return


def do1LOV(plovvalue):
    deva = DefaultValue()
    deva.deva_value = handleXML.findColumn(plovvalue, "Name")
    deva.deva_descr = handleXML.findColumn(plovvalue, "Note")
    deva.deva_uc = "filldbea"
    deva.deva_dc = datetime.today()
    deva.deva_sort_order = handleXML.findColumn(plovvalue, "Pos")
    domaguid = handleXML.findRefGuid(plovvalue, "Object_ID")
    doma = Domain().getbyextref(psrcid=domaguid,psrcname=SOURCE_EAXMI)
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

    arcguid: str = handleXML.findColumn(parc, 'ea_guid')
    arc = Arc(psrcname=Externalref.SOURCE_EAXML, psrcid=arcguid)
    arc.arcs_name = handleXML.findColumn(parc, "Name") + handleXML.findColumn(parc, "Object_ID")
    arc.arcs_uc = handleXML.findColumn(parc, 'Author')
    arc.arcs_dc = handleXML.findColumn(parc, 'CreatedDate')
    arc.arcs_dm = handleXML.findColumn(parc, 'ModifiedDate')

    arcbase,arcrelas = [],[]
    for relaguid in getrelationkeys():
        if (getrelation(relaguid, "srcentiguid") != arcguid and getrelation(relaguid, "dstentiguid") != arcguid):
            continue
        if getrelation(relaguid,"isArc"):
            arcbase.append(relaguid)
        else:
            arcrelas.append(relaguid)
    #for

    if len(arcbase) != 1:
        logmessages.writelog(f"Arc {arcguid} has not exactly one arc-relationship")
        return
    # fi
    arcbase = getrelation(arcbase[0])
    srcentiguid, dstentiguid = arcbase["srcentiguid"], arcbase["dstentiguid"]
    arcentiguid = srcentiguid if dstentiguid == arcguid else dstentiguid
    arcenti = Entity().getbyextref(psrcid=arcentiguid,psrcname=SOURCE_EAXMI)
    if arcenti is None:
        logmessages.writelog(f"Arc {arcguid} not connected to knwon entity {arcentiguid}")
        return

    arc.arcs_enti_id = arcenti.enti_id
    arcID = arc.insert()

    for relaguid in arcrelas:
        srcentiguid, dstentiguid = getrelation(relaguid,"srcentiguid"), getrelation(relaguid,"dstentiguid")
        otherentiguid = srcentiguid if dstentiguid == arcguid else dstentiguid
        otherenti = Entity().getbyextref(psrcid=otherentiguid,psrcname=SOURCE_EAXMI)
        if otherenti is None:
            logmessages.writelog(f"Arc {arcguid} not connected to known entity {otherentiguid}")
            continue

        rela = getrelation(relaguid,"rela")
        rela.rela_arc_id_from = arcID if srcentiguid == arcguid else None
        rela.rela_arc_id_to = arcID if dstentiguid == arcguid else None
        rela.rela_enti_id_from = arcenti.enti_id if srcentiguid == arcguid else otherenti.enti_id
        rela.rela_enti_id_to = arcenti.enti_id if srcentiguid != arcguid else otherenti.enti_id
        rela.insert()
    return


def do1Relation(prelaxml):
    relaguid = handleXML.findColumn(prelaxml, 'ea_guid')
    srcentiguid = handleXML.findRefGuid(prelaxml, "Start_Object_ID")
    srcenti = Entity().getbyextref(psrcid=srcentiguid,psrcname=SOURCE_EAXMI)
    dstentiguid = handleXML.findRefGuid(prelaxml, "End_Object_ID")
    dstenti = Entity().getbyextref(psrcid=dstentiguid,psrcname=SOURCE_EAXMI)
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

    setrelation(relaguid, rela= rela
        , srcentiguid= srcentiguid, dstentiguid= dstentiguid
        , isArc= isArc
        , linecolor= 0
        , Start_Edge= handleXML.findColumn(prelaxml, "Start_Edge")
        , End_Edge= handleXML.findColumn(prelaxml, "End_Edge")
        , PtStartX= handleXML.findColumn(prelaxml, "PtStartX")
        , PtStartY= handleXML.findColumn(prelaxml, "PtStartY")
        , PtEndX= handleXML.findColumn(prelaxml, "PtEndX")
        , PtEndY= handleXML.findColumn(prelaxml, "PtEndY"))
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
    proj.proj_name = handleXML.findField(pprojxml, 'name')
    proj.proj_uc = "fillDBea"
    times = pprojxml.find('times')
    proj.proj_dc = handleXML.findField(times, 'created')
    proj.proj_dm = handleXML.findField(times, 'modified')
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

    fileversion = handleXML.findField(earoot,f'{XMIPREFIX}version')
    assert (fileversion == XMIVERSION), f"File has version {fileversion} (expected {XMIVERSION})"

    for element in earoot:
        if element.tag.endswith('Model'):
            modele = element
        if element.tag.endswith('Extension'):
            extension = element

    transferModel.insertlanguages()
    initDomains()
    transferobjtypes(proot=extension
                     , ptransferfunc=transfer1project
                     ,Type = "Package"
                     )
    transferobjtypes(proot=modelroot
                     , ptransferfunc=do1Entity
                     , Type="Class")
    transferModel.doSubentities()

    transferobjtypes(proot=modelroot
                     , ptransferfunc=do1Domain
                     , Stereotype="Domain")

    transferobjtypes(proot=modelroot
                     , ptransferfunc=do1LOV
                     , Stereotype="Enumeration")

    transferobjtypes(proot=modelroot
                     , ptransferfunc=do1Arc
                     , Type="Constraint")


    transferobjtypes(proot=modelroot
                     , ptransferfunc=do1Relation
                     , Type="")

    transferobjtypes(proot=modelroot
                     , ptransferfunc=do1Arc
                     , Type="Constraint")

    filllanguages()

    transferobjtypes(proot=modelroot, pobjtype='t_diagram'
                     , ptransferfunc=do1entitydiag
                     , Diagram_Type="Logical")

    transferobjtypes(proot=modelroot, pobjtype='t_diagramobjects'
                     , ptransferfunc=do1diagobj
                     )

    transferobjtypes(proot=modelroot, pobjtype='t_diagramlinks'
                     , ptransferfunc=do1diaglink
                     )
    movediaglegend()

    # transferdiagattrs()

    return
# end transferEAModel
