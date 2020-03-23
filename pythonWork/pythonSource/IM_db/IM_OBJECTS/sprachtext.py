from IM_DB import dbDML
from .baseobject import Baseobject
from .sprache import spraLookup

class Sprachtext(Baseobject):
    _tablename:str ='sprachtexte'
    _prefix:str ='sptx'
    _columnlist:list = ['sptx_id', 'sptx_attrname', 'sptx_text', 'sptx_spra_id'
                        , 'sptx_mode_id', 'sptx_uc', 'sptx_dc', 'sptx_um', 'sptx_dm']

    def __init__(self):
        super().__init__(tablename=Sprachtext._tablename,prefix=Sprachtext._prefix
                        ,columnlist = Sprachtext._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Sprachtext._tablename
                               , psql="""
CREATE TABLE sprachtexte(
        sptx_id           integer primary key autoincrement,
    	sptx_attrname	  varchar(30) NOT NULL,
        sptx_text         varchar(4000) ,
        sptx_spra_id      integer,
        sptx_mode_id      integer NOT NULL,
        sptx_uc           varchar(30) NOT NULL,
        sptx_dc           varchar(30) NOT NULL,
        sptx_um           varchar(30) ,
        sptx_dm           varchar(30),
    	constraint sptx_attrnameUC check(sptx_attrname = upper(sptx_attrname)),
    	constraint sptx_uk unique (sptx_attrname,sptx_spra_id,sptx_mode_id),
        CONSTRAINT sptx_mode_fk FOREIGN KEY(sptx_mode_id)
    									   REFERENCES modellelement(mode_id),
    	CONSTRAINT sptx_spra_fk FOREIGN KEY(sptx_spra_id)
    									   REFERENCES sprachen(spra_id)	
        )"""
                            )
    @staticmethod
    def delete():
        Baseobject.delete(Sprachtext._tablename)

    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(pclass=Sprachtext
                                ,pwhere=pwhere,porderby=porderby)
#Sprachtext

def fuelledefaulttexte(plang):
    dbDML.exec("""insert into sprachtexte 
                    (sptx_attrname,  sptx_text
                   ,sptx_mode_id, sptx_uc, sptx_dc
                   , sptx_spra_id)
                  select * from 
                    (select 'ENTI_NAME' attrname, enti_name text 
                        ,mode_id,enti_uc,enti_dc
                    from modellelement
                    join entitaeten on enti_id = mode_enti_id
                    union all
                   select 'ENTI_COMMENT' attrname, enti_beschr text 
                        ,mode_id,enti_uc,enti_dc
                    from modellelement
                    join entitaeten on enti_id = mode_enti_id                    
                    union all
                   select 'ENTI_SYNONYM' attrname, group_concat(syno_name,', ') text 
                        ,enti_id,enti_uc,enti_dc
                    from modellelement
                    join synonyme on syno_id = mode_syno_id
                    join entitaeten on enti_id = syno_enti_id
                    group by enti_id,enti_uc,enti_dc                    
                    union all
                   select 'ATTR_COMMENT' attrname, attr_beschr text 
                        ,mode_id,attr_uc,attr_dc
                    from modellelement
                    join attributes on attr_id = mode_attr_id    
                    union all                
                   select 'ATTR_NAME' attrname, attr_anzname text 
                        ,mode_id,attr_uc,attr_dc
                    from modellelement
                    join attributes on attr_id = mode_attr_id 
                    union all                
                   select 'RELA_TEXT_FROM' attrname, bezi_assoc_von_zu text 
                        ,mode_id,bezi_uc,bezi_dc
                    from modellelement
                    join beziehungen on bezi_id = mode_bezi_id 
                    union all                
                   select 'RELA_TEXT_TO' attrname, bezi_assoc_zu_von text 
                        ,mode_id,bezi_uc,bezi_dc
                    from modellelement
                    join beziehungen on bezi_id = mode_bezi_id 
                )
                cross join (select {})
                where text is not null
                   """.format(plang))
#fuelledefaulttexte

def insertSprachtexte(ptexte, pmodeid, plang):
#    sprachtexte = [[vonText,creby,crety,'TEXT_FROM']
#                  ,[zuText,creby,crety,'TEXT_TO']]

    p_defaultlang = dbParam.dbDefaultLang if p_defaultlang is None else p_defaultlang
    values = [v for v in p_texte]
    # (values)
    lsql= """insert into sprachtexte 
                    (sptx_attrname,  sptx_text
                   ,sptx_mode_id, sptx_uc, sptx_dc
                   , sptx_spra_id)
                  select  attrname, case  when defaultlang = spra_iso_code2 then '' 
                                    else '*'|| defaultlang ||'* ' end
                                    || ? text
                    ,modeid, ? uc,? dc, spra_id
                  from sprachen
                  cross join (select '{}' modeid, '{}' defaultlang,  ? attrname)
                  where not exists 
                    (select 1 from sprachtexte
                        where sptx_spra_id = spra_id
                         and sptx_mode_id = modeid
                         and  sptx_attrname = attrname
                    ) 
                """.format( p_modeid,p_defaultlang)
    dbDML.execmany(lsql, values)

# die Originalnamen werden überschrieben
    l_sql = """ update sprachtexte
                set sptx_text = ?
                   ,sptx_um = ?
                   ,sptx_dm = ?
                where sptx_spra_id = {}
                and sptx_attrname = ?
                and sptx_mode_id = {}
                """.format(sprache.spraLookup(p_defaultlang),p_modeid)
    dbDML.execmany(l_sql, values)
#insertSprachTexte