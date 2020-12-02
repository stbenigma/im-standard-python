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
    dbDML.exec("""insert into UDP_VALUES(
                udpv_value,  udpv_mode_id,   udpv_udpr_id
                ,udpv_uc,   udpv_dc)
                select NULL,tabl_id,udpr_id,tabl_uc,tabl_dc
                from tables
                cross join (select metp_udpr_id as udpr_id
                             from modelelem_type
                             join modelemtype_properties on metp_melt_id = melt_id
                             where melt_shortname = '{}')
                where tabl_id = {}
            """ .format(Modelelemtype.TABL,ptablId))
#insertUdpTable
def insertUdpColumn(pcoluId):
    dbDML.exec("""insert into UDP_VALUES(
                udpv_value,  udpv_mode_id,   udpv_udpr_id
                ,udpv_uc,   udpv_dc)
                select NULL,colu_id,udpr_id,colu_uc,colu_dc
                from columns
                cross join (select metp_udpr_id as udpr_id
                             from modelelem_type
                             join modelemtype_properties on metp_melt_id = melt_id
                             where melt_shortname = '{}')
                where colu_id = {}
            """ .format(Modelelemtype.INTF, pcoluId))
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

