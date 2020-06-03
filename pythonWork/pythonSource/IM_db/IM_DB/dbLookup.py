from IM_DB import dbDML
import sqlite3

def doLookup(pguid,psql,withnotfound=False):
    if (pguid == None):
        lretval =  None
    else:
        try:
            lretval = dbDML.lookup(psql . format(pguid))
        except sqlite3.Error as er:
            if withnotfound:
                lretval = None
            else:
                raise er
    #fi
    return lretval
#doLookup

def beziId (pguid):
    return doLookup(pguid,'select bezi_id from beziehungen where bezi_odm_guid ="{}"')
#beziId

def arcsID (pguid):
    return doLookup(pguid,'select arcs_id from arcs where arcs_odm_guid ="{}"')
#arcsId

def diatid (p_name):
    return doLookup(p_name,'select diat_id from diagrammtypen where upper(diat_bez) =upper("{}")')
#diatid

def bdegLookup(pname):
        return doLookup(pname, 'select bdeg_id from benudef_eigenschaft where bdeg_name = "{}"'
                        ,withnotfound=True)
# bdegLookup

