from .baseobject import Baseobject

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
#Sprache

def liesDefaultLang():
    lDefLang = Sprache().select(pwhere="""spra_ist_modellsprache = 'TRUE'""")
    if (lDefLang is None): return None
    if (len(lDefLang) == 0): return None
    return lDefLang[0].spra_iso_code2
#liesDefaultLang

def spraLookup(piso):
    if (len(piso) == 2):
        colname = 'spra_iso_code2'
    elif (len(piso) == 3):
        colname = 'spra_iso_code3'
    else:
        return None
    #fi
    try:
        data = Sprache.select(pwhere="""{} = lower("{}")""".format(colname,piso))
        return data[0].spra_id
    except: return None
#spraLookup

def sprachen(p_id,p_attrname):
    return doLookup(p_id, """select {} from sprachen 
                                where spra_id = {}""".format(p_attrname,'{}'))
#spraLookup
