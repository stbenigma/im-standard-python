from IM_DB import dbDML

def doLookup(pguid,psql):
    if (pguid == None):
        return None
    else:
        return dbDML.lookup(psql . format(pguid))
    #fi
#doLookup

def entiID (pguid):
    return doLookup(pguid,'select enti_id from entitaeten where enti_odm_guid ="{}"')
#entiId

def beziId (pguid):
    return doLookup(pguid,'select bezi_id from beziehungen where bezi_odm_guid ="{}"')
#beziId

def arcsID (pguid):
    return doLookup(pguid,'select arcs_id from arcs where arcs_odm_guid ="{}"')
#arcsId

def attrID (pguid):
    return doLookup(pguid,'select attr_id from attributes where attr_odm_guid ="{}"')
#attrId

def datyLookupGrundTyp (pguid):
    return doLookup(pguid,'select daty_grundtyp from datatypes where daty_odm_guid ="{}"')
#datyLookup

def wrtbLookup (pguid):
    return doLookup(pguid,'select wrtb_id from wertebereiche where wrtb_odm_guid = "{}"' )
#wrtbLookup

def meltLookup(pkurzname):
    return doLookup(pkurzname, 'select melt_id from modellelem_typ where melt_kurzname = "{}"')
# MeltLookup

def modeAttrLookup(attrId):
    return doLookup(attrId, 'select mode_id from modellelement where mode_attr_id = "{}"')
# modeAttrLookup
def modeEntiLookup(entiId):
    return doLookup(entiId, 'select mode_id from modellelement where mode_enti_id = "{}"')
# modeEntiLookup

def bdegLookup(pname):
        return doLookup(pname, 'select bdeg_id from benudef_eigenschaft where bdeg_name = "{}"')
# MeltLookup

def wrtbLookupByName(pname):
    return doLookup(pname,'select wrtb_id from wertebereiche where upper(wrtb_name) = upper("{}")' )
#wrtbLookup

def spraLookup(piso):
    if (len(piso) == 2):
        return doLookup(pname, """select spra_id from sprachen 
                                where spra_iso_code2 = lower("{}")""")
    elif (len(piso) == 3):
        return doLookup(pname, """select spra_id from sprachen 
                            where spra_iso_code3 = lower("{}")""")
    else:
        return None
    #fi
#spraLookup
