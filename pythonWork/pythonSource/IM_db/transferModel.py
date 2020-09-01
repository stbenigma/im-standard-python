import math
import os
import re
import sqlite3
import xml.etree.ElementTree as ET
from datetime import date

import transferRelational
from IM_DB import dbInserts, dbDML, dbLookup, dbConnect, parameters, dbParam, logging
from IM_OBJECTS import *
from mystring import nvl

GUIDPATTERN: str = '[A-Z0-9-]{20,45}'


class color:
    def __init__(self, foregcolor, backgcolor, fontcolor, fontname, fontsize, fontstyle):
        self.backgcolor = backgcolor
        self.foregcolor = foregcolor
        self.fontcolor = fontcolor
        self.fontname = fontname
        self.fontsize = fontsize
        self.fontstyle = fontstyle
    # end __init__


# color

# entry of keys found in entites
# [Schluessel, (listof attr and relationship guids)]
schluessel = []
# Classification type colors
# classguid : color
classcolors = dict()
# default colors
# elementtypename : color
defcolors = dict()


def findText(set, name):
    try:
        return set.find(name).text
    except:
        return None


# findText

def findField(set, name):
    try:
        return set.get(name)
    except:
        return None


# findField


def nameflags(pstr: str, pflag: str) -> bool:
    """checks [NLT] at end of names (my erd-Extension)"""
    if (pstr is None): return
    lmatch = "\[.{0,2}" + pflag + ".{0,2}\]"
    return (True if re.match(lmatch, pstr) else False)


def is_historisized(pstr: str) -> bool:
    return nameflags(pstr=pstr, pflag='T')


def is_langdept(pstr: str) -> bool:
    return nameflags(pstr=pstr, pflag='L')


def is_repeated(pstr: str) -> bool:
    return nameflags(pstr=pstr, pflag='N')


def transferTypes():
    types = ET.parse(parameters.odmIMDirec() + parameters.odmKonfDirec() + parameters.odmTypesFile())
    root = types.getroot()
    for typ in root.findall('logicaltype'):
        Datatype(pname=findField(typ, 'name')
                 , pbasetype=Datatype.baseType(findText(typ, 'mapping'))
                ,psrcname=Externalref.SOURCE_ODM,pscrid=findField(typ, 'objectid')
                ).insert()
    # endfor


def do1structtype(filename):
    structdomains = ET.parse(filename)
    structdom = structdomains.getroot()
    if (findField(structdom, "class") != "oracle.dbtools.crest.model.design.datatypes.StructuredType"): return
    # print (findField(structdom,"name"))
    doma = Domain(psrcname=Externalref.SOURCE_ODM,psrcid=findField(structdom, "id"))
    doma.doma_name = findField(structdom, "name")
    doma.doma_uc = findText(structdom, "createdBy")
    doma.doma_dc = findText(structdom, "createdTime")
    doma.doma_type = 'GRP'
    doma.doma_origin = Domain.DOMAIN
    doma.insert()

    elements = structdom.findall("attributes/Attribute")
    for el in elements:
        # print (doma.doma_name,findField(el,"name"),findText(el,'type'))
        dgrm = Domaingroup(psrcname=Externalref.SOURCE_ODM,pscrid=findText(el,'id'))
        daty = Modelelement.getelementbyextref(psrcid=findText(pxml, 'type'),
                                               psrcname=Externalref.SOURCE_ODM)
        dgrm.dgrm_doma_id_group = doma.doma_id
        dgrm.dgrm_name = findField(el, "name")
        dgrm.dgrm_descr = findText(el, "comment")
        dgrm.dgrm_uc = findText(el, "createdBy")
        dgrm.dgrm_dc = findText(el, "createdTime")
        dgrm.dgrm_is_mandatory = Boolean.bool2str(Boolean.str2bool(findText(el, "mandatory")))
        elwrtb = Domain().getbyextref(type)
        if elwrtb is None:
            # nimm vorläufig unknown, da mein Typ evtl. noch nicht da ist.
            elwrtbid = Domain().getunknown().doma_id
        else:
            elwrtbid = elwrtb.doma_id
        dgrm.dgrm_doma_id_member = elwrtbid
        xxdgrm.insert()
    # for


def liesunsfuelldoma(pdoma, pxml):
    pdoma.doma_uc = findText(pxml, 'createdBy')
    pdoma.doma_dc = findText(pxml, 'createdTime')
    daty = Modelelement.getelementbyextref(psrcid=findText(pxml, 'logicalDatatype'),psrcname=Externalref.SOURCE_ODM)
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
            # print (findField(lovval,'value'),findField(lovval,'description'),lovval.attrib)
            lovs.update({findField(lovval, 'value'): findField(lovval, 'description')})
        # endfor
        # print (len(lovs))
    # endif
    ranges = pxml.findall('listOfRanges/rangeDef')
    if not (ranges == []):
        range = (findText(ranges[0], 'beginValue'), findText(ranges[0], 'endValue'))
    else:
        range = (None, None)
    # endif

    # noch nicht übernommenm< defaultValue > a @ b.ch < / defaultValue >

    if (pdoma.doma_type == 'BIN'):
        pdoma.doma_bin_contenttype = 'BILD'  # 'FILM','GRAPH','TEXT','TON'
        pdoma.doma_bin_spfo_id = None
    elif (pdoma.doma_type == 'LOV'):
        zahl = re.search('\A\d* ', nvl(findText(pxml, 'dataTypeSize')))
        pdoma.doma_text_maxlng = zahl.group() if not (zahl is None) else None
    elif (pdoma.doma_type == Domain.TXT):
        #            print(re.search('\A\d* ','123 ab').group())
        zahl = re.search('\A\d* ', nvl(findText(pxml, 'dataTypeSize')))
        pdoma.doma_text_maxlng = zahl.group() if not (zahl is None) else None
        constr = pxml.find('checkConstraint')
        if not (constr is None):
            # print(constr.findall('*'))
            impl = constr.find('implementationDef')
            if not (impl is None):
                pdoma.doma_text_syntaxrule = findField(impl, 'definition')
    elif (pdoma.doma_type == Domain.DAT):
        pdoma.doma_dat_minvalue = range[0]
        pdoma.doma_dat_maxvalue = range[1]
        pdoma.doma_dat_granularity = Domain.MINUTE
    elif (pdoma.doma_type == 'NUM'):
        pdoma.doma_num_minvalue = range[0]
        pdoma.doma_num_maxvalue = range[1]
        prec = findText(pxml, 'dataTypePrecision')
        scale = findText(pxml, 'dataTypeScale')
        pdoma.doma_num_fract_digits = 0 if scale is None else int(scale)
        pdoma.doma_num_total_digits = 0 if prec is None else int(prec)
        pdoma.doma_num_round_value = None
        pdoma.doma_phyu_id = PhysicalUnit.getorcreate(pname=findText(root, 'unitOfMeasure')).phyu_id
    # fi
    pdoma.insert()

    if (lov is not None) & (lov != {}):
        for idx, key in enumerate(lovs.keys(), start=1):
            deva = DefaultValue()
            deva.deva_value = key
            deva.deva_doma_id = pdoma.doma_id
            deva.deva_sort_order = idx
            deva.deva_uc = pdoma.doma_uc
            deva.deva_dc = pdoma.doma_dc
            deva.deva_displ = lovs[key]
            deva.insert()
        # for
    # fi


def transferDomains():
    domains = ET.parse(parameters.odmDomainsFilePath())
    root = domains.getroot()
    for dom in root.findall('domains/Domain'):
        doma = Domain(psrcname=Externalref.SOURCE_ODM,psrcid=findField(dom, "id"))
        doma.doma_name = findField(dom, "name")
        doma.doma_descr = findText(dom, 'comment')
        doma.doma_origin = Domain.DOMAIN
        liesunsfuelldoma(pdoma=doma, pxml=dom)
    # for

    dosegfiles(pdirec=parameters.odmstructypesdir(), transferfiles=do1structtype)

    """update group domains a their types may now be available"""
    Domaingroup.updmembers()


# end transferDomains

def hex2int(phex):
    return None if (phex is None) else int(phex, 16)


def int2hex(pint):
    if (pint is None): return pint
    lint = pint if (type(pint) == int) else int(pint)
    lint = lint + (hex2int('FFFFFF') if (lint < 0) else 0)
    if lint == -1:  # -1 wird führt zu -0x1 was die Selektion später erschwert
        lint = hex2int('FFFFFF')
    retval = '000000' + hex(lint)[2:]
    retval = retval[len(retval) - 6:]
    return retval


def toString(str, upper=False):
    if str is None:
        return "''"
    else:
        return (str.upper())
    # fi


# toString

def transferentity(penti, pdiagid, puc, pdc):
    entiodm = findField(penti, 'oid')
    enti = Entitaet().getbyextref(entiodm)
    hiddenelements = penti.find("hiddenElements")
    if hiddenelements is not None:
        elemtext = findField(hiddenelements, "elements")
    else:
        elemtext = ""
    hiddenattrs = elemtext.split(' ')
    hiddenattrs2 = []
    for e in hiddenattrs:
        if e != "": hiddenattrs2.append(Attribut().getID(pguid=e))
    attrs = Attribut.select(pwhere="attr_enti_id = {}".format(enti.enti_id), porderby="attr_anz_rhflg")
    attrids = [a.attr_id for a in attrs]
    attrids = list(set(attrids) - set(hiddenattrs2))
    # print (attrids,hiddenattrs2)

    layout = penti.find('bounds')
    col = defcolors['Entity']  # defaults können mal geladen werden
    if (findText(penti, 'useDefaultColor') == 'false'):

        col.backgcolor = findText(penti, 'backgroundColor')
        col.foregcolor = findText(penti, 'foregroundColor')
        # print (backgroundc,foregroundc)
        font = penti.find('fonts/FontObject[foType ="Title"]')
        # deutsche ODMnutzuer schreiben Titel in die Kongig....
        if font is None: font = penti.find('fonts/FontObject[foType ="Titel"]')
        # fontname,fontsize,fontstyle):
        v = findText(font, 'colorRGB')
        col.fontcolor = v if v is not None else col.fontcolor
        v = findText(font, 'fontStyle')
        col.fontstyle = v if v is not None else col.fontstyle
        v = findText(font, 'fontSize')
        col.fontsize = v if v is not None else col.fontsize
    else:
        # check wether entity belongs to category
        if (enti.enti_category_guid is None):
            col = defcolors['Entity']
        else:
            try:
                col = classcolors[enti.enti_category_guid]
            except Exception as e:
                # print(e) flls class nicht mehr exisitert
                col = defcolors['Entity']
        # fi
    # fi
    # print (col.foregcolor,col.backgcolor)
    # eled_position_x,eled_position_y,eled_breite,eled_hoehe
    # ,eled_deckkraft,eled_farbe,eled_randbreite,eled_randdeckkraft
    # ,eled_randfarbe, eled_schriftgroesse, eled_schriftfarbe, eled_mode_id
    # ,eled_diag_id, eled_uc, eled_dc, eled_um
    # , eled_dm

    index = 0
    entix = int(findField(layout, 'x'))
    entiy = int(findField(layout, 'y'))
    entiwidth = int(findField(layout, 'width'))
    entiheight = int(findField(layout, 'height'))
    # if there are several copies on a diagramm, repeat the insert with new index und insert succeeds
    while True:
        row = (entix, entiy, entiwidth, entiheight
               , 100, int2hex(col.backgcolor), None, 100
               , int2hex(col.foregcolor), col.fontsize, int2hex(col.fontcolor),
               Modelelement.getidbyelemid(pentiid=enti.enti_id)
               , pdiagid, index, puc, pdc
               , None, None)
        # print (row)
        try:
            dbInserts.insertelementdarst(pdata=row)
            attrx = int(entix) + 26  # x1,x2=16,26 y=30
            attry = int(entiy) + 30
            attrwidth = int(entiwidth) - 36
            attrheight = 13
            for aid in attrids:
                attrrow = (attrx, attry, attrwidth, attrheight
                           , 100, int2hex(col.backgcolor), int2hex(col.fontcolor), 100
                           , None, None, None, Modelelement.getidbyelemid(pattrid=aid)
                           , pdiagid, 0, puc, pdc
                           , None, None)
                try:
                    dbInserts.insertelementdarst(pdata=attrrow)
                except Exception as e:
                    print(e)
                attry += attrheight
                # Maximal bis zur Grösse der Entität
                if ((attry - entiy) > (entiheight - 10)): break
            # for
            break  # no more looping for copies of element on diagramm
        except sqlite3.IntegrityError:
            index += 1
        except Exception as ex:
            print(str(ex))
            print(row)
            raise ex
    # while


# transferentity

def transferdiaobj(pobjects, pdiagid, puc, pdc):
    for o in pobjects:
        type = findField(o, 'otype')
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
    if (pidx == 0): return psource
    if (pidx == (pmaxidx - 1)): return ptarget
    return None


# conmector
def transferdiaconnect(pconnectors, pdiagid, puc, pdc):
    for c in pconnectors:
        type = findField(c, 'otype')
        if (type == 'Relation'):
            relaguid = findField(c, "oid")
            beziid = dbLookup.beziId(relaguid)
            linewidth = findText(c, 'lineWidth')
            sourcelabel = c.find('sourceLabel/labelBounds')
            sttex = findField(sourcelabel, 'x')
            sttey = findField(sourcelabel, 'y')
            sttew = findField(sourcelabel, 'width')
            stteh = findField(sourcelabel, 'height')
            targetlabel = c.find('targetLabel/labelBounds')
            entex = findField(targetlabel, 'x')
            entey = findField(targetlabel, 'y')
            entew = findField(targetlabel, 'width')
            enteh = findField(targetlabel, 'height')

            """Labels können negative Starts haben, verschiebe sie in den positiven Bereich"""
            if sttey is not None and int(sttey) < 0: sttey, entey = 0, int(entey) - int(sttey)
            if sttey is not None and int(sttey) < 0: sttey, entey = 0, int(entey) - int(sttey)

            bezi = dbDML.select("""select rela_mandatory_from_to,rela_mandatory_to_from
                                        ,rela_type
                                         ,case bezi_source_enti_guid 
                                         when source.enti_odm_guid then 'FALSE' 
                                            else 'TRUE' end switch
                                    from beziehungen
                                    join entitaeten source on source.enti_id = rela_enti_id_from
                                    where rela_id ={}
                    """.format(beziid))
            lbezitype = bezi[0][2]
            sourcelinetype = 'SOLID' if (bezi[0][0] == 'TRUE') else 'DASHED'
            targetlinetype = 'SOLID' if (bezi[0][1] == 'TRUE') else 'DASHED'
            sourcecard = '1' if (lbezitype in ('ISA', '1:1')) else 'M'
            targetcard = '1' if (lbezitype in ('ISA', '1:1', 'M:1')) else 'M'
            if (bezi[0][3] == 'TRUE'):  # switch source and target
                sourcecard, targetcard = targetcard, sourcecard
                sourcelinetype, targetlinetype = targetlinetype, sourcelinetype
                sttex, entex = entex, sttex
                sttey, entey = entey, sttey
                sttew, entew = entew, sttew
                stteh, enteh = enteh, stteh
            # fi

            """
    beda_diag_id, beda_mode_id, beda_linienbreite, beda_liniefarbe
    ,beda_liniedeckkraft, beda_starttext_x, beda_starttext_y, beda_starttext_breite
    ,beda_starttext_hoehe, beda_endtext_x, beda_endtext_y, beda_endtext_breite
    ,beda_endtext_hoehe, beda_schriftfarbe, beda_schriftgroesse, beda_uc
    ,beda_dc, beda_um, beda_dm)
"""
            row = (pdiagid, Modelelement.getidbyelemid(prelaid=beziid), linewidth, None
                   , 1, sttex, sttey, sttew
                   , stteh, entex, entey, entew
                   , enteh, None, 10, puc, pdc, None, None
                   )
            bedaid = dbInserts.insertelbezidarst(row)

            points = c.findall('points/point')
            points = [{'x': int(findField(p, 'x')), 'y': int(findField(p, 'y'))} for p in points]
            if len(points) == 2:
                """1elementige Linien werden um einen Mittelpunkt ergänzt wegen -- oder solid"""
                midpos = lambda x1, x2: round((x1 - x2) / 2 + x2)
                points.insert(1, {'x': midpos(points[0]['x'], points[1]['x']),
                                  'y': midpos(points[0]['y'], points[1]['y'])})
            # fi
            pointsegs = []
            for idx, point in enumerate(points):
                """ lise_rhfg, lise_beda_id, lise_x, lise_y
    , lise_linientyp,lise_konnektor, lise_uc, lise_dc
    , lise_um,lise_dm,nkel
    """
                x, y = point['x'], point['y']
                if len(pointsegs) > 0:
                    """ ab dem 2. Punkt wird im vorherigen Punkte der Winkel zum nächsten hinzugefügt"""
                    calcwinkel = lambda ey, sy, ex, sx: math.atan2(ey - sy, ex - sx)
                    prevpoint = pointsegs[len(pointsegs) - 1]
                    prevpoint[10] = calcwinkel(y, prevpoint[3], x, prevpoint[2])
                pointsegs.append([idx, bedaid, x, y
                                     , linetype(pidx=idx, pmaxidx=len(points)
                                                , psourcelt=sourcelinetype, ptargetlt=targetlinetype)
                                     , connector(pidx=idx, pmaxidx=len(points)
                                                 , psource=sourcecard, ptarget=targetcard)
                                     , puc, pdc, None, None, None])
            # for
            dbInserts.insertlinieseg(pointsegs)
        else:
            pass
        # fi


# transferdiaconnect

# transferdiaconnect

def transferdiaarc(parcs, pdiagid, puc, pdc):
    pass


# transferdiaarc

# def doGUIDfile(pdirec,pfile,transferfiles):
#    #nur GUID als Namen erlaubt.
##    if re.match(r'{}.xml'.format(GUIDPATTERN),pfile):
#        fileName = pdirec + pfile
#        transferfiles(fileName)
#    #fi
##doGUIDfile

def doxmlfiles(pdirec, ptransfer, ppattern=r".*"):
    try:
        listdir = os.listdir(pdirec)
    except:
        print('doXMLfiles: directory "{}" not found.'.format(pdirec))
        return
    # try
    for file in listdir:
        if re.match(ppattern, file):
            ptransfer(pdirec + file)
        # fi
    # for


# doxmlfiles

def dosegfiles(pdirec, transferfiles):
    try:
        listdir = os.listdir(pdirec)
    except:
        logging.writelog('dosSEGfiles: directory "{}" not found.'.format(pdirec))
        return
    # try
    for el in listdir:
        if re.match('seg_.*', el):
            doxmlfiles(pdirec=pdirec + el + '/'
                       , ptransfer=transferfiles
                       , ppattern=r'{}.xml'.format(GUIDPATTERN))


#            for file in os.listdir(pdirec + el):
#                doGUIDfile(pdirec=pdirec + el + '/',pfile=file,transferfiles=transferfiles)
#            #for
# fi
# for
# dosegfiles

def do1diagramm(pfilename):
    # print (p_filename)
    try:
        diagramme = ET.parse(pfilename)
    except:
        print("Diagramm nicht lesbar: {}".format(pfilename))
        return
    dia = diagramme.getroot()
    diag = Diagramm()
    diag.diag_name = findField(dia, 'name')
    if (diag.diag_name == 'Logical'):
        return
    # entcomm = findText(root,'comment')
    # creby = findText(root,'createdBy')
    # creti = findText(root,'createdTime')
    """'
                    ,'diag_odm_guid', 
                    """
    diag.diag_diat_id = Diagrammtyp.getbyname(pname='Entity').diat_id
    # print(findField(dia,'name'), findField(dia,'id'))
    # diag_name,diag_diat_id,diag_uc,diag_dc,diag_um,diag_dm

    if (findText(dia, 'showLegend') == 'true'):
        legende = dia.find("objectViews/OView[@otype='Legend']")
        bounds = legende.find("bounds")
        diag.diag_legendx = findField(bounds, 'x')
        diag.diag_legendy = findField(bounds, 'y')
    else:
        diag.diag_legendx = None
        diag.diag_legendy = None
    # fi
    diag.diag_uc = findText(dia, 'createdBy')
    diag.diag_dc = findText(dia, 'createdTime')
    diag.diag_odm_guid = findField(dia, 'id')
    diag.diag_um = findText(dia, 'modifiedBy')
    # print (row)
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


#    for el in os.listdir(parameters.odmentisubviewdirec()):
#        #filename = parameters.odmentisubviewdirec() +  el
#        #do1diagramm(p_filename=filename)
#        doGUIDfile(pdirec = parameters.odmentisubviewdirec()
#                   , pfile = el
#                   , transferfiles = do1diagramm)
#    #endfor
# transferdiagramme

def insertderiveddomain(ptypeguid, pattrname, pvatername, pattrxml):
    doma = Domain()
    doma.doma_name = pattrname
    domatest = Domain.getbyname(pname=doma.doma_name)
    if (domatest is not None):
        # es gibt ihn schon, füge den Vaternamen dazu
        doma.doma_name = pattrname + '-' + pvatername
    doma.doma_origin = Domain.DERIVED
    if nvl(ptypeguid) != '': doma.doma_daty_id = Datatype.getidbyextid(ptypeguid)
    doma.doma_descr = "generiertes Domain für Datentyp für Attribut {}.{}".format(pvatername, pattrname)

    liesunsfuelldoma(pdoma=doma, pxml=pattrxml)
    return doma


# insertderiveddomain


def findeOderErstelleDom(pdomguid, pstructdomguid, ptypeguid, pattrname, pvatername, pattrxml):
    dom = None
    if pdomguid is not None:
        dom = Domain().getbyextref(pdomguid)
    elif pstructdomguid is not None:
        dom = Domain().getbyextref(pstructdomguid)
    elif ptypeguid is not None:
        dom = insertderiveddomain(ptypeguid=ptypeguid, pattrname=pattrname, pvatername=pvatername, pattrxml=pattrxml)
    #
    if dom is None:
        dom = Domain().getbyname('Unknown')
    return dom.doma_id


# findeOderErstelleDom

def do1Arc(fileName):
    arcXML = ET.parse(fileName).getroot()
    if (findField(arcXML, "class") != "oracle.dbtools.crest.model.design.logical.Arc"): return

    arc = Arc(pname=findField(arcXML, "name")
              , pentiid=Entitaet().getID(findText(arcXML, 'entity'))
              , puc=findText(arcXML, 'createdBy')
              , pdc=findText(arcXML, 'createdTime'))
    arcid = arc.insert()
    Externalref(psrcname=Externalref.SOURCE_ODM, psrcid=findField(arcXML, "id")).insert()

    """map all relations to this arc"""
    relations = arcXML.findall('relations/relationID')
    relids = ','.join("'{}'".format(r.text) for r in relations)
    # DEBUG Arc 2x auf Beziehung
    #    if findField(arcXML, "name") in ('xxArc_9', 'xxArc_11'):
    #        print(findField(arcXML, "id"), findField(arcXML, "name"), findText(arcXML, 'entity'))
    if False:
        res = dbDML.select("""select case earc.enti_odm_guid
                            when evon.enti_odm_guid
                            then arcs_id else null end von_arcs_id
                            ,case earc.enti_odm_guid
                            when ezu.enti_odm_guid
                            then arcs_id else null end zu_arcs_id
                 ,arcs_id,arcs_name,rela_id,rela_name,earc.enti_name,earc.enti_odm_guid,ezu.enti_odm_guid
                    from arcs
                    cross join beziehungen
                    join entitaeten earc on arcs_enti_id = earc.enti_id
                    left join entitaeten evon on rela_enti_id_from = evon.enti_id
                    left join entitaeten ezu on rela_enti_id_to = ezu.enti_id
                    where arcs_id = {}
                and bezi_odm_guid in ({})""".format(arcid, relids))
        # print(res)
    Relation.updaterela(parcid=arcid, prelids=relids)

    # print(findField(arc,"name"),rel.text)


# do1Arc

def transferArcs():
    dosegfiles(pdirec=parameters.odmArcDirec(), transferfiles=do1Arc)


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
                bdegId = dbLookup.bdegLookup(findField(prop, 'name'))
                # print('      ', findField(prop,'name'), findField(prop,'value'), bdegId)
                udps.append((findField(prop, 'value'), pmodeid, bdegId))
            except:
                """dynamische Properties lassen wir aus"""
                pass
        # for
    # fi
    # look for comments in the notesfield of the element
    note = findText(pobj, 'notes')
    if (note is not None):
        prop = re.finditer(r'\[(([A-Z]{2})[^[]+)\[\n([^]]*)\][A-Z]{2}[^]]+\]', note, re.DOTALL)
        # liefert group1 name,group2 sprache, group3 text
        for i, p in enumerate(prop):
            # print (i,p.group(0),'\n1:',p.group(1),'\n2:',p.group(2),'\n3:',p.group(3))
            bdegId = dbLookup.bdegLookup(p.group(1))
            # print('      ', findField(prop,'name'), findField(prop,'value'), bdegId)
            udps.append((p.group(3).rstrip(), pmodeid, bdegId))
        # for
    # fi

    if len(udps) > 0:
        # print (udps)
        Userdefpropvalue.updvalues(prows=udps)
    # fi


def do1Attribute(plfnr, pattrxml, pentiId=None, prelaId=None):
    # wegen FK-PK zusätzliche Attribute werden nicht übernommen
    if (findText(pattrxml, 'referedAttribute') is not None):
        return
    if pentiId is not None:
        vatername = Entitaet().getbyid(pid=pentiId).enti_name
    elif prelaId is not None:
        vatername = "Beziehung ({})".format(prelaId)

    xmlname = findField(pattrxml, 'name')
    # strip [] am Ende des Namens

    lmodeId = Modelelement(pmeltshortname=Modelelemtype.ATTR).insert()
    attr = Attribut(pname=re.sub(' ?\[[LNT]+\]', '', xmlname), pentiid=pentiId, prelaid=prelaId)
    attr.attr_id = lmodeId
    attr.attr_tech_name = findText(pattrxml, 'preferredAbbreviation')
    if attr.attr_tech_name is None:
        attr.attr_tech_name = re.sub('[-,.()\[\]äöüèéàÄ~ÖÜ ]', '_', str.upper(attr.attr_anzname))
    attr.attr_uc = findText(pattrxml, 'createdBy')
    attr.attr_dc = findText(pattrxml, 'createdTime')
    attr.attr_doma_id = findeOderErstelleDom(pdomguid=findText(pattrxml, 'domain')
                                             , pstructdomguid=findText(pattrxml, 'structuredType')
                                             , ptypeguid=findText(pattrxml, 'logicalDatatype')
                                             , pattrname=attr.attr_anzname
                                             , pvatername=vatername
                                             , pattrxml=pattrxml)
    attr.attr_beschr = findText(pattrxml, 'comment')
    attr.attr_anz_rhflg = plfnr
    attr.attr_deskriptor = 'FALSE'
    attr.attr_pflichtattr = Boolean.bool2str(findText(pattrxml, 'nullsAllowed') == 'true')
    attr.attr_historisiert = Boolean.bool2str(is_historisized(xmlname))
    attr.attr_wiederholt = Boolean.bool2str(is_repeated(xmlname))
    attr.attr_sprachabhaengig = Boolean.bool2str(is_langdept(xmlname))
    attr.attr_verschluesselt = 'FALSE'
    attr.attr_odm_guid = findField(pattrxml, 'id')
    attrId = attr.insert()

    dbInserts.insertUdpAttr(attrId)
    updateUDP(pmodeid=lmodeId, pobj=pattrxml)

    documents = getdokuref(pelem=pattrxml)
    ModelelemDoku.insertdokuref(pdocguidlist=documents, pmodeid=lmodeId)


# do1Attribute

def fillKeys(p_enti, p_entiid):
    global schluessel
    allkeys = p_enti.find('identifiers')
    if allkeys is not None:
        idx = 0
        for key in allkeys.findall('identifier'):
            kr = findText(key, 'newElementsIDs')
            #                arefs = key.findall('usedAttributes/attributeRef')
            #                keyrefs = []
            #                for i in range(len(arefs)):
            #                    keyrefs.append(arefs[i].text)
            #                    #print (i,arefs[i].text)
            #
            #            else:
            if (kr is not None):
                keyrefs = kr.split(',')
                idx += 1
                # print(idx, findField(enti,'name'), findField(key,'id'), findField(enti,'id'), keyrefs)
                schl = Schluessel()
                schl.schl_laufnr = idx
                schl.schl_name = findField(key, 'name')
                schl.schl_odm_guid = findField(key, 'id')
                schl.schl_uc = findText(key, 'createdBy')
                schl.schl_dc = findText(key, 'createdTime')
                schl.schl_enti_id = p_entiid
                schl.insert()

                schluessel.append([schl, keyrefs])
            # fi
        # rof
        # [Schluessel, (listof attr and relationship guids)]
    # fi


def transferKeys():
    global schluessel
    # Schlüssel sind eingefügt es folgen die SchlüsselElemente, die ich jetzt alle haben sollte
    # schlüssel [[Schluessel, (Liste der Referenzen)]]
    for schlentry in schluessel:
        schl = schlentry[0]
        reflist = schlentry[1]
        # nun die Schlüsselelemente
        for ke in reflist:
            scel = Schluesselelement()
            scel.scel_schl_id = schl.schl_id
            scel.scel_uc = schl.schl_uc
            scel.scel_dc = schl.schl_dc
            scel.scel_attr_id = Attribut().getID(ke)
            if scel.scel_attr_id is None:
                try:
                    scel.scel_rela_id = dbLookup.beziId(ke)
                    scel.scel_attr_id = None
                except sqlite3.Error as e:
                    print(str(e))
                    print(ke, scel)
                    raise e
                # try
            else:
                scel.scel_rela_id = None
            # if
            scel.insert()
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
                docguid = findField(doc, 'id')
                # print(docguid)
                documents.append(docguid)
            # for
            documents = tuple(documents)
        # fi
    else:
        """<documents usedDucuments="701E5525-A8EE-3C6F-E78B-28B04D93F93D"/>
        """
        docs = findField(pelem.find("documents"), 'usedDucuments')
        if (docs is not None):
            documents = tuple(docs.split(' '))
    # fi
    # print(documents)
    return documents


# getdokuref

def do1Entity(fileName):
    tree = ET.parse(fileName)
    entixml = tree.getroot()
    if (findField(entixml, "class") != "oracle.dbtools.crest.model.design.logical.Entity"): return
    entname = findField(entixml, "name")
    entcomm = findText(entixml, 'comment')
    creby = findText(entixml, 'createdBy')
    creti = findText(entixml, 'createdTime')
    enti_category_guid = findText(entixml, 'typeID')
    documents = getdokuref(pelem=entixml)
    lmodeId = Modelelement(pmeltshortname=Modelelemtype.ENTI).insert()
    enti = Entitaet()
    enti.enti_id = lmodeId
    enti.enti_odm_guid = findField(entixml, 'id')
    enti.enti_name = entname
    enti.enti_beschr = entcomm
    enti.enti_uc = creby
    enti.enti_dc = creti
    enti.enti_enti_guid = findText(entixml, 'hierarchicalParent')
    enti.enti_category_guid = enti_category_guid
    entiId = enti.insert()
    dbInserts.insertUdpEntity(entiId)

    sobj = findText(entixml, 'synonym')
    if (sobj is not None):
        for syn in sobj.split(','):
            synoname = syn.strip()
            syno = Synonym(pname=synoname, pentiid=entiId)
            syno.syno_id = Modelelement(pmeltshortname=Modelelemtype.SYNO).insert()
            syno.insert()
        # for
    # fi

    # print (entname,translate.translate(p_text=entname,p_fromlang='de',p_tolang='en'),translate.translate(p_text=entname,p_fromlang='de',p_tolang='fr'))

    updateUDP(pmodeid=lmodeId, pobj=entixml)
    ModelelemDoku.insertdokuref(pdocguidlist=documents, pmodeid=lmodeId)

    attrs = entixml.find('attributes')
    if attrs is not None:
        for idx, attr in enumerate(attrs, start=1):
            # alle Attribute
            # print(findField(attr,'name'),findField(attr,'id'))
            do1Attribute(plfnr=idx, pattrxml=attr, pentiId=entiId)
        # rof
    # fi
    fillKeys(p_enti=entixml, p_entiid=entiId)


# do1Entity


def transferEntitaeten():
    # lösche die Entitäten
    dosegfiles(pdirec=parameters.odmEntityDirec(), transferfiles=do1Entity)


# transferEntitaeten

def doSubentities():
    Entitaet.setsuperentityid()

    for superenti in Entitaet.select(
            pwhere="(select count(*) from entitaeten as e1 where e1.enti_enti_id = enti.enti_id) > 0"):
        Arc(pname=superenti.enti_name + '_subtype', pentiid=superenti.enti_id
            , puc=superenti.enti_uc, pdc=superenti.enti_dc).insert()
    # for
    # dbDML.exec("""insert into arcs (arcs_name, arcs_enti_id,arcs_uc,arcs_dc)
    #                    select name || '_subtype', id,uc,um from
    #                               (select enti_name as name, enti_id as id,enti_uc as uc ,enti_dc as um
    #                                       ,(select count(*) from entitaeten as e1 where e2.enti_odm_guid = e1.enti_enti_guid) as subanz
    #                                from entitaeten as e2
    #                                ) where subanz > 0
    #                """)

    Relation.insertisa()


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
    tree = ET.parse(fileName)
    relaxml = tree.getroot()
    documents = getdokuref(pelem=relaxml)

    rela = Relation()
    rela.rela_name = findField(relaxml, 'name')
    rela.rela_assoc_from_to = findText(relaxml, 'nameOnSource')
    rela.rela_hist_from_to = Boolean.bool2str(is_historisized(rela.rela_assoc_from_to))
    rela.rela_assoc_to_from = findText(relaxml, 'nameOnTarget')
    rela.rela_hist_to_from = Boolean.bool2str(is_historisized(rela.rela_assoc_to_from))
    rela.rela_maptype_from_to = Relation.ONE if (findText(relaxml, 'sourceCardinality') == '1') else Relation.MANY
    rela.rela_maptype_to_from = Relation.ONE if (findText(relaxml, 'targetCardinalityString') == '1') else Relation.MANY
    rela.rela_mandatory_from_to = Boolean.strnegbool(findText(relaxml, 'optionalSource'))
    rela.rela_mandatory_to_from = Boolean.strnegbool(findText(relaxml, 'optionalTarget'))
    rela.rela_type = rela.simpleType()
    rela.rela_uc = findText(relaxml, 'createdBy')
    rela.rela_dc = findText(relaxml, 'createdTime')

    sourceentiguid = findText(relaxml, 'sourceEntity')
    targetentiguid = findText(relaxml, 'targetEntity')
    rela.rela_enti_id_from = Entitaet().getID(sourceentiguid)
    rela.rela_enti_id_to = Entitaet().getID(targetentiguid)
    if (rela.rela_enti_id_from is None or rela.rela_enti_id_to is None):
        logging.writelog(
            "Entity Id {} oder {} nicht gefunden. Datenleichen von Realtion mit gelöschten Entities".format(
                sourceentiguid, targetentiguid))
        return
    # fi

    rela.insert()
    dbInserts.insertUdpBezi(bezi.bezi_id)

    updateUDP(pmodeid=lmodeId, pobj=relaxml)
    ModelelemDoku.insertdokuref(pdocguidlist=documents, pmodeid=lmodeId)

    attrs = relaxml.find('attributes')
    if attrs is not None:
        for idx, attr in enumerate(attrs, start=1):
            # alle Attribute
            # print((findField(attr,'name'),findField(attr,'id')))
            do1Attribute(plfnr=idx, pattrxml=attr, prelaId=beziId)
        # endfor
    # fi


# do1Relation

def transferRelations():
    # lösche die Beziehungen
    dosegfiles(pdirec=parameters.odmRelationDirec(), transferfiles=do1Relation)
    dbConnect.myDbConn.commit()


def do1UDPFile(pudpThema, pfileName):
    tree = ET.parse(pfileName)
    root = tree.getroot()
    lupdThema = pudpThema
    lgroups = {'': '-'}  # für ungruppierte properties
    for groups in root.findall('udp_groups'):
        for child in groups:
            # print(findField(child,'name'))
            lgroups[findField(child, 'id')] = findField(child, 'name')
        # for
    # for

    # die speziellen Properties (translation of comments in notes manuell einfüllen
    if (lupdThema == parameters.odmUDPTranslFileName()):
        for lgrpkey, lgrpvalue in lgroups.items():
            if lgrpkey != '':
                ludpid = dbInserts.insertUDP(pData=(lupdThema, lgrpvalue, lgrpvalue + '_ENTI_COMMENT', None
                                                    , None, 'FALSE', None, '--', date.today().__str__()))
                dbInserts.insertModelltypEigen(
                    (Modelelemtype.getidbyshortname(pshortname=Modelelemtype.type2melt('Entity')), ludpid))

                ludpid = dbInserts.insertUDP(pData=(lupdThema, lgrpvalue, lgrpvalue + '_ATTR_COMMENT', None
                                                    , None, 'FALSE', None, '--', date.today().__str__()))
                dbInserts.insertModelltypEigen(
                    (Modelelemtype.getidbyshortname(pshortname=Modelelemtype.type2melt('Attribute')), ludpid))
            # fi
        # for
    # fi

    props = root.find('properties')
    for prop in props.findall('property'):
        group = findField(prop, 'group_id')
        propname = findField(prop, 'name')
        propdisplayname = findField(prop, 'dispalay_name')
        proptype = findField(prop, 'type')
        propdefault = findField(prop, 'default_value')
        proptext = findText(prop, 'description')
        ludp = (lupdThema, lgroups[group], propname, propdefault
                , proptext, 'FALSE', None
                , '--', date.today().__str__())
        udpId = dbInserts.insertUDP(pData=ludp)

        obj = prop.findall('objects/object')
        for o in obj:
            """"< object class ="oracle.dbtools.crest.model.design.relational.Column" visible="false" color="-1" / >"""
            lMelt = re.split("\.", findField(o, 'class'))[6]
            lmeltid = Modelelemtype.type2melt(lMelt)
            if lmeltid != "":
                try:
                    dbInserts.insertModelltypEigen((Modelelemtype.getidbyshortname(pshortname=lmeltid), udpId))
                except Exception as err:
                    print(err)
                    logging.writelog(
                        "mapping type '{}' for UDP {}:{}:{} not found".format(lmeltid, lupdThema, group, propname))
                    logging.writelog(err)
                    pass
            # fi

        # print (ludp)
        lov = prop.find('list_of_values')
        if (lov is not None):
            wrtbId = dbInserts.insertLovWrtb(pName=lupdThema + '_' + propname)

            # end insertLovWrtb

            items = lov.findall('item')
            for val in items:
                # print (findField(val,'value'),findField(val,'default'))
                deva = DefaultValue()
                deva.deva_value = findField(val, 'value')
                deva.deva_doma_id = wrtbId
                deva.deva_anzeige = findField(val, 'value')
                deva.deva_uc = 'system'
                deva.deva_dc = date.today().__str__()
                try:
                    deva.insert(pdoerrhdlng=False)
                except (sqlite3.IntegrityError):
                    logging.writelog("duplicate entry in Vorgabewerte theme:'{}' property:'{}' value:'{}'"
                                     .format(pudpThema, propname, deva.deva_value))

            # for
            Userdefprop.setdomid(pdomid=wrtbId, pudpid=udpId)
        # fi
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

def transferUPDdef():
    # lösche die UDP
    #    l_sql = """select count(*) from benudef_wert union select count(*) from benudef_eigenschaft"""
    #    result = dbDML.select(l_sql)
    #    for row in result:
    #        print(row)
    for file in os.listdir(parameters.odmFilesDirec()):
        filename, file_extension = os.path.splitext(file)
        # print(filename, file_extension)
        if (file_extension == '.udposdm'):
            filepath = parameters.odmFilesDirec() + file
            # print (filepath)
            do1UDPFile(pudpThema=filename, pfileName=filepath)
        # fi
    # endfor

    dbConnect.myDbConn.commit()


# transferUDPdef

def transferUDP():
    transferUPDdef()


# transferUDP

def insertBaseData():
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
        Sprache(pname=value[0], piso2=key, piso3=value[1]).insert()

    if not deflang in languages: deflang = 'de'
    Sprache.setmodellang(pmodellang=deflang)
    Sprache.setallreplacementlang()

    Modelelemtype.fillmelt()
    diat = Diagrammtyp()
    diat.diat_bez = 'Entity'
    diat.diat_uc = 'stb'
    diat.diat_dc = date.today()
    diat.insert()
    #    medi_diat_id, medi_melt_id,medi_uc,mdei_dc,medi_um,mdei_dm
    dbInserts.insertmeltdiat(
        (diat.diat_id, Modelelemtype.getidbyshortname(pshortname=Modelelemtype.ENTI), 'stb', date.today(), None, None))
    dbInserts.insertmeltdiat(
        (diat.diat_id, Modelelemtype.getidbyshortname(pshortname=Modelelemtype.RELA), 'stb', date.today(), None, None))


# insertBaseData

def loeschmodell():
    transferRelational.loeschmodell()

    dbDML.delete("modelltyp_eigensch")
    dbDML.delete("benudef_wert")
    dbDML.delete("benudef_eigenschaft")
    Schluesselelement.delete()
    Schluessel.delete()
    Relation.delete()
    Arc.delete()
    Attribut.delete()
    Synonym.delete()
    Entitaet.delete()
    ModelelemDocu.delete()
    Document.delete()
    Externalref.delete()
    Modelelement.delete()
    Diagramm.delete()
    dbDML.delete("benudef_eigenschaft")
    DefaultValue.delete()
    Domaingroup.delete()
    Domain.delete()
    dbDML.delete("speicherformate")
    dbDML.delete("linie_segment")
    dbDML.delete("beziehung_darst")
    dbDML.delete("elementdarst")
    dbDML.delete("melt_diat")
    Datatype.delete()
    dbDML.delete("diagramme")
    dbDML.delete('bereich_elemdarst')
    Modelelemtype.delete()
    Diagrammtyp.delete()
    Sprache.delete()
    Sprachtext.delete()
    dbDML.delete('geschaeftsbereich')
    PhysicalUnit.delete()
    Storageformat.delete()
    Projekt.delete()


# loeschmodell

def loadcolors(coldict, classkey, elem):
    for fo in elem.findall('fonts/font_object'):
        if ((findField(fo, 'fo_type') == 'Title')
                or (findField(fo, 'fo_type') == 'Titel')):  # es könnte auch Deutsch sein
            coldict[classkey].fontcolor = findField(fo, 'font_color')
            coldict[classkey].fontname = findField(fo, 'font_name')
            coldict[classkey].fontsize = findField(fo, 'font_size')
            coldict[classkey].fontstyle = findField(fo, 'font_style')
        # fi
    # for


# loadcolors

def loaddefaultcolors():
    settings = ET.parse(parameters.odmsettingsfile())
    root = settings.getroot()
    classif = root.find('classification_types')

    for ty in classif:
        # classname = findField(ty,'name')
        classguid = findField(ty, 'id')
        # foregcolor, backgcolor,fontcolor,fontname,fontsize,fontstyle):
        classcolors[classguid] = \
            color(findField(ty, 'fgcolor'), findField(ty, 'color'), None, None, None, None)
        loadcolors(coldict=classcolors, classkey=classguid, elem=ty)
        # print(classname,classcolors[classguid].foregcolor,classcolors[classguid].backgcolor)
    # for
    default = root.find('default_fonts_and_colors')
    for de in default:
        classname = findField(de, 'classname')
        defcolors[classname] = color(findField(de, 'foreground')
                                     , findField(de, 'background')
                                     , None, None, None, None)
        loadcolors(coldict=defcolors, classkey=classname, elem=de)
        # print(classname,defcolors[classname].fontsize)
    # for


# loaddefaultcolors

def filllanguages():
    Sprachtext.insertsprachtexte(pudpthema=parameters.odmUDPTranslFileName())
    # fill all elements in default language
    Sprachtext.filldefaulttext(dbParam.dbDefaultLangID)
    Sprache.deleteunused()


# filllanguages

def transferprojekt():
    proj = ET.parse(parameters.odmIMDirec() + parameters.odmModelName() + parameters.odmIMExtension())
    root = proj.getroot()
    comm = findText(root, 'comment')
    if comm is None:
        defspra = parameters.dbDefaultLang()
        sprachen = parameters.dbLanguages()
    else:
        defspra = re.search(r'currentLang=([A-Z]{2})', comm).group(1)
        sprachen = re.search(r'languages=([A-Z,]*)', comm).group(1)
    # print (findField(root,'name'),comm,sprachen,defspra)
    proj = Projekt()
    proj.proj_name = findField(root, 'name')
    proj.proj_uc = findText(root, 'createdBy')
    proj.proj_dc = findText(root, 'createdTime')
    proj.proj_sprachen = sprachen
    proj.proj_akt_sprache = defspra
    proj.insert()

    if defspra is not None:
        defspra = defspra.lower()
        # setze die Defaultsprache aus dem Modell
        if Sprache.spraidlookup(piso=defspra) is None:
            raise Exception("Language '{}' does not exist".format(defspra))
        Sprache.setmodellang(pmodellang=defspra)
        Sprache.setallreplacementlang()
        dbParam.liesdefaultlang()
        parameters.dbDefaultLang(defspra)
    # fi
# transferprojekt

def do1Document(fileName):
    global docuparents
    tree = ET.parse(fileName)
    root = tree.getroot()
    id =findField(root, 'id')
    docu = Document(psrcname=Externalref.SOURCE_ODM,psrcid=id)
    docu.docu_name = findField(root, "name")
    type= findText(root, 'type')
    if type is not None and type != '':
        docu.docu_stfo_id = Storageformat.getorcreate(pname=type).stfo_id
    docu.docu_reference = findText(root, 'reference')
    pd = findText(root, 'parentDocument')
    if (pd is not None and pd != ''):
        docuparents [id]= findText(root, 'parentDocument')
    docu.insert()

docuparents ={}
def transferDocuments():
    global docuparents
    docuparents = {}
    dosegfiles(pdirec=parameters.odmdocumentdirec(), transferfiles=do1Document)
    Document.updparents(psrcname=Externalref.SOURCE_ODM,pparents=docuparents)


def removeemptyudp():
    Userdefpropvalue.removeemptyUDP(('.'))


# transferDocuments
def transferODMModel():
    """überträgt das ganze ODM Modell in die DB"""
    transferprojekt()
    dbParam.liesdefaultlang()
    transferTypes()
    transferDocuments()
    transferDomains()
    return
    transferUDP()
    transferEntitaeten()
    transferRelations()
    transferArcs()
    doSubentities()
    transferKeys()
    loaddefaultcolors()
    transferdiagramme()
    filllanguages()
    transferRelational.transfer()
    removeemptyudp()
    Schnittstelleattr.fillextid()
# end transferODMModel
