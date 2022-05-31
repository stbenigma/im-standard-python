from SSOT_db import existsDB
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_db.IM_OBJECTS import Language

def dblanguages(pdbfilepath,pmodellang=None,planguages=None):
    """
    if db exists, read defaultlanguage and languagelist as strings
    if not, return the 2 paramaeters
    :param pdbfilepath: database filepath
    :param pmodellang: default modellang if no db
    :param planguages: default languages if no db
    :return: modellang, languages
    """

    if existsDB(pdbfilepath):
        dbConnect.push() #make sure to have my private connection
        #get language parameters out of db and ignore parameters if db exists
        dbConnect.openDB(pfilepath=pdbfilepath,pversioncheck=False)
        modellang = Language.getdefaultlang().lang_iso_code2
        languages = ','.join(l for l in Language.getlanguagecodes())
        dbConnect.pop()
    else:
        modellang = pmodellang
        languages = planguages

    return modellang,languages
