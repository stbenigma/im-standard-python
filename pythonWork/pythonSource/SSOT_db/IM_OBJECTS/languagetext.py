from SSOT_db.SQL_INFRA import dbDML
from .baseobject import Baseobject
import re


class Languagetext(Baseobject):
    EN: str = 'en'
    DE: str = 'de'
    FR: str = 'fr'
    ENTI_NAME: str = 'ENTI_NAME'
    ENTI_COMMENT: str = 'ENTI_COMMENT'
    ENTI_TOOLTIP: str = 'ENTI_TOOLTIP'
    ATTR_NAME: str = 'ATTR_NAME'
    ATTR_COMMENT: str = 'ATTR_COMMENT'
    ATTR_TOOLTIP: str = 'ATTR_TOOLTIP'
    DOMA_NAME: str = 'DOMA_NAME'
    DOMA_DESCR: str = 'DOMA_DESCR'
    RELA_TEXT_FROM: str = 'RELA_TEXT_FROM'
    RELA_TEXT_TO: str = 'RELA_TEXT_TO'
    ENTI_SYNONYM: str = 'ENTI_SYNONYM'
    BURU_NAME: str = 'BURU_NAME'
    BURU_DESCR: str = 'BURU_DESCR'
    BURU_ERRORMSG: str = 'BURU_ERRORMSG'
    EXPL_VALUE: str = 'EXPL_VALUE'
    ODMtranslAttributes = [ENTI_NAME, ENTI_COMMENT, ENTI_TOOLTIP,
         ATTR_NAME, ATTR_COMMENT, ATTR_TOOLTIP,
         ENTI_SYNONYM,
         RELA_TEXT_TO, RELA_TEXT_FROM,
         DOMA_NAME, DOMA_DESCR,
         BURU_NAME, BURU_DESCR, BURU_ERRORMSG,
        EXPL_VALUE
                           ]

    __greportLang: str = None

    _tablename: str = 'lang_texts'
    _prefix: str = 'lgtx'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self, **kwargs):
        super().__init__()
        for col, val in kwargs.items():
            if col in self._columnlist:
                self.setcolvalue(col, Boolean.bool2str(val) if type(val) is bool else val)

    @staticmethod
    def filldefaulttext(plang):
        """füllt sämtliche übersetzten Elemente in die lang_texts der Defaultsprache ein.
           D.h. alle übersetzten Attribute haben mind. in der Defaultsprache einen  Eintrag.
           Synonyms and exampleshave been handled beforehand (they are in a comma-separated list...)
        """
        assert plang, "No language provided"
        """select to get all multilanguage fields we know of. Has to be changed, if in a MultiLangbaseobject
            a multilangcolumns changes"""
        multilangfields = """select 'ENTI_NAME' mlt_attrname, enti_name mlt_text
                                ,enti_id mlt_id,enti_uc mlt_uc,enti_dc mlt_dc
                                    from entities 
                                    union all
                                   select 'ENTI_COMMENT' attrname, enti_descr text 
                                        ,enti_id,enti_uc,enti_dc
                                    from entities                     
                                    union all
                                   select 'ENTI_TOOLTIP' attrname, enti_tooltip text 
                                        ,enti_id,enti_uc,enti_dc
                                    from entities                     
                                    union all
                                   select 'ATTR_COMMENT' attrname, attr_descr text 
                                        ,attr_id,attr_uc,attr_dc
                                    from attributes     
                                    union all
                                   select 'ATTR_TOOLTIP' attrname, attr_tooltip text 
                                        ,attr_id,attr_uc,attr_dc
                                    from attributes     
                                    union all                
                                   select 'ATTR_NAME' attrname, attr_displ_name text 
                                        ,attr_id,attr_uc,attr_dc
                                    from attributes  
                                    union all                
                                   select 'RELA_TEXT_FROM' attrname, rela_assoc_from_to text 
                                        ,rela_id,rela_uc,rela_dc
                                    from relations  
                                    union all                
                                   select 'RELA_TEXT_TO' attrname, rela_assoc_to_from text 
                                        ,rela_id,rela_uc,rela_dc
                                    from relations
                                    union all 
                                   select 'DOMA_NAME' attrname, doma_name text 
                                        ,doma_id,doma_uc,doma_dc
                                    from DOMAINS
                                    union all  
                                   select 'DOMA_DESCR' attrname, doma_descr text 
                                        ,doma_id,doma_uc,doma_dc
                                    from DOMAINS
                                    union all  
                                   select 'BURU_NAME' attrname, buru_name text 
                                        ,buru_id,buru_uc,buru_dc
                                    from business_rules  
                                    union all  
                                   select 'BURU_DESCR' attrname, buru_descr text 
                                        ,buru_id,buru_uc,buru_dc
                                    from business_rules  
                                    union all  
                                   select 'BURU_ERRORMSG' attrname, buru_errormsg text 
                                        ,buru_id,buru_uc,buru_dc
                                    from business_rules 
                                    """
        """correct possible inconsistencies where the original field is NULL but the udp translated value is not
            remove all lang_texts (inserted by insertlang_texts) having empty original values"""
        dbDML.exec(f"""delete from lang_texts
                    where(lgtx_attrname, lgtx_mode_id)
                        in (select mlt_attrname, mlt_id
                                from ({multilangfields})
                                where mlt_text is Null or mlt_text = ""
                                )""")
        dbDML.exec(f"""insert into lang_texts 
                    (lgtx_attrname,  lgtx_text
                   ,lgtx_mode_id, lgtx_uc, lgtx_dc
                   , lgtx_lang_id)
                  select mlt_attrname,  mlt_text, mlt_id, mlt_uc, mlt_dc,lang_id 
                  from ({multilangfields})
                cross join (select {plang} as lang_id)
                   """)
        return

    @staticmethod
    def insertlang_texts(pudpthema):
        """übertrage alle lang_texts (ausser in der Default Language aus UDP (siehe filldefaulttext) in die lang_texts
        """
        lsql = """insert  into lang_texts (lgtx_attrname, lgtx_text, lgtx_lang_id, lgtx_mode_id, lgtx_uc, lgtx_dc)
            select attrname,udpv_value,lang_id,udpv_mode_id,udpv_uc,udpv_dc
            from (select udpv_value,
                      udpv_mode_id,
                      lower(substr(udpr_name, 1, 2)) spracheiso2,
                      substr(udpr_name, 4)           attrname
                ,udpv_uc,udpv_dc
               from UDP_VALUES
                join USER_DEFINED_PROPERTIES on udpr_id = udpv_udpr_id
            where udpr_theme = '{}'
            and udpr_name not like '___ENTI_SYNONYM'
            )
        join languages on lang_iso_code2 = spracheiso2
        where lang_is_base_lang = 'FALSE'""".format(pudpthema)
        dbDML.exec(lsql)

        lsql = """insert  into lang_texts (lgtx_attrname, lgtx_text, lgtx_lang_id, lgtx_mode_id, lgtx_uc, lgtx_dc)
            select 'ENTI_SYNONYM' attrname,syno_name,lang_id,syno_id,syno_uc,syno_dc
            from synonyms
        cross join languages 
        where lang_is_base_lang = 'TRUE'"""
        dbDML.exec(lsql)
        return

    @staticmethod
    def getlang_texts(pattrname, pmodeid):
        lsql = """with lgtx as 
            (select lgtx_lang_id,lgtx_text
             from lang_texts
            where lgtx_attrname = ?
            and lgtx_mode_id = ?
            )
        select lang.lang_iso_code2,
            case when lgtxori.lgtx_text is not NULL
                then lgtxori.lgtx_text
                else case when lgtxdef.lgtx_text is NULL or lgtxdef.lgtx_text = ""  
                        then lgtxdef.lgtx_text
                        else "*" || langlang.lang_iso_code2 || "* " || lgtxdef.lgtx_text 
                      end 
                end text
        from languages lang
        left join languages langlang on langlang.lang_id = lang.LANG_LANG_ID
        left join lgtx as lgtxori on lgtxori.lgtx_lang_id = lang.lang_id
        left join lgtx as lgtxdef on lgtxdef.lgtx_lang_id = lang.lang_lang_id
        order by lang.lang_iso_code2"""
        values = (pattrname, pmodeid)
        data = dbDML.select(lsql, *values)
        retval = {d[0]: d[1] for d in data}
        return retval

    @staticmethod
    def transltext(pattrname, pmodeid, plang):
        data = dbDML.select("""
        select lgtx_text
        from lang_texts
        join languages on lang_id = lgtx_lang_id
        where lgtx_mode_id = {}
        and lgtx_attrname = '{}'
        and lower(lang_iso_code2) = lower('{}') 
        """.format(pmodeid, pattrname, plang))
        return data[0][0] if (len(data) > 0) else ''

    @staticmethod
    def reportLang(newval=None):
        if newval is None:
            return Languagetext.__greportLang
        else:
            Languagetext.__greportLang = newval
        return

    @staticmethod
    def fillnontranslatedtexts(ptypes):
        """all non translated texts for the modelelementtype in ptypes
        are copied into non-default-language
        so we accept the defaltlanguage text as the proper text for any language
        """
        types = re.sub(r"(\w+)",r"'\1'",",".join(ptypes))
        """get all langtexts from the default-language
            for all mode_types in the given list
            multiply them with non-default languages
            if they do not yet exists in the new language
            insert them into lang_texts
        """
        lsql = f"""insert into lang_texts
                (lgtx_attrname ,lgtx_text,lgtx_lang_id,lgtx_mode_id,lgtx_uc,lgtx_dc)
                select lgtx_attrname ,lgtx_text,new_lang_id,lgtx_mode_id,lgtx_uc,lgtx_dc
                from lang_texts lgt
                join modelelement on lgt.lgtx_mode_id = modelelement.mode_id
                        and mode_type in ({types})
                join languages as baselang on lgt.lgtx_lang_id = baselang.lang_id
                                and  baselang.lang_is_base_lang = 'TRUE'
                cross join (select lang_id as new_lang_id 
                            from languages 
                            where lang_is_base_lang = 'FALSE')
                where not exists(select 1 from lang_texts comp
                    where comp.lgtx_mode_id = lgt.lgtx_mode_id
                    and comp.lgtx_attrname = lgt.lgtx_attrname
                    and comp.lgtx_lang_id = new_lang_id)
"""
        cnt = dbDML.exec(psql=lsql)
        return
# Languagetext
