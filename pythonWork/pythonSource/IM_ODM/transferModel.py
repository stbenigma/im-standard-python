import math
import os, re
from IM_DB import dbConnect, parameters, logmessages
from IM_OBJECTS import *
from IM_ODM import transferRelational,handleXML
from mystring import nvl



GUIDPATTERN: str = '[A-Z0-9-]{20,45}'
UDPEXTENSION: str = 'udposdm'

def hex2int(phex):
    return None if (phex is None) else int(phex, 16)

def int2hex(pint):
    if (pint is None): return pint
    lint = pint if (type(pint) == int) else int(pint)
    retval = hex(lint & 0xfffffff)
    retval = retval[2:8]
    return retval

class Color:
    BLACK = 0
    WHITE = -1
    BLUE = hex2int("602de8")
    def __init__(self, foregcolor=None, backgcolor=None, fontcolor=None, fontname=None, fontsize=None, fontstyle=None):
        self.backgcolor = backgcolor
        self.foregcolor = foregcolor
        self.fontcolor = fontcolor
        self.fontname = fontname
        self.fontsize = fontsize
        self.fontstyle = fontstyle
    # end __init__
# Color

""" entry of keys found in entites
 [Key, (listof attr and relationship guids)]
"""
schluessel = []

""" Classification type colors
 classguid : Color
"""
classcolors = dict()
""" Classification id's
 classguid : id
"""
classids = dict()

""" default colors
 {elementtypename : Color}
"""
defcolors = dict()

"""List of entities die erst bearbeitet werden können, wenn alle entities geladen sind
   {entityguid: {"entity":, "color":, "superentitityguid":, "subentities":[ids], "categoryguid":}}
"""
entities = dict()
def getentitykeys():
    global entities
    return entities.keys()
def setentity(pguid,**kwargs):
    global entities
    if pguid not in entities: entities[pguid]={}
    for key,val in kwargs.items():
        entities[pguid][key]=val
def getentity(pguid,pvalue=None):
    global entities
    if pvalue is None:
        return entities[pguid]
    else:
        return entities[pguid][pvalue]

"""domains in non-default file are IM or interface (relationale model) dependent.
    fix interface-id of Domains at end of transfer.
    {doma_id : filename of domainfile}
 """
interfacedomains = dict()

def nameflags(pstr: str, pflag: str) -> bool:
    """checks [NLT] at end of names (my erd-Extension)"""
    if (pstr is None): return False
    lmatch = "\[.{0,2}" + pflag + ".{0,2}\]"
    return True if re.search(lmatch, pstr) else False


def is_historisized(pstr: str) -> bool:
    return nameflags(pstr=pstr, pflag='T')


def is_langdept(pstr: str) -> bool:
    return nameflags(pstr=pstr, pflag='L')


def is_repeated(pstr: str) -> bool:
    return nameflags(pstr=pstr, pflag='N')


def transferTypes():
    types = handleXML.parseXML(pfilename=parameters.odmIMDirec() + parameters.odmKonfDirec() + parameters.odmTypesFile())
    root = types.getroot()
    for typ in root.findall('logicaltype'):
        Datatype(pname=handleXML.findField(typ, 'name')
                 , pbasetype=Datatype.baseType(handleXML.findText(typ, 'mapping'))
                ,psrcname=Externalref.SOURCE_ODM,pscrid=handleXML.findField(typ, 'objectid')
                ).insert()
    # endfor

"""List of not yet finished domain
    {id of unfinished domain : guid of type it is supposed to be}"""
unkndomains = {}
def do1structtype(filename):
    global unkndomains
    structdomains = handleXML.parseXML(pfilename=filename)
    structdom = structdomains.getroot()
    if (handleXML.findField(structdom, "class") != "oracle.dbtools.crest.model.design.datatypes.StructuredType"): return
    # print (handleXML.findField(structdom,"name"))
    doma = Domain(psrcname=Externalref.SOURCE_ODM,psrcid=handleXML.findField(structdom, "id"))
    doma.doma_name = handleXML.findField(structdom, "name")
    doma.doma_descr = handleXML.findText(structdom, "comment")
    doma.doma_uc = handleXML.findText(structdom, "createdBy")
    doma.doma_dc = handleXML.findText(structdom, "createdTime")
    doma.doma_type = Domain.GRP
    doma.doma_origin = Domain.DOMAIN

    doma.insert()

    elements = structdom.findall("attributes/Attribute")
    for el in elements:
        # print (doma.doma_name,handleXML.findField(el,"name"),handleXML.findText(el,'type'))
        dgrmsrcid =handleXML.findField(el, 'id')
        dgrm = DomaingroupMember(psrcname=Externalref.SOURCE_ODM, psrcid=dgrmsrcid)
        dgrm.dgrm_doma_id_group = doma.doma_id
        dgrm.dgrm_name = handleXML.findField(el, "name")
        dgrm.dgrm_descr = handleXML.findText(el, "comment")
        dgrm.dgrm_uc = handleXML.findText(el, "createdBy")
        dgrm.dgrm_dc = handleXML.findText(el, "createdTime")
        dgrm.dgrm_is_mandatory = Boolean.bool2str(Boolean.str2bool(handleXML.findText(el, "mandatory")))

        """in struct types the "type" is either datatype or structtype or domain """
        reftypeguid = handleXML.findText(el, 'type')
        reftype = Modelelement.getelementbyextref(psrcname=Externalref.SOURCE_ODM,psrcid=reftypeguid)
        unknowndoma = True
        if isinstance(reftype,Domain):
            dgrm.dgrm_doma_id_member = reftype.doma_id
            unknowndoma = False
        elif isinstance(reftype,Datatype):
            dgrm.dgrm_doma_id_member = findorcreateDomain(ptypeguid=reftypeguid
                           , pattrname=dgrm.dgrm_name
                           , pfathername=doma.doma_name
                           , pdomatype=Domain.DOMAIN
                           , pattrxml=el)
            unknowndoma = False
        else :
            """type has not yet been parsed or does not exist at all or is type I haven't considered
                remember for update"""
            dgrm.dgrm_doma_id_member = Domain.getunknown().doma_id
            unknowndoma = True
        dgrm.insert()
        if unknowndoma: unkndomains[dgrm.dgrm_id] = reftypeguid
    # for
"""    attr.attr_doma_id = findorcreateDomain(pdomguid=handleXML.findText(pattrxml, 'domain')
                                           , pstructdomguid=handleXML.findText(pattrxml, 'structuredType')
                                           , ptypeguid=handleXML.findText(pattrxml, 'logicalDatatype')
                                           , pattrname=attr.attr_displ_name
                                           , pfathername=vatername
                                           , pattrxml=pattrxml)
"""
def dostructtypes():
    global unkndomains
    dosegfiles(pdirec=parameters.odmstructypesdir(), transferfiles=do1structtype,pmandatoryfile=False)

    """update group domains as their types may now be available"""
    for key,val in unkndomains.items():
        doma = Modelelement.getelementbyodmguid(psrcid=val)
        if isinstance(doma,Domain):
            DomaingroupMember.updmember(pid=key,pdomaid=doma.doma_id)
        else:
            logmessages.writelog("Illegal domainreference {} (id={}) for structured type member {}".format(type(doma), key, val))
        #fi

def liesunsfuelldoma(pdoma, pxml,pdatyid=None):
    pdoma.doma_uc = handleXML.findText(pxml, 'createdBy')
    pdoma.doma_dc = handleXML.findText(pxml, 'createdTime')
    if pdatyid is None:
        daty = Modelelement.getelementbyextref(psrcid=handleXML.findText(pxml, 'logicalDatatype'),psrcname=Externalref.SOURCE_ODM)
    else:
        daty = Datatype().getbyid(pid=pdatyid)
    if daty is None:
        pdoma.doma_daty_id = None
        pdoma.doma_type = Domain.TXT
    else:
        pdoma.doma_daty_id = daty.daty_id
        pdoma.doma_type = Domain.TXT if (daty.daty_basetype is None) \
                                    else Domain.basetype2domatype(pdatybasetype=daty.daty_basetype)

    lov = pxml.find('listOfValues')
    if (lov is not None) and (lov != {}):
        pdoma.doma_type = Domain.LOV
        lovs = dict()
        for lovval in lov:
            # print (handleXML.findField(lovval,'value'),handleXML.findField(lovval,'description'),lovval.attrib)
            lovs.update({handleXML.findField(lovval, 'value'): handleXML.findField(lovval, 'description')})
        # endfor
        # print (len(lovs))
    # endif
    ranges = pxml.findall('listOfRanges/rangeDef')
    if not (ranges == []):
        range = (handleXML.findText(ranges[0], 'beginValue'), handleXML.findText(ranges[0], 'endValue'))
    else:
        range = (None, None)
    # endif

    # noch nicht übernommenm< defaultValue > a @ b.ch < / defaultValue >
    deriveddomaname = f"DER-{pdoma.doma_type}_"
    if (pdoma.doma_type == Domain.BIN):
        pdoma.doma_bin_contenttype = Domain.IMAGE  # 'FILM','GRAPH','TEXT','TON'
        pdoma.doma_bin_spfo_id = None
        deriveddomaname += f"{nvl(pdoma.doma_bin_contenttype,'')}"
    elif (pdoma.doma_type == Domain.LOV):
        zahl = re.search('\A\d+', nvl(handleXML.findText(pxml, 'dataTypeSize')))
        pdoma.doma_txt_maxlng = None if zahl is None else zahl.group()
        deriveddomaname = None
    elif (pdoma.doma_type == Domain.TXT):
        #            print(re.search('\A\d* ','123 ab').group())
        zahl = re.search('\A\d+', nvl(handleXML.findText(pxml, 'dataTypeSize')))
        pdoma.doma_txt_maxlng = None if zahl is None else zahl.group()
        buru = getcheckconstraint(pxml=pxml)
        if buru:
            regexpprefix: str = "REGEXP:"
            if (pdoma.doma_type == Domain.TXT) and buru.buru_rule.startswith(regexpprefix):
                pdoma.doma_txt_syntaxrule = re.sub(regexpprefix, '', buru.buru_rule)
            else:
                buru.buru_name = nvl(buru.buru_name, pdoma.doma_name + '_CHK')
                buru.buru_impact = 'REFUSE'
                buru.buru_level = BusinessRule.BURU_LEVEL_ATTR
                buru.insert()
            # fi
        # fi
        if pdoma.doma_txt_syntaxrule is not None:
            deriveddomaname = None
        else:
            deriveddomaname += f"{nvl(pdoma.doma_txt_maxlng,'')}"
    elif (pdoma.doma_type == Domain.DAT):
        pdoma.doma_dat_minvalue = range[0]
        pdoma.doma_dat_maxvalue = range[1]
        pdoma.doma_dat_granularity = Domain.MINUTE
        deriveddomaname += f"{nvl(pdoma.doma_dat_granularity,'')}_{nvl(pdoma.doma_dat_minvalue,'')}_{nvl(pdoma.doma_dat_maxvalue,'')}"
    elif (pdoma.doma_type == Domain.NUM):
        pdoma.doma_num_minvalue = range[0]
        pdoma.doma_num_maxvalue = range[1]
        prec = handleXML.findText(pxml, 'dataTypePrecision')
        if prec is None:
            prec = handleXML.findText(pxml, 'precision') # in struct-type attributes
        scale = handleXML.findText(pxml, 'dataTypeScale')
        if scale is None:
            scale = handleXML.findText(pxml, 'scale') #in struct-type attributes
        pdoma.doma_num_fract_digits = 0 if scale is None else int(scale)
        pdoma.doma_num_total_digits = 0 if prec is None else int(prec)
        pdoma.doma_num_round_value = None
        unitofmeasure = handleXML.findText(pxml, 'unitOfMeasure')
        if unitofmeasure is not None: pdoma.doma_phyu_id = PhysicalUnit.getorcreate(pname=unitofmeasure).phyu_id
        deriveddomaname += f"{nvl(pdoma.doma_num_total_digits,'')}_{nvl(pdoma.doma_num_fract_digits,'')}_{nvl(pdoma.doma_num_minvalue,'')}_{nvl(pdoma.doma_num_maxvalue,'')}_{nvl(pdoma.doma_num_round_value,'')}"

    # fi
    if deriveddomaname is not None and pdoma.doma_origin == Domain.DERIVED:
        doma = Domain.getbyname(pname=deriveddomaname)
        if (doma is None):
            pdoma.doma_name = deriveddomaname
            pdoma.insert()
            doma = pdoma
    else:
        pdoma.insert()
        doma = pdoma

    if (lov is not None) & (lov != {}):
        for idx, key in enumerate(lovs.keys(), start=1):
            deva = DefaultValue()
            deva.deva_value = key
            deva.deva_doma_id = doma.doma_id
            deva.deva_sort_order = idx
            deva.deva_uc = doma.doma_uc
            deva.deva_dc = doma.doma_dc
            deva.deva_displ = lovs[key]
            deva.insert()
        # for
    # fi
    return doma


def do1domainfile(pfilename):
    global interfacedomains
    interfacename = lambda name: None if (name  == parameters.odmdefdomainsfile()[:-4]) else name
    domains = handleXML.parseXML(pfilename=pfilename)
    root = domains.getroot()

    for dom in root.findall('domains/Domain'):
        doma = Domain(psrcname=Externalref.SOURCE_ODM,psrcid=handleXML.findField(dom, "id"))
        doma.doma_name = handleXML.findField(dom, "name")
        doma.doma_descr = handleXML.findText(dom, 'comment')
        doma.doma_origin = Domain.DOMAIN
        doma = liesunsfuelldoma(pdoma=doma, pxml=dom)

        intfname = interfacename(handleXML.findField(root, 'fileName'))
        if intfname is not None:
            interfacedomains[doma.doma_id] = intfname
    # for
    return

def transferDomains():
    do1domainfile(pfilename=parameters.odmDefDomainsfilePath())

    doxmlfiles(pdirec=parameters.odmdomainsdirec()
               , ptransfer=do1domainfile
               , ppattern=r'.*\.{}'.format('xml')
               ,pmandatorydirec=False)

    dostructtypes()
# end transferDomains



def transferentity(penti, pdiagid, puc, pdc):
    global defcolors,classcolors

    entiodm = handleXML.findField(penti, 'oid')
    enti = Entity().getbyODMref(psrcid=entiodm)
    hiddenelements = penti.find("hiddenElements")
    if hiddenelements is not None:
        elemtext = handleXML.findField(hiddenelements, "elements")
    else:
        elemtext = ""
    hiddenattrs = elemtext.split(' ')
    hiddenattrs2 = []
    for e in hiddenattrs:
        if e != "":
            attr = Attribute().getbyODMref(psrcid=e)
            if attr is not None: hiddenattrs2.append(attr.attr_id)
    attrs = Attribute.select(pwhere=("attr_enti_id = ?", enti.enti_id), porderby="attr_displ_seq")
    attrids = [a.attr_id for a in attrs]
    attrids = list(set(attrids) - set(hiddenattrs2))

    layout = penti.find('bounds')
    defcol = defcolors['Entity']  # defaults zum Ergänzen
    if (handleXML.findText(penti, 'useDefaultColor') == 'false'):
        backgcolor = handleXML.findText(penti, 'backgroundColor')
        foregcolor = handleXML.findText(penti, 'foregroundColor')
        # print (backgroundc,foregroundc)
        font = penti.find('fonts/FontObject[foType ="Title"]')
        # deutsche ODMnutzuer schreiben Titel in die Konfig....
        if font is None: font = penti.find('fonts/FontObject[foType ="Titel"]')
        # fontname,fontsize,fontstyle):
        fontcolor = nvl(handleXML.findText(font, 'colorRGB'),defcol.fontcolor)
        fontstyle = nvl(handleXML.findText(font, 'fontStyle') ,defcol.fontstyle)
        fontsize = nvl(handleXML.findText(font, 'fontSize') , defcol.fontsize)
        col = Color(foregcolor=foregcolor, backgcolor=backgcolor, fontname=None, fontcolor=fontcolor, fontsize=fontsize, fontstyle=fontstyle)
    else:
        # check wether entity belongs to category
        enticatguid = None if entiodm is None else getentity(entiodm,"categoryguid")
        #print (enti.enti_name,enti.getscrid(),enticatguid)
        if (enticatguid is None):
            col = defcolors['Entity']
        else:
            try:
                col = classcolors[enticatguid]
            except Exception as e:
                col = defcolors['Entity']
        # fi
    # fi

    index = 0
    entix = int(handleXML.findField(layout, 'x'))
    entiy = int(handleXML.findField(layout, 'y'))
    entiwidth = int(handleXML.findField(layout, 'width'))
    entiheight = int(handleXML.findField(layout, 'height'))
    # if there are several copies on a diagramm, repeat the insert with new index und insert succeeds
    while True:
        eler = Elementrep()
        eler.eler_mode_id = enti.enti_id
        eler.eler_diag_id = pdiagid
        eler.eler_index = index
        eler.eler_position_x = entix
        eler.eler_position_y = entiy
        eler.eler_width = entiwidth
        eler.eler_height = entiheight
        eler.eler_opacity = 100
        eler.eler_color = int2hex(col.backgcolor)
        eler.eler_marginwidth = None
        eler.eler_marginopacity = 100
        eler.eler_margincolor = int2hex(col.foregcolor)
        eler.eler_fontsize = col.fontsize
        eler.eler_fontcolor = int2hex(col.fontcolor)
        eler.eler_uc = puc
        eler.eler_dc = pdc
        try:
            eler.insert(pdoerrhdlng=False)
            attrx = int(entix) + 26  # x1,x2=16,26 y=30
            attry = int(entiy) + 30
            attrwidth = int(entiwidth) - 36
            attrheight = 13
            for aid in attrids:
                atteler = Elementrep()
                atteler.eler_mode_id = aid
                atteler.eler_diag_id = pdiagid
                atteler.eler_index = eler.eler_index
                atteler.eler_position_x = attrx
                atteler.eler_position_y = attry
                atteler.eler_width = attrwidth
                atteler.eler_height = attrheight
                atteler.eler_opacity = 100
                atteler.eler_color = int2hex(col.backgcolor)
                atteler.eler_marginwidth = None
                atteler.eler_marginopacity = 100
                atteler.eler_margincolor = int2hex(col.foregcolor)
                atteler.eler_fontsize = col.fontsize
                atteler.eler_fontcolor = int2hex(col.fontcolor)
                atteler.eler_uc = puc
                atteler.eler_dc = pdc
                try:
                    atteler.insert()
                except UniqueKeyException as err:
                    raise err
                except Exception as e:
                    logmessages.writelog("Attr-representation")
                    logmessages.writelog(str(e))
                    logmessages.writelog(atteler.tostring())
                    raise e
                attry += attrheight
                # Maximal bis zur Grösse der Entität
                if ((attry - entiy) > (entiheight - 10)): break
            # for
            break  # no more looping for copies of element on diagramm

        except UniqueKeyException as err:
            index += 1
            if index > 100: #emergency stop
                raise err
        except Exception as ex:
            logmessages.writelog("Entity-representation")
            logmessages.writelog(str(ex))
            logmessages.writelog(eler.tostring())
            raise ex
    # while

# transferentity

def transferdiaobj(pobjects, pdiagid, puc, pdc):
    for o in pobjects:
        type = handleXML.findField(o, 'otype')
        if (type == 'Image'):
            pass
        elif (type == 'Entity'):
            transferentity(penti=o, pdiagid=pdiagid, puc=puc, pdc=pdc)
        elif (type == 'Note'):
            pass
        # fi


# transferdiaobj

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

def transferdiaconnect(pconnectors, pdiagid, puc, pdc):
    for c in pconnectors:
        type = handleXML.findField(c, 'otype')
        if (type == 'Relation'):
            relaguid = handleXML.findField(c, "oid")
            rela = Relation().getbyODMref(psrcid=relaguid)
            linewidth = handleXML.findText(c, 'lineWidth')
            sourcelabel = c.find('sourceLabel/labelBounds')
            sttex = handleXML.findField(sourcelabel, 'x')
            sttey = handleXML.findField(sourcelabel, 'y')
            sttew = handleXML.findField(sourcelabel, 'width')
            stteh = handleXML.findField(sourcelabel, 'height')
            targetlabel = c.find('targetLabel/labelBounds')
            entex = handleXML.findField(targetlabel, 'x')
            entey = handleXML.findField(targetlabel, 'y')
            entew = handleXML.findField(targetlabel, 'width')
            enteh = handleXML.findField(targetlabel, 'height')

            """Labels können negative Starts haben, verschiebe sie in den positiven Bereich"""
            if sttey is not None and int(sttey) < 0: sttey, entey = 0, int(entey) - int(sttey)
            if sttey is not None and int(sttey) < 0: sttey, entey = 0, int(entey) - int(sttey)

            sourcelinetype = Linesegment.SOLID if rela.getmandatoryfromto() else Linesegment.DASHED
            targetlinetype = Linesegment.SOLID if rela.getmandatorytofrom() else Linesegment.DASHED

            """ sollte ich nicht mehr brauchen, da ich originalrichtung übernehme
            if (False):
                #if (rela[0][3] == 'TRUE'):  # switch source and target
                sourcecard, targetcard = targetcard, sourcecard
                sourcelinetype, targetlinetype = targetlinetype, sourcelinetype
                sttex, entex = entex, sttex
                sttey, entey = entey, sttey
                sttew, entew = entew, sttew
                stteh, enteh = enteh, stteh
            # fi"""

            relr = Relationrep()
            relr.relr_diag_id = pdiagid
            relr.relr_mode_id = rela.rela_id
            relr.relr_linewidth = linewidth
            relr.relr_linecolor = None
            relr.relr_lineopacity = 100
            relr.relr_startedge = None
            relr.relr_startposition = None
            relr.relr_start_connector = rela.rela_maptype_to_from
            relr.relr_starttext_angle = None
            relr.relr_starttext_distance = None
            relr.relr_starttext_x = sttex
            relr.relr_starttext_y = sttey
            relr.relr_starttext_width = sttew
            relr.relr_starttext_height = stteh
            relr.relr_endedge = None
            relr.relr_endposition = None
            relr.relr_end_connector = rela.rela_maptype_from_to
            relr.relr_endtext_angle = None
            relr.relr_endtext_distance = None
            relr.relr_endtext_x = entex
            relr.relr_endtext_y = entey
            relr.relr_endtext_width = entew
            relr.relr_endtext_height = enteh
            relr.relr_fontcolor = None
            relr.relr_fontsize = 10
            relr.relr_uc = puc
            relr.relr_dc = pdc
            relr.insert()

            points = c.findall('points/point')
            points = [{'x': int(handleXML.findField(p, 'x')), 'y': int(handleXML.findField(p, 'y'))} for p in points]
            if len(points) == 2:
                """1-elementige Linien werden um einen Mittelpunkt ergänzt wegen -- oder solid"""
                midpos = lambda x1, x2: round((x1 - x2) / 2 + x2)
                points.insert(1, {'x': midpos(points[0]['x'], points[1]['x']),
                                  'y': midpos(points[0]['y'], points[1]['y'])})
            # fi

            linesegs = []
            prevlise = None
            for idx, point in enumerate(points):
                lise = Linesegment()
                lise.lise_x = point['x']
                lise.lise_y = point['y']
                lise.lise_seq = idx
                lise.lise_relr_id = relr.relr_id
                lise.lise_linetype = linetype(pidx=idx, pmaxidx=len(points)
                                            , psourcelt=sourcelinetype, ptargetlt=targetlinetype)
                lise.lise_uc = puc
                lise.lise_dc = pdc
                if len(linesegs) > 0:
                    """ ab dem 2. Punkt wird im vorherigen Punkt der Winkel zum nächsten hinzugefügt"""
                    calcwinkel = lambda ey, sy, ex, sx: math.atan2(ey - sy, ex - sx)
                    prevlise.lise_angle = calcwinkel(lise.lise_y, prevlise.lise_y, lise.lise_x, prevlise.lise_x)
                prevlise = lise
                linesegs.append(lise)
            # for
            for lise in linesegs:
                lise.insert()
        else:
            pass
        # fi
# transferdiaconnect

def transferdiaarc(parcs, pdiagid, puc, pdc):
    pass


def doxmlfiles(pdirec, ptransfer, ppattern=r".*",pmandatorydirec = True):
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


def dosegfiles(pdirec, transferfiles,pmandatoryfile=True):
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
# dosegfiles


def do1diagramm(pfilename):
    # print (p_filename)
    try:
        diagramme = handleXML.parseXML(pfilename=pfilename)
    except Exception as ex:
        print("Diagram nicht lesbar: {}".format(pfilename))
        return
    dia = diagramme.getroot()
    diag = Diagram(psrcname=Externalref.SOURCE_ODM, psrcid=handleXML.findField(dia, 'id'))
    diag.diag_name = handleXML.findField(dia, 'name')
    if (diag.diag_name == 'Logical'):
        return
    diag.diag_diat_id = Diagramtype.getbyname(pname=Diagramtype.ENTITY).diat_id
    # print(handleXML.findField(dia,'name'), handleXML.findField(dia,'id'))

    if (handleXML.findText(dia, 'showLegend') == 'true'):
        legende = dia.find("objectViews/OView[@otype='Legend']")
        bounds = legende.find("bounds")
        diag.diag_legendx = handleXML.findField(bounds, 'x')
        diag.diag_legendy = handleXML.findField(bounds, 'y')
    else:
        diag.diag_legendx = None
        diag.diag_legendy = None
    # fi
    diag.diag_uc = handleXML.findText(dia, 'createdBy')
    diag.diag_dc = handleXML.findText(dia, 'createdTime')
    diag.diag_um = handleXML.findText(dia, 'modifiedBy')
    diag.insert()
    objects = dia.findall('objectViews/OView')
    if (len(objects) > 0):
        transferdiaobj(pobjects=objects, pdiagid=diag.diag_id, puc=diag.diag_uc, pdc=diag.diag_dc)
    connectors = dia.findall('connectors/Connector')
    if (len(connectors) > 0):
        transferdiaconnect(pconnectors=connectors, pdiagid=diag.diag_id, puc=diag.diag_uc, pdc=diag.diag_dc)
    arcsXML = dia.findall('arcs/Arc')
    if (len(arcsXML) > 0):
        transferdiaarc(parcs=arcsXML, pdiagid=diag.diag_id, puc=diag.diag_uc, pdc=diag.diag_dc)
    # print (dianame,len(objects),len(connectors),len(arcs))


# do1diagramm

def transferdiagramme():
    doxmlfiles(pdirec=parameters.odmentisubviewdirec()
               , ptransfer=do1diagramm
               , ppattern=r'{}.xml'.format(GUIDPATTERN))


# transferdiagramme

def insertderiveddomain(ptypeguid, pattrname, pvatername, pdomatype,pattrxml,pintfid=None):
    doma = Domain(psrcname=Externalref.SOURCE_ODM,psrcid=Modelelemtype.DOMA+handleXML.findField(pattrxml, 'id'))
    doma.doma_name = pattrname
    domatest = Domain.getbyname(pname=doma.doma_name)
    if (domatest is not None):
        # es gibt ihn schon, füge den Vaternamen dazu
        doma.doma_name = pattrname + '-' + pvatername
    doma.doma_origin = pdomatype
    doma.doma_intf_id = pintfid
    if nvl(ptypeguid) != '':
        doma.doma_daty_id = Modelelement.getmodebyodmguid(psrcid=ptypeguid).mode_id
    doma.doma_descr = "generiertes Domain für Datentyp für Attribute {}.{}".format(pvatername, pattrname)

    doma = liesunsfuelldoma(pdoma=doma, pxml=pattrxml,pdatyid=doma.doma_daty_id)
    return doma
# insertderiveddomain


def findorcreateDomain(pattrname, pfathername, pdomatype,pattrxml,pintfid = None
                       , pdomguid=None, pstructdomguid=None, ptypeguid=None):
    def handleguid(pguid):
        if pguid is None: return None
        typeelem = Modelelement.getelementbyodmguid(psrcid=pguid)

        if typeelem is None:
            """domain not yet known"""
            return Domain().getunknown().doma_id
        elif isinstance(typeelem, Domain):
            return typeelem.doma_id  # Done, domain found
        else:
            logmessages.writelog("Attr: {}, Father: {}, Domain Guid {} leads to unknown element type {}"
                                 .format(pattrname, pfathername, pguid, type(typeelem)))
            return Domain().getunknown().doma_id
        # fi
    #handleguid

    domaid = handleguid(pdomguid)
    if domaid is not None: return domaid
    domaid = handleguid(pstructdomguid)
    if domaid is not None: return domaid

    if ptypeguid is not None:
        typeelem = Modelelement.getelementbyodmguid(psrcid=ptypeguid)
        if typeelem is None:
            """domain not yet known"""
            return Domain().getunknown().doma_id
        elif isinstance(typeelem, Datatype):
            doma = insertderiveddomain(ptypeguid=ptypeguid, pattrname=pattrname, pvatername=pfathername,pdomatype=pdomatype,
                                           pattrxml=pattrxml,pintfid = pintfid)
            return doma.doma_id
        else:
            logmessages.writelog("Attr: {}, Father: {}, Domain Guid {} leads to unknown element type {}"
                                 .format(pattrname, pfathername, ptypeguid, type(typeelem)))
            return Domain().getunknown().doma_id
        # fi
    # fi
    return Domain().getunknown().doma_id
# findorcreateDomain


def do1Arc(fileName):
    arcXML = handleXML.parseXML(pfilename=fileName).getroot()
    if (handleXML.findField(arcXML, "class") != "oracle.dbtools.crest.model.design.logical.Arc"): return

    arc = Arc(pname=handleXML.findField(arcXML, "name")
              , pentiid=Entity().getIDbyODMref(psrcid=handleXML.findText(arcXML, 'entity'))
              , puc=handleXML.findText(arcXML, 'createdBy')
              , pdc=handleXML.findText(arcXML, 'createdTime')
              ,psrcname=Externalref.SOURCE_ODM,psrcid=handleXML.findField(arcXML, "id"))
    arcid = arc.insert()

    """map all relations to this arc"""
    relations = arcXML.findall('relations/relationID')
    relids = ','.join("'{}'".format(r.text) for r in relations)
    # DEBUG Arc 2x auf Beziehung
    #    if handleXML.findField(arcXML, "name") in ('xxArc_9', 'xxArc_11'):
    #        print(handleXML.findField(arcXML, "id"), handleXML.findField(arcXML, "name"), handleXML.findText(arcXML, 'entity'))
    Relation.setarcinrela(prelids=relids,parcid=arcid)
# do1Arc

def transferArcs():
    dosegfiles(pdirec=parameters.odmArcDirec(), transferfiles=do1Arc)
    Relation.setrelatypes()
# transferArcs

def updateUDP(pmodeid, pobj):
    udps = []
    """<propertyMap>
        <property name="EXT_ATTR_ID" value="."/>
        <property name="EXT_SORT_ORDER" value="13.0"/>
        </propertyMap>
    """
    props = pobj.find('propertyMap')
    if (props is not None):
        for prop in props:
            try:
                udpr  = Userdefprop.getbyname(pname=handleXML.findField(prop, 'name'))
                # print('      ', handleXML.findField(prop,'name'), handleXML.findField(prop,'value'), bdegId)
                val = handleXML.findField(prop, 'value')
                if udpr.udpr_name.endswith('_ATTR_NAME'):
                    val = removeattrmeta(val)
                udps.append((val, pmodeid, udpr.udpr_id))
            except Exception as e:
                """dynamische Properties lassen wir aus"""
                pass
        # for
    # fi
    # look for comments in the notesfield of the element
    note = handleXML.findText(pobj, 'notes')
    if (note is not None):
        prop = re.finditer(r'\[(([A-Z]{2})[^[]+)\[\n([^]]*)\][A-Z]{2}[^]]+\]', note, re.DOTALL)
        # liefert group1 name,group2 sprache, group3 text
        for i, p in enumerate(prop):
            # print (i,p.group(0),'\n1:',p.group(1),'\n2:',p.group(2),'\n3:',p.group(3))
            udpr = Userdefprop.getbyname(pname=p.group(1))
            # print('      ', handleXML.findField(prop,'name'), handleXML.findField(prop,'value'), bdegId)
            udps.append((p.group(3).rstrip(), pmodeid, udpr.udpr_id))
        # for
    # fi

    if len(udps) > 0:
        # print (udps)
        Userdefpropvalue.updvalues(prows=udps)
    # fi
    return

def getcheckconstraint(pxml):
    """within attributedefinition
        <constraintName>My Constr Name</constraintName>
        <useDomainConstraints>false</useDomainConstraints>  -- missing = true, if there is a domain
    in attribute and domains
        <checkConstraint>
            <implementationDef dbType="Generic Constraint" definition="abcde"/>
        </checkConstraint>

    """
    constrname = handleXML.findText(pxml, "constraintName")
    constrxml = pxml.find("checkConstraint")
    useDomainConstr = Boolean.str2bool(nvl(handleXML.findText(pxml, 'useDomainConstraints'), 'true'))
    if constrxml is None: return
    rules = [(handleXML.findField(impldef, 'dbType'), handleXML.findField(impldef, 'definition')) for impldef in constrxml]
    if (len(rules) == 0): return
    descr = '\n'.join("dbtype={}    rule={}".format(r[0], r[1]) for r in rules)
    buru = BusinessRule()
    buru.buru_name = constrname
    buru.buru_descr = descr
    buru.buru_rule = rules[0][1]  # first solution, take the first rule in the list
    buru.buru_type = BusinessRule.BURU_TYPE_CHECK
    buru.buru_errormsg = 'Rule {} violated. {}'.format(constrname, buru.buru_rule)
    return buru

def getformula(pelemname, pmodetype, pmodeid, pxml):
    """
    <formulaDesc>bisdat - vondat</formulaDesc>
    <sourceType>Aggregate</sourceType>
    <sourceType>Derived</sourceType>

    """
    formula = handleXML.findText(pxml,"formulaDesc")
    sourctype = handleXML.findText(pxml,"sourceType")
    if formula is None: return
    buru = BusinessRule()
    buru.buru_descr = "Function: {} formula: {}".format(sourctype,formula)
    buru.buru_rule = formula
    buru.buru_type = BusinessRule.BURU_TYPE_CALC
    return buru

def doconstraints(pelemname, pmodetype, pmodeid, pxml):
    buru = getcheckconstraint(pxml)
    if buru and pmodetype == Modelelemtype.ATTR:
        buru.buru_name = nvl(buru.buru_name,pelemname)
        buru.buru_impact = 'REFUSE'
        buru.buru_level = BusinessRule.BURU_LEVEL_ATTR
        buruid = buru.insert()
        bure = BusinessruleElement(pburuid=buruid, pattrid=pmodeid)
        bure.insert()
    #fi

    buru = getformula(pelemname, pmodetype, pmodeid, pxml)
    if buru and pmodetype == Modelelemtype.ATTR:
        buru.buru_name = nvl(buru.buru_name,pelemname)
        buru.buru_impact = 'denormalised (calcualated) Value'
        buru.buru_level = BusinessRule.BURU_LEVEL_ATTR
        buruid = buru.insert()
        bure = BusinessruleElement(pburuid=buruid, pattrid=pmodeid,pwriteable=True)
        bure.insert()
    #fi
    return


def do1Attribute(plfnr, pattrxml,pentiId):
    # wegen FK-PK zusätzliche Attribute werden nicht übernommen
    if (handleXML.findText(pattrxml, 'referedAttribute') is not None):
        return
    vatername = Entity().getbyid(pid=pentiId).enti_name

    xmlname = handleXML.findField(pattrxml, 'name')
    # strip [] am Ende des Namens

    attr = Attribute(pname=removeattrmeta(xmlname), pentiid=pentiId
                     , psrcname=Externalref.SOURCE_ODM, psrcid=handleXML.findField(pattrxml, 'id'))
    attr.attr_tech_name = handleXML.findText(pattrxml, 'preferredAbbreviation')
    if attr.attr_tech_name is None:
        attr.attr_tech_name = re.sub('[-,.()\[\]äöüèéàÄ~ÖÜ ]', '_', str.upper(attr.attr_displ_name))
    attr.attr_uc = handleXML.findText(pattrxml, 'createdBy')
    attr.attr_dc = handleXML.findText(pattrxml, 'createdTime')
    attr.attr_tooltip = handleXML.findText(pattrxml, 'commentInRDBMS')
    attr.attr_doma_id = findorcreateDomain(pdomguid=handleXML.findText(pattrxml, 'domain')
                                           , pstructdomguid=handleXML.findText(pattrxml, 'structuredType')
                                           , ptypeguid=handleXML.findText(pattrxml, 'logicalDatatype')
                                           , pattrname=attr.attr_displ_name
                                           , pfathername=vatername
                                            ,pdomatype=Domain.DERIVED
                                           , pattrxml=pattrxml)
    attr.attr_descr = handleXML.findText(pattrxml, 'comment')
    attr.attr_displ_seq = plfnr
    attr.attr_is_descriptive = 'FALSE'
    attr.attr_is_mandatory = Boolean.bool2str(handleXML.findText(pattrxml, 'nullsAllowed') != 'true')
    attr.attr_is_historicised = Boolean.bool2str(is_historisized(xmlname))
    attr.attr_is_repeated = Boolean.bool2str(is_repeated(xmlname))
    attr.attr_is_translated = Boolean.bool2str(is_langdept(xmlname))
    attr.attr_is_encrypted = 'FALSE'
    attrId = attr.insert()

    Userdefpropvalue.fillallvalues(pattrid=attrId)
    updateUDP(pmodeid=attrId, pobj=pattrxml)

    documents = getdokuref(pelem=pattrxml)
    ModelelemDocu.insertdocuref(pdocguidlist=documents, pmodeid=attrId)
    ModelelemOrgu.insertorguref(porguidlist=getpartyref(pelem=pattrxml), pmodeid=attrId)

    doconstraints(pelemname=vatername + '.' + attr.attr_tech_name, pmodetype=Modelelemtype.ATTR, pmodeid=attrId, pxml=pattrxml)

# do1Attribute

def fillKeys(p_enti, p_entiid):
    global schluessel
    allkeys = p_enti.find('identifiers')
    if allkeys is not None:
        for key in allkeys.findall('identifier'):
            kr = handleXML.findText(key, 'newElementsIDs')
            #                arefs = key.findall('usedAttributes/attributeRef')
            #                keyrefs = []
            #                for i in range(len(arefs)):
            #                    keyrefs.append(arefs[i].text)
            #                    #print (i,arefs[i].text)
            #
            #            else:
            if (kr is not None):
                keyrefs = kr.split(',')
                # print(idx, handleXML.findField(enti,'name'), handleXML.findField(key,'id'), handleXML.findField(enti,'id'), keyrefs)
                keys = Key(psrcid=handleXML.findField(key, 'id'),psrcname=Externalref.SOURCE_ODM)
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
                    logmessages.writelog("key-element {} for key {} in entity {} is probably attribute group member and will be ignored ".format(ke,key.keys_name,Entity().getbyid(key.keys_enti_id).getname()))
                    continue
            else:
                kele.kele_rela_id = None
            # if
            kele.insert()
        # for
    # for


def getdokuref(pelem, pstruct=False):
    documents = None
    if pstruct:
        """
        <documents>
        <Document id="7EBDC037-8728-C627-4B33-CEDF979E7C13"/>
        </documents>
        """
        docs = pelem.find('documents')
        if docs is not None:
            documents = []
            for idx, doc in enumerate(docs, start=1):
                # alle referenzierten Dokumente
                docguid = handleXML.findField(doc, 'id')
                # print(docguid)
                documents.append(docguid)
            # for
            documents = tuple(documents)
        # fi
    else:
        """<documents usedDucuments="701E5525-A8EE-3C6F-E78B-28B04D93F93D"/>
        """
        docs = handleXML.findField(pelem.find("documents"), 'usedDucuments')
        if (docs is not None):
            documents = tuple(docs.split(' '))
    # fi
    # print(documents)
    return documents
# getdokuref

def getpartyref(pelem):
    parties = []
    """
    <responsibleParties>
    <party>7EBDC037-8728-C627-4B33-CEDF979E7C13</party>
    </responsibleParties>
    """
    """ in relational_models
    <responsibleParties>
    <Party id="B7591938-640A-FC73-0F8D-22E92BFFB269"/>
    <Party id="ACDA33C9-C352-DEC9-2424-A8B256602462"/>
    </responsibleParties>
    """
    elemparties = pelem.findall('responsibleParties/party')
    if len(elemparties) > 0:
        parties = []
        for party in elemparties:
            # alle referenzierten Dokumente
            parties.append(party.text)
        # for
        parties = tuple(parties)
    else:
        elemparties = pelem.findall('responsibleParties/Party')
        if elemparties is not None:
            parties = []
            for party in elemparties:
                # alle referenzierten Dokumente
                parties.append(handleXML.findField(party,"id"))
            # for
            parties = tuple(parties)
        #fi
    # fi
    return parties
# getpartyref


def do1Entity(fileName):
    global classids
    tree = handleXML.parseXML(pfilename=fileName)
    entixml = tree.getroot()
    #es hat noch fremde XMLS in den Verzeichnissen
    if (handleXML.findField(entixml, "class") != "oracle.dbtools.crest.model.design.logical.Entity"): return

    "natürliche Person"
    entiguid = handleXML.findField(entixml, 'id')
    enti = Entity(psrcname=Externalref.SOURCE_ODM, psrcid=entiguid)
    enti.enti_name = handleXML.findField(entixml, "name")
    enti.enti_descr = handleXML.findText(entixml, 'comment')
    enti.enti_tooltip = handleXML.findText(entixml, 'note')
    enti.enti_uc = handleXML.findText(entixml, 'createdBy')
    enti.enti_dc = handleXML.findText(entixml, 'createdTime')
    enticategoryguid = handleXML.findText(entixml, 'typeID')
    if enticategoryguid is not None and enticategoryguid != '':
        if enticategoryguid in classids:
            enti.enti_enca_id = classids[enticategoryguid]
        else:
            print ("classid {} in {} not found".format(enticategoryguid, enti.enti_name))

    i=1 #safeguard for eternal loop
    while i<10:
        try:
            entiId = enti.insert()
            break
        except Exception as e:
            logmessages.writelog("in Entity {}: {} ".format(entiguid, enti.enti_name))
            logmessages.writelog(e.__str__())
            logmessages.writelog(e.__str__())
            #Entities can have duplicate names (merging in github)
            if re.match(r"UNIQUE constraint failed: ENTITIES.ENTI_NAME",e.__str__()):
                rela.rela_name += "v{}".format(str(i))
                i += 1
            else: raise Exception("Insert-error in entities: see logfile")
            if (i == 10): raise Exception("Key-error in entities: see logfile")
        #try
    #while

    entientiguid = handleXML.findText(entixml, 'hierarchicalParent')
    setentity(entiguid,entity=enti, color=None, superentitityguid=entientiguid, subentities=[]
              , categoryguid=enticategoryguid)

    Userdefpropvalue.fillallvalues(pentiid=entiId)

    sobj = handleXML.findText(entixml, 'synonym')
    if (sobj is not None):
        syns = sobj.split(',')
        for syn in syns:
            #syn.strip()
            syno = Synonym(pname=syn, pentiid=entiId)
            syno.insert()
        # for
    # fi

    # print (entname,translate.translate(p_text=entname,p_fromlang='de',p_tolang='en'),translate.translate(p_text=entname,p_fromlang='de',p_tolang='fr'))

    updateUDP(pmodeid=entiId, pobj=entixml)
    ModelelemDocu.insertdocuref(pdocguidlist=getdokuref(pelem=entixml), pmodeid=entiId)
    ModelelemOrgu.insertorguref(porguidlist=getpartyref(pelem=entixml), pmodeid=entiId)

    attrs = entixml.find('attributes')
    if attrs is not None:
        for idx, attr in enumerate(attrs, start=1):
            # alle Attribute
            # print(handleXML.findField(attr,'name'),handleXML.findField(attr,'id'))
            do1Attribute(plfnr=idx, pattrxml=attr, pentiId=entiId)
        # rof
    # fi
    fillKeys(p_enti=entixml, p_entiid=entiId)
# do1Entity


def transferEntities():
    # lösche die Entitäten
    dosegfiles(pdirec=parameters.odmEntityDirec(), transferfiles=do1Entity)
# transferEntities

def doSubentities():
    #fill all subentity-id-lists

    for guid in getentitykeys():
        val = getentity(guid)
        entientiguid = getentity(guid,"superentitityguid")
        enti = getentity(guid,"entity")
        if entientiguid is not None:
            target = getentity(entientiguid,"subentities")
            if target is not None:
                # hat eine superentity, fülle in seine idliste
                target.append(enti.enti_id)
            else:
                logmessages.writelog(f"Cannot find superentity {entientiguid} to link with {guid}")
        #fi
    #for

    #get all superentity guids
    superentiguids = set(getentity(key,"superentitityguid") for key in getentitykeys())
    superentiguids.discard(None)

    """create an arc for every superentity"""
    for superentiguid in superentiguids:
        superentity = entities.get(superentiguid)
        if superentity is not None: # skip arc if superentity reference is broken
            superenti = getentity(superentiguid,"entity")
            subentiids = getentity(superentiguid,"subentities")
            arc = Arc(pname=superenti.enti_name + '_subtype', pentiid=superenti.enti_id
                      , puc=superenti.enti_uc, pdc=superenti.enti_dc)
            arc.insert()
            Relation.insertisa(parc=arc,pentiids=subentiids)
        #fi
    #for


def abbildTyp(ptyp):
    if (ptyp == '1'):
        return '1'
    elif (ptyp == '*'):
        return 'M'
    else:
        return None
    # fi
# abbildTyp


def do1Relation(fileName):
    tree = handleXML.parseXML(pfilename=fileName)
    relaxml = tree.getroot()
    documents = getdokuref(pelem=relaxml)

    relaguid = handleXML.findField(relaxml, 'id')
    rela = Relation(psrcname=Externalref.SOURCE_ODM,psrcid=relaguid)
    rela.rela_name = handleXML.findField(relaxml, 'name')
    rela.rela_assoc_from_to = handleXML.findText(relaxml, 'nameOnSource')
    rela.rela_hist_from_to = Boolean.bool2str(is_historisized(rela.rela_assoc_from_to))
    rela.rela_assoc_to_from = handleXML.findText(relaxml, 'nameOnTarget')
    rela.rela_hist_to_from = Boolean.bool2str(is_historisized(rela.rela_assoc_to_from))
    rela.rela_maptype_from_to = Relation.ONE if (handleXML.findText(relaxml, 'sourceCardinality') == '1') else Relation.MANY
    rela.rela_maptype_to_from = Relation.ONE if (handleXML.findText(relaxml, 'targetCardinalityString') == '1') else Relation.MANY
    rela.rela_mandatory_from_to = Boolean.strnegbool(handleXML.findText(relaxml, 'optionalSource'))
    rela.rela_mandatory_to_from = Boolean.strnegbool(handleXML.findText(relaxml, 'optionalTarget'))
    rela.rela_type = rela.simpleType()
    rela.rela_uc = handleXML.findText(relaxml, 'createdBy')
    rela.rela_dc = handleXML.findText(relaxml, 'createdTime')

    sourceentiguid = handleXML.findText(relaxml, 'sourceEntity')
    targetentiguid = handleXML.findText(relaxml, 'targetEntity')
    rela.rela_enti_id_from = Externalref.getODMmodeid(psrcid=sourceentiguid)
    rela.rela_enti_id_to = Externalref.getODMmodeid(psrcid=targetentiguid)
    if (rela.rela_enti_id_from is None or rela.rela_enti_id_to is None):
        logmessages.writelog(
            "in Relation {}: Entity Id {} or {} not found. Datenleichen von Relation mit gelöschten Entities".
                format(relaguid,sourceentiguid, targetentiguid))
        return
    # fi

    i=1 #safeguard for eternal loop
    while i<10:
        try:
            rela.insert()
            break
        except UniqueKeyException as e:
            #ODM can have duplicate names for exception. Add digit to name
            logmessages.writelog("in Relation {}: {} ".format(relaguid, rela.rela_name))
            logmessages.writelog(e.__str__())
            #relations can have duplicate names (merging in github)
            rela.rela_name += "v{}".format(str(i))
            i += 1
            if (i == 10): raise Exception("Key-error in relations: see logfile")
        except Exception as e:
            logmessages.writelog("in Relation {}: {} ".format(relaguid, rela.rela_name))
            logmessages.writelog(e.__str__())
            raise e
        #try
    #while
    Userdefpropvalue.fillallvalues(prelaid=rela.rela_id)

    updateUDP(pmodeid=rela.rela_id, pobj=relaxml)
    ModelelemDocu.insertdocuref(pdocguidlist=documents, pmodeid=rela.rela_id)
    ModelelemOrgu.insertorguref(porguidlist=getpartyref(pelem=relaxml), pmodeid=rela.rela_id)

    attrs = relaxml.find('attributes')
    if attrs is not None:
        """Relationattributes are not handled"""
        logmessages.writelog("Relationattributes are not handled (Relation {})".format(rela.rela_name))
        #for idx, attr in enumerate(attrs, start=1):
        #    # alle Attribute
        #    # print((handleXML.findField(attr,'name'),handleXML.findField(attr,'id')))
        #    do1Attribute(plfnr=idx, pattrxml=attr, prelaId=rela.rela_id)
        ## endfor
    # fi
# do1Relation

def transferRelations():
    # lösche die Beziehungen
    dosegfiles(pdirec=parameters.odmRelationDirec(), transferfiles=do1Relation)
    dbConnect.myDbConn.commit()


def do1UDPFile(pfileName):
    tree = handleXML.parseXML(pfilename=pfileName)
    root = tree.getroot()
    filename= re.match("^[^.]*",os.path.split(pfileName)[1])[0]
    ludpTheme = filename
    lgroups = {'': '-'}  # für ungruppierte properties
    for groups in root.findall('udp_groups'):
        for child in groups:
            # print(handleXML.findField(child,'name'))
            lgroups[handleXML.findField(child, 'id')] = handleXML.findField(child, 'name')
        # for
    # for

    # die speziellen Properties (translation of comments in notes manuell einfüllen
    if (ludpTheme == parameters.odmUDPTranslFileName()):
        for lgrpkey, lgrpvalue in lgroups.items():
            if lgrpkey != '':
                udpr = Userdefprop(ptheme=ludpTheme,pgroup=lgrpvalue,pname=lgrpvalue + '_ENTI_COMMENT')
                udpr.udpr_descr = "created for comments, solved in notes because of multiline strings"
                udprid = udpr.insert()

                metpid = ModelelementProperty(pmeltid=Modelelemtype.getidbyshortname(pshortname=Modelelemtype.ENTI)
                                            ,pudprid=udprid).insert()

                udpr = Userdefprop(ptheme=ludpTheme,pgroup=lgrpvalue,pname=lgrpvalue + '_ATTR_COMMENT')
                udpr.udpr_descr = "created for comments, solved in notes because of multiline strings"

                udprid = udpr.insert()

                metpid = ModelelementProperty(pmeltid=Modelelemtype.getidbyshortname(pshortname=Modelelemtype.ATTR)
                                            ,pudprid=udprid).insert()
            # fi
        # for
    # fi

    props = root.find('properties')
    for prop in props.findall('property'):
        group = handleXML.findField(prop, 'group_id')
        propname = handleXML.findField(prop, 'name')
        propdisplayname = handleXML.findField(prop, 'dispalay_name')
        proptype = handleXML.findField(prop, 'type')
        propdefault = handleXML.findField(prop, 'default_value')
        proptext = handleXML.findText(prop, 'description')
        udpr = Userdefprop(ptheme=ludpTheme,pgroup=lgroups[group],pname=propname)
        udpr.udpr_descr = proptext
        udpr.udpr_defaultvalue = propdefault
        udprid = udpr.insert()

        obj = prop.findall('objects/object')
        for o in obj:
            """"< object class ="oracle.dbtools.crest.model.design.relational.Column" visible="false" Color="-1" / >"""
            lMelt = Modelelemtype.type2melt(re.split("\.", handleXML.findField(o, 'class'))[6])
            if lMelt != "":
                lmeltid = Modelelemtype.getidbyshortname(lMelt)
                try:
                    metpid = ModelelementProperty(pmeltid=lmeltid,pudprid=udprid).insert()
                except Exception as err:
                    print(err)
                    logmessages.writelog(
                        "mapping type '{}' for UDP {}:{}:{} not found".format(lmeltid, ludpTheme, group, propname))
                    logmessages.writelog(err)
                    pass
            # fi

        # print (ludp)
        lov = prop.find('list_of_values')
        # Currently no Domains for UDP's and therefore no LOVs in UDPs
        # if False and (lov is not None):
        #     wrtbId = dbInserts.insertLovWrtb(pName=ludpTheme + '_' + propname)
        #
        #     # end insertLovWrtb
        #
        #     items = lov.findall('item')
        #     for val in items:
        #         # print (handleXML.findField(val,'value'),handleXML.findField(val,'default'))
        #         deva = DefaultValue()
        #         deva.deva_value = handleXML.findField(val, 'value')
        #         deva.deva_doma_id = wrtbId
        #         deva.deva_anzeige = handleXML.findField(val, 'value')
        #         deva.deva_uc = 'system'
        #         deva.deva_dc = date.today().__str__()
        #         try:
        #             deva.insert(pdoerrhdlng=False)
        #         except (sqlite3.IntegrityError):
        #             logmessages.writelog("duplicate entry in Vorgabewerte theme:'{}' property:'{}' value:'{}'"
        #                                  .format(ludpTheme, propname, deva.deva_value))
        #
        #     # for
        #     Userdefprop.setdomid(pdomid=wrtbId, pudpid=udprid)
        # # fi
    # for
# do1UDPFile

def dofiles(pdirec, pfileregexp, ptransferfunc):
    for file in os.listdir(parameters.odmFilesDirec()):
        filename, file_extension = os.path.splitext(file)
        if (pfileregexp.filename):
            filepath = parameters.odmIMDirec() + file
            # print (filepath)
            ptransferfunc(filepath)
        # fi
    # endfor


# dofiles

def transferUDP():
    doxmlfiles(pdirec=parameters.odmFilesDirec()
               , ptransfer=do1UDPFile
               , ppattern=r'.*\.{}'.format(UDPEXTENSION))

    dbConnect.myDbConn.commit()
# transferUDP


def insertlanguages():
    languages = {'de': ['Deutsch', 'deu']
        , 'en': ['English', 'eng']
        , 'fr': ['Français', 'fra']
        , 'es': ['Español', 'esp']
        , 'it': ['Italiano', 'ita']
                 }
    # (spra_iso_name, spra_iso_code2, spra_iso_code3
    # , spra_ist_textsprache, spra_spra_id, spra_uc
    # , spra_dc
    deflang = parameters.dbDefaultLang()
    for key, value in languages.items():
        Language(pname=value[0], piso2=key, piso3=value[1]).insert()

    if not deflang in languages: deflang = 'de'
    Language.setmodellang(pmodellang=deflang)
    Language.setallreplacementlang()

def insertmelts():
    Modelelemtype.fillmelt()

def insertdiagtypes():
    diatid = Diagramtype(pname=Diagramtype.ENTITY).insert()
    MeltDiat(pdiatid=diatid,pmeltid=Modelelemtype.getidbyshortname(pshortname=Modelelemtype.ENTI)).insert()
    MeltDiat(pdiatid=diatid, pmeltid=Modelelemtype.getidbyshortname(pshortname=Modelelemtype.RELA)).insert()
    MeltDiat(pdiatid=diatid, pmeltid=Modelelemtype.getidbyshortname(pshortname=Modelelemtype.ATTR)).insert()
    diatid = Diagramtype(pname=Diagramtype.RELATIONAL).insert()

def insertBaseData():
    insertmelts()
    insertdiagtypes()
# insertBaseData

def loadcolors(color:Color, elem):
    for fo in elem.findall('fonts/font_object'):
        if ((handleXML.findField(fo, 'fo_type') == 'Title')
                or (handleXML.findField(fo, 'fo_type') == 'Titel')):  # es könnte auch Deutsch sein
            color.fontcolor = handleXML.findField(fo, 'font_color')
            color.fontname = handleXML.findField(fo, 'font_name')
            color.fontsize = handleXML.findField(fo, 'font_size')
            color.fontstyle = handleXML.findField(fo, 'font_style')
        # fi
    # for
# loadcolors

def loaddefaultcolors():
    global defcolors,classcolors,classids
    settings = handleXML.parseXML(pfilename=parameters.odmsettingsfile())
    root = settings.getroot()
    classif = root.find('classification_types')

    for ty in classif:
        catname = handleXML.findField(ty,'name')
        category = EntityCategory(pname=catname.strip())
        classid = category.insert()
        classguid = handleXML.findField(ty, 'id')
        classids[classguid] = classid

        # foregcolor, backgcolor,fontcolor,fontname,fontsize,fontstyle):
        color = Color(foregcolor=handleXML.findField(ty, 'fgcolor'), backgcolor= handleXML.findField(ty, 'color'))
        loadcolors(color=color, elem=ty)
        classcolors[classguid] = color
        elui = ElementUI()
        elui.elui_enca_id = classid
        elui.elui_color = int2hex(color.backgcolor)
        elui.elui_margincolor = int2hex(color.foregcolor)
        elui.elui_fontsize = color.fontsize
        elui.elui_fontcolor = int2hex(color.fontcolor)
        elui.insert()
    # for

    default = root.find('default_fonts_and_colors')
    for de in default:
        classname = handleXML.findField(de, 'classname')
        color= Color(handleXML.findField(de, 'foreground')
                                , handleXML.findField(de, 'background')
                                , None, None, None, None)
        loadcolors(color = color, elem=de)
        defcolors[classname] = color
        if classname == "Entity":
            categoryid = EntityCategory(pname=classname).insert()
            elui = ElementUI()
            elui.elui_enca_id = categoryid
            elui.elui_color = int2hex(color.foregcolor)
            elui.elui_margincolor = int2hex(color.backgcolor)
            elui.elui_fontsize = color.fontsize
            elui.elui_fontcolor = int2hex(color.fontcolor)
            elui.insert()
    # for
# loaddefaultcolors

def filllanguages():
    Languagetext.insertlang_texts(pudpthema=parameters.odmUDPTranslFileName())
    #copy comma-list-synonym into synoyms
    Synonym.transfersynotransl()
    # fill all elements in default language
    Languagetext.filldefaulttext(parameters.dbDefaultLangID())
    Language.deleteunused()
    return

def fillelementdisplays():
    Modelelement.insertudpelems(pudpthema=parameters.odmUDPElemdisplFileName())
    return


def transferproject():
    proj = handleXML.parseXML(pfilename=parameters.odmIMDirec() + parameters.modelName() + parameters.odmIMExtension())
    root = proj.getroot()
    comm = handleXML.findText(root, 'comment')
    if comm is None:
        defspra = parameters.dbDefaultLang()
        sprachen = parameters.dbLanguages()
    else:
        defspra = re.search(r'currentLang=([A-Z]{2})', comm).group(1)
        sprachen = re.search(r'languages=([A-Z,]*)', comm).group(1)
    # print (handleXML.findField(root,'name'),comm,sprachen,defspra)
    proj = Project()
    proj.proj_name = handleXML.findField(root, 'name')
    proj.proj_uc = handleXML.findText(root, 'createdBy')
    proj.proj_dc = handleXML.findText(root, 'createdTime')
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
# transferproject

def do1Document(fileName):
    global docuparents
    tree = handleXML.parseXML(pfilename=fileName)
    root = tree.getroot()
    id =handleXML.findField(root, 'id')
    docu = Document(psrcname=Externalref.SOURCE_ODM,psrcid=id)
    docu.docu_name = handleXML.findField(root, "name")
    type= handleXML.findText(root, 'type')
    if type is not None and type != '':
        docu.docu_stfo_id = Storageformat.getorcreate(pname=type).stfo_id
    docu.docu_reference = handleXML.findText(root, 'reference')
    pd = handleXML.findText(root, 'parentDocument')
    if (pd is not None and pd != ''):
        docuparents [id]= handleXML.findText(root, 'parentDocument')
    docu.insert()

def do1Orgunit(fileName):
    global orguparents,contacts

    tree = handleXML.parseXML(pfilename=fileName)
    root = tree.getroot()
    srcid =handleXML.findField(root, 'id')
    orgu = OragnisationalUnit(psrcname=Externalref.SOURCE_ODM,psrcid=srcid)
    orgu.orgu_name = handleXML.findField(root, "name")
    orgu.orgu_uc = handleXML.findText(root, "createdBy")
    orgu.orgu_dc = handleXML.findText(root, "createdTime")
    orgu.orgu_descr = handleXML.findText(root, "comment")
    pd = handleXML.findText(root, 'parentParty')
    if (pd is not None and pd != ''):
        orguparents [srcid] = pd
    conts = root.findall('contacts/contact')
    for cont in conts:
        orgu.orgu_mail = contacts[cont.text]['email']
        orgu.orgu_telefon = contacts[cont.text]['phone']
        break #currently only 1 contact per orgunit
    orgu.insert()

docuparents ={}
def transferDocuments():
    global docuparents
    docuparents = {}
    dosegfiles(pdirec=parameters.odmdocumentdirec(), transferfiles=do1Document,pmandatoryfile=False)
    Document.updparents(psrcname=Externalref.SOURCE_ODM,pparents=docuparents)

orguparents ={}
def transferorgunits():
    global orguparents
    orguparents = {}
    dosegfiles(pdirec=parameters.odmorgunitdirec(), transferfiles=do1Orgunit,pmandatoryfile=False)
    OragnisationalUnit.updparents(psrcname=Externalref.SOURCE_ODM,pparents=orguparents)


def removeemptyudp():
    """remove all UDP's which are empty (containing '.' or '' or null as value"""
    Userdefpropvalue.removeemptyUDP(('.',''))

def removefixedudp():
    """remove all UDP's which are pa rt of our model"""
    modeludps = [(parameters.odmUDPElemdisplFileName(), val) for val in Modelelement.ODMattrmapping.values()]
    for lang in Language.select():
        for name in Languagetext.ODMtranslAttributes:
            modeludps.append(
                (parameters.odmUDPTranslFileName(), "{}_{}".format(lang.lang_iso_code2.upper(), name.upper())))
        #for
    #for

    Userdefprop.removemodelUDP(modeludps)
    return

def removeattrmeta(pstr):
    return re.sub(r' ?\[[LNT]+\]','',pstr)

emails = {}
def do1email(fileName):
    global emails
    tree = handleXML.parseXML(pfilename=fileName)
    root = tree.getroot()
    emails [handleXML.findField(root, 'id')] = {'name' : handleXML.findField(root, "name")
                                       ,'descr': handleXML.findText(root, "comment")
                                       ,'uc' : handleXML.findText(root, "createdBy")
                                        ,'dc' : handleXML.findText(root, "createdTime")
                                        ,'email' : handleXML.findText(root, "emailAddress")
                                      }
#do1email
phones = {}
def do1phone(fileName):
    global phones
    tree = handleXML.parseXML(pfilename=fileName)
    root = tree.getroot()
    phones[handleXML.findField(root, 'id')] = {'name' : handleXML.findField(root, "name")
                                       ,'descr': handleXML.findText(root, "comment")
                                       ,'uc' : handleXML.findText(root, "createdBy")
                                        ,'dc' : handleXML.findText(root, "createdTime")
                                        ,'phoneno' : handleXML.findText(root, "phoneNumber")
                                        , 'phnetype': handleXML.findText(root, "phoneType")
                                       }
#do1phone
contacts = {}
def do1contact(fileName):
    global contacts,emails,phones
    tree = handleXML.parseXML(pfilename=fileName)
    root = tree.getroot()
    phone,mail = "",""

    ems = root.findall("emails/email")
    for em in ems:
        e = emails
        mail = emails[em.text]['email']
        break #currently we take only the first
    phs = root.findall("phones/phone")
    for ph in phs:
        phone = phones[ph.text]['phoneno']
        break    #currently we take only the first
    id = handleXML.findField(root, 'id')
    contacts[id] = {'name' : handleXML.findField(root, "name")
                                       ,'descr': handleXML.findField(root, "comment")
                                        ,'email' : mail
                                        ,'phone': phone
                                       ,'uc' : handleXML.findField(root, "createdBy")
                                        ,'dc' : handleXML.findField(root, "createdTime")
                                       }
#do1contact

def transferODMModel(**kwargs):
    global interfacedomains
    """provisional Element internal buffers"""
    businfodirec = parameters.odmIMDirec() + parameters.modelName() + '/businessinfo/'
    dosegfiles(pdirec=businfodirec+'email/',transferfiles=do1email,pmandatoryfile=False)
    dosegfiles(pdirec=businfodirec+'phone/',transferfiles=do1phone,pmandatoryfile=False)
    dosegfiles(pdirec=businfodirec+'contact/',transferfiles=do1contact,pmandatoryfile=False)

    """überträgt das ganze ODM Modell in die DB"""
    insertlanguages()
    transferproject()
    transferTypes()
    transferDocuments()
    transferorgunits()
    transferDomains()
    transferUDP()
    loaddefaultcolors()
    transferEntities()
    transferRelations()
    transferArcs()
    doSubentities()
    transferKeys()
    transferdiagramme()
    transferRelational.transfer()
    Datatype.deleteunused()
    Column.fillextid()
    Domain.fixdomaininterfaces(interfacedomains)
    BusinessRule.setburuelements()
    removeemptyudp()
    filllanguages()
    fillelementdisplays()
    removefixedudp()
# end transferODMModel
