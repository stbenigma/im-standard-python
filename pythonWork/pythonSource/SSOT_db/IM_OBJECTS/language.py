from .baseobject import Baseobject
from SSOT_db.SQL_INFRA import dbDML
from SSOT_infra import Parameter,nvl


def expandiso2(plang:str):
    lang = plang.lower() if plang else None
    exp = Parameter.SUPPORTEDLANGUAGES.get(lang)
    if  exp is not None :
        return exp[0:2]
    else:
        return [lang,lang]

class Language(Baseobject):
    _tablename:str ='languages'
    _prefix:str ='lang'
    _idcolname: str = _prefix + '_id'
    _columnlist = dict()
    _defaultorderby = "lang_iso_code2"

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.lang_is_text_lang = nvl(self.lang_is_text_lang,'TRUE')
        self.lang_is_base_lang = nvl(self.lang_is_base_lang,'FALSE')
        defname,defiso3 = expandiso2(self.lang_iso_code2)
        self.lang_iso_code3 = nvl(self.lang_iso_code3,defiso3)
        self.lang_iso_name = nvl(self.lang_iso_name,defname)

    @classmethod
    def getdefaultlang(cls):
        lDefLangs = Language.select(pwhere=("""lang_is_base_lang = ?""", 'TRUE'))
        if (lDefLangs is None): return None
        if (len(lDefLangs) == 0): return None
        if (len(lDefLangs) > 1): raise Exception("More than one model-Language defined")
        return lDefLangs[0]

    @classmethod
    def getdefaultlangid(cls):
        return cls.getdefaultlang().lang_id

    @staticmethod
    def getlanguagecodes():
        lDefLangs = Language.select(porderby="lang_iso_code2")
        langs = [lang.lang_iso_code2 for lang in lDefLangs]
        return langs


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

    @classmethod
    def deleteunused(cls):
        result = cls.delete(pwhere="""not exists(select 1 from LANG_TEXTS
                            where lgtx_lang_id = lang_id
                            )""")
        # remove dangling references to deleted languages
        dbDML.exec("""update LANGUAGES set lang_lang_id = null 
            where lang_lang_id not in (select lang_id from LANGUAGES)""")
        return result
    #deleteunused

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
        cnt = dbDML.exec("""update languages  
        set lang_lang_id = 
            case when lang_is_base_lang  = 'TRUE'
            then NULL
            else (select sp2.lang_id 
                from languages sp2 
                where sp2.lang_is_base_lang = 'TRUE'
                )
            end
        where lang_lang_id is NULL""")
        return cnt
#Language


