from .baseobject import Baseobject
from IM_DB import dbDML

class Sprache(Baseobject):
    _tablename:str ='sprachen'
    _prefix:str ='spra'
    _columnlist:list = ['spra_id', 'spra_iso_name', 'spra_iso_code2', 'spra_iso_code3', 'spra_ist_textsprache'
                    , 'spra_ist_modellsprache', 'spra_spra_id', 'spra_uc', 'spra_dc', 'spra_um', 'spra_dm']

    def __init__(self):
        super().__init__(tablename=Sprache._tablename,prefix=Sprache._prefix
                        ,columnlist = Sprache._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Sprache._tablename
                               , psql="""
CREATE TABLE sprachen(
        spra_id                integer primary key autoincrement,
        spra_iso_name          varchar(60) NOT NULL,
        spra_iso_code2         CHAR(2) NOT NULL,
        spra_iso_code3         CHAR(3) NOT NULL,
        spra_ist_textsprache   varchar(5) NOT NULL,
        spra_ist_modellsprache   varchar(5) NOT NULL,
        spra_spra_id           integer,
        spra_uc                varchar(30) NOT NULL,
        spra_dc                varchar(30) NOT NULL,
        spra_um                varchar(30) ,
        spra_dm                varchar(30),
        constraint spra_txt_bool CHECK(spra_ist_textsprache IN(
            'FALSE',
            'TRUE'
        )),
        constraint spra_mod_bool CHECK(spra_ist_modellsprache IN(
            'FALSE',
            'TRUE'
        )),
        constraint spra_iso3_low CHECK(spra_iso_code3 = lower(spra_iso_code3)),
        constraint spra_iso2_low CHECK(spra_iso_code2 = lower(spra_iso_code2)),
    	constraint spra_iso_uk unique (spra_iso_name),
    	constraint spra_iso2_uk unique (spra_iso_code2),
    	constraint spra_iso3_uk unique (spra_iso_code3)
    )"""
                            )
    @staticmethod
    def delete():
        Baseobject.delete(Sprache._tablename)

    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(pclass=Sprache
                                ,pwhere=pwhere,porderby=porderby)
    @staticmethod
    def liesdefaultlang():
        lDefLangs = Sprache.select(pwhere="""spra_ist_modellsprache = 'TRUE'""")
        if (lDefLangs is None): return None
        if (len(lDefLangs) == 0): return None
        return lDefLangs[0]
    #liesdefaultlang

    @staticmethod
    def liesdeflangid():
        ldeflang = Sprache.liesdefaultlang()
        if (ldeflang is None): return None
        else: return ldeflang.spra_id
    # liesdeflangid

    @staticmethod
    def liesdeflangiso2():
        ldeflang = Sprache.liesdefaultlang()
        if (ldeflang is None): return None
        else: return ldeflang.spra_iso_code2
    #liesdeflangiso2

    @staticmethod
    def deleteunused():
        dbDML.exec("""delete from sprachen
                        where not exists(select 1 from sprachtexte
                                       where sptx_spra_id = spra_id
                                       )
                    """)
    #deleteunsed

    @staticmethod
    def spraidlookup(piso):
        if (len(piso) == 2): colname = 'spra_iso_code2'
        elif (len(piso) == 3): colname = 'spra_iso_code3'
        else: return None
        #fi
        try:
            sprachen = Sprache.select(pwhere="""{} = lower("{}")""".format(colname,piso))
            return sprachen[0].spra_id
        except: return None
    #spraidlookup

    #def sprachen(p_id,p_attrname):
    ##    return doLookup(p_id, """select {} from sprachen
    #                                where spra_id = {}""".format(p_attrname,'{}'))
    #spraLookup

    @staticmethod
    def setmodellang(pmodellang):
        dbDML.exec("""update sprachen 
                        set spra_ist_modellsprache = 
                            case lower(spra_iso_code2) 
                            when '{}' then 'TRUE'
                            else 'FALSE'
                            end
                    """.format(pmodellang))
    #setmodellang

    @ staticmethod
    def setreplacementlang():
        #currently modellang is always replacement lang
        dbDML.exec("""update sprachen  
        set spra_spra_id = 
            case when spra_ist_modellsprache  = 'TRUE'
            then NULL
            else (select sp2.spra_id 
                from sprachen sp2 
                where sp2.spra_ist_modellsprache = 'TRUE'
                )
            end
        """)
    #setreplacementlang
#Sprache


