from datetime import date
from IM_DB import dbDML,logging
from IM_OBJECTS import *

def  insertLovWrtb(pName,pherkunft = Domain.DERIVED):
    doma = Domain()
    doma.doma_name = pName
    doma.doma_beschr = 'einfache Werteliste'
    doma.doma_typ = Domain.LOV
    doma.doma_origin= pherkunft
    doma.doma_uc = 'system'
    doma.doma_dc = date.today()
    return doma.insert()


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

def insertUdpTable(ptablId):
    dbDML.exec("""insert into benudef_wert(
                bdwe_wert,  bdwe_mode_id,   bdwe_bdeg_id
                ,bdwe_uc,   bdwe_dc)
                select NULL,mode_id,bdeg_id,tabl_uc,tabl_dc
                from tabellen
                join modelelement on mode_tabl_id = tabl_id
                cross join (select mote_bdeg_id as bdeg_id
                             from modelelem_type
                             join modelltyp_eigensch on mote_melt_id = melt_id
                             where melt_shortname = 'TABL')
                where tabl_id = {}
            """ .format(ptablId))
#insertUdpTable
def insertUdpColumn(pschaId):
    dbDML.exec("""insert into benudef_wert(
                bdwe_wert,  bdwe_mode_id,   bdwe_bdeg_id
                ,bdwe_uc,   bdwe_dc)
                select NULL,mode_id,bdeg_id,scha_uc,scha_dc
                from main.schnittstelle_attrs
                join modelelement on mode_scha_id = scha_id
                cross join (select mote_bdeg_id as bdeg_id
                             from modelelem_type
                             join modelltyp_eigensch on mote_melt_id = melt_id
                             where melt_shortname = 'INTF')
                where scha_id = {}
            """ .format(pschaId))
#insertUdpColumn

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
                from RELATIONS
                join modelelement on mode_rela_id = rela_id
                cross join (select mote_bdeg_id as bdeg_id
                             from modelelem_type
                             join modelltyp_eigensch on mote_melt_id = melt_id
                             where melt_shortname = 'RELA')
                where rela_id = {}
            """ .format(beziId))
#insertUdpBezi


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

