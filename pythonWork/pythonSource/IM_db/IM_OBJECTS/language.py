from .baseobject import Baseobject
from datetime import date
from IM_DB import dbDML

class Language(Baseobject):
    _tablename:str ='languages'
    _prefix:str ='lang'
    _columnlist = []
    _defaultorderby = "lang_iso_code2"

    def __init__(self,pname=None,piso2=None,piso3=None):
        if (len(Language._columnlist) == 0): Language._columnlist = Baseobject.gettablecolumns(Language._tablename)
        super().__init__()
        self.lang_iso_name = pname
        self.lang_iso_code2 = piso2
        self.lang_iso_code3 =  piso3
        self.lang_is_text_lang ='TRUE'
        self.lang_is_base_lang = 'FALSE'
        self.lang_uc ='stb'
        self.lang_dc = date.today()


    @staticmethod
    def getdefaultlang():
        lDefLangs = Language.select(pwhere=("""lang_is_base_lang = ?""", 'TRUE'))
        if (lDefLangs is None): return None
        if (len(lDefLangs) == 0): return None
        if (len(lDefLangs) > 1): raise Exception("More than one model-Language defined")
        return lDefLangs[0]
    #getdefaultlang

    def getreplacementlang(self):
        return Language.select(pwhere=('lang_id=?', self.lang_lang_id))[0]

    @staticmethod
    def liesdeflangid():
        ldeflang = Language.getdefaultlang()
        if (ldeflang is None): return None
        else: return ldeflang.lang_id
    # liesdeflangid

    @staticmethod
    def liesdeflangiso2():
        ldeflang = Language.getdefaultlang()
        if (ldeflang is None): return None
        else: return ldeflang.lang_iso_code2
    #liesdeflangiso2

    @staticmethod
    def deleteunused():
        dbDML.exec("""delete from languages
                        where not exists(select 1 from LANG_TEXTS
                                       where lgtx_lang_id = lang_id
                                       )
                    """)
    #deleteunsed

    @staticmethod
    def spraidlookup(piso):
        if (len(piso) == 2): colname = 'lang_iso_code2'
        elif (len(piso) == 3): colname = 'lang_iso_code3'
        else: return None
        #fi
        try:
            languages = Language.select(pwhere=("""{} = lower(?)""".format(colname), piso))
            return languages[0].lang_id
        except: return None
    #spraidlookup

    @staticmethod
    def setmodellang(pmodellang):
        dbDML.exec("""update languages 
                        set lang_is_base_lang = 
                            case lower(lang_iso_code2) 
                            when '{}' then 'TRUE'
                            else 'FALSE'
                            end
                    """.format(pmodellang))
    #setmodellang

    @ staticmethod
    def setallreplacementlang():
        #make sure everybody has a replacementlanguage
        dbDML.exec("""update languages  
        set lang_lang_id = 
            case when lang_is_base_lang  = 'TRUE'
            then NULL
            else (select sp2.lang_id 
                from languages sp2 
                where sp2.lang_is_base_lang = 'TRUE'
                )
            end
        where lang_lang_id is NULL""")
    #setallreplacementlang
#Language


