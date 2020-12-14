from .baseobject import Baseobject
from datetime import date
from IM_DB import dbDML

class Language(Baseobject):
    _tablename:str ='languages'
    _prefix:str ='lang'
    _columnlist = []

    def __init__(self,pname=None,piso2=None,piso3=None):
        if (len(Language._columnlist) == 0): Language._columnlist = Baseobject.gettablecolumns(Language._tablename)
        super().__init__(tablename=Language._tablename, prefix=Language._prefix)
        self.lang_iso_name = pname
        self.lang_iso_code2 = piso2
        self.lang_iso_code3 =  piso3
        self.lang_is_text_lang ='TRUE'
        self.lang_is_base_lang = 'FALSE'
        self.lang_uc ='stb'
        self.lang_dc = date.today()

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Language._tablename
                               , psql="""
CREATE TABLE LANGUAGES
    (
     LANG_ID INTEGER NOT NULL primary key autoincrement,
     LANG_ISO_NAME VARCHAR (60) NULL ,
     LANG_ISO_CODE2 CHAR (2) NOT NULL CONSTRAINT LANG_ISO2_CHK CHECK ( LANG_ISO_CODE2 = lower(LANG_ISO_CODE2) ) ,
     LANG_ISO_CODE3 CHAR (3) NOT NULL CONSTRAINT LANG_ISO3_CHK CHECK ( LANG_ISO_CODE3 = lower(LANG_ISO_CODE3) ) ,
     LANG_IS_TEXT_LANG VARCHAR (5) NOT NULL CHECK ( LANG_IS_TEXT_LANG IN ('FALSE', 'TRUE') ) ,
     LANG_IS_BASE_LANG VARCHAR (5) NOT NULL CHECK ( LANG_IS_BASE_LANG IN ('FALSE', 'TRUE') ) ,
     LANG_LANG_ID integer NULL ,
     LANG_UC VARCHAR(30) NULL  ,
     LANG_DC VARCHAR (30) NOT NULL ,
     LANG_UM VARCHAR (30) NULL ,
     LANG_DM VARCHAR (30) NULL
    ,CONSTRAINT LANG_ISO_NAME_UN UNIQUE (LANG_ISO_NAME ASC)
      ,CONSTRAINT LANG_ISO_CODE2_UN UNIQUE (LANG_ISO_CODE2 ASC)
      ,CONSTRAINT LANG_ISO_CODE3_UN UNIQUE (LANG_ISO_CODE3 ASC)
      ,CONSTRAINT LANG_REPLACE_FK FOREIGN KEY      (     LANG_LANG_ID)
      REFERENCES LANGUAGES      (     LANG_ID )      ON DELETE SET NULL
  )"""
           )
    @staticmethod
    def delete():
        Baseobject.delete(Language._tablename)

    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(pclass=Language
                                ,pwhere=pwhere,porderby=porderby)
    @staticmethod
    def getdefaultlang():
        lDefLangs = Language.select(pwhere="""lang_is_base_lang = 'TRUE'""")
        if (lDefLangs is None): return None
        if (len(lDefLangs) == 0): return None
        return lDefLangs[0]
    #getdefaultlang

    def getreplacementlang(self):
        return Language.select(pwhere='lang_id={}'.format(self.lang_lang_id))[0]

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
            languages = Language.select(pwhere="""{} = lower("{}")""".format(colname, piso))
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
        #currently modellang is always replacement lang
        dbDML.exec("""update languages  
        set lang_lang_id = 
            case when lang_is_base_lang  = 'TRUE'
            then NULL
            else (select sp2.lang_id 
                from languages sp2 
                where sp2.lang_is_base_lang = 'TRUE'
                )
            end
        """)
    #setallreplacementlang
#Language


