from SSOT_db.SQL_INFRA import dbConnect
from SSOT_db.IM_OBJECTS import Languagetext, ColAttrMap, Modelelement

def checkdatabase():
    """
    checks special consistency of database
    - Uniqueness of translated texts
    - mismatch between text-in object vs default-lang-text in languagetexts
    - tangling modelelements

    :return: [error,...]
    """
    assert dbConnect.isopenDB(),"Database must be open"
    errorlist=[]
    errorlist += Languagetext.checkMLuk()
    errorlist += Languagetext.checkMLdefaultentry()
    errorlist += ColAttrMap.checksuperentitymap()
    errorlist += Modelelement.selecttanglingmode()
    #print (Modelelement.selecttanglingmode())
    return errorlist

