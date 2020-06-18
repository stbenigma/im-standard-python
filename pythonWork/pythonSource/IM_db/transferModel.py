
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

GUIDPATTERN:str = '[A-Z0-9-]{20,45}'

class color:
    def __init__(self, foregcolor, backgcolor,fontcolor,fontname,fontsize,fontstyle):
        self.backgcolor = backgcolor
        self.foregcolor = foregcolor
        self.fontcolor = fontcolor
        self.fontname = fontname
        self.fontsize = fontsize
        self.fontstyle = fontstyle
    #end __init__
#color

#entry of keys found in entites
# [Schluessel, (listof attr and relationship guids)]
schluessel = []
# Classification type colors
# classguid : color
classcolors = dict()
# default colors
# elementtypename : color
defcolors = dict()


def findText(set,name):
    try:
        return set.find(name).text
    except:
        return None
#findText

def findField(set,name):
    try:
        return set.get(name)
    except:
        return None
#findField


def transferTypes():
    types = ET.parse(parameters.odmIMDirec() + parameters.odmKonfDirec() + parameters.odmTypesFile())
    root = types.getroot()
    for typ in root.findall('logicaltype'):
        Datatype(pname=findField(typ,'name')
                 ,pgrundtyp=Datatype.basisType(findText(typ,'mapping'))
                 ,podmguid = findField(typ,'objectid')).insert()
    #endfor
#transferTypes


def do1structtype(filename):
    structdomains = ET.parse(filename)
    structdom = structdomains.getroot()
    if (findField(structdom,"class") != "oracle.dbtools.crest.model.design.datatypes.StructuredType"): return
    #print (findField(structdom,"name"))
    wrtb = Wertebereich()
    wrtb.wrtb_name = findField(structdom,"name")
    wrtb.wrtb_odm_guid = findField(structdom,"id")
    wrtb.wrtb_uc = findText(structdom,"createdBy")
    wrtb.wrtb_dc = findText(structdom,"createdTime")
    wrtb.wrtb_typ = 'GRP'
    wrtb.wrtb_herkunft = Wertebereich.DOMAIN
    wrtb.insert()

    elements = structdom.findall("attributes/Attribute")
    for el in elements:
        #print (wrtb.wrtb_name,findField(el,"name"),findText(el,'type'))
        wbgr = Wertebereichgruppe()
        wbgr.wbgr_type_ref = findText(el,'type')
        wbgr.wbgr_wrtb_id_gruppe = wrtb.wrtb_id
        wbgr.wbgr_name = findField(el,"name")
        wbgr.wbgr_beschr = findText(el,"comment")
        wbgr.wbgr_uc = findText(el,"createdBy")
        wbgr.wbgr_dc = findText(el,"createdTime")
        elwrtbid = Wertebereich().getbyguid(wbgr.wbgr_type_ref).wrtb_id
        if elwrtbid is None:
            #nimm vorläufig unknown, da mein Typ evtl. noch nicht da ist.
            elwrtbid = Wertebereich().getunknown().wrtb_id
        #fi
        wbgr.wbgr_wrtb_id_member = elwrtbid
        wbgr.insert()
    #for
#do1structtype

def liesunsfuellwrtb(pwrtb, pxml):
    pwrtb.wrtb_uc = findText(pxml,'createdBy')
    pwrtb.wrtb_dc = findText(pxml,'createdTime')
    pwrtb.wrtb_datatype_odm = findText(pxml, 'logicalDatatype')
    daty = Datatype().getbyguid(pwrtb.wrtb_datatype_odm)
    pwrtb.wrtb_daty_id = daty.daty_id
    pwrtb.wrtb_typ = daty.daty_grundtyp if daty.daty_grundtyp is not None else 'TEXT'

    #print (pwrtb.wrtb_datatype_ref,pwrtb.wrtb_typ )

    lov = pxml.find('listOfValues')
    if (lov is not None) and (lov != {}):
        pwrtb.wrtb_typ = 'LOV'
        lovs = dict()
        for lovval in lov:
            #                print (findField(lovval,'value'),findField(lovval,'description'),lovval.attrib)
            lovs.update({findField(lovval,'value'): findField(lovval,'description')})
        # endfor
        # print (len(lovs))
    # endif
    ranges = pxml.findall('listOfRanges/rangeDef')
    if not (ranges == []):
        range=(findText(ranges[0],'beginValue'),findText(ranges[0],'endValue'))
    else:
        range = (None,None)
    #endif
 
    #noch nicht übernommenm< defaultValue > a @ b.ch < / defaultValue >
 
    if (pwrtb.wrtb_typ =='BIN'):
        pwrtb.wrtb_bin_inhalttyp = 'BILD' # 'FILM','GRAPH','TEXT','TON'
        wrtb_bin_spfo_id = None
    elif (pwrtb.wrtb_typ == 'LOV'):
        zahl=re.search('\A\d* ',nvl(findText(pxml,'dataTypeSize')))
        pwrtb.wrtb_text_maxlng = zahl.group() if not (zahl is None) else None
    elif (pwrtb.wrtb_typ =='TEXT'):
 #            print(re.search('\A\d* ','123 ab').group())
        zahl=re.search('\A\d* ',nvl(findText(pxml,'dataTypeSize')))
        pwrtb.wrtb_text_maxlng = zahl.group() if not (zahl is None) else None
        constr =pxml.find('checkConstraint')
        if not (constr is None):
            #print(constr.findall('*'))
            impl = constr.find('implementationDef')
            if not (impl is None):
              pwrtb.wrtb_text_syntaxregel = findField(impl,'definition')
    elif (pwrtb.wrtb_typ =='ZPKT'):
        pwrtb.wrtb_zpkt_minwert = range[0]
        pwrtb.wrtb_zpkt_maxwert = range[1]
        pwrtb.wrtb_zpkt_granularitaet = 'MINUTE'
    elif (pwrtb.wrtb_typ =='NUM'):
        pwrtb.wrtb_num_minwert = range[0]
        pwrtb.wrtb_num_maxwert = range[1]
        prec = findText(pxml,'dataTypePrecision')
        scale = findText(pxml,'dataTypeScale')
        pwrtb.wrtb_num_nachkstellen = 0 if scale is None else int(scale)
        pwrtb.wrtb_num_vorkstellen = 0 if prec is None else int(prec) - pwrtb.wrtb_num_nachkstellen
        pwrtb.wrtb_num_rundng_einh = None
        pwrtb.wrtb_num_pheh =  findText(pxml,'unitOfMeasure')
    #fi
    try:
        pwrtb.insert()
    except Exception as e:
        print (pwrtb.wrtb_name)
        print (str(e))

    if (lov is not None) & (lov != {}):
        for idx, key in enumerate(lovs.keys(), start=1):
            vgwt = Vorgabewert()
            vgwt.vgwt_wert = key
            vgwt.vgwt_wrtb_id = pwrtb.wrtb_id
            vgwt.vgwt_sortrhfg = idx
            vgwt.vgwt_uc = pwrtb.wrtb_uc
            vgwt.vgwt_dc = pwrtb.wrtb_dc
            vgwt.vgwt_anzeige = lovs[key]
            vgwt.insert()
        # for
    # fi
#liesundfuellwrtb

def transferDomains():
    #lösche die Domains
    #print(parameters.odmDomainsFilePath())
    domains = ET.parse(parameters.odmDomainsFilePath())
    root = domains.getroot()
    for dom in root.findall('domains/Domain'):
        wrtb = Wertebereich()
        wrtb.wrtb_name = findField(dom, "name")
        wrtb.wrtb_odm_guid = findField(dom, "id")
        wrtb.wrtb_beschr = findText(dom,'comment')
        wrtb.wrtb_herkunft = Wertebereich.DOMAIN
        liesunsfuellwrtb(pwrtb=wrtb, pxml=dom)
        lmodeId = Modellelement.insertmode(pwrtbid=wrtb.wrtb_id)
    #for
    
    dosegfiles(pdirec=parameters.odmstructypesdir(),transferfiles=do1structtype)

    """update group domains a their types may now be available"""
    Wertebereichgruppe.updmembers()

#end transferDomains

def hex2int(phex):
    return  None if (phex is None)  else int(phex,16)
def int2hex(pint):
    if (pint is None): return pint
    lint = pint if (type(pint) == int) else int(pint)
    lint = lint + (hex2int('FFFFFF') if (lint < 0) else 0)
    if lint == -1: #-1 wird führt zu -0x1 was die Selektion später erschwert
        lint = hex2int('FFFFFF')
    retval = '000000'+ hex(lint)[2:]
    retval = retval[len(retval)-6:]
    return retval

def toString(str,upper = False):
    if str is None:
        return "''"
    else:
        return(str.upper())
    #fi
#toString

def transferentity(penti, pdiagid, puc, pdc):
    entiodm = findField(penti,'oid')
    enti = Entitaet().getbyguid(entiodm)
    hiddenelements = penti.find ("hiddenElements")
    if hiddenelements is not None:
        elemtext=findField(hiddenelements,"elements")
    else: elemtext = ""
    hiddenattrs=elemtext.split(' ')
    hiddenattrs2 = []
    for e in hiddenattrs:
        if e != "": hiddenattrs2.append(Attribut().getID(pguid=e))
    attrs = Attribut.select(pwhere="attr_enti_id = {}".format(enti.enti_id),porderby="attr_anz_rhflg")
    attrids = [a.attr_id for a in attrs]
    attrids = list(set(attrids) - set(hiddenattrs2))
    #print (attrids,hiddenattrs2)

    layout= penti.find('bounds')
    col = defcolors['Entity'] #defaults können mal geladen werden
    if (findText(penti, 'useDefaultColor') == 'false'):

        col.backgcolor = findText(penti, 'backgroundColor')
        col.foregcolor = findText(penti, 'foregroundColor')
        #print (backgroundc,foregroundc)
        font = penti.find('fonts/FontObject[foType ="Title"]')
        #deutsche ODMnutzuer schreiben Titel in die Kongig....
        if font is None: font = penti.find('fonts/FontObject[foType ="Titel"]')
        #fontname,fontsize,fontstyle):
        v = findText(font,'colorRGB')
        col.fontcolor = v if v is not None else col.fontcolor
        v = findText(font, 'fontStyle')
        col.fontstyle = v if v is not None else col.fontstyle
        v = findText(font, 'fontSize')
        col.fontsize = v if v is not None else col.fontsize
    else:
        #check wether entity belongs to category
        if (enti.enti_category_guid is None):
            col = defcolors['Entity']
        else:
            try:
                col = classcolors[enti.enti_category_guid]
            except Exception as e:
                #print(e) flls class nicht mehr exisitert
                col = defcolors['Entity']
        #fi
    #fi
    #print (col.foregcolor,col.backgcolor)
    #eled_position_x,eled_position_y,eled_breite,eled_hoehe
    #,eled_deckkraft,eled_farbe,eled_randbreite,eled_randdeckkraft
    #,eled_randfarbe, eled_schriftgroesse, eled_schriftfarbe, eled_mode_id
    #,eled_diag_id, eled_uc, eled_dc, eled_um
    #, eled_dm

    index = 0
    entix=int(findField(layout,'x'))
    entiy=int(findField(layout,'y'))
    entiwidth=int (findField(layout,'width'))
    entiheight=int(findField(layout,'height'))
    #if there are several copies on a diagramm, repeat the insert with new index und insert succeeds
    while True:
        row = (entix, entiy, entiwidth, entiheight
              , 100, int2hex(col.backgcolor), None, 100
              , int2hex(col.foregcolor),col.fontsize, int2hex(col.fontcolor), Modellelement.getidbyelemid(pentiid=enti.enti_id)
             , pdiagid, index,puc, pdc
            , None, None)
        #print (row)
        try:
            dbInserts.insertelementdarst(pdata=row)
            attrx = int(entix) + 26 #x1,x2=16,26 y=30
            attry = int(entiy) + 30
            attrwidth = int(entiwidth) - 36
            attrheight = 13
            for aid in attrids:
                attrrow=(attrx,attry,attrwidth,attrheight
                         ,100,int2hex(col.backgcolor),int2hex(col.fontcolor),100
                         ,None,None,None,Modellelement.getidbyelemid(pattrid=aid)
                         ,pdiagid,0,puc,pdc
                         ,None,None)
                try:
                    dbInserts.insertelementdarst(pdata=attrrow)
                except Exception as e: print(e)
                attry += attrheight
                # Maximal bis zur Grösse der Entität
                if ((attry-entiy) > (entiheight - 10)): break
            #for
            break # no more looping for copies of element on diagramm
        except sqlite3.IntegrityError:
            index +=1
        except Exception as ex:
            print(str(ex))
            print(row)
            raise ex
    #while
#transferentity

def transferdiaobj(pobjects, pdiagid, puc, pdc):
    for o in pobjects:
        type = findField(o,'otype')
        if (type == 'Image'):
            pass
        elif (type == 'Entity'):
            transferentity(penti=o, pdiagid=pdiagid, puc=puc, pdc=pdc)
        elif (type == 'Note'):
            pass
        #fi
#transferdiaobj

def linetype(pidx,pmaxidx,psourcelt,ptargetlt):
    if (pidx < ((pmaxidx-1) / 2)):
        return psourcelt
    else:
        return ptargetlt
    #fi
#linetype

def connector(pidx,pmaxidx,psource,ptarget):
    #ist kein Segment sondern in Punkt. es macht nur 1 oder M Sinn
    if (pidx == 0): return psource
    if (pidx == (pmaxidx-1)): return ptarget
    return None
#conmector
def transferdiaconnect(pconnectors, pdiagid, puc, pdc):
    for c in pconnectors:
        type = findField(c,'otype')
        if (type == 'Relation'):
            relaguid=findField(c,"oid")
            beziid = dbLookup.beziId(relaguid)
            linewidth=findText(c,'lineWidth')
            sourcelabel=c.find('sourceLabel/labelBounds')
            sttex=findField(sourcelabel,'x')
            sttey=findField(sourcelabel,'y')
            sttew=findField(sourcelabel,'width')
            stteh=findField(sourcelabel,'height')
            targetlabel=c.find('targetLabel/labelBounds')
            entex=findField(targetlabel,'x')
            entey=findField(targetlabel,'y')
            entew=findField(targetlabel,'width')
            enteh=findField(targetlabel,'height')

            """Labels können negative Starts haben, verschiebe sie in den positiven Bereich"""
            if sttey is not None and int(sttey) < 0 : sttey,entey = 0,int(entey) - int(sttey)
            if sttey is not None and int(sttey) < 0 : sttey,entey = 0,int(entey) - int(sttey)

            bezi = dbDML.select("""select bezi_pflicht_assoc_von_zu,bezi_pflicht_assoc_zu_von
                                        ,bezi_type
                                         ,case bezi_source_enti_guid 
                                         when source.enti_odm_guid then 'FALSE' 
                                            else 'TRUE' end switch
                                    from beziehungen
                                    join entitaeten source on source.enti_id = bezi_enti_id_von
                                    where bezi_id ={}
                    """.format(beziid))
            bezitype=bezi[0][2]
            sourcelinetype='SOLID' if (bezi[0][0]=='TRUE') else 'DASHED'
            targetlinetype='SOLID' if (bezi[0][1]=='TRUE') else 'DASHED'
            sourcecard= '1' if (bezitype in ('ISA','1:1')) else 'M'
            targetcard='1' if (bezitype in ('ISA','1:1','M:1')) else 'M'
            if (bezi[0][3]=='TRUE'): #switch source and target
                sourcecard,targetcard = targetcard,sourcecard
                sourcelinetype,targetlinetype = targetlinetype,sourcelinetype
                sttex,entex=entex,sttex
                sttey,entey=entey,sttey
                sttew,entew=entew,sttew
                stteh,enteh=enteh,stteh
            #fi

            """
    beda_diag_id, beda_mode_id, beda_linienbreite, beda_liniefarbe
    ,beda_liniedeckkraft, beda_starttext_x, beda_starttext_y, beda_starttext_breite
    ,beda_starttext_hoehe, beda_endtext_x, beda_endtext_y, beda_endtext_breite
    ,beda_endtext_hoehe, beda_schriftfarbe, beda_schriftgroesse, beda_uc
    ,beda_dc, beda_um, beda_dm)
"""
            row=(pdiagid, Modellelement.getidbyelemid(pbeziid=beziid), linewidth, None
                 , 1, sttex, sttey, sttew
                 , stteh, entex, entey, entew
                 , enteh, None, 10, puc, pdc, None, None
                 )
            bedaid=dbInserts.insertelbezidarst(row)

            points=c.findall('points/point')
            points=[{'x':int(findField(p,'x')),'y':int(findField(p,'y'))} for p in points]
            if len(points)==2:
                """1elementige Linien werden um einen Mittelpunkt ergänzt wegen -- oder solid"""
                midpos = lambda x1,x2: round((x1-x2)/2+x2)
                points.insert(1,{'x':midpos(points[0]['x'],points[1]['x']),'y':midpos(points[0]['y'],points[1]['y'])})
            #fi
            pointsegs=[]
            for idx,point in enumerate(points):
                """ lise_rhfg, lise_beda_id, lise_x, lise_y
    , lise_linientyp,lise_konnektor, lise_uc, lise_dc
    , lise_um,lise_dm,nkel
    """
                x,y=point['x'],point['y']
                if len(pointsegs)> 0:
                    """ ab dem 2. Punkt wird im vorherigen Punkte der Winkel zum nächsten hinzugefügt"""
                    calcwinkel = lambda ey, sy, ex, sx: math.atan2(ey - sy, ex - sx)
                    prevpoint = pointsegs[len(pointsegs)-1]
                    prevpoint[10] = calcwinkel(y,prevpoint[3],x,prevpoint[2])
                pointsegs.append([idx,bedaid,x,y
                                ,linetype(pidx=idx, pmaxidx=len(points)
                                          ,psourcelt= sourcelinetype,ptargetlt=targetlinetype)
                                ,connector(pidx=idx,pmaxidx=len(points)
                                           ,psource=sourcecard,ptarget=targetcard)
                                ,puc,pdc,None,None,None])
            #for
            dbInserts.insertlinieseg(pointsegs)
        else: pass
        #fi
#transferdiaconnect

# transferdiaconnect

def transferdiaarc(parcs, pdiagid, puc, pdc):
    pass
# transferdiaarc

#def doGUIDfile(pdirec,pfile,transferfiles):
#    #nur GUID als Namen erlaubt.
##    if re.match(r'{}.xml'.format(GUIDPATTERN),pfile):
#        fileName = pdirec + pfile
#        transferfiles(fileName)
#    #fi
##doGUIDfile

def doxmlfiles (pdirec,ptransfer,ppattern=r".*"):
    try:
        listdir=os.listdir(pdirec)
    except:
        print('doXMLfiles: directory "{}" not found.'.format(pdirec))
        return
    #try
    for file in listdir:
        if re.match(ppattern, file):
            ptransfer(pdirec + file)
        #fi
    #for
#doxmlfiles

def dosegfiles(pdirec,transferfiles):
    try:
        listdir=os.listdir(pdirec)
    except:
        print('dosSEGfiles: directory "{}" not found.'.format(pdirec))
        return
    #try
    for el in listdir:
        if re.match('seg_.*', el):
            doxmlfiles(pdirec=pdirec + el + '/'
                       ,ptransfer=transferfiles
                       ,ppattern=r'{}.xml'.format(GUIDPATTERN))
#            for file in os.listdir(pdirec + el):
#                doGUIDfile(pdirec=pdirec + el + '/',pfile=file,transferfiles=transferfiles)
#            #for
        #fi
    #for
#dosegfiles

def do1diagramm(pfilename):
    #print (p_filename)
    try:
        diagramme = ET.parse(pfilename)
    except:
        print("Diagramm nicht lesbar: {}".format(pfilename))
        return
    dia = diagramme.getroot()
    diag = Diagramm()
    diag.diag_name = findField(dia,'name')
    if (diag.diag_name == 'Logical'):
        return
    #entcomm = findText(root,'comment')
    #creby = findText(root,'createdBy')
    #creti = findText(root,'createdTime')
    """'
                    ,'diag_odm_guid', 
                    """
    diag.diag_diat_id = Diagrammtyp.getbyname(pname='Entity').diat_id
    #print(findField(dia,'name'), findField(dia,'id'))
    #diag_name,diag_diat_id,diag_uc,diag_dc,diag_um,diag_dm

    if (findText(dia,'showLegend') == 'true'):
        legende =dia.find("objectViews/OView[@otype='Legend']")
        bounds=legende.find("bounds")
        diag.diag_legendx = findField(bounds,'x')
        diag.diag_legendy = findField(bounds,'y')
    else:
        diag.diag_legendx = None
        diag.diag_legendy = None
    #fi
    diag.diag_uc = findText(dia,'createdBy')
    diag.diag_dc = findText(dia,'createdTime')
    diag.diag_odm_guid = findField(dia,'id')
    diag.diag_um = findText(dia,'modifiedBy')
    #print (row)
    diag.insert()
    objects = dia.findall('objectViews/OView')
    if (len(objects) > 0):
        transferdiaobj(pobjects=objects, pdiagid=diag.diag_id, puc=diag.diag_uc, pdc=diag.diag_dc)
    connectors = dia.findall('connectors/Connector')
    if (len(connectors) > 0):
        transferdiaconnect(pconnectors=connectors, pdiagid=diag.diag_id, puc=diag.diag_uc, pdc=diag.diag_dc)
    arcs = dia.findall('arcs/Arc')
    if (len(arcs) > 0):
        transferdiaarc(parcs=arcs, pdiagid=diag.diag_id, puc=diag.diag_uc, pdc=diag.diag_dc)
    #print (dianame,len(objects),len(connectors),len(arcs))
#do1diagramm

def transferdiagramme():
    doxmlfiles(pdirec=parameters.odmentisubviewdirec()
               ,ptransfer=do1diagramm
               ,ppattern=r'{}.xml'.format(GUIDPATTERN))
#    for el in os.listdir(parameters.odmentisubviewdirec()):
#        #filename = parameters.odmentisubviewdirec() +  el
#        #do1diagramm(p_filename=filename)
#        doGUIDfile(pdirec = parameters.odmentisubviewdirec()
#                   , pfile = el
#                   , transferfiles = do1diagramm)
#    #endfor
#transferdiagramme

def insertderiveddomain(ptypeguid, pattrname, pvatername, pattrxml):
    wrtb = Wertebereich()
    wrtb.wrtb_name = pattrname
    if (Wertebereich.getbyname(pname=pattrname).wrtb_name == pattrname):
        #es gibt ihn schon, füge den Vaternamen dazu
        wrtb.wrtb_name = pattrname + '-' + pvatername
    wrtb.wrtb_herkunft = Wertebereich.DERIVED
    wrtb.wrtb_datatype_ref = ptypeguid
    wrtb.wrtb_beschr = "generiertes Domain für Datentyp für Attribut {}.{}".format(pvatername,pattrname)

    liesunsfuellwrtb(pwrtb=wrtb, pxml=pattrxml)
    return wrtb
#insertderiveddomain


def findeOderErstelleDom(pdomguid, pstructdomguid, ptypeguid, pattrname,pvatername,pattrxml):
    dom = None
    if pdomguid is not None:
        dom = Wertebereich().getbyguid(pdomguid)
    elif pstructdomguid is not None:
        dom = Wertebereich().getbyguid(pstructdomguid)
    elif ptypeguid is not None:
        dom = insertderiveddomain(ptypeguid=ptypeguid,pattrname=pattrname,pvatername=pvatername,pattrxml=pattrxml)
    #
    if dom is None:
        dom = Wertebereich().getbyname('Unknown')
    return dom.wrtb_id
#findeOderErstelleDom

def do1Arc(fileName):
    arc= ET.parse(fileName).getroot()
    if (findField(arc, "class") != "oracle.dbtools.crest.model.design.logical.Arc"): return

    #(arcs_name, arcs_enti_id, arcs_odm_guid
    # , arcs_uc, arcs_dc)
    arcs_id = dbInserts.insertArc(parc=(findField(arc,"name"),Entitaet().getID(findText(arc,'entity'))\
                              ,findField(arc,"id"),findText(arc,'createdBy'),findText(arc,'createdTime')))
    """map all relations to this arc"""
    relations = arc.findall('relations/relationID')
    relids = ''
    for idx,r in enumerate(relations):
        sep = ',' if idx > 0 else ''
        relids += sep+"'"+r.text+"'"
#    relids = ''.join("'{}',".format(r for r in relations))
    #print (relids)
    #DEBUG Arc 2x auf Beziehung
    if findField(arc,"name") in ('xxArc_9','xxArc_11'):
        print (findField(arc,"id"),findField(arc,"name"),findText(arc,'entity'))
        res = dbDML.select("""select case earc.enti_odm_guid
                            when evon.enti_odm_guid
                            then arcs_id else null end von_arcs_id
                            ,case earc.enti_odm_guid
                            when ezu.enti_odm_guid
                            then arcs_id else null end zu_arcs_id
                 ,arcs_id,arcs_name,bezi_id,bezi_name,earc.enti_name,earc.enti_odm_guid,ezu.enti_odm_guid
                    from arcs
                    cross join beziehungen
                    join entitaeten earc on arcs_enti_id = earc.enti_id
                    left join entitaeten evon on bezi_enti_id_von = evon.enti_id
                    left join entitaeten ezu on bezi_enti_id_zu = ezu.enti_id
                    where arcs_id = {}
                and bezi_odm_guid in ({})""".format(arcs_id,relids))
        print (res)
    dbDML.exec("""update beziehungen
                set (bezi_von_arcs_id,bezi_zu_arcs_id) =
                    (select case earc.enti_odm_guid
                            when evon.enti_odm_guid
                            then arcs_id else bezi_von_arcs_id end von_arcs_id
                            ,case earc.enti_odm_guid
                            when ezu.enti_odm_guid
                            then arcs_id else bezi_zu_arcs_id end zu_arcs_id
                    from arcs
                    join entitaeten earc on arcs_enti_id = earc.enti_id
                    left join entitaeten evon on bezi_enti_id_von = evon.enti_id
                    left join entitaeten ezu on bezi_enti_id_zu = ezu.enti_id
                    where arcs_id = {}
                    )
                where bezi_odm_guid in ({})
                """.format(arcs_id,relids))
        #print(findField(arc,"name"),rel.text)

#do1Arc

def transferArcs():
    dosegfiles(pdirec=parameters.odmArcDirec(),transferfiles=do1Arc)
#transferArcs

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
                bdegId = dbLookup.bdegLookup(findField(prop,'name'))
                # print('      ', findField(prop,'name'), findField(prop,'value'), bdegId)
                udps.append((findField(prop,'value'), pmodeid, bdegId))
            except:
                """dynamische Properties lassen wir aus"""
                pass
        #for
    #fi
    # look for comments in the notesfield of the element
    note = findText(pobj, 'notes')
    if (note is not None):
        prop = re.finditer(r'\[(([A-Z]{2})[^[]+)\[\n([^]]*)\][A-Z]{2}[^]]+\]', note, re.DOTALL)
        # liefert group1 name,group2 sprache, group3 text
        for i, p in enumerate(prop):
            #print (i,p.group(0),'\n1:',p.group(1),'\n2:',p.group(2),'\n3:',p.group(3))
            bdegId = dbLookup.bdegLookup(p.group(1))
            # print('      ', findField(prop,'name'), findField(prop,'value'), bdegId)
            udps.append((p.group(3).rstrip(), pmodeid, bdegId))
        #for
    # fi

    if len(udps) > 0:
        #print (udps)
        dbDML.execmany(psql="""update benudef_wert
                            set bdwe_wert = ?
                            where bdwe_mode_id = ?
                            and bdwe_bdeg_id = ?
                        """, recs=udps)
    # fi
#updateUDP

def do1Attribute(plfnr, pattrxml, pentiId=None, pbeziId=None):
    #wegen FK-PK zusätzliche Attribute werden nicht übernommen
    if (findText(pattrxml, 'referedAttribute') is not None):
        return
    if pentiId is not None:
        vatername = Entitaet().getbyid(pid=pentiId).enti_name
    elif pbeziId is not None:
        vatername = "Beziehung ({})".format(pbeziId)

    xmlname = findField(pattrxml, 'name')
    #strip [] am Ende des Namens
    attr = Attribut(pname=re.sub(' ?\[[LNT]+\]','',xmlname),pentiid=pentiId,pbeziid=pbeziId)
    attr.attr_tech_name = findText(pattrxml, 'preferredAbbreviation')
    if attr.attr_tech_name is None:
        attr.attr_tech_name = re.sub('[-,.()\[\]äöüèéàÄ~ÖÜ ]','_',str.upper(attr.attr_anzname))
    attr.attr_uc = findText(pattrxml, 'createdBy')
    attr.attr_dc = findText(pattrxml, 'createdTime')
    attr.attr_wrtb_id = findeOderErstelleDom(pdomguid=findText(pattrxml, 'domain')
                               , pstructdomguid=findText(pattrxml, 'structuredType')
                               , ptypeguid=findText(pattrxml, 'logicalDatatype')
                               , pattrname=attr.attr_anzname
                               ,pvatername=vatername
                               ,pattrxml=pattrxml)
    attr.attr_beschr = findText(pattrxml, 'comment')
    attr.attr_anz_rhflg = plfnr
    attr.attr_deskriptor = 'FALSE'
    attr.attr_pflichtattr = 'FALSE' if (findText(pattrxml, 'nullsAllowed') == 'true') else 'TRUE'
    attr.attr_historisiert = 'TRUE' if (re.search('\[.*T.*\]', xmlname) is not None) else 'FALSE'
    attr.attr_wiederholt = 'TRUE' if (re.search('\[.*N.*\]', xmlname) is not None) else 'FALSE'
    attr.attr_sprachabhaengig = 'TRUE' if (re.search('\[.*L.*\]', xmlname) is not None) else 'FALSE'
    attr.attr_verschluesselt = 'FALSE'
    attr.attr_odm_guid = findField(pattrxml, 'id')
    try:
        attrId = attr.insert()
    except  sqlite3.Error as e:
        print(str(e))
        print('Entity = {}'.format(vatername))
        print(attr.attr_anzname)
        raise e
    #try
    lmodeId= Modellelement.insertmode(pattrid=attrId)
    dbInserts.insertUdpAttr(attrId)
    updateUDP(pmodeid=lmodeId, pobj=pattrxml)

    documents = getdokuref(pelem= pattrxml)
    ModelelemDoku.insertdokuref(pdocguidlist=documents, pmodeid=lmodeId)
#do1Attribute

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
                #print(idx, findField(enti,'name'), findField(key,'id'), findField(enti,'id'), keyrefs)
                schl = Schluessel()
                schl.schl_laufnr = idx
                schl.schl_name = findField(key,'name')
                schl.schl_odm_guid = findField(key,'id')
                schl.schl_uc = findText(key, 'createdBy')
                schl.schl_dc = findText(key, 'createdTime')
                schl.schl_enti_id = p_entiid
                schl.insert()

                schluessel.append([schl, keyrefs])
            #fi
        # rof
        # [Schluessel, (listof attr and relationship guids)]
    # fi
#fillKeys

def transferKeys():
    global schluessel
    # Schlüssel sind eingefügt es folgen die SchlüsselElemente, die ich jetzt alle haben sollte
    #schlüssel [[Schluessel, (Liste der Referenzen)]]
    for schlentry in schluessel:
        schl = schlentry[0]
        reflist = schlentry[1]
        #nun die Schlüsselelemente
        for ke in reflist:
            scel = Schluesselelement()
            scel.scel_schl_id = schl.schl_id
            scel.scel_uc = schl.schl_uc
            scel.scel_dc = schl.schl_dc
            try:
                scel.scel_attr_id = Attribut().getID(ke)
                scel.scel_bezi_id = None
            except:
                try:
                    scel.scel_bezi_id = dbLookup.beziId(ke)
                    scel.scel_attr_id = None
                except sqlite3.Error as e:
                    print (str(e))
                    print (ke, scel)
                    raise e
                #try
            #yrt
            scel.insert()
        #rof
    #rof
# transferKeys
def getdokuref(pelem,pstruct=False) :
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
                docguid=findField(doc,'id')
                #print(docguid)
                documents.append(docguid)
            #for
            documents = tuple(documents)
        #fi
    else:
        """<documents usedDucuments="701E5525-A8EE-3C6F-E78B-28B04D93F93D"/>
        """
        docs = findField(pelem.find("documents"), 'usedDucuments')
        if (docs is not None):
            documents = tuple(docs.split(' '))
    #fi
    #print(documents)
    return documents
#getdokuref

def do1Entity(fileName):
    tree = ET.parse(fileName)
    entixml = tree.getroot()
    if (findField(entixml,"class") != "oracle.dbtools.crest.model.design.logical.Entity"): return
    entname = findField(entixml,"name")
    entcomm = findText(entixml,'comment')
    creby = findText(entixml,'createdBy')
    creti = findText(entixml,'createdTime')
    enti_category_guid = findText(entixml,'typeID')
    documents = getdokuref(pelem= entixml)
    enti = Entitaet()
    enti.enti_odm_guid = findField(entixml,'id')
    enti.enti_name = entname
    enti.enti_beschr = entcomm
    enti.enti_uc = creby
    enti.enti_dc = creti
    enti.enti_enti_guid = findText(entixml,'hierarchicalParent')
    enti.enti_category_guid = enti_category_guid
    entiId = enti.insert()
    lmodeId = Modellelement.insertmode(pentiid=entiId)
    dbInserts.insertUdpEntity(entiId)

    sobj =findText(entixml,'synonym')
    if (sobj is not None):
        for syn in sobj.split(','):
            synoname = syn.strip()
            synid = Synonym(pname=synoname,pentiid=entiId).insert()
            Modellelement.insertmode(psynoid=synid)
        #for
    #fi

    #print (entname,translate.translate(p_text=entname,p_fromlang='de',p_tolang='en'),translate.translate(p_text=entname,p_fromlang='de',p_tolang='fr'))

    updateUDP(pmodeid=lmodeId, pobj=entixml)
    ModelelemDoku.insertdokuref(pdocguidlist=documents, pmodeid=lmodeId)

    attrs= entixml.find('attributes')
    if attrs is not None:
        for idx,attr in enumerate(attrs,start=1):
        #alle Attribute
            #print(findField(attr,'name'),findField(attr,'id'))
            do1Attribute(plfnr=idx, pattrxml=attr, pentiId=entiId)
        #rof
    #fi
    fillKeys(p_enti=entixml, p_entiid=entiId)
#do1Entity


def transferEntitaeten():
    #lösche die Entitäten
    dosegfiles(pdirec=parameters.odmEntityDirec(),transferfiles=do1Entity)
#transferEntitaeten

def doSubentities():
    dbDML.exec("""insert into arcs (arcs_name, arcs_enti_id,arcs_uc,arcs_dc) 
                       select name || '_subtype', id,uc,um from 
                                  (select enti_name as name, enti_id as id,enti_uc as uc ,enti_dc as um
                                          ,(select count(*) from entitaeten as e1 where e2.enti_odm_guid = e1.enti_enti_guid) as subanz
                                   from entitaeten as e2
                                   ) where subanz > 0
                   """)


    #    dbDML.exec("update entitaeten as e1 set enti_enti_id = "
    #                 +"(select enti_id from entitaeten as e2 where enti_odm_guid = e1.enti_enti_guid)"
    #                       + " where enti_enti_guid is NOT NULL and enti_enti_id is NULL"
    #                )


    dbDML.exec("""insert into beziehungen (bezi_type, bezi_enti_id_von, bezi_assoc_von_zu
                    ,bezi_pflicht_assoc_von_zu, bezi_hist_von_zu
                    , bezi_enti_id_zu, bezi_assoc_zu_von, BEZI_PFLICHT_ASSOC_ZU_VON, bezi_hist_zu_von
                    , bezi_von_arcs_id,bezi_uc, bezi_dc,bezi_name)
                select 'ISA', slave_enti_id,''
                            , 'TRUE','FALSE'
                            ,master_enti_id,'','TRUE','FALSE'
                            ,arcs_id,arcs_uc, arcs_dc
                            ,arcs_name + '_' + slave_enti_name beziname
                            from arcs
                            join (select enti_id as master_enti_id
                                       , enti_odm_guid as master_guid from entitaeten) on master_enti_id = arcs_enti_id
                            join  (select enti_id as slave_enti_id
                                       , enti_enti_guid as slave_master_guid 
                                       ,enti_name as slave_enti_name from entitaeten) on slave_master_guid = master_guid
                           where arcs_odm_guid is null
                """)
    dbConnect.myDbConn.commit()
#doSubentities

def abbildTyp(ptyp):
    if (ptyp == '1'):
        return '1'
    elif (ptyp == '*'):
        return 'M'
    else:
        return None
    #fi
#abbildTyp

def strNegBool(pbool):
    if (pbool == None):
        return None
    elif (pbool.upper() == 'TRUE'):
        return 'FALSE'
    elif (pbool.upper() == 'FALSE'):
        return 'TRUE'
    else:
        return None
    #fi
#strNegBool

def beziType(srcCard, targCard, srcOpt,targOpt,arcId = None):
    # ISA: 1:1 und
    #      zuSeite Pflicht, vonSeite optional
    #           oder beide sind Pflicht und die zuSeite beziehung ist in einem Arc
    #    1:1 sonst
    #
    if ((srcCard == '1') and (targCard == '1')):
        #alte lösung        if ((srcOpt == 'false') and (targOpt == 'false') and (arcId is not None)):
        if ((srcOpt == 'false') or (targOpt == 'false') ):
            return 'ISA'
        else:
            return '1:1'
        #fi
    elif ((srcCard == 'M') and (targCard == 'M')):
        return 'M:N'
    else:
        return 'M:1'
    #fi
#beziType

def do1Relation(fileName):
    tree = ET.parse(fileName)
    relaxml = tree.getroot()
    relname=findField(relaxml,'name')
    optSrc = findText(relaxml, 'optionalSource')
    optTarg = findText(relaxml, 'optionalTarget')
    cardSrc = findText(relaxml, 'sourceCardinality')
    cardTarg = findText(relaxml, 'targetCardinalityString')
    documents = getdokuref(pelem= relaxml)

    lbeziType = beziType(srcCard= abbildTyp(cardSrc)
                    ,targCard=abbildTyp(cardTarg)
                    ,srcOpt=optSrc
                    ,targOpt= optTarg)
        # bezi_type, bezi_enti_id_von, bezi_assoc_von_zu
    #      ,bezi_pflicht_assoc_von_zu, bezi_hist_von_zu
    #     , bezi_enti_id_zu,bezi_assoc_zu_von
    #     , BEZI_PFLICHT_ASSOC_ZU_VON,bezi_hist_zu_von
    #     , bezi_odm_guid,bezi_uc, bezi_dc,bezi_name
    #     ,bezi_source_enti_guid,  bezi_target_enti_guid
    vonText = findText(relaxml,'nameOnSource')
    zuText = findText(relaxml, 'nameOnTarget')
    creby = findText(relaxml,'createdBy')
    creti = findText(relaxml,'createdTime')
    sourceentiguid = findText(relaxml,'sourceEntity')
    targetentiguid = findText(relaxml,'targetEntity')
    try:
        lrow=[lbeziType
             , Entitaet().getID(sourceentiguid),vonText
             ,strNegBool(optSrc), 'FALSE'
             , Entitaet().getID(targetentiguid), zuText
             ,strNegBool(optTarg),'FALSE'
             ,findField(relaxml,'id'),creby,creti,relname
            ,sourceentiguid,targetentiguid
             ]
            #findField(root,'name')\           ,findText(root,'comment')\
           #           ,findText(root,'transferable')           ,findText(root,'deleteRule')\
    except  sqlite3.Error as e:
        if (e.__str__() == 'No Data Found'):
            print ("Entity Id {} oder {} nicht gefunden. Datenleichen von Bezi mit gelöschten Entities".format(sourceentiguid,targetentiguid))
            return
        else:
            raise e
        # fi
    # yrt

    # isA darf nur von von nach zu gehen. d.h. von Beziehung muss NOT NULL sein.
    if ((lbeziType == 'ISA' and optSrc == 'true')
        or (lbeziType == 'ISA' and optSrc == 'false' and optTarg == 'false' )  #und der Arc ist auf der VonSeite
        or (lbeziType == 'M:1' and abbildTyp(cardSrc) == '1')
       ):
        #tausche von und zu aus
        lrow[1], lrow[5] = lrow[5], lrow[1] #Entity-Id
        lrow[2], lrow[6] = lrow[6], lrow[2] #text
        lrow[3], lrow[7] = lrow[7], lrow[3] #Optionalität
        lrow[4], lrow[8] = lrow[8], lrow[4]  # history
    #fi
    row = tuple(lrow)
    #print (row)

    try:
        beziId = dbInserts.insertBeziehung(row)
    except (sqlite3.IntegrityError):
        logging.writelog (row)
        return
    lmodeId = Modellelement.insertmode(pbeziid=beziId)
    dbInserts.insertUdpBezi(beziId)

    updateUDP(pmodeid=lmodeId, pobj=relaxml)
    ModelelemDoku.insertdokuref(pdocguidlist=documents, pmodeid=lmodeId)

    attrs= relaxml.find('attributes')
    if attrs is not None:
        for idx,attr in enumerate(attrs,start=1):
            #alle Attribute
            #print((findField(attr,'name'),findField(attr,'id')))
            do1Attribute(plfnr=idx, pattrxml=attr, pbeziId=beziId)
        #endfor
    #fi

#do1Relation

def transferRelations():
    #lösche die Beziehungen
    dosegfiles(pdirec=parameters.odmRelationDirec(),transferfiles=do1Relation)
    dbConnect.myDbConn.commit()
#transferRelations

def do1UDPFile(pudpThema,pfileName):
    tree = ET.parse(pfileName)
    root = tree.getroot()
    lupdThema = pudpThema
    lgroups = {'':'-'}
    for groups in root.findall('udp_groups'):
        for child in groups:
            #print(findField(child,'name'))
            lgroups[findField(child,'id')] = findField(child,'name')
        #for
    #for

    props = root.find('properties')
    #print (props)
    propgroups=[]
    for prop in props.findall('property'):
        group = findField(prop,'group_id')
        propname = findField(prop,'name')
        #print (findField(prop,'name'))
        #print (findField(prop,'name'),findField(prop,'dispalay_name'),lgroups[findField(prop,'group_id')],findField(prop,'default_value'),findText(prop,'description'))
        #bdeg_thema, bdeg_gruppe, bdeg_name, bdeg_default_value
        #bdeg_beschreibung, bdeg_optional, bdeg_wrtb_id,
        #bdeg_uc, bdeg_dc
        ludp = (lupdThema,lgroups[group],propname,findField(prop,'default_value')
                ,findText(prop,'description'),'FALSE',None
                ,'--',date.today().__str__())
        udpId = dbInserts.insertUDP(pData=ludp)
        if (lupdThema == parameters.odmUDPTranslFileName()):
            #die speziellen Properties manuell
            if not (group in propgroups): #nur einmal eintragen je Sprache (Gruppe)
                propgroups.append(group)
                ludpid=dbInserts.insertUDP(pData=(lupdThema, lgroups[findField(prop,'group_id')]
                    , lgroups[group]+'_ENTI_COMMENT', None
                    , None, 'FALSE', None, '--', date.today().__str__()))
                dbInserts.insertModelltypEigen((Modellelemtyp.getidbyshortname(pkurzname=Modellelemtyp.type2melt('Entity')), ludpid))
                ludpid=dbInserts.insertUDP(pData=(lupdThema, lgroups[findField(prop,'group_id')]
                    , lgroups[group]+'_ATTR_COMMENT', None
                    , None, 'FALSE', None, '--', date.today().__str__()))

                dbInserts.insertModelltypEigen((Modellelemtyp.getidbyshortname(pkurzname=Modellelemtyp.type2melt('Attribute')), ludpid))
            #fi
        #fi

        obj = prop.findall('objects/object')
        for o in obj:
            lMelt = re.split( "\.",findField(o,'class'))[6]
            #print( type2melt(lMelt))
            #print (lMelt)
            lmeltid=Modellelemtyp.type2melt(lMelt)
            if lmeltid != "":
                try:    dbInserts.insertModelltypEigen((dbLookup.meltLookup(lmeltid), udpId))
                except: pass
            #fi


        #print (ludp)
        lov = prop.find('list_of_values')
        if (lov is not None):
            wrtbId= dbInserts.insertLovWrtb(pName=lupdThema + '_' +propname)

            # end insertLovWrtb

            items = lov.findall('item')
            for val in items:
                #print (findField(val,'value'),findField(val,'default'))
                vgwt = Vorgabewert()
                vgwt.vgwt_wert = findField(val,'value')
                vgwt.vgwt_wrtb_id = wrtbId
                vgwt.vgwt_anzeige = findField(val,'value')
                vgwt.vgwt_uc = 'system'
                vgwt.vgwt_dc = date.today().__str__()
                try:
                    vgwt.insert()
                except (sqlite3.IntegrityError):
                    logging.writelog("duplicate entry in Vorgabewerte theme:'{}' property:'{}' value:'{}'"
                                     .format(pudpThema,propname,vgwt.vgwt_wert))

            #for
            dbDML.exec("""update benudef_eigenschaft  set bdeg_wrtb_id = {}  where bdeg_Id = {} """
                        .format (wrtbId,udpId))

        # fi
    # for
#do1UDPFile

def dofiles(pdirec,pfileregexp,ptransferfunc):
    for file in os.listdir(parameters.odmFilesDirec()):
        filename, file_extension = os.path.splitext(file)
        if (pfileregexp.filename):
            filepath = parameters.odmIMDirec() + file
            #print (filepath)
            ptransferfunc(filepath)
        #fi
    # endfor
#dofiles

def transferUPDdef():
    # lösche die UDP
#    l_sql = """select count(*) from benudef_wert union select count(*) from benudef_eigenschaft"""
#    result = dbDML.select(l_sql)
#    for row in result:
#        print(row)
    for file in os.listdir(parameters.odmFilesDirec()):
        filename, file_extension = os.path.splitext(file)
        #print(filename, file_extension)
        if (file_extension =='.udposdm'):
            filepath = parameters.odmFilesDirec() + file
            #print (filepath)
            do1UDPFile(pudpThema=filename,pfileName=filepath)
        #fi
    # endfor

    dbConnect.myDbConn.commit()
#transferUDPdef

def transferUDP():
    transferUPDdef()
#transferUDP

def insertBaseData():
    languages = {'de' : ['Deutsch','deu']
                ,'en': ['English', 'eng']
                ,'fr': ['Français', 'fra']
                ,'es': ['Español', 'esp']
                ,'it': ['Italiano', 'ita']
                }
    #(spra_iso_name, spra_iso_code2, spra_iso_code3
    #, spra_ist_textsprache, spra_spra_id, spra_uc
    #, spra_dc
    deflang = parameters.dbDefaultLang()
    for key,value in languages.items():
        Sprache(pname=value[0],piso2=key,piso3=value[1]).insert()
    if not deflang in languages: deflang = 'de'
    Sprache.setmodellang(pmodellang=deflang)
    Sprache.setallreplacementlang()

    Modellelemtyp.fillmelt()
    diat = Diagrammtyp()
    diat.diat_bez = 'Entity'
    diat.diat_uc = 'stb'
    diat.diat_dc = date.today()
    diat.insert()
    #    medi_diat_id, medi_melt_id,medi_uc,mdei_dc,medi_um,mdei_dm
    dbInserts.insertmeltdiat((diat.diat_id, Modellelemtyp.getidbyshortname(pkurzname='ENTI'),'stb', date.today(), None, None))
    dbInserts.insertmeltdiat((diat.diat_id, Modellelemtyp.getidbyshortname(pkurzname='BEZI'),'stb', date.today(), None, None))
#insertBaseData

def loeschmodell():
    transferRelational.loeschmodell()

    dbDML.delete("benudef_eigenschaft")
    Schluesselelement.delete()
    Schluessel.delete()
    dbDML.delete("beziehungen")
    dbDML.delete("arcs")
    Attribut.delete()
    Synonym.delete()
    Entitaet.delete()
    ModelelemDoku.delete()
    Dokument.delete()
    Modellelement.delete()
    Diagramm.delete()
    dbDML.delete("benudef_eigenschaft")
    Vorgabewert.delete()
    Wertebereichgruppe.delete()
    Wertebereich.delete()
    dbDML.delete("speicherformate")
    dbDML.delete("linie_segment")
    dbDML.delete("beziehung_darst")
    dbDML.delete("elementdarst")
    dbDML.delete("melt_diat")
    Datatype.delete()
    dbDML.delete("diagramme")
    dbDML.delete('bereich_elemdarst')
    Modellelemtyp.delete ()
    Diagrammtyp.delete()
    Sprache.delete()
    Sprachtext.delete()
    dbDML.delete('geschaeftsbereich')
    Projekt.delete()

#loeschmodell

def loadcolors(coldict, classkey, elem):
    for fo in elem.findall('fonts/font_object'):
        if ((findField(fo, 'fo_type') == 'Title')
           or (findField(fo, 'fo_type') == 'Titel')): #es könnte auch Deutsch sein
            coldict[classkey].fontcolor = findField(fo, 'font_color')
            coldict[classkey].fontname = findField(fo, 'font_name')
            coldict[classkey].fontsize = findField(fo, 'font_size')
            coldict[classkey].fontstyle = findField(fo, 'font_style')
        # fi
    # for
#loadcolors

def loaddefaultcolors():
    settings = ET.parse(parameters.odmsettingsfile())
    root = settings.getroot()
    classif = root.find('classification_types')

    for ty in classif:
        #classname = findField(ty,'name')
        classguid = findField(ty,'id')
        # foregcolor, backgcolor,fontcolor,fontname,fontsize,fontstyle):
        classcolors[classguid] = \
           color(findField(ty,'fgcolor'),findField(ty,'color'),None,None,None,None)
        loadcolors(coldict=classcolors,classkey=classguid,elem=ty)
        #print(classname,classcolors[classguid].foregcolor,classcolors[classguid].backgcolor)
    #for
    default = root.find('default_fonts_and_colors')
    for de in default:
        classname = findField(de,'classname')
        defcolors[classname] = color(findField(de,'foreground')
                                                     ,findField(de,'background')
                                                     ,None,None,None,None)
        loadcolors(coldict=defcolors,classkey=classname,elem=de)
        #print(classname,defcolors[classname].fontsize)
    #for
#loaddefaultcolors

def filllanguages():
    Sprachtext.insertsprachtexte(pudpthema=parameters.odmUDPTranslFileName())
    #fill all elements in default language
    Sprachtext.filldefaulttext(dbParam.dbDefaultLangID)
    Sprache.deleteunused()

#filllanguages

def transferprojekt():
    proj = ET.parse(parameters.odmIMDirec() + parameters.odmModelName() + parameters.odmIMExtension())
    root = proj.getroot()
    comm = findText(root,'comment')
    if comm is None:
        defspra = parameters.dbDefaultLang()
        sprachen = parameters.dbLanguages()
    else:
        defspra = re.search(r'currentLang=([A-Z]{2})',comm).group(1)
        sprachen = re.search(r'languages=([A-Z,]*)', comm).group(1)
    #print (findField(root,'name'),comm,sprachen,defspra)
    proj = Projekt()
    proj.proj_name = findField(root,'name')
    proj.proj_uc = findText(root,'createdBy')
    proj.proj_dc = findText(root, 'createdTime')
    proj.proj_sprachen = sprachen
    proj.proj_akt_sprache = defspra
    proj.insert()

    dl,dl2 = dbParam.dbDefaultLang,parameters.dbDefaultLang()
    if defspra is not None:
        defspra = defspra.lower()
        #setze die Defaultsprache aus dem Modell
        if Sprache.spraidlookup(piso=defspra) is None:
            raise Exception("Language '{}' does not exist".format(defspra))
        Sprache.setmodellang(pmodellang=defspra)
        Sprache.setallreplacementlang()
        dbParam.liesdefaultlang()
        parameters.dbDefaultLang(defspra)
    #fi
#transferprojekt

def do1Document(fileName):
    tree = ET.parse(fileName)
    root = tree.getroot()
    doku = Dokument()
    doku.doku_name = findField(root,"name")
    doku.doku_format = findText(root, 'type')
    doku.doku_referenz = None
    doku.doku_odm_guid = findField(root, 'id')
    doku.doku_parent_odm_guid = findText(root, 'parentDocument')
    #DOKU_NAME, DOKU_FORMAT, DOKU_REFERENZ, DOKU_ODM_GUID, DOKU_PARENT_ODM_GUID
    doku.insert()
#do1Document

def transferDocuments():
    dosegfiles(pdirec=parameters.odmdocumentdirec(), transferfiles=do1Document)
    Dokument.updparents()
    #print(dbDML.select("""select * from Dokumente """))

#transferDocuments
def transferODMModel():
    """überträgt das ganze ODM Modell in die DB"""
    transferprojekt()
    dbParam.liesdefaultlang()
    transferTypes()
    transferDocuments()
    transferDomains()
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

#end transferODMModel