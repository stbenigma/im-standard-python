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


def diatid (p_name):
    return doLookup(p_namex,'select diat_id from diagrammtypen where upper(diat_bez) =upper("{}")')
#diatid


