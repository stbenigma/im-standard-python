from IM_DB import dbDML
from .baseobject import Baseobject

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
    @staticmethod
    def sptxistleer():
        data = dbDML.select("""select count(*) from main.sprachtexte""")
        return data[0][0] == 0

    @staticmethod
    def filldefaulttext(plang):
        """füllt sämtliche übersetzten Elemente in die Sprachtexte der Defaultsprache ein.
           D.h. alle übersetzten Attribute haben mind. in der Defaultsprache einen  Eintrag.
        """
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
                   select 'ENTI_SYNONYM' attrname, syno_name text 
                        ,mode_id,enti_uc,enti_dc
                    from modellelement
                    join synonyme on syno_id = mode_syno_id
                    join entitaeten on enti_id  = syno_enti_id
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
                    union all 
                   select 'WRTB_NAME' attrname, wrtb_name text 
                        ,mode_id,wrtb_uc,wrtb_dc
                    from modellelement
                    join wertebereiche on wrtb_id = mode_wrtb_id 
                )
                cross join (select {} as spra_id)
                   """.format(plang))
    #filldefaulttext

    @staticmethod
    def insertsprachtexte(pudpthema):
        """übertrage alle Sprachtexte (ausser in der Default Sprache aus UDP in die Sprachtexte
        """
        lsql = """insert  into sprachtexte (sptx_attrname, sptx_text, sptx_spra_id, sptx_mode_id, sptx_uc, sptx_dc)
            select attrname,bdwe_wert,spra_id,bdwe_mode_id,bdwe_uc,bdwe_dc
            from (select bdwe_wert,
                      bdwe_mode_id,
                      lower(substr(bdeg_name, 1, 2)) spracheiso2,
                      substr(bdeg_name, 4)           attrname
                ,bdwe_uc,bdwe_dc
               from benudef_wert
                join benudef_eigenschaft on bdeg_id = bdwe_bdeg_id
            where bdeg_thema = '{}'
            )
        join sprachen on spra_iso_code2 = spracheiso2
        where spra_ist_modellsprache = 'FALSE'""".format(pudpthema)
        dbDML.exec(lsql)
    # insertsprachTexte

    @staticmethod
    def getsprachtexte(pattrname,pmodeid):
        lsql = """with sptx as 
            (select sptx_spra_id,sptx_text
             from sprachtexte
            where sptx_attrname = '{}'
            and sptx_mode_id = {}
            )
        select spra_iso_code2,
            case when sptx.sptx_text is not NULL
                then sptx.sptx_text
                else sptxdef.sptx_text
                end text
        from sprachen
        left join sptx as sptx on sptx.sptx_spra_id = spra_id
        left join sptx as sptxdef on sptxdef.sptx_spra_id = spra_spra_id""".format(pattrname,pmodeid if pmodeid is not None else 'NULL')
        data = dbDML.select(lsql)
        retval = {d[0]:d[1] for d in data}
        return retval
    #getsprachtexte
#Sprachtext

