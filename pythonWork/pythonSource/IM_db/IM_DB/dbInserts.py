from datetime import date

from IM_DB import dbDML, dbLookup


def  insertEnti(enti):
    lsql="""
    insert into entitaeten 
       (enti_odm_guid ,enti_augb_id,enti_tech_name     
       ,enti_name,enti_beschr     ,enti_tooltip    
       ,enti_kurzname   ,enti_prefix             ,enti_beispiele          
       ,enti_erw_tupel         ,enti_uc ,enti_dc
       ,enti_enti_guid,enti_enti_id,enti_category_guid) 
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) 
    """
    return dbDML.insert(lsql,enti)

#end insertEnti


def insertSynonym(p_data):
    lsql = """
        insert into synonyme ( syno_name, syno_enti_id) 
            values (?,?) 
        """
    return dbDML.insert(lsql, p_data)
# end insertSynonym

def  insertLovWrtb(pName,pherkunft = 'DOM'):
    return insertWrtb(wrtb=(None,pName, 'einfache Werteliste '
                                ,'LOV',pherkunft,None,None
                                ,None,None,None
                                ,None,None,None
                                ,None,None,None
                                ,None,None,'--'
                                ,date.today(),None,None,None))
#end insertLovWrtb


def insertdiagrammtyp(p_data):
    lsql="""
    insert into diagrammtypen(
    diat_bez   ,diat_uc ,diat_dc,diat_um ,diat_dm) 
        values (?,?,?,?,?)
    """
    return dbDML.insert(lsql,p_data)
#insertdiagrammtyp

def insertAttribute(pattr):
    lsql="""
    insert into attributes (attr_enti_id,attr_wrtb_id,attr_tech_name
    ,attr_anzname,attr_tooltip,attr_beschr
    ,attr_business_rule,attr_anz_rhflg,attr_deskriptor
    ,attr_pflichtattr,attr_historisiert,attr_wiederholt
    ,attr_sprachabhaengig,attr_verschluesselt,attr_uc
    ,attr_dc,attr_odm_guid,attr_bezi_id) 
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """
    #print (lsql,pattr)
    return dbDML.insert(lsql,pattr)
#end insertAttributes

#def insertDataTypes(pdaty):
#    lsql = """
#        insert into datatypes (daty_name,daty_grundtyp,daty_odm_guid)
#            values (?,?,?)
#        """
#    return dbDML.insert(lsql, pdaty)
# end insertDataTypes

def insertArc(parc):
    lsql = """
        insert into arcs 
          (arcs_name, arcs_enti_id, arcs_odm_guid
          ,arcs_uc   , arcs_dc ) 
            values (?,?,?,?,?)
        """
    return dbDML.insert(lsql, parc)

def insertBeziehung(pdata):
    lsql = """
        insert into beziehungen 
          (bezi_type, bezi_enti_id_von, bezi_assoc_von_zu
     ,bezi_pflicht_assoc_von_zu, bezi_hist_von_zu
    , bezi_enti_id_zu,bezi_assoc_zu_von
    , BEZI_PFLICHT_ASSOC_ZU_VON,bezi_hist_zu_von
    , bezi_odm_guid,bezi_uc, bezi_dc,bezi_name
    ,bezi_source_enti_guid,  bezi_target_enti_guid
    ) 
            values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
    return dbDML.insert(lsql, pdata)

def insertMelt(pdata):
    lsql = """
        insert into modellelem_typ(
    melt_kurzname,  melt_name
    ,melt_uc,  melt_dc) 
            values (?,?,?,?)
        """

    dbDML.insertmany(lsql, pdata)

# end insertDataTypes

def insertUDP(pData):
# bdeg_thema, bdeg_gruppe, bdeg_name, bdeg_default_value
# bdeg_beschreibung, bdeg_optional, bdeg_wrtb_id,
# bdeg_uc, bdeg_dc
    lsql = """
       insert into benudef_eigenschaft(
        bdeg_thema, bdeg_gruppe, bdeg_name, bdeg_default_value,
        bdeg_beschreibung, bdeg_optional, bdeg_wrtb_id,
         bdeg_uc, bdeg_dc) 
           values (?,?,?,?,?,?,?,?,?)
       """
    return dbDML.insert(lsql, pData)
#insertUDP

def insertModellElemTyp(pData):
    lsql= """insert into modelltyp_eigensch (mote_melt_id , mote_bdeg_id)
                values(?,?)"""
    return dbDML.insert(lsql, pData)
#insertModellElemTyp

def insertmodellelement(pData):
    #mode_wrtb_id,,  mode_attr_id
    #mode_buru_id,   mode_bezi_id,   mode_enti_id
    #mode_orge_id,   mode_melt_id,   mode_uc
    #mode_dc
    lsql = """insert into modellelement (mode_wrtb_id,  mode_attr_id
        ,mode_buru_id,   mode_bezi_id,   mode_enti_id
        ,mode_orge_id,   mode_syno_id, mode_tabl_id,mode_scha_id,mode_schn_id 
        ,mode_melt_id,   mode_uc, mode_dc)
        values(?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    return dbDML.insert(lsql, pData)
#insertmodellelement

def insertModeEnti(entiId):
    return insertmodellelement(pData=(None, None, None, None, entiId, None, None, None, None, None, dbLookup.meltLookup('ENTI'), '--', date.today()))
#insertModeEnti
def insertModeAttr(attrId):
    return insertmodellelement(pData=(None, attrId, None, None, None, None, None, None, None, None, dbLookup.meltLookup('ATTR'), '--', date.today()))
#insertModeAttr
def insertmodesyno(p_synid):
    return insertmodellelement(pData=(None, None, None, None, None, None, p_synid, None, None, None, dbLookup.meltLookup('SYNO'), '--', date.today()))
#insertModeAttr
def insertModeBezi(beziId):
    return insertmodellelement(pData=(None, None, None, beziId, None, None, None, None, None, None, dbLookup.meltLookup('BEZI'), '--', date.today()))
def insertModeScha(Id):
    return insertmodellelement(pData=(None, None, None,  None, None, None, None, None, Id, None, dbLookup.meltLookup('SCHA'), '--', date.today()))
def insertModeSchn(Id):
    return insertmodellelement(pData=(None, None, None, None, None, None, None, None, None, Id, dbLookup.meltLookup('SCHN'), '--', date.today()))
def insertModeTabl(Id):
    return insertmodellelement(pData=(None, None, None, None, None, None, None, Id, None, None, dbLookup.meltLookup('TABL'), '--', date.today()))
def insertModeWrtb(Id):
    return insertmodellelement(pData=(Id, None, None, None, None, None, None, None, None, None, dbLookup.meltLookup('WRTB'), '--', date.today()))
#insertModebezi
def insertmeltdiat(p_Data):
    lsql= """insert into
melt_diat(
    medi_diat_id, medi_melt_id,medi_uc,medi_dc
    ,medi_um,medi_dm   )
     values(?,?,?,?,?,?)
     """
    dbDML.insert(lsql,p_Data)
#insertmeltdiat

def insertBenudef_wert(pData):
    lsql= """insert into benudef_wert(
                bdwe_wert,  bdwe_mode_id,   bdwe_bdeg_id
                ,bdwe_uc,   bdwe_dc)
            values(?,?,?,?,?)"""
    dbDML.insert(lsql,pData)
#insertBenudef_wert

def insertSchluessel(pData):
    lsql = """
            insert into schluessel (schl_laufnr,    schl_name,  schl_odm_guid
                ,schl_uc,   schl_dc,    schl_enti_id) 
                values (?,?,?,?,?,?)
            """
    return dbDML.insert(lsql, pData)
#insertSchluessel

def insertSchlElem(pData):
    lsql = """
            insert into schluesselelement (scel_schl_id,   scel_attr_id
                                            ,scel_bezi_id,  scel_uc, scel_dc) 
                values (?,?,?,?,?)
            """
    return dbDML.insert(lsql, pData)
#insertSchlElem

def insertSprachtexte(pData):
    lsql = """insert into sprachtext (sptx_attrname,  sptx_text,  sptx_spra_id
                                ,sptx_mode_id, sptx_uc,   sptx_dc    ) 
                            values (?,?,?,?,?,?)
            """
    return dbDML.insertmany(lsql, pData)
#insertSprachtext

def insertelementdarst(pdata):
    lsql = """insert into 
    elementdarst(     
    eled_position_x,eled_position_y,eled_breite,eled_hoehe
    ,eled_deckkraft,eled_farbe,eled_randbreite,eled_randdeckkraft
    ,eled_randfarbe, eled_schriftgroesse, eled_schriftfarbe, eled_mode_id
    ,eled_diag_id, eled_index, eled_uc, eled_dc, eled_um
    , eled_dm)
    values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)    
    """
    return dbDML.insertmany(lsql, pdata)
#insertelementdarst

def insertelbezidarst(pdata):
    lsql = """insert into 
    beziehung_darst(
    beda_diag_id, beda_mode_id, beda_linienbreite, beda_liniefarbe
    ,beda_liniedeckkraft, beda_starttext_x, beda_starttext_y, beda_starttext_breite
    ,beda_starttext_hoehe, beda_endtext_x, beda_endtext_y, beda_endtext_breite
    ,beda_endtext_hoehe, beda_schriftfarbe, beda_schriftgroesse, beda_uc
    ,beda_dc, beda_um, beda_dm)
    values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)    
    """
    return dbDML.insert(lsql, pdata)
#insertbezidarst

def insertUdpEntity(entiId):
    dbDML.exec("""insert into benudef_wert(
                bdwe_wert,  bdwe_mode_id,   bdwe_bdeg_id
                ,bdwe_uc,   bdwe_dc)
                select NULL,mode_id,bdeg_id,enti_uc,enti_dc
                from entitaeten
                join modellelement on mode_enti_id = enti_id
                cross join (select mote_bdeg_id as bdeg_id
                             from modellelem_typ
                             join modelltyp_eigensch on mote_melt_id = melt_id
                             where melt_kurzname = 'ENTI')
                where enti_id = {}
            """ .format(entiId))
#insertUdpEntity
def insertUdpTable(ptablId):
    dbDML.exec("""insert into benudef_wert(
                bdwe_wert,  bdwe_mode_id,   bdwe_bdeg_id
                ,bdwe_uc,   bdwe_dc)
                select NULL,mode_id,bdeg_id,tabl_uc,tabl_dc
                from tabellen
                join modellelement on mode_tabl_id = tabl_id
                cross join (select mote_bdeg_id as bdeg_id
                             from modellelem_typ
                             join modelltyp_eigensch on mote_melt_id = melt_id
                             where melt_kurzname = 'TABL')
                where tabl_id = {}
            """ .format(ptablId))
#insertUdpTable
def insertdiagramm(p_data):
    lsql = """insert into
diagramme(
    diag_name,diag_diat_id,diag_odm_guid
    ,diag_legendx,diag_legendy,diag_uc
    ,diag_dc,diag_um,diag_dm )     
        values (?,?,?,?,?,?,?,?,?)
    """
    return dbDML.insert(lsql, p_data)
#insertdiagramme

def insertlinieseg(pdata):
    lsql = """insert into
linie_segment(
    lise_rhfg, lise_beda_id, lise_x, lise_y
    , lise_linientyp,lise_konnektor, lise_uc, lise_dc
    , lise_um,lise_dm,lise_winkel )
                            values (?,?,?,?,?,?,?,?,?,?,?)
    """
    return dbDML.insert(lsql, pdata)
#insertlinieseg

def insertUdpBezi(beziId):
    dbDML.exec("""insert into benudef_wert(
                bdwe_wert,  bdwe_mode_id,   bdwe_bdeg_id
                ,bdwe_uc,   bdwe_dc)
                select NULL,mode_id,bdeg_id,bezi_uc,bezi_dc
                from beziehungen
                join modellelement on mode_bezi_id = bezi_id
                cross join (select mote_bdeg_id as bdeg_id
                             from modellelem_typ
                             join modelltyp_eigensch on mote_melt_id = melt_id
                             where melt_kurzname = 'BEZI')
                where bezi_id = {}
            """ .format(beziId))
#insertUdpBezi


def insertUdpAttr(attrId):
    dbDML.exec("""insert into benudef_wert(
                bdwe_wert,  bdwe_mode_id,   bdwe_bdeg_id
                ,bdwe_uc,   bdwe_dc)
                select NULL,mode_id,bdeg_id,attr_uc,attr_dc
                from attributes
                join modellelement on mode_attr_id = attr_id
                cross join (select mote_bdeg_id as bdeg_id
                             from modellelem_typ
                             join modelltyp_eigensch on mote_melt_id = melt_id
                             where melt_kurzname = 'ATTR')
                where attr_id = {}
            """ .format(attrId))
#insertUdpAttr

def insertgeschaeftsbereich(pdata):
    lsql = """insert into geschaeftsbereich 
            (gber_name, gber_beschreibung, gber_zweck
            , gber_uc, GBER_DC, GBER_UM
            , gber_dm)
                   values (?,?,?,?,?,?,?)
           """
    return dbDML.insert(lsql, pdata)
#insertgeschaeftsbereich
def insertbereich_darst(pdata):
    lsql = """insert into bereich_elemdarst 
                (BELD_MELT_ID, BELD_GBER_ID, BELD_BREITE
                , BELD_HOEHE, BELD_DECKKRAFT, BELD_FARBE
                , BELD_RANDBREITE, BELD_RANDDECKKRAFT, BELD_RANDFARBE
                , BELD_SCHRIFTGROESSE, BELD_SCHRIFTFARBE, BELD_UC
                , BELD_DC, BELD_UM, BELD_DM)
                   values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
           """
    return dbDML.insert(lsql, pdata)
#insertbereich_darst

