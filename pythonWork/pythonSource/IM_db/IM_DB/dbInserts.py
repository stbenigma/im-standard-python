from IM_DB import dbDML,dbLookup,dbParam
from IM_ODM import odmParam
from datetime import date

def  insertEnti(enti):
    lsql="""
    insert into entitaeten 
       (enti_odm_guid ,enti_augb_id,enti_tech_name     
       ,enti_name,enti_beschr     ,enti_tooltip    
       ,enti_kurzname   ,enti_prefix             ,enti_beispiele          
       ,enti_erw_tupel         ,enti_uc ,enti_dc
       ,enti_enti_guid,enti_enti_id) 
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?) 
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

def  insertWrtb(wrtb):
    #print ('InsertWrtb',wrtb)
    lsql="""
    insert into wertebereiche 
       (wrtb_business_rule  ,wrtb_name  ,wrtb_beschr    
       ,wrtb_typ,        wrtb_zpkt_minwert   ,wrtb_zpkt_maxwert          
       ,wrtb_zpkt_granularitaet,        wrtb_text_maxlng    ,wrtb_text_syntaxregel
       ,        wrtb_num_maxwert        ,wrtb_num_minwert           ,wrtb_num_vorkstellen       
        ,wrtb_num_nachkstellen          ,wrtb_num_rundng_einh,        wrtb_num_pheh_id  
          ,wrtb_bin_inhalttyp,        wrtb_bin_spfo_id    ,wrtb_uc  
            ,wrtb_dc        ,wrtb_odm_guid ,wrtb_datatype_ref)
        values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) 
    """
    return dbDML.insert(lsql,wrtb)

#end insertWrtb
def insertwrtbgruppe(wbgr):
    lsql="""
    insert into wertebereichgruppen 
       (wbgr_wrtb_id_gruppe, wbgr_name,wbgr_beschr
       ,WBGR_WRTB_ID_MEMBER,wbgr_type_ref,WBGR_UC
       ,WBGR_DC,WBGR_UM, wbgr_dm)
        values (?,?,?,?,?,?,?,?,?) 
    """
    return dbDML.insert(lsql,wbgr)

#insertwrtbgruppe

def  insertLovWrtb(pName):
    return insertWrtb(wrtb=(None,pName, 'einfache Werteliste '
                                ,'LOV',None,None
                                ,None,None,None
                                ,None,None,None
                                ,None,None,None
                                ,None,None,'--'
                                ,date.today(),None,None))
#end insertLovWrtb

def insertVorgabewert(pvgwt):
    lsql="""
    insert into vorgabewerte (vgwt_wert ,    vgwt_sortrhfg,
        vgwt_wrtb_id,   vgwt_anzeige   ,    vgwt_beschr
        ,vgwt_uc, vgwt_dc) 
        values (?,?,?,?,?,?,?)
    """
    return dbDML.insert(lsql,pvgwt)
#end insertVorgabewert
def insertdiagrammtyp(p_data):
    lsql="""
    insert into diagrammtypen(
    diat_bez   ,diat_uc ,diat_dc,diat_um ,diat_dm) 
        values (?,?,?,?,?)
    """
    return dbDML.insert(lsql,p_data)
#end insertVorgabewert

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

def insertDataTypes(pdaty):
    lsql = """
        insert into datatypes (daty_name,daty_grundtyp,daty_odm_guid) 
            values (?,?,?)
        """
    return dbDML.insert(lsql, pdaty)
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
    , BEZI_PFLICHT_ASSOC_ZU_VON,bezi_hist_zu_von, bezi_arcs_id
    , bezi_odm_guid,bezi_uc, bezi_dc,bezi_name) 
            values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
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
        ,mode_orge_id,   mode_syno_id ,mode_melt_id,   mode_uc
        ,mode_dc)
        values(?,?,?,?,?,?,?,?,?,?)"""
    return dbDML.insert(lsql, pData)
#insertmodellelement

def insertModeEnti(entiId):
    return insertmodellelement(pData=(None, None, None, None, entiId, None, None, dbLookup.meltLookup('ENTI'), '--', date.today()))
#insertModeEnti
def insertModeAttr(attrId):
    return insertmodellelement(pData=(None, attrId, None, None, None, None, None, dbLookup.meltLookup('ATTR'), '--', date.today()))
#insertModeAttr
def insertmodesyno(p_synid):
    return insertmodellelement(pData=(None, None, None, None, None, None, p_synid, dbLookup.meltLookup('SYNO'), '--', date.today()))
#insertModeAttr
def insertModeBezi(beziId):
    return insertmodellelement(pData=(None, None, None, beziId, None, None, None, dbLookup.meltLookup('BEZI'), '--', date.today()))
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

def insertSprache(pData):
    lsql = """insert into sprachen (spra_iso_name, spra_iso_code2, spra_iso_code3
                                  ,spra_ist_textsprache, spra_ist_modellsprache, spra_spra_id
                                  , spra_uc,spra_dc) 
                            values (?,?,?,?,?,?,?,?)
            """
    return dbDML.insert(lsql, pData)
#insertSprache

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
    ,eled_diag_id, eled_uc, eled_dc, eled_um
    , eled_dm)
    values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)    
    """
    return dbDML.insertmany(lsql, pdata)
#insertelementdarst

def insertelbezidarst(p_data):
    lsql = """insert into 
beziehung_darst(
    beda_diag_id, beda_mode_id, beda_linienbreite, beda_liniefarbe
    ,beda_liniedeckkraft, beda_starttext_x, beda_starttext_y, beda_starttext_breite
    ,beda_starttext_hoehe, beda_endtext_x, beda_endtext_y, beda_endtext_breite
    ,beda_endtext_hoehe, beda_schriftfarbe, beda_schriftgroesse, beda_uc
    ,beda_dc, beda_um, beda_dm)
    values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)    
)	          """
    return dbDML.insertmany(lsql, p_Data)
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

def insertlinieseg(p_data):
    lsql = """insert into
linie_segment(
    lise_rhfg, lise_beda_id, lise_x, lise_y
    , lise_linientyp,lise_konnektor, lise_uc, lise_dc
    , lise_um,lise_dm 
                            values (?,?,?,?,?,?,?,?,?,?)
    """
    return dbDML.insert(lsql, p_Data)
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

def insertSprachtexte(p_texte, p_modeid, p_defaultlang=None):
#    sprachtexte = [[vonText,creby,crety,'TEXT_FROM']
#                  ,[zuText,creby,crety,'TEXT_TO']]

    p_defaultlang = dbParam.dbDefaultLang if p_defaultlang is None else p_defaultlang
    values = [v for v in p_texte]
    # (values)
    lsql= """insert into sprachtexte 
                    (sptx_attrname,  sptx_text
                   ,sptx_mode_id, sptx_uc, sptx_dc
                   , sptx_spra_id)
                  select  attrname, case  when defaultlang = spra_iso_code2 then '' 
                                    else '*'|| defaultlang ||'* ' end
                                    || ? text
                    ,modeid, ? uc,? dc, spra_id
                  from sprachen
                  cross join (select '{}' modeid, '{}' defaultlang,  ? attrname)
                  where not exists 
                    (select 1 from sprachtexte
                        where sptx_spra_id = spra_id
                         and sptx_mode_id = modeid
                         and  sptx_attrname = attrname
                    ) 
                """.format( p_modeid,p_defaultlang)
    dbDML.execmany(lsql, values)

# die Originalnamen werden überschrieben
    l_sql = """ update sprachtexte
                set sptx_text = ?
                   ,sptx_um = ?
                   ,sptx_dm = ?
                where sptx_spra_id = {}
                and sptx_attrname = ?
                and sptx_mode_id = {}
                """.format(dbLookup.spraLookup(p_defaultlang),p_modeid)
    dbDML.execmany(l_sql, values)
#insertSprachTexte
def insertSprachtext(pdata):
    #print (pdata)
    lsql= """insert into sprachtexte 
                    (sptx_attrname,  sptx_text
                   ,sptx_mode_id, sptx_uc, sptx_dc
                   , sptx_spra_id)
                  values (?,?,?,?,?,?)
          """
    dbDML.insertmany(lsql, pdata)
#insertSprachText
def insertprojekt(pdata):
    lsql = """insert into projekt 
                        (proj_name ,  proj_uc, proj_dc
                        ,proj_sprachen, proj_akt_sprache)
                      values (?,?,?,?,?)
              """
    return dbDML.insert(lsql, pdata)
#insertprojekt
