
import xml.etree.ElementTree as ET
import re,os,sqlite3
from datetime import date
from IM_DB import dbInserts,dbDML,dbLookup,dbConnect,parameters

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
#entry of keys found in entites
# (keyguid:(entiid,idx,keyName,uc,dc, (listof attr and relationship guids))
keys = dict()

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
    dbDML.delete("datatypes")


    types = ET.parse(parameters.odmIMDirec() + parameters.odmKonfDirec() + parameters.odmTypesFile())
    root = types.getroot()
    for typ in root.findall('logicaltype'):
        #print(typ.get('name'),typ.get('objectid'))
        #print(typ.find('mapping').text) #das erste genügt für den Moment

        dbInserts.insertDataTypes(pdaty=(typ.get('name'),basisType(typ.find('mapping').text),typ.get('objectid')))
    #endfor
#transferTypes


def transferDomains():
    #lösche die Domains
    dbDML.delete("vorgabewerte")
    dbDML.delete("wertebereiche")
    dbDML.delete("speicherformate")

    #print(parameters.odmDomainsFilePath())
    domains = ET.parse(parameters.odmDomainsFilePath())
    root = domains.getroot()
    for dom in root.findall('domains/Domain'):
        wrtb = Wertebereich(pname=dom.get('name'),pid=dom.get('id'))
        #print ("Domain name={} id={}" .format (wrtb.wrtb_name,wrtb.wrtb_odm_guid));
        #print (dom.find('createdBy').text,dom.find('createdTime').text)
        wrtb.wrtb_uc = dom.find('createdBy').text
        wrtb.wrtb_dc = dom.find('createdTime').text
        wrtb.wrtb_beschr = findText(dom,'comment')
        logDT = dom.find('logicalDatatype')
        wrtb.wrtb_datatype_ref = logDT.text if logDT is not None else None
        wrtb.wrtb_typ = dbLookup.datyLookupGrundTyp(wrtb.wrtb_datatype_ref)
        if wrtb.wrtb_typ is None:
            wrtb.wrtb_typ = 'TEXT'
        #print (wrtb.wrtb_datatype_ref,wrtb.wrtb_typ )

        lov = dom.find('listOfValues')
        if (lov is not None) & (lov != {}):
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
            range=(ranges[0].find('beginValue').text,ranges[0].find('endValue').text)
        else:
            range = (None,None)
        #endif

        #print(wrtb.wrtb_datatype_ref,dbDML.lookup('select  daty_grundtyp  from datatypes where  daty_odm_guid ="{}"'.format(wrtb.wrtb_datatype_ref)))
        #noch nicht übernommenm< defaultValue > a @ b.ch < / defaultValue >

        if (wrtb.wrtb_typ =='BIN'):
            wrtb.wrtb_bin_inhalttyp == 'BILD' # 'FILM','GRAPH','TEXT','TON'
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
                dbInserts.insertVorgabewert(pvgwt=(key, idx, wrtbid, lovs[key], None))
            #end for
        #endif
#end transferDomains
def toString(str,upper = False):
    if str is None:
        return "''"
    else:
        return(str.upper())
    #fi
#toString

def findeOderErstelleDom(domGuid,typeGuid,attrName):
    if (domGuid == None):
        domGuid='unkwown'
    #fi
    try:
        domId = dbLookup.wrtbLookup(domGuid)
    except:
        domId = dbLookup.wrtbLookupByName('Unknown')
    #try
    return domId
#findeOderErstelleDom

def do1Arc(fileName):
    arc= ET.parse(fileName).getroot()
#    print (arc.get("id"),arc.get("name"),arc.find('entity').text)

    #(arcs_name, arcs_enti_id, arcs_odm_guid
    # , arcs_uc, arcs_dc)
    dbInserts.insertArc(parc=(arc.get("name"),dbLookup.entiID(arc.find('entity').text)\
                              ,arc.get("id"),arc.find('createdBy').text,arc.find('createdTime').text))
#do1Arc

def transferArcs():
    dbDML.delete("arcs")

    for el in os.listdir(parameters.odmArcDirec()):
        if re.match('seg_.*', el):
            for file in os.listdir(parameters.odmArcDirec() + el):
                fileName = parameters.odmArcDirec() + el + '/' + file
                #print (fileName)
                do1Arc(fileName)
            #enfor
        #endif
    #endfor

#transferTypes

def updateUDP(p_modeid, p_obj):
    udps = []
    props = p_obj.find('propertyMap')
    if (props is not None):
        for prop in props:
            try:
                bdegId = dbLookup.bdegLookup(prop.get('name'))
                # print('      ', prop.get('name'), prop.get('value'), bdegId)
                udps.append((prop.get('value'), p_modeid, bdegId))
            except:
                """dynamische Properties lassen wir aus"""
                pass
        # rof
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
    #wegen FK-PK zursätzliche Attribute werden nicht übernommen
    if (findText(attr, 'referedAttribute') is not None):
        return

    ganzName = findField(attr,'name')
    abbrevName = findText(attr,'preferredAbbreviation')
    attrName=re.search('[^\[]*',ganzName).group().rstrip()
    creby = findText(attr,'createdBy')
    creti = findText(attr,'createdTime')
    techiName = nvl(abbrevName,re.sub('[-,.()\[\]äöüèéàÄ~ÖÜ ]','_',str.upper(attrName)))
    domId=findeOderErstelleDom(domGuid=findText(attr,'domain'),typeGuid=findText(attr,'logicalDatatype'),attrName=attrName)
    attrcomm = findText(attr,'comment')
    attrId = dbInserts.insertAttribute(pattr=(\
        entiId,domId,techiName
        ,attrName,findText(attr,''),attrcomm
        ,findText(attr,''),n
        ,'FALSE','FALSE' if (findText(attr,'nullsAllowed') == 'true') else 'TRUE','TRUE' if (re.search('\[.*T.*\]', ganzName) is not None) else 'FALSE'
        ,'TRUE' if (re.search('\[.*N.*\]', ganzName) is not None) else 'FALSE','TRUE' if (re.search('\[.*L.*\]', ganzName) is not None) else 'FALSE','FALSE'
        ,findText(attr,'createdBy')   ,findText(attr,'createdTime'),findField(attr,'id'),beziId
    ))
    lmodeId=dbInserts.insertModeAttr(attrId)
    dbInserts.insertUdpAttr(attrId)
    updateUDP(p_modeid=lmodeId, p_obj=attr)
    sprachtexte = [[attrName,creby,creti,'ATTR_NAME']
                  ,[attrcomm,creby,creti,'ATTR_COMMENT']]
    dbInserts.insertSprachtexte(p_texte=sprachtexte, p_modeid=lmodeId)

#do1Attribute
def    fillKeys(enti,entiId):
    allkeys = enti.find('identifiers')
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
                keys[key.get('id')] = (entiId,idx, key.get('name'),findText(key,'createdBy'),findText(key,'createdTime')
                                       ,keyrefs)
            #fi
        # rof
        # (keyguid:(entiid,idx,keyName,uc,dc, (listof attr and relationship guids))
    # fi
#fillKeys

def transferKeys(keys):
    # (keyguid:(entiid,idx,keyName,uc,dc, (listof attr and relationship guids))
    for keyGuid in keys:
        #schl_laufnr, schl_name, schl_odm_guid
        #, schl_uc, schl_dc, schl_enti_id
        keyId = dbInserts.insertSchluessel((keys[keyGuid][1],keys[keyGuid][2],keyGuid
                                    ,keys[keyGuid][3],keys[keyGuid][4],keys[keyGuid][0]))
        #print (keyGuid,keys[keyGuid])

        #nun die Schlüsselelemente
        for ke in keys[keyGuid][5]:
            try:
                attrId = dbLookup.attrID(ke)
                beziId = None
            except:
                beziId = dbLookup.beziId(ke)
                attrId = None
            #yrt
            #scel_schl_id,   scel_attr_id,scel_bezi_id,  scel_uc, scel_dc
            dbInserts.insertSchlElem((keyId,attrId,beziId,keys[keyGuid][3],keys[keyGuid][4]))
            #print(keyId, ke,attrId,beziId)
        #rof
    #rof
# transferKeys


def do1Entity(fileName):
    tree = ET.parse(fileName)
    root = tree.getroot()
    entname = root.get("name")
    entcomm = findText(root,'comment')
    creby = findText(root,'createdBy')
    creti = findText(root,'createdTime')
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
            sprachtexte = [[syno,creby,creti, 'ENTI_SYNONYM']]
            dbInserts.insertSprachtexte(p_texte=sprachtexte, p_modeid=modeid)

    #fi

    #print (entname,translate.translate(p_text=entname,p_fromlang='de',p_tolang='en'),translate.translate(p_text=entname,p_fromlang='de',p_tolang='fr'))

    updateUDP(p_modeid=lmodeId, p_obj=root)
    sprachtexte = [[entname,creby,creti,'ENTI_NAME']
                  ,[entcomm,creby,creti,'ENTI_COMMENT']]
    dbInserts.insertSprachtexte(p_texte=sprachtexte, p_modeid=lmodeId)

    attrs= root.find('attributes')
    if attrs is not None:
        for idx,attr in enumerate(attrs,start=1):
        #alle Attribute
            #print(attr.get('name'),attr.get('id'))
            do1Attribute(n=idx,attr=attr,entiId=entiId)
        #rof
    #fi
    fillKeys(enti=root,entiId=entiId)
#do1Entity

def transferEntitaeten():
    #lösche die Entitäten
    dbDML.delete("synonyme")
    dbDML.delete("entitaeten")

    for el in os.listdir(parameters.odmEntityDirec()):
        if re.match('seg_.*', el):
            for file in os.listdir(parameters.odmEntityDirec() + el):
                if  (re.match('.*New',file) == None) and \
                        (re.search('DS_Store', file) == None):
                    fileName = parameters.odmEntityDirec() + el + '/' + file
                    #print (fileName)
                    do1Entity(fileName)
                #endif
            #enfor
        #endif
    #endfor
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
#    if root.get('id') in ['E2F6422D-57B7-8EEF-2E4E-9D2B1E8A7742'
#,'3DF2EB21-4E7D-A57A-58B5-E3220941ACE1'
#,'ED734E28-4F24-502D-65A3-6614EE919185']:
#        print(root.get('id'),'=',findText(root,'arc'))
    try:
        beziArcId = dbLookup.arcsID(findText(root,'arc'))
    except  sqlite3.Error as e:
        if (e.__str__() == 'No Data Found'):
            beziArcId = None
        else:
            raise e
        #fi
    #yrt
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
    try:
        lrow=[lbeziType
             , dbLookup.entiID(findText(root,'sourceEntity')),vonText
             ,strNegBool(optSrc), 'FALSE'
             , dbLookup.entiID(findText(root,'targetEntity')), zuText
             ,strNegBool(optTarg),'FALSE', beziArcId
             ,root.get('id'),findText(root,'createdBy'),findText(root,'createdTime'),root.get('name')
             ]
            #root.get('name')\           ,findText(root,'comment')\
           #           ,findText(root,'transferable')           ,findText(root,'deleteRule')\
    except  sqlite3.Error as e:
        if (e.__str__() == 'No Data Found'):
            """Entity Id nicht gefunden. Datenleichen von Bezi mit gelöschten Entities"""
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

    updateUDP(p_modeid=lmodeId, p_obj=root)
    sprachtexte = [[vonText,creby,creti,'TEXT_FROM']
                  ,[zuText,creby,creti,'TEXT_TO']]
    dbInserts.insertSprachtexte(p_texte=sprachtexte, p_modeid=lmodeId)

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
    dbDML.delete("beziehungen")
    for el in os.listdir(parameters.odmRelationDirec()):
        if re.match('seg_.*', el):
            for file in os.listdir(parameters.odmRelationDirec() + el):
                fileName = parameters.odmRelationDirec() + el + '/' + file
#               print (fileName)
                do1Relation(fileName)
            #enfor
        #endif
    #endfor
    dbConnect.myDbConn.commit()
#transferRelations

def fillMelt():
    #lösche die Modellelementtypen
    dbDML.delete("modellelem_typ")

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
            #groups,findText(groups,'group name'))
        #endfor
    #enffor
    #print (lgroups)

    props = root.find('properties')
    #print (props)
    for prop in props.findall('property'):
        #print (prop.get('name'))
        #print (prop.get('name'),prop.get('dispalay_name'),lgroups[prop.get('group_id')],prop.get('default_value'),findText(prop,'description'))
        #bdeg_thema, bdeg_gruppe, bdeg_name, bdeg_default_value
        #bdeg_beschreibung, bdeg_optional, bdeg_wrtb_id,
        #bdeg_uc, bdeg_dc
        ludp = (lupdThema,lgroups[prop.get('group_id')],prop.get('name'),prop.get('default_value')
                ,findText(prop,'description'),'FALSE',None
                ,'--',date.today().__str__())
        udpId = dbInserts.insertUDP(pData=ludp)

        obj = prop.findall('objects/object')
        for o in obj:
            lMelt = re.split( "\.",o.get('class'))[6]
            #print( type2melt(lMelt))
            #print (lMelt)
            try:
                dbInserts.insertModellElemTyp((dbLookup.meltLookup(type2melt(lMelt)),udpId))
            except:
                None


        #print (ludp)
        lov = prop.find('list_of_values')
        if (lov is not None):
            wrtbId= dbInserts.insertLovWrtb(pName=lupdThema + '_' +prop.get('name'))

            for val in lov:
                #print (val.get('value'),val.get('default'))
                dbInserts.insertVorgabewert(pvgwt=(val.get('value'),None,wrtbId,val.get('value'),None))
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
    dbDML.delete("benudef_eigenschaft")
    l_sql = """select count(*) from benudef_wert union select count(*) from benudef_eigenschaft"""
    result = dbDML.select(l_sql)
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

    #UDP für Beziehungen sind aktuell noch als Allg. Properties aufgeführt.
    #Kopiere alle properties <sp>_.... aus Relation in die UDP
    for el in os.listdir(parameters.odmRelationDirec()):
        if re.match('seg_.*', el):
            for file in os.listdir(parameters.odmRelationDirec() + el):
                fileName = parameters.odmRelationDirec() + el + '/' + file
                #               print (fileName)
                tree = ET.parse(fileName)
                root = tree.getroot()
                props = root.find('propertyMap')
                if (props is not None):
                    for prop in props.findall('property'):
                        lName = prop.get('name')
                        if (re.match("(DE|EN)_",lName)):
                            #print (fileName,lName,lName[:2])
                            # bdeg_thema, bdeg_gruppe, bdeg_name, bdeg_default_value
                            # bdeg_beschreibung, bdeg_optional, bdeg_wrtb_id,
                            # bdeg_uc, bdeg_dc
                            ludp = (odmParam.imTranslationFileName,lName[:2]
                                   ,lName, None
                                    , 'udp for relations from ODM', 'TRUE', None
                                    , '--', date.today().__str__())
                            udpId = dbInserts.insertUDP(pData=ludp)
                            try:
                                dbInserts.insertModellElemTyp((dbLookup.meltLookup(type2melt('Relation')), udpId))
                            except:
                                pass
                            #try
                        #fi
                    #endfor
                #fi

                #nur das 1. ist notwendig
                break
            #endfor
        #endif
        break
    #endfor

    dbConnect.myDbConn.commit()

#transferUDPdef

def transferUDP():
    fillMelt()
    transferUPDdef()
#transferUDP

def insertBaseData():
    #(spra_iso_name, spra_iso_code2, spra_iso_code3
    #, spra_ist_textsprache, spra_spra_id, spra_uc
    #, spra_dc
    dbDML.delete('sprachtexte')
    dbDML.delete('sprachen')
    ldeId= dbInserts.insertSprache(('Deutsch','de','deu','TRUE','TRUE',None,'stb', date.today()));
    dbInserts.insertSprache(('English',  'en', 'eng', 'TRUE', 'FALSE',ldeId, 'stb', date.today()));
    dbInserts.insertSprache(('Français', 'fr', 'fra', 'TRUE', 'FALSE',ldeId, 'stb', date.today()));
#insertBaseData

def transferODMModel():
    """überträgt das ganze ODM Modell in die DB"""
    dbDML.delete("modellelement")
    dbDML.delete("attributes")
    dbDML.delete("benudef_eigenschaft")

    transferTypes()
    transferDomains()
    transferUDP()
    transferEntitaeten()
    transferArcs()
    transferRelations()
    doSubentities()
    transferKeys(keys)

    if (1==2):
        print("\nARCS")
        att=dbDML.select("select * from arcs "
                         "join (select enti_id, enti_name from entitaeten) on enti_id = arcs_enti_id")
        for a in att:
            print (a)

#    att=dbDML.select("""select von_name, bezi_assoc_von_zu,bezi_assoc_zu_von,zu_name
#                    ,beziehungen.*  
#                     from beziehungen 
#                    join (select enti_id as von_id, enti_name as von_name from entitaeten) on von_id = bezi_enti_id_von
#                     join (select enti_id as zu_id, enti_name as zu_name from entitaeten) on zu_id = bezi_enti_id_zu
#                     """)
    if (1==2):
        att=dbDML.select("""select *   from beziehungen order by bezi_odm_guid""")
        print("\nRELATIONS")
        for a in att:
            print (a)
    if (1==2):
        att = dbDML.select("""select attr_id,attr_anzname, attr_tech_name,enti_name,enti_odm_guid,enti_id  
        from attributes join entitaeten on enti_id = attr_enti_id 
        order by enti_id,attr_anzname""")
        print("\nAttributes")
        for a in att:
            print(a)
    if (1==2):
        att=dbDML.select("""select be.*,wrtb_name   from  benudef_eigenschaft as be
                            left join wertebereiche on wrtb_id = bdeg_wrtb_id""")
        print("\nUDP")
        for a in att:
            print (a)
    if (1==2):
        att=dbDML.select("""select * from wertebereiche""")
        print("\nDomains")
        for a in att:
            print (a)

    if (1==2):
        att=dbDML.select("""select * from modellelement""")
        print("\nModellelemente")
        for a in att:
            print (a)
    if (1==2):
        att=dbDML.select("""select * from modellelem_typ join modelltyp_eigensch on melt_id = mote_melt_id""")
        print("\nModellelementtypen")
        for a in att:
            print (a)
    if (1==2):
        att=dbDML.select("""select bw.* from benudef_wert as bw 
                join modellelement on mode_id = bdwe_mode_id
                join entitaeten on enti_id = mode_enti_id
                where enti_name = 'Adresse'""")
        print("\nBenudef Werte")
        for a in att:
            print (a)

        if (1 == 2):
            #        att = dbDML.select("""select * from wertebereiche""")
            att = dbDML.select("""select * from modelltyp_eigensch""")
            print("\nModelltypeigenschaften")
            for a in att:
                print(a)

    if (1 == 2):
        att = dbDML.select("""select * from benudef_eigenschaft """)
        print("\nBenudef Eigensch")
        for a in att:
            print(a)
    if (1 == 2):
        att = dbDML.select("""select * FROM schluessel join schluesselelement
        left join attributes on attr_id = scel_attr_id
        left join beziehungen on bezi_id = scel_bezi_id""")
        print("\nSchluessel")
        for a in att:
            print(a)

#end transferODMModel