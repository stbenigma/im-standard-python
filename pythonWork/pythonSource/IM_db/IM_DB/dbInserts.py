from datetime import date
from IM_DB import dbDML,logmessages
from IM_OBJECTS import *

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
            """ .format(Modelelemtype.COLU, pcoluId))
#insertUdpColumn


