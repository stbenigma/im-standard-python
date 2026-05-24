import json
import re
from datetime import datetime
from IM_STANDARD import nvl
from IM_STANDARD.SQL.SQL_INFRA import DbDML


class Sql2IMJsonschema():
    """
    extract all elements from the sqldatabase and create a standardjson-schema
    file
    """

    FKCOLS = {"synonyms": "syno_enti_id",
              "examples": "expl_mode_id",
              "user_defined_props": "udpv_mode_id",
              "lov_values": "lovv_doma_id"
              }

    DOMATYPES = {"TXT": "Text",
                 "GRP": "Groupdomain",
                 "LOV": "ListOfValues",
                 "NUM": "Numeric",
                 "DAT": "Datetime",
                 "BIN": "Binary",
                 "BOO": "Boolean"
                 }

    def __init__(self, mydb: DbDML):
        self._mydb: DbDML = mydb
        self.standardjson = dict()

        return

    @staticmethod
    def _str2json(values: list):
        """
            changes all str entries, enclosed in [] or {} in json elements
        :return: directly in values
        """
        for entry in values:
            removelist = []
            for key, val in entry.items():
                if val is None:
                    removelist.append(key)
                if isinstance(val, str) and re.match("^^({[^}]*}|\[[^]]*\])$", val):
                    entry[key] = json.loads(val, strict=False)
                if isinstance(val, str) and val in ('TRUE', 'FALSE'):
                    entry[key] = val == 'TRUE'
            for key in removelist:
                del entry[key]

    def _sqlvalue(self, val):
        """
        adds '' to a value for a select statement
        if it is string
        :param val:
        :return: 'val'
        """
        return "'" + val + "'"

    def _langtextsql(self, colname: str,
                     fkname: str,
                     keycolname: str = "lang_iso_code2",
                     valcolname: str = "lgtx_text"):
        """ return select for language text subquery
        select select '{'||group_concat('''' ||lang_iso_code2||''':''' ||lgtx_text||'''',',') ||'}'as enti_name
               from lang_texts
               join languages on lgtx_lang_id = lang_id

        """
        return f"""(select '{{' || {self._mydb.dictgroup(keycolname=keycolname,
                                                         valcolname=valcolname)}
                            ||'}}' 
               from lang_texts
               join languages on lgtx_lang_id = lang_id
                   where lgtx_attrname='{colname}'  
                   and lgtx_mode_id={fkname})"""

    def _langssql(self):
        """
         :return: subselect for list of lang_iso_code2 in model_languages
        """
        return f"""(select '[' || {self._mydb.listgroup(colname="lang_iso_code2")} ||']' 
               from languages
               join model_languages on mola_lang_id=lang_id               
                where mola_modl_id=modl_id)"""

    def _listsql(self, tablename: str,
                 colname: str,
                 idcol: str) -> str:
        return f"""(select '[' || group_concat('"'||REPLACE({colname}, '"', '\\"')||'"',',')||']' 
               from {tablename}
                where {self.FKCOLS[tablename]}={idcol})"""

    def _additionalpropssql(self,
                            idcol: str) -> str:
        return self._dictsql(tablename="user_defined_props",
                             keycolname="udpv_name",
                             valcolname="udpv_value",
                             idcol=idcol)

    def _dictsql(self, tablename: str,
                 keycolname: str,
                 valcolname: str,
                 idcol: str) -> str:
        return f"""(select '{{' || {self._mydb.dictgroup(keycolname=keycolname,
                                                         valcolname=valcolname)}
                            ||'}}' 
               from {tablename}
                where {self.FKCOLS[tablename]}={idcol})"""

    def _mapstring(self, col: str, mapping: dict) -> str:
        """
        retruns a sql expression mapping a columnvalue to any of the values in the list
        :param: col
        :param mapping:
        :return: case col when x then y end
        """
        maplist = ' '.join([f" when {self._sqlvalue(key)} then {self._sqlvalue(val)}" for key, val in mapping.items()])
        return f"""case {col} {maplist} end"""

    def _withprefix(self, val, prefix: str):
        """
        add prefix, if val is not None, else return Nont
        :param val:
        :param prefix:
        :return:
        """
        return None if val is None else prefix + str(val)

    def generatebusinessmodel(self):
        self.generateentities()
        self.generateattributes()
        self.generaterelations()
        # self.generatebusinessrules()
        self.generatekeys()

        return

    def _addlist(self,
                 elementname: str,
                 sql: str = None,
                 elements: dict = None, ):
        if sql is not None:
            elements = self._mydb.select(sql=sql)
            self._str2json(elements)

        if elementname in self.standardjson["Model"]:
            self.standardjson["Model"][elementname].extend(elements)
        else:
            self.standardjson["Model"][elementname] = elements

        return

    def generatekeys(self):
        """ get all keys from attributes and relations and fill the entities keys property
            assume attributes and relationships are already done"""
        return

    def generateentities(self):
        sql = f"""select 'ENTI' || enti_id as elementid,
            {self._langtextsql(colname="enti_name",
                               fkname="enti_id")} as name,
            {self._langtextsql(colname="enti_descr",
                               fkname="enti_id")} as description,
            enti_tooltip as shortdescr,
            enti_prefix as prefix,
            enti_short_name as shortname,                         
            case when enti_enca_id is null then null else 'CATG' || enti_enca_id end  as categoryid,
            {self._listsql(tablename="synonyms",
                           colname="syno_name",
                           idcol="enti_id")} as synonyms,
            {self._listsql(tablename="examples",
                           colname="expl_value",
                           idcol="enti_id")} as examples,
            mode_dc as dc,
            mode_uc as uc,
                mode_um as um,
                mode_dm as dm,
            {self._additionalpropssql(idcol="enti_id")}  as additionalProps
        from entities    
        join modelelements on mode_id=enti_id
        """
        self._addlist(sql=sql,
                      elementname="Entities")
        return

    def generaterelations(self):
        return

    def generateattributes(self):
        sql = f"""select 'ATTR' ||attr_id as elementid,
            {self._langtextsql(colname="attr_tech_name",
                               fkname="attr_id")} as name,
            {self._langtextsql(colname="attr_descr",
                               fkname="attr_id")} as description,
            'DOMA' || attr_doma_group_id as domainid,
             case when attr_enti_id is null 
                    THEN 'DOMA' || attr_doma_id
                    else 'ENTI' || attr_enti_id 
            end as parentid,
            attr_displ_name as dispname,
            attr_tooltip as tooltip,
            attr_displ_seq as sortorder,
            attr_is_mandatory as mandatory,
            attr_is_descriptive as descriptive,
            attr_is_historicised as temporal,
            attr_is_translated as multilang,
            attr_is_repeated as repeated,
            attr_is_encrypted as encrypted,
            {self._listsql(tablename="examples",
                           colname="expl_value",
                           idcol="attr_id")} as examples,
                                       mode_dc as dc,
            mode_uc as uc,
                            mode_um as um,
                            mode_dm as dm,

            {self._additionalpropssql(idcol="attr_id")}  as additionalProps
        from attributes    
        join modelelements on mode_id=attr_id
        """

        self._addlist(sql=sql, elementname="Attributes")
        return

    def generatedomains(self):
        sql = f"""select 'DOMA' ||doma_id as elementid,
            {self._langtextsql(colname="doma_name",
                               fkname="doma_id")} as name,
            {self._langtextsql(colname="doma_descr",
                               fkname="doma_id")} as description,
            {self._mapstring(col="doma_type", mapping=self.DOMATYPES)} as domaintype,
            doma_txt_maxlng as maxlength,
            doma_txt_minlng as minlength,
            doma_txt_syntaxrule as pattern,
            case 
                when doma_num_minvalue is null then doma_dat_minvalue 
                else doma_num_minvalue 
            end as minvalue,
            case 
                when doma_num_maxvalue is null then doma_dat_maxvalue 
                else doma_num_maxvalue 
            end as minvalue,
            doma_num_fract_digits as fractdigits,
            doma_num_total_digits as totaldigits,
            doma_num_round_value as roundto,
            doma_num_physunit as physunit,
            doma_dat_granularity as granularity,
            {self._listsql(tablename="examples",
                           colname="expl_value",
                           idcol="doma_id")} as examples,
            mode_dc as dc,
            mode_uc as uc,
            mode_um as um,
            mode_dm as dm,
            {self._additionalpropssql(idcol="doma_id")}  as additionalProps
        from domains    
        join modelelements on mode_id=doma_id
        """
        """        subtypeproperties["domaintype"] = domaintypes[domaintype]
        elif domaintype == "DATETIME":
            subtypeproperties["granularity"] = "MINUTE"
        elif domaintype == "DATE":
            subtypeproperties["granularity"] = "DAY"
            """
        elements = self._mydb.select(sql=sql)
        self._str2json(elements)

        for doma in elements:
            lovvalsql = f"""select lovv_value as lovvalue,
                            lovv_displ as display,
                         lovv_sort_order as sortorder,
                         lovv_descr as description
                   from lov_values
                    where lovv_doma_id={doma.get("elementid")[4:]}
                    order by lovv_sort_order
                    """
            lovvals = self._mydb.select(sql=lovvalsql)
            if len(lovvals) > 0:
                self._str2json(lovvals)
                doma["lovvalues"] = {val.get("lovvalue"):
                                         {key2: val2 for key2, val2 in val.items()
                                            if (key2 != "lovvalue" and nvl(val2) != "")}
                                     for val in lovvals}

        self._addlist(elements=elements, elementname="Domains")

        return

    def generatecategories(self, catgtype: str):
        sql = f"""select 'CATG' ||enca_id as elementid,
            {self._langtextsql(colname="enca_name",
                               fkname="enca_id")} as name,
            {self._langtextsql(colname="enca_descr",
                               fkname="enca_id")} as description,   
            case when enca_enca_id is null then null else 'CATG' || enca_enca_id end  as parentid,                                                                       
            mode_dc as dc,
            mode_uc as uc,
            mode_um as um,
            mode_dm as dm,
            {self._additionalpropssql(idcol="enca_id")}  as additionalProps
        from entity_categories    
        join modelelements on mode_id=enca_id
        """
        self._addlist(sql=sql, elementname="Categories")
        return

    def generatejson(self, status=None):
        self.standardjson = dict()
        assert status in ("PUBL", "GTOP", "ALL", None), "status  must be PUBL, GTOP or ALL"

        now = datetime.now().replace(microsecond=0).isoformat()

        modelsel = f"""select modl_id, 
                            modl_name as modelname,
                            modl_descr as description,
                            modl_targetenvironment as targetentvionment,
                            case modl_type
                            when "IM" then "Information Model"
                            when "DM" then "Data Model"
                            when "AM" then "Artefact Model"
                            end as modeltype,
                            mode_uc as uc,
                            mode_dc as dc,
                            mode_um as um,
                            mode_dm as dm,
                            mola_mainlanguage as mainlanguage,
                            "0.0" as modelversion,
                            {self._langssql()} as languages,
                            {self._additionalpropssql(idcol="modl_id")}  as additionalProps
                    from models 
                    join main.modelelements on mode_id=modl_id
                    join model_languages on mola_modl_id=modl_id
                    join main.languages on lang_id = mola_lang_id
        """
        models = self._mydb.select(sql=modelsel)
        self._str2json(models)
        for model in models:
            self.standardjson["Model"] = model

        # self.generatecategories(catgtype="DOMAIN", status=status)
        self.generatecategories(catgtype="ENTITY")
        self.generatedomains()
        self.generatebusinessmodel()
        # self.generatederivations(status=status)
        # self.generatemappings(status=status)
        # self.generatetransformations(status=status)
        # self.generatediagrams(status=status)
        # self.generatediagrams(status=status)

        return self.standardjson


if __name__ == '__main__':
    pass
