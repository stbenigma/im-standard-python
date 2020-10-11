from datetime import date
from IM_DB import dbDML,logmessages
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

