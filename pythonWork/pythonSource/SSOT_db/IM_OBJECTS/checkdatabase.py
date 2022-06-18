from SSOT_db.SQL_INFRA import dbConnect
from .languagetext import Languagetext

def checkdatabase():
    """
    checks special consistency of database
    - Uniqueness of translated texts
    - mismatch between text-in object vs default-lang-text in languagetexts

    :return: [error,...]
    """
    assert dbConnect.isopenDB(),"Database must be open"
    errorlist=[]
    errorlist += Languagetext.checkMLuk()
    errorlist += Languagetext.checkMLdefaultentry()
    return errorlist