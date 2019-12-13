
import xml.etree.ElementTree as ET
import re,os,sqlite3
from datetime import date
from IM_DB import dbInserts,dbDML,dbLookup,dbConnect,parameters,dbParam

class Wertebereich:
    def __init__(self, pname, pid):
        self.wrtb_name = pname
        self.wrtb_business_rule = None
        self.wrtb_beschr = None
        self.wrtb_typ = 'TEXT'
        self.wrtb_zpkt_minwert = None
        self.wrtb_zpkt_maxwert = None
        self.wrtb_zpkt_granularitaet = None
        self.wrtb_text_maxlng = None
        self.wrtb_text_syntaxregel = None
        self.wrtb_num_maxwert = None
        self.wrtb_num_minwert = None
        self.wrtb_num_vorkstellen = None
        self.wrtb_num_nachkstellen = None
        self.wrtb_num_rundng_einh = None
        self.wrtb_num_pheh = None
        self.wrtb_bin_inhalttyp = None
        self.wrtb_bin_spfo_id = None
        self.wrtb_uc = None
        self.wrtb_dc = None
        self.wrtb_odm_guid = pid
        self.wrtb_datatype_ref = None
    #end __init__
#end Wertebereich
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
# (keyguid:(entiid,idx,keyName,uc,dc, (listof attr and relationship guids))
keys = dict()
# Classification type colors
# classguid : color
classcolors = dict()
# default colors
# elementtypename : color
defcolors = dict()

def nvl(x,y=''):
    if x is None: return y
    else: return x
#nvl

def type2melt(type):
    trans = {"Entity" : "ENTI"
              ,"Attribute" : "ATTR"
        , "Relation": "BEZI"
        , "Table": ""
            ,"Column" : ""
             ,"FKIndexAssociation":""
             }
    return trans[type]
#type2melt

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

def basisType(dt):
    if (dt in ('BLOB','RAW, size','BFIE','BINARY_DOUBLE','BINARY_DOUBLE','CLOB'\
               ,'LONG','LONG RAW','NCLOB','')):
        return 'BIN'
    elif (dt in ('DATE','TIMESTAMP') or (re.match('INTERVAL.*',dt))):
        return 'ZPKT'
    elif (re.match('NUMBER.*',dt) or re.match('.*INT.*',dt) or re.match('FLOAT.*',dt)\
            or re.match('.*REAL.*',dt)):
        return 'NUM'
    else:
        return 'TEXT'
#basisType

def transferTypes():
    """rudimentäre Version der Typenübernahme
        müsste noch mit Systemen verknüpft werden.
    """


    types = ET.parse(parameters.odmIMDirec() + parameters.odmKonfDirec() + parameters.odmTypesFile())
    root = types.getroot()
    for typ in root.findall('logicaltype'):
        #print(typ.get('name'),typ.get('objectid'))
        #print(typ.find('mapping').text) #das erste genügt für den Moment

        dbInserts.insertDataTypes(pdaty=(typ.get('name'),basisType(typ.find('mapping').text),typ.get('objectid')))
    #endfor
#transferTypes


def do1structtype(filename):
    structdomains = ET.parse(filename)
    structdom = structdomains.getroot()
    if (findField(structdom,"class") != "oracle.dbtools.crest.model.design.datatypes.StructuredType"): return
    #print (structdom.get("name"))
    wrtb = Wertebereich(pname=findField(structdom,("name")),pid=findField(structdom,"id"))
    wrtb.wrtb_uc = findText(structdom,"createdBy")
    wrtb.wrtb_dc = findText(structdom,"createdTime")
    wrtb.wrtb_typ = 'GRP'
    wrtbid = dbInserts.insertWrtb(wrtb=(
        wrtb.wrtb_business_rule,wrtb.wrtb_name ,        wrtb.wrtb_beschr,
        wrtb.wrtb_typ,        wrtb.wrtb_zpkt_minwert,        wrtb.wrtb_zpkt_maxwert,
        wrtb.wrtb_zpkt_granularitaet,        wrtb.wrtb_text_maxlng,
        wrtb.wrtb_text_syntaxregel,        wrtb.wrtb_num_maxwert,
        wrtb.wrtb_num_minwert,        wrtb.wrtb_num_vorkstellen,
        wrtb.wrtb_num_nachkstellen,        wrtb.wrtb_num_rundng_einh,        wrtb.wrtb_num_pheh,
        wrtb.wrtb_bin_inhalttyp,        wrtb.wrtb_bin_spfo_id,        wrtb.wrtb_uc,
        wrtb.wrtb_dc,        wrtb.wrtb_odm_guid,        wrtb.wrtb_datatype_ref))

    elements = structdom.findall("attributes/Attribute")
    for el in elements:
        #print (wrtb.wrtb_name,findField(el,"name"),findText(el,'type'))
        reftype = findText(el,'type')
        elwrtb = dbLookup.wrtbLookup(pguid=reftype)
        if elwrtb is None:
            #nimm vorläufig unknown, da mein Typ evtl. noch nicht da ist.
            elwrtb = dbLookup.wrtbLookupByName(pname='Unknown')
        dbInserts.insertwrtbgruppe(wbgr=(wrtbid, findField(el,"name")
            ,findText(el,"comment"),elwrtb,reftype,findText(el,"createdBy")
            ,findText(el,"createdTime"),None,None))
    #for
#do1structtype
def transferDomains():
    #lösche die Domains
    #print(parameters.odmDomainsFilePath())
    domains = ET.parse(parameters.odmDomainsFilePath())
    root = domains.getroot()
    for dom in root.findall('domains/Domain'):
        wrtb = Wertebereich(pname=findField(dom, ("name")), pid=findField(dom, "id"))
        #print ("Domain name={} id={}" .format (wrtb.wrtb_name,wrtb.wrtb_odm_guid));
        #print (dom.find('createdBy').text,dom.find('createdTime').text)
        wrtb.wrtb_uc = findText(dom,'createdBy')
        wrtb.wrtb_dc = findText(dom,'createdTime')
        wrtb.wrtb_beschr = findText(dom,'comment')
        logDT = dom.find('logicalDatatype')
        wrtb.wrtb_datatype_ref = logDT.text if logDT is not None else None
        wrtb.wrtb_typ = dbLookup.datyLookupGrundTyp(wrtb.wrtb_datatype_ref)
        if wrtb.wrtb_typ is None:
            wrtb.wrtb_typ = 'TEXT'
        #print (wrtb.wrtb_datatype_ref,wrtb.wrtb_typ )

        lov = dom.find('listOfValues')
        if (lov is not None) and (lov != {}):
            wrtb.wrtb_typ = 'LOV'
            lovs = dict()
            for lovval in lov:
                #                print (lovval.get('value'),lovval.get('description'),lovval.attrib)
                lovs.update({lovval.get('value'): lovval.get('description')})
            # endfor
            # print (len(lovs))
        # endif
        ranges = dom.findall('listOfRanges/rangeDef')
        if not (ranges == []):
            range=(findText(ranges[0],'beginValue'),findText(ranges[0],'endValue'))
        else:
            range = (None,None)
        #endif

        #print(wrtb.wrtb_datatype_ref,dbDML.lookup('select  daty_grundtyp  from datatypes where  daty_odm_guid ="{}"'.format(wrtb.wrtb_datatype_ref)))
        #noch nicht übernommenm< defaultValue > a @ b.ch < / defaultValue >

        if (wrtb.wrtb_typ =='BIN'):
            wrtb.wrtb_bin_inhalttyp = 'BILD' # 'FILM','GRAPH','TEXT','TON'
            wrtb_bin_spfo_id = None
        elif (wrtb.wrtb_typ == 'LOV'):
            zahl=re.search('\A\d* ',nvl(findText(dom,'dataTypeSize')))
            wrtb.wrtb_text_maxlng = zahl.group() if not (zahl is None) else None
        elif (wrtb.wrtb_typ =='TEXT'):
#            print(re.search('\A\d* ','123 ab').group())
            zahl=re.search('\A\d* ',nvl(findText(dom,'dataTypeSize')))
            wrtb.wrtb_text_maxlng = zahl.group() if not (zahl is None) else None
            constr =dom.find('checkConstraint')
            if not (constr is None):
                #print(constr.findall('*'))
                impl = constr.find('implementationDef')
                if not (impl is None):
                    wrtb.wrtb_text_syntaxregel = impl.get('definition')
        elif (wrtb.wrtb_typ =='ZPKT'):
            wrtb.wrtb_zpkt_minwert = range[0]
            wrtb.wrtb_zpkt_maxwert = range[1]
            wrtb.wrtb_zpkt_granularitaet = 'MINUTE'
        elif (wrtb.wrtb_typ =='NUM'):
            wrtb.wrtb_num_minwert = range[0]
            wrtb.wrtb_num_maxwert = range[1]
            wrtb.wrtb_num_vorkstellen = findText(dom,'dataTypeScale')
            wrtb.wrtb_num_nachkstellen = findText(dom,'dataTypePrecision')
            wrtb.wrtb_num_rundng_einh = None
            wrtb.wrtb_num_pheh =  findText(dom,'unitOfMeasure')
        #endif

        wrtbid = dbInserts.insertWrtb\
        (wrtb=(
        wrtb.wrtb_business_rule,wrtb.wrtb_name ,        wrtb.wrtb_beschr,
        wrtb.wrtb_typ,        wrtb.wrtb_zpkt_minwert,        wrtb.wrtb_zpkt_maxwert,
        wrtb.wrtb_zpkt_granularitaet,        wrtb.wrtb_text_maxlng,
        wrtb.wrtb_text_syntaxregel,        wrtb.wrtb_num_maxwert,
        wrtb.wrtb_num_minwert,        wrtb.wrtb_num_vorkstellen,
        wrtb.wrtb_num_nachkstellen,        wrtb.wrtb_num_rundng_einh,        wrtb.wrtb_num_pheh,
        wrtb.wrtb_bin_inhalttyp,        wrtb.wrtb_bin_spfo_id,        wrtb.wrtb_uc,
        wrtb.wrtb_dc,        wrtb.wrtb_odm_guid,        wrtb.wrtb_datatype_ref))
        #print("nach inset wertebereich id={}" .format(wrtbid))

        if (lov is not None) & (lov != {}):
            for idx,key in enumerate(lovs.keys(),start=1):
                #print ('{}: {} = {}' .format(idx,key,lovs[key]))
                #vgwt_wert,  vgwt_sortrhfg, vgwt_wrtb_id, vgwt_anzeige, vgwt_beschr
                dbInserts.insertVorgabewert(pvgwt=(key, idx, wrtbid, lovs[key], None
                                                   ,wrtb.wrtb_uc, wrtb.wrtb_dc))
            #end for
        #endif

    dosegfiles(pdirec=parameters.odmstructypesdir(),transferfiles=do1structtype)

    """update group domains a their types may now be available"""
    ukwnid = dbLookup.wrtbLookupByName(pname='Unknown')
    lsql= """select wbgr_id,wbgr_type_ref
            from wertebereichgruppen
    """
    lupd= """update wertebereichgruppen
            set wbgr_wrtb_id_member = ?
            where wbgr_id = ?
    """
    wbgrs = dbDML.select(lsql)
    for wbgr in wbgrs:
        wrtbid = dbLookup.wrtbLookup(pguid=wbgr[1])
        if wrtbid is None:
            wrtbid = ukwnid
        dbDML.exec(lupd,wrtbid,wbgr[0])

#end transferDomains

def hex2int(phex):
    return  None if (phex is None)  else int(phex,16)
def int2hex(pint):
    if (pint is None): return pint
    lint = pint if (type(pint) == int) else int(pint)
    lint = lint + hex2int('FFFFFF') if (lint < 0) else 0
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
    entiodm = penti.get('oid')
    entiid = dbLookup.entiID(entiodm)
    hiddenelements = penti.find ("hiddenElements")
    if hiddenelements is not None:
        elemtext=findField(hiddenelements,"elements")
    else: elemtext = ""
    hiddenattrs=elemtext.split(' ')
    hiddenattrs2 = []
    for e in hiddenattrs:
        if e != "": hiddenattrs2.append(dbLookup.attrID(e))
    attrs = dbDML.select("""select attr_id from attributes 
                            where attr_enti_id = {}
                            order by attr_anz_rhflg""".format(entiid))
    attrids = [a[0] for a in attrs]
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
        #muss über Modell und saubere Tabellen abgehandelt werden
        pass
#        if (enticategoryid is None):
#            col = defcolors['Entity']
#        else:
#            col = classcolors[enticategoryid]
#        #fi
    #fi
    #print (col.foregcolor,col.backgcolor)
    #eled_position_x,eled_position_y,eled_breite,eled_hoehe
    #,eled_deckkraft,eled_farbe,eled_randbreite,eled_randdeckkraft
    #,eled_randfarbe, eled_schriftgroesse, eled_schriftfarbe, eled_mode_id
    #,eled_diag_id, eled_uc, eled_dc, eled_um
    #, eled_dm

    index = 0
    entix=int(layout.get('x'))
    entiy=int(layout.get('y'))
    entiwidth=int (layout.get('width'))
    entiheight=int(layout.get('height'))
    #if there are several copies on a diagramm, repeat the insert with new index und insert succeeds
    while True:
        row = (entix, entiy, entiwidth, entiheight
              , 100, int2hex(col.backgcolor), None, 100
              , int2hex(col.foregcolor),col.fontsize, int2hex(col.fontcolor), dbLookup.modeEntiLookup(p_entiid=entiid)
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
                         ,None,None,None,dbLookup.modeAttrLookup(aid)
                         ,pdiagid,0,puc,pdc
                         ,None,None)
                try:
                    dbInserts.insertelementdarst(pdata=attrrow)
                except Exception as e: print(e)
                attry += attrheight
                # Maximal bis zur Grösse der Entität
                if ((attry-entiy) > (entiheight - 10)): break
            #for
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
        type = o.get('otype')
        if (type == 'Image'):
            pass
        elif (type == 'Entity'):
            transferentity(penti=o, pdiagid=pdiagid, puc=puc, pdc=pdc)
        elif (type == 'Note'):
            pass
        #fi
#transferdiaobj

def linetype(pidx,pmaxidx,psourcelt,ptargetlt):
    if (pidx <= ((pmaxidx-1) / 2)):
        return psourcelt
    else:
        return ptargetlt
    #fi
#linetype

def connector():
    #ist kein Segment sondern in Punkt. es macht nur 1 oder M Sinn
    return 1
#conmector
def transferdiaconnect(pconnectors, pdiagid, puc, pdc):
    for c in pconnectors:
        type = c.get('otype')
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

            """
    beda_diag_id, beda_mode_id, beda_linienbreite, beda_liniefarbe
    ,beda_liniedeckkraft, beda_starttext_x, beda_starttext_y, beda_starttext_breite
    ,beda_starttext_hoehe, beda_endtext_x, beda_endtext_y, beda_endtext_breite
    ,beda_endtext_hoehe, beda_schriftfarbe, beda_schriftgroesse, beda_uc
    ,beda_dc, beda_um, beda_dm)
"""
            row=(pdiagid,dbLookup.modeid(p_beziid=beziid),linewidth,None
                 ,1,sttex,sttey,sttew
                 ,stteh,entex,entey,entew
                 ,enteh,None,10,puc,pdc,None,None
                 )
            bedaid=dbInserts.insertelbezidarst(row)

            points=c.findall('points/point')
            pointsegs=[]
            bezi = dbDML.select("""select bezi_enti_id_von,bezi_source_enti_guid
                                    ,bezi_enti_id_zu ,bezi_target_enti_guid 
                                    from beziehungen
                                    join entitaeten source on source.enti_odm_guid = bezi_source_enti_guid
                                    join entitaeten target on target.enti_odm_guid = bezi_target_enti_guid
                    """)
            sourcelinetype = 'SOLID'
            targetlinetype = 'DASHED'
            for idx,point in enumerate(points):
                """ lise_rhfg, lise_beda_id, lise_x, lise_y
    , lise_linientyp,lise_konnektor, lise_uc, lise_dc
    , lise_um,lise_dm 
    """
                pointsegs.append((idx,bedaid,findField(point,'x'),findField(point,'y')
                                ,linetype(pidx=idx, pmaxidx=len(points)
                                          ,psourcelt= sourcelinetype,ptargetlt=targetlinetype)
                                ,connector(),puc,pdc,None,None))
            #for
            dbInserts.insertlinieseg(pointsegs)
        else: pass
        #fi
#transferdiaconnect

# transferdiaconnect
def transferdiaarc(parcs, pdiagid, puc, pdc):
    pass
# transferdiaarc

def dosegfiles(pdirec,transferfiles):
    try:
        listdir=os.listdir(pdirec)
    except:
        print('directory "{}" not found.'.format(pdirec))
        return
    #try
    for el in listdir:
        if re.match('seg_.*', el):
            for file in os.listdir(pdirec + el):
                #nur GUID als Namen erlaubt.
                if re.match(r'[A-Z0-9-]{30,45}.xml',file):
#                if  ((re.search('DS_Store', file) == None)
#                    and (not file.startswith('.'))):
                    fileName = pdirec + el + '/' + file
                    #print (fileName)
                    transferfiles(fileName)
                #fi
            #for
        #fi
    #for
#dosegfiles

def do1diagramm(p_filename):
    #print (p_filename)
    diagramme = ET.parse(p_filename)
    dia = diagramme.getroot()
    dianame = dia.get('name')
    if (dianame == 'Logical'):
        return
    #entcomm = findText(root,'comment')
    #creby = findText(root,'createdBy')
    #creti = findText(root,'createdTime')
    diatid = dbLookup.diatid(p_name='Entity')
    #print(dia.get('name'), dia.get('id'))
    #diag_name,diag_diat_id,diag_uc,diag_dc,diag_um,diag_dm
    if (findText(dia,'showLegend') == 'true'):
        legende =dia.find("objectViews/OView[@otype='Legend']")
        bounds=legende.find("bounds")
        legendx = findField(bounds,'x')
        legendy = findField(bounds,'y')
    else:
        legendx = None
        legendy = None
    #fi
    uc = findText(dia,'createdBy')
    dc = findText(dia,'createdTime')
    row = (dianame, diatid,dia.get('id'),legendx,legendy, uc
           ,dc,findText(dia,'modifiedBy'),None)
    #print (row)
    diagid = dbInserts.insertdiagramm(p_data=row)
    objects = dia.findall('objectViews/OView')
    if (len(objects) > 0):
        transferdiaobj(pobjects=objects, pdiagid=diagid, puc=uc, pdc=dc)
    connectors = dia.findall('connectors/Connector')
    if (len(connectors) > 0):
        transferdiaconnect(pconnectors=connectors, pdiagid=diagid, puc=uc, pdc=dc)
    arcs = dia.findall('arcs/Arc')
    if (len(arcs) > 0):
        transferdiaarc(parcs=arcs, pdiagid=diagid, puc=uc, pdc=dc)
    #print (dianame,len(objects),len(connectors),len(arcs))
#do1diagramm

def transferdiagramme():
    for el in os.listdir(parameters.odmentisubviewdirec()):
        filename = parameters.odmentisubviewdirec() +  el
        do1diagramm(p_filename=filename)
    #endfor
#transferdiagramme

def findeOderErstelleDom(pdomguid, pstructdomguid, ptypeguid, pattrname):
    domId = None
    if pdomguid is not None:
        domId = dbLookup.wrtbLookup(pdomguid)
    elif pstructdomguid is not None:
        domId = dbLookup.wrtbLookup(pstructdomguid)
    #
    if domId is None: domId = dbLookup.wrtbLookupByName('Unknown')
    return domId
#findeOderErstelleDom

def do1Arc(fileName):
    arc= ET.parse(fileName).getroot()
    if (findField(arc, "class") != "oracle.dbtools.crest.model.design.logical.Arc"): return
#    print (arc.get("id"),arc.get("name"),arc.find('entity').text)

    #(arcs_name, arcs_enti_id, arcs_odm_guid
    # , arcs_uc, arcs_dc)
    dbInserts.insertArc(parc=(arc.get("name"),dbLookup.entiID(arc.find('entity').text)\
                              ,arc.get("id"),arc.find('createdBy').text,arc.find('createdTime').text))
#do1Arc

def transferArcs():
    dosegfiles(pdirec=parameters.odmArcDirec(),transferfiles=do1Arc)
#transferArcs

def updateUDP(pmodeid, pobj):
    udps = []
    props = pobj.find('propertyMap')
    if (props is not None):
        for prop in props:
            try:
                bdegId = dbLookup.bdegLookup(prop.get('name'))
                # print('      ', prop.get('name'), prop.get('value'), bdegId)
                udps.append((prop.get('value'), pmodeid, bdegId))
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
            # print('      ', prop.get('name'), prop.get('value'), bdegId)
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

def do1Attribute(n,attr,entiId=None,beziId=None):
    #print (attr.find('createdTime').text,findText(attr,'nullsAllowed'));
#    attr_enti_id, attr_wrtb_id, attr_tech_name
#    , attr_anzname, attr_tooltip, attr_beschr
#    , attr_business_rule, attr_anz_rhflg
#    , attr_deskriptor, attr_pflichtattr, attr_historisiert
#    , attr_wiederholt, attr_sprachabhaengig, attr_verschluesselt
#    attr_uc, attr_dc,attr_odm_guid,attr_bezi_id
    #wegen FK-PK zusätzliche Attribute werden nicht übernommen
    if (findText(attr, 'referedAttribute') is not None):
        return

    ganzName = findField(attr,'name')
    abbrevName = findText(attr,'preferredAbbreviation')
    attrName=re.search('[^\[]*',ganzName).group().rstrip()
    creby = findText(attr,'createdBy')
    creti = findText(attr,'createdTime')
    techiName = nvl(abbrevName,re.sub('[-,.()\[\]äöüèéàÄ~ÖÜ ]','_',str.upper(attrName)))
    domId=findeOderErstelleDom(pdomguid=findText(attr, 'domain')
                               , pstructdomguid=findText(attr,'structuredType')
                               , ptypeguid=findText(attr, 'logicalDatatype')
                               , pattrname=attrName)
    attrcomm = findText(attr,'comment')
    attrset=(entiId,domId,techiName
        ,attrName,findText(attr,''),attrcomm
        ,findText(attr,''),n
        ,'FALSE','FALSE' if (findText(attr,'nullsAllowed') == 'true') else 'TRUE'
             ,'TRUE' if (re.search('\[.*T.*\]', ganzName) is not None) else 'FALSE'
        ,'TRUE' if (re.search('\[.*N.*\]', ganzName) is not None) else 'FALSE'
             ,'TRUE' if (re.search('\[.*L.*\]', ganzName) is not None) else 'FALSE','FALSE'
        ,creby,creti,findField(attr,'id'),beziId
    )
    try:
        attrId = dbInserts.insertAttribute(pattr=attrset)
    except  sqlite3.Error as e:
        print(str(e))
        print(attrset)
        raise e
    #try
    lmodeId=dbInserts.insertModeAttr(attrId)
    dbInserts.insertUdpAttr(attrId)
    updateUDP(pmodeid=lmodeId, pobj=attr)

#do1Attribute

def fillKeys(p_enti, p_entiid):
    global keys
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
                #print(idx, enti.get('name'), key.get('id'), enti.get('id'), keyrefs)
                keys[key.get('id')] = (p_entiid, idx, key.get('name'), findText(key, 'createdBy'), findText(key, 'createdTime')
                                       , keyrefs)
            #fi
        # rof
        # (keyguid:(entiid,idx,keyName,uc,dc, (listof attr and relationship guids))
    # fi
#fillKeys

def transferKeys(p_keys):
    # (keyguid:(entiid,idx,keyName,uc,dc, (listof attr and relationship guids))
    for keyGuid in p_keys:
        #schl_laufnr, schl_name, schl_odm_guid
        #, schl_uc, schl_dc, schl_enti_id
        keyset=(p_keys[keyGuid][1], p_keys[keyGuid][2], keyGuid
                                    , p_keys[keyGuid][3], p_keys[keyGuid][4], p_keys[keyGuid][0])
        keyId = dbInserts.insertSchluessel(keyset)
        #print (keyGuid,keys[keyGuid])

        #nun die Schlüsselelemente
        for ke in p_keys[keyGuid][5]:
            try:
                attrId = dbLookup.attrID(ke)
                beziId = None
            except:
                try:
                    beziId = dbLookup.beziId(ke)
                    attrId = None
                except sqlite3.Error as e:
                    print (str(e))
                    print (ke,keyset)
                    raise e
                #try
            #yrt
            #scel_schl_id,   scel_attr_id,scel_bezi_id,  scel_uc, scel_dc
            dbInserts.insertSchlElem((keyId, attrId, beziId, p_keys[keyGuid][3], p_keys[keyGuid][4]))
            #print(keyId, ke,attrId,beziId)
        #rof
    #rof
# transferKeys


def do1Entity(fileName):
    tree = ET.parse(fileName)
    root = tree.getroot()
    if (findField(root,"class") != "oracle.dbtools.crest.model.design.logical.Entity"): return
    entname = root.get("name")
    entcomm = findText(root,'comment')
    creby = findText(root,'createdBy')
    creti = findText(root,'createdTime')
    enticategoryid = findText(root,'typeID')
    row=(root.get('id'),None,None\
        ,entname,entcomm,None\
        ,None,None,None\
        ,None,creby,creti
        ,findText(root,'hierarchicalParent'),None)
    #print ("Entity:", row)
    #enti_odm_guid, enti_augb_id, enti_tech_name
    #, enti_name, enti_beschr, enti_tooltip
    #, enti_kurzname, enti_prefix, enti_beispiele
    #, enti_erw_tupel, enti_uc, enti_dc
    #,enti_enti_guid,enti_enti_id
    entiId = dbInserts.insertEnti(enti=row)
    lmodeId =dbInserts.insertModeEnti(entiId)
    dbInserts.insertUdpEntity(entiId)

    sobj =findText(root,'synonym')
    if (sobj is not None):
        for syn in sobj.split(','):
            syno = syn.strip()
            synid = dbInserts.insertSynonym((syno,entiId))
            modeid = dbInserts.insertmodesyno(synid)
    #fi

    #print (entname,translate.translate(p_text=entname,p_fromlang='de',p_tolang='en'),translate.translate(p_text=entname,p_fromlang='de',p_tolang='fr'))

    updateUDP(pmodeid=lmodeId, pobj=root)

    attrs= root.find('attributes')
    if attrs is not None:
        for idx,attr in enumerate(attrs,start=1):
        #alle Attribute
            #print(attr.get('name'),attr.get('id'))
            do1Attribute(n=idx,attr=attr,entiId=entiId)
        #rof
    #fi
    fillKeys(p_enti=root, p_entiid=entiId)
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
                    , bezi_arcs_id, bezi_uc, bezi_dc,bezi_name)
                select 'ISA', slave_enti_id,''
                            , 'TRUE','FALSE'
                            ,master_enti_id,'','TRUE','FALSE'
                            ,arcs_id,arcs_uc, arcs_dc,'' beziname
                            from arcs
                            join (select enti_id as master_enti_id
                                       , enti_odm_guid as master_guid from entitaeten) on master_enti_id = arcs_enti_id
                            join  (select enti_id as slave_enti_id
                                       , enti_enti_guid as slave_master_guid from entitaeten) on slave_master_guid = master_guid
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

def beziType(srcCard, targCard, srcOpt,targOpt,arcId):
    # ISA: 1:1 und
    #      zuSeite Pflicht, vonSeite optional
    #           oder beide sind Pflicht und die zuSeite beziehung ist in einem Arc
    #    1:1 sonst
    #
    if ((srcCard == '1') and (targCard == '1')):
        if ((srcOpt == 'false') and (targOpt == 'false') and (arcId is not None)
           ):
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
    root = tree.getroot()
    if (findField(root,"class") != "oracle.dbtools.crest.model.design.logical.Relation"): return
    try:
        beziArcId = dbLookup.arcsID(findText(root,'arc'))
    except  sqlite3.Error as e:
        if (e.__str__() == 'No Data Found'):
            beziArcId = None
        else:
            raise e
        #fi
    #try
    relname=root.get('name')
    optSrc = findText(root, 'optionalSource')
    optTarg = findText(root, 'optionalTarget')
    cardSrc = findText(root, 'sourceCardinality')
    cardTarg = findText(root, 'targetCardinalityString')

    lbeziType = beziType(srcCard= abbildTyp(cardSrc)
                    ,targCard=abbildTyp(cardTarg)
                    ,srcOpt=optSrc
                    ,targOpt= optTarg
                    ,arcId=beziArcId)
        # bezi_isa_assoc, bezi_enti_id_von, bezi_assoc_von_zu
        # , bezi_abbildtyp_zu_von ,bezi_pflicht_assoc_von_zu,bezi_hist_von_zu
        # ,bezi_enti_id_zu,bezi_assoc_zu_von, bezi_abbildtyp_zu_von
        # ,BEZI_PFLICHT_ASSOC_ZU_VON,bezi_hist_zu_von,bezi_arcs_id
        # ,bezi_odm_guid,bezi_uc, bezi_dc,bezi_name
    vonText = findText(root,'nameOnSource')
    zuText = findText(root, 'nameOnTarget')
    creby = findText(root,'createdBy')
    creti = findText(root,'createdTime')
    sourceentiguid = findText(root,'sourceEntity')
    targetentiguid = findText(root,'targetEntity')
    try:
        lrow=[lbeziType
             , dbLookup.entiID(sourceentiguid),vonText
             ,strNegBool(optSrc), 'FALSE'
             , dbLookup.entiID(targetentiguid), zuText
             ,strNegBool(optTarg),'FALSE', beziArcId
             ,root.get('id'),creby,creti,relname
            ,sourceentiguid,targetentiguid
             ]
            #root.get('name')\           ,findText(root,'comment')\
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
        #Entity-Id
        lrow[1], lrow[5] = lrow[5], lrow[1]
        #text
        lrow[2], lrow[6] = lrow[6], lrow[2]
        #Optionalität
        lrow[3], lrow[7] = lrow[7], lrow[3]
    #fi
    row = tuple(lrow)
    #print (row)

    beziId = dbInserts.insertBeziehung(row)
    lmodeId = dbInserts.insertModeBezi(beziId)
    dbInserts.insertUdpBezi(beziId)

    updateUDP(pmodeid=lmodeId, pobj=root)

    attrs= root.find('attributes')
    if attrs is not None:
        for idx,attr in enumerate(attrs,start=1):
            #alle Attribute
            #print((attr.get('name'),attr.get('id')))
            do1Attribute(n=idx,attr=attr,beziId=beziId)
        #endfor
    #fi

#do1Relation

def transferRelations():
    #lösche die Beziehungen
    dosegfiles(pdirec=parameters.odmRelationDirec(),transferfiles=do1Relation)
    dbConnect.myDbConn.commit()
#transferRelations

def fillMelt():
    #lösche die Modellelementtypen

    # melt_kurzname,  melt_name    ,melt_uc,  melt_dc
    modellelementtypen = \
    [('ATTR', 'Attribute', 'stb', date.today()) \
        , ('BEZI', 'Beziehungen', 'stb', date.today()) \
        , ('BURU', 'Business Rules', 'stb', date.today()) \
        , ('ENTI', 'Entitäten', 'stb', date.today()) \
        , ('WRTB', 'Wertebereiche', 'stb', date.today()) \
        , ('SYNO', 'Synonyme', 'stb', date.today()) \
     ]

    dbInserts.insertMelt(modellelementtypen)

#fillMelt

def do1UDPFile(pudpThema,pfileName):
    tree = ET.parse(pfileName)
    root = tree.getroot()
    lupdThema = pudpThema
    lgroups = {'':'-'}
    for groups in root.findall('udp_groups'):
        for child in groups:
            #print(child.get('name'))
            lgroups[child.get('id')] = child.get('name')
        #for
    #for

    props = root.find('properties')
    #print (props)
    propgroups=[]
    for prop in props.findall('property'):
        group = prop.get('group_id')
        #print (prop.get('name'))
        #print (prop.get('name'),prop.get('dispalay_name'),lgroups[prop.get('group_id')],prop.get('default_value'),findText(prop,'description'))
        #bdeg_thema, bdeg_gruppe, bdeg_name, bdeg_default_value
        #bdeg_beschreibung, bdeg_optional, bdeg_wrtb_id,
        #bdeg_uc, bdeg_dc
        ludp = (lupdThema,lgroups[group],prop.get('name'),prop.get('default_value')
                ,findText(prop,'description'),'FALSE',None
                ,'--',date.today().__str__())
        udpId = dbInserts.insertUDP(pData=ludp)
        if (lupdThema == parameters.odmUDPTranslFileName()):
            #die speziellen Properties manuell
            if not (group in propgroups): #nur einmal eintragen je Sprache (Gruppe)
                propgroups.append(group)
                ludpid=dbInserts.insertUDP(pData=(lupdThema, lgroups[prop.get('group_id')]
                    , lgroups[group]+'_RELA_TEXT_FROM', None
                    , None, 'FALSE', None, '--', date.today().__str__()))
                dbInserts.insertModellElemTyp((dbLookup.meltLookup(type2melt('Relation')), ludpid))
                ludpid=dbInserts.insertUDP(pData=(lupdThema, lgroups[prop.get('group_id')]
                    , lgroups[group]+'_RELA_TEXT_TO', None
                    , None, 'FALSE', None, '--', date.today().__str__()))
                dbInserts.insertModellElemTyp((dbLookup.meltLookup(type2melt('Relation')), ludpid))
                ludpid=dbInserts.insertUDP(pData=(lupdThema, lgroups[prop.get('group_id')]
                    , lgroups[group]+'_ENTI_COMMENT', None
                    , None, 'FALSE', None, '--', date.today().__str__()))
                dbInserts.insertModellElemTyp((dbLookup.meltLookup(type2melt('Entity')), ludpid))
                ludpid=dbInserts.insertUDP(pData=(lupdThema, lgroups[prop.get('group_id')]
                    , lgroups[group]+'_ATTR_COMMENT', None
                    , None, 'FALSE', None, '--', date.today().__str__()))
                dbInserts.insertModellElemTyp((dbLookup.meltLookup(type2melt('Attribute')), ludpid))
            #fi
        #fi

        obj = prop.findall('objects/object')
        for o in obj:
            lMelt = re.split( "\.",o.get('class'))[6]
            #print( type2melt(lMelt))
            #print (lMelt)
            lmeltid=type2melt(lMelt)
            if lmeltid != "":
                try:    dbInserts.insertModellElemTyp((dbLookup.meltLookup(lmeltid),udpId))
                except: pass
            #fi


        #print (ludp)
        lov = prop.find('list_of_values')
        if (lov is not None):
            wrtbId= dbInserts.insertLovWrtb(pName=lupdThema + '_' +prop.get('name'))

            for val in lov:
                #print (val.get('value'),val.get('default'))
                dbInserts.insertVorgabewert(pvgwt=(val.get('value'),None,wrtbId,val.get('value'),None
                                                   ,'--',date.today().__str__()))
                  #vgwt_wert ,    vgwt_sortrhfg,
                #          vgwt_wrtb_id,   vgwt_anzeige   ,    vgwt_beschr)
            #rof
            dbDML.exec("""update benudef_eigenschaft  set bdeg_wrtb_id = {}  where bdeg_Id = {} """
                        .format (wrtbId,udpId))

        # fi
    # rof
#do1UDPFile

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
    #(spra_iso_name, spra_iso_code2, spra_iso_code3
    #, spra_ist_textsprache, spra_spra_id, spra_uc
    #, spra_dc
    ldeId= dbInserts.insertSprache(('Deutsch','de','deu','TRUE','TRUE',None,'stb', date.today()));
    dbInserts.insertSprache(('English',  'en', 'eng', 'TRUE', 'FALSE',ldeId, 'stb', date.today()));
    dbInserts.insertSprache(('Français', 'fr', 'fra', 'TRUE', 'FALSE',ldeId, 'stb', date.today()));
    dbInserts.insertSprache(('Español,', 'es', 'esp', 'TRUE', 'FALSE',ldeId, 'stb', date.today()));
    dbInserts.insertSprache(('Italiano,', 'it', 'ita', 'TRUE', 'FALSE',ldeId, 'stb', date.today()));

    fillMelt()
    entidiaid = dbInserts.insertdiagrammtyp(('Entity','stb',date.today(),None,None))
    #    medi_diat_id, medi_melt_id,medi_uc,mdei_dc,medi_um,mdei_dm
    dbInserts.insertmeltdiat((entidiaid, dbLookup.meltLookup(p_kurzname='ENTI'),'stb', date.today(), None, None))
    dbInserts.insertmeltdiat((entidiaid, dbLookup.meltLookup(p_kurzname='BEZI'),'stb', date.today(), None, None))
#insertBaseData

def loeschmodell():
    dbDML.delete("benudef_eigenschaft")
    dbDML.delete("beziehungen")
    dbDML.delete("arcs")
    dbDML.delete("attributes")
    dbDML.delete("synonyme")
    dbDML.delete("entitaeten")
    dbDML.delete("modellelement")
    dbDML.delete('diagramme')
    dbDML.delete("benudef_eigenschaft")
    dbDML.delete("vorgabewerte")
    dbDML.delete("wertebereichgruppen")
    dbDML.delete("wertebereiche")
    dbDML.delete("speicherformate")
    dbDML.delete("linie_segment")
    dbDML.delete("beziehung_darst")
    dbDML.delete("elementdarst")
    dbDML.delete("melt_diat")
    dbDML.delete("datatypes")
    dbDML.delete("diagramme")
    dbDML.delete("modellelem_typ")
    dbDML.delete('diagrammtypen')
    dbDML.delete('sprachtexte')
    dbDML.delete('sprachen')
    dbDML.delete('projekt')
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
    translations = dbDML.select("""
    select * from 
    (select substr(bdeg_name,4)attrname, bdwe_wert
            ,mode_id, bdwe_uc, bdwe_dc
            ,substr(bdeg_name,1,2) sprache
            ,bdeg_thema
     from benudef_wert
     join benudef_eigenschaft on bdeg_id = bdwe_bdeg_id
     join modellelement on mode_id = bdwe_mode_id
    )
     where bdeg_thema = '{}'
     and upper(sprache) != upper('{}')
    """.format(parameters.odmUDPTranslFileName(),dbParam.dbDefaultLang))
    for t in translations:
        #print (t )
        #sptx_attrname,  sptx_text,sptx_mode_id, sptx_uc, sptx_dc, sptx_spra_id
        dbInserts.insertSprachtext(pdata=[(t[0],t[1],t[2],t[3],t[4],dbLookup.spraLookup(t[5]))])
    #for
    #fill all elements in default language
    dbDML.exec("""insert into sprachtexte 
                    (sptx_attrname,  sptx_text
                   ,sptx_mode_id, sptx_uc, sptx_dc
                   , sptx_spra_id)
                  select * from 
                    (select 'ENTI_NAME' attrname, enti_name text 
                        ,mode_id,enti_uc,enti_dc
                    from modellelement
                    join entitaeten on enti_id = mode_enti_id
                    union all
                   select 'ENTI_COMMENT' attrname, enti_beschr text 
                        ,mode_id,enti_uc,enti_dc
                    from modellelement
                    join entitaeten on enti_id = mode_enti_id                    
                    union all
                   select 'ENTI_SYNONYM' attrname, group_concat(syno_name,', ') text 
                        ,enti_id,enti_uc,enti_dc
                    from modellelement
                    join synonyme on syno_id = mode_syno_id
                    join entitaeten on enti_id = syno_enti_id
                    group by enti_id,enti_uc,enti_dc                    
                    union all
                   select 'ATTR_COMMENT' attrname, attr_beschr text 
                        ,mode_id,attr_uc,attr_dc
                    from modellelement
                    join attributes on attr_id = mode_attr_id    
                    union all                
                   select 'ATTR_NAME' attrname, attr_anzname text 
                        ,mode_id,attr_uc,attr_dc
                    from modellelement
                    join attributes on attr_id = mode_attr_id 
                    union all                
                   select 'RELA_TEXT_FROM' attrname, bezi_assoc_von_zu text 
                        ,mode_id,bezi_uc,bezi_dc
                    from modellelement
                    join beziehungen on bezi_id = mode_bezi_id 
                    union all                
                   select 'RELA_TEXT_TO' attrname, bezi_assoc_zu_von text 
                        ,mode_id,bezi_uc,bezi_dc
                    from modellelement
                    join beziehungen on bezi_id = mode_bezi_id 
                )
                cross join (select {})
                where text is not null
                   """.format(dbParam.dbDefaultLangID))
    # sptx_attrname,  sptx_text,sptx_mode_id, sptx_uc, sptx_dc, sptx_spra_id
#filllanguages

def transferprojekt():
    proj = ET.parse(parameters.odmIMDirec() + parameters.odmModelName() + parameters.odmIMExtension())
    root = proj.getroot()
    comm = findText(root,'comment')
    defspra=re.search(r'currentLang=([A-Z]{2})',comm).group(1)
    sprachen=re.search(r'languages=([A-Z,]*)',comm).group(1)
    #print (findField(root,'name'),comm,sprachen,defspra)
    dbInserts.insertprojekt(pdata=(findField(root,'name'),findText(root,'createdBy')
        , findText(root, 'createdTime'),sprachen,defspra))
    if (defspra is not None
        and dbParam.dbDefaultLang.lower() != defspra.lower()):
        #setze die Defaultsprache aus dem Modell
        if dbLookup.spraLookup(defespra.lower()) is None:
            raise Exception("Language '{}' does not exist".format(defspra))
        dbDML.exec("""update sprachen set spra_ist_modellsprache = 'FALSE'
                           where lower(spra_iso_code2)  = lower('{}')
                      """.format (dbParam.dbDefaultLang))
        dbDML.exec("""update sprachen set spra_ist_modellsprache = 'TRUE'
                       where lower(spra_iso_code2)  = lower('{}')
                    """.format(defspra))
    #fi
#transferprojekt

def transferODMModel():
    """überträgt das ganze ODM Modell in die DB"""
    transferprojekt()
    dbParam.liesDefaultLang()
    transferTypes()
    transferDomains()
    transferUDP()
    transferEntitaeten()
    transferArcs()
    transferRelations()
    doSubentities()
    transferKeys(keys)
    loaddefaultcolors()
    transferdiagramme()
    filllanguages()

#end transferODMModel