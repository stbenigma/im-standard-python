import json
import logging
import re
from datetime import datetime

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD, SKOS, DCTERMS

from IM_STANDARD import nvl
from IM_STANDARD.SQL.SQL_INFRA import DbDML


class Sql2IMJson:
    FKCOLS = {"synonyms": "syno_enti_id",
              "examples": "expl_mode_id",
              "user_defined_props": "udpv_mode_id",
              "lov_values": "lovv_doma_id"
              }

    DOMATYPES = {"TXT": "TextDomain",
                 "GRP": "GroupDomain",
                 "LOV": "LOVDomain",
                 "NUM": "NumericDomain",
                 "DAT": "DatetimeDomain",
                 "BIN": "BinaryDomain",
                 "BOO": "BooleanDomain"
                 }

    BURUTYPES = {'CALC': 'calculation',
                 'CHECK': 'check',
                 'TRIGGER': 'trigger'
                 }
    BURULEVEL = {'ATTR': 'attribute',
                 'DB': 'database',
                 'ENTI': 'entity',
                 'TUPL': 'tuple'
                 }

    RELATYPES = {'1:1': "1:1", 'M:1': 'M:1', 'M:N': 'M:N',
                 'ROLE': 'role', 'SUBTYPE': 'subtype'
                 }

    def __init__(self, mydb: DbDML):
        self._mydb: DbDML = mydb

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
                if isinstance(val, str) and re.match("^{[^}]*}|\[[^]]*]$", val):
                    entry[key] = json.loads(val, strict=False)
                if isinstance(val, str) and val in ('TRUE', 'FALSE'):
                    entry[key] = val == 'TRUE'
            for key in removelist:
                del entry[key]

    @staticmethod
    def _sqlvalue(val):
        """
        adds '' to a value for a select statement
        if it is string
        :param val:
        :return: 'val'
        """
        return "'" + val + "'"

    @staticmethod
    def _listsql(tablename: str,
                 colname: str,
                 idcol: str) -> str:
        return f"""(select '[' || group_concat('"'||REPLACE({colname}, '"', '\\"')||'"',',')||']' 
               from {tablename}
                where {Sql2IMJson.FKCOLS[tablename]}={idcol})"""

    @staticmethod
    def _mapstring(col: str, mapping: dict) -> str:
        """
        retruns a sql expression mapping a columnvalue to any of the values in the list
        :param: col
        :param mapping:
        :return: case col when x then y end
        """
        maplist = ' '.join(
            [f" when {Sql2IMJson._sqlvalue(key)} then {Sql2IMJson._sqlvalue(val)}" for key, val in mapping.items()])
        return f"""case {col} {maplist} end"""

    @staticmethod
    def _withprefix(val, prefix: str):
        """
        add prefix, if val is not None, else return Nont
        :param val:
        :param prefix:
        :return:
        """
        return None if val is None else prefix + str(val)

    def _langtextsql(self, colname: str,
                     fkname: str,
                     keycolname: str = "lang_iso_code2",
                     valcolname: str = "lgtx_text"):
        """ return select for language text subquery
        select select '{'||group_concat('''' ||lang_iso_code2||''':''' ||lgtx_text||'''',',') ||'}'as enti_name
               from lang_texts
               join languages on lgtx_lang_id = lang_id

        """
        defaultsql=f"""(select  {self._dictgroup(keycolname=keycolname,
                                   valcolname='defaultvalue')}
                    from translatedvalues
                   where lgtx_attrname='{colname}'  
                   and lgtx_mode_id={fkname})"""

        realsql=    f"""(select {self._dictgroup(keycolname=keycolname,
                                   valcolname=valcolname)} 
               from lang_texts
               join languages on lgtx_lang_id = lang_id
                   where lgtx_attrname='{colname}'  
                   and lgtx_mode_id={fkname})
                   """

        return defaultsql

    def _langssql(self):
        """
         :return: subselect for list of lang_iso_code2 in model_languages
        """
        return f"""(select '[' || {self._mydb.listgroup(colname="lang_iso_code2")} ||']' 
               from languages
               join model_languages on mola_lang_id=lang_id               
                where mola_modl_id=modl_id)"""

    def _additionalpropssql(self,
                            idcol: str) -> str:
        return self._dictsql(tablename="user_defined_props",
                             keycolname="udpv_name",
                             valcolname="udpv_value",
                             idcol=idcol)

    def _dictgroup(self,keycolname:str,valcolname:str):
        return f"""'{{' || {self._mydb.dictgroup(keycolname=keycolname,
                                   valcolname=valcolname)}
                    || '}}'"""

    def _dictsql(self, tablename: str,
                 keycolname: str,
                 valcolname: str,
                 idcol: str) -> str:
        return f"""(select {self._dictgroup(keycolname=keycolname,
                                   valcolname=valcolname)} 
               from {tablename}
                where {self.FKCOLS[tablename]}={idcol})"""

    def selelementjson(self, sql):
        elements = self._mydb.select(sql=sql)
        self._str2json(elements)
        return elements

    def selmodeljson(self):
        sql = f"""select 'MODL'||modl_id as elementid,                                                                       
                            modl_name as modelname,
                            modl_descr as description,
                            modl_targetenvironment as targetenvironment,
                            case modl_type
                            when 'IM' then 'Information Model'
                            when 'DM' then 'Data Model'
                            when 'AM' then 'Artefact Model'
                            end as modeltype,
                            mode_uc as uc,
                            mode_dc as dc,
                            mode_um as um,
                            mode_dm as dm,
                            lang_iso_code2 as mainlanguage,
                            '0.0' as modelversion,
                            {self._langssql()} as languages,
                            {self._additionalpropssql(idcol="modl_id")}  as additionalProps
                    from models 
                    join modelelements on mode_id=modl_id
                    join model_languages on (mola_modl_id=modl_id
                                            and mola_mainlanguage='TRUE')
                    join languages on lang_id = mola_lang_id
        """
        elements=self.selelementjson(sql=sql)
        return elements

    def selcategoryjson(self):
        sql = f"""select 'CATG' ||enca_id as elementid,
            {self._langtextsql(colname="enca_name",
                               fkname="enca_id")} as name,
            {self._langtextsql(colname="enca_descr",
                               fkname="enca_id")} as description,   
            case when enca_enca_id is null then null else 'CATG' || enca_enca_id end  as categoryid,
            'MODL' ||mode_modl_id as modelid,                                                                       
            mode_dc as dc,
            mode_uc as uc,
            mode_um as um,
            mode_dm as dm,
            {self._additionalpropssql(idcol="enca_id")}  as additionalProps
        from entity_categories    
        join modelelements on mode_id=enca_id
        """

        return self.selelementjson(sql=sql)

    def seldomainjson(self):
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
            end as maxvalue,
            doma_num_fract_digits as fractdigits,
            doma_num_total_digits as totaldigits,
            doma_num_round_value as roundto,
            doma_num_physunit as physunit,
            doma_dat_granularity as granularity,
            {self._listsql(tablename="examples",
                           colname="expl_value",
                           idcol="doma_id")} as examples,
            'MODL'||mode_modl_id as modelid,                                                                       
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
        elements = self.selelementjson(sql=sql)

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
        return elements

    def selentityjson(self):
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
            'MODL'||mode_modl_id as modelid,                                                                       
            mode_dc as dc,
            mode_uc as uc,
                mode_um as um,
                mode_dm as dm,
            {self._additionalpropssql(idcol="enti_id")}  as additionalProps
        from entities    
        join modelelements on mode_id=enti_id
        """
        return self.selelementjson(sql=sql)

    def selattributejson(self):
        sql = f"""select 'ATTR' ||attr_id as elementid,
            attr_tech_name as name, 
            {self._langtextsql(colname="attr_descr",
                               fkname="attr_id")} as description,
            'DOMA' || attr_doma_id as domainid,
             case when attr_enti_id is null 
                    THEN 'DOMA' || attr_doma_group_id
                    else 'ENTI' || attr_enti_id 
            end as parentid,
            {self._langtextsql(colname="attr_displ_name",
                               fkname="attr_id")} as displname,
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
            mode_uc as uc,
                            mode_um as um,
                            mode_dm as dm,

            {self._additionalpropssql(idcol="attr_id")}  as additionalProps
        from attributes    
        join modelelements on mode_id=attr_id
        """

        return self.selelementjson(sql=sql)

    def selrelationjson(self):
        """
        "relationtype": "SUBTYPE",
        "fwd": {
            "entityid": "ENTI98",
            "assoctext": {
                "de": "ist",
                "en": "is"
            },
            "cardinality": "1",
            "mandator'": true
        },

        """
        sql = f"""
        select
        'RELA' || rela_id as elementid,
        {self._langtextsql(colname="rela_name",
                           fkname="rela_id")} as name,
        {self._mapstring(col="rela_type", mapping=self.RELATYPES)} as relationtype,
        '{{ }}' as fwd,
        '{{ }}' as bwd,
        'ENTI' || rela_enti_id_from as entityid_from,
        'ENTI' || rela_enti_id_to as entityid_to,
        rela_hist_from_to as historicised_from,
        rela_hist_to_from as historicised_to,
        rela_maptype_from_to as cardinality_from,
        rela_maptype_to_from as cardinality_to,
        rela_mandatory_from_to as mandatory_from,
        rela_mandatory_to_from as mandatory_to,
        rela_arc_no_from as arcnumber_from,
        rela_arc_no_to as arcnumber_to,
        {self._langtextsql(colname="rela_assoc_from_to",
                           fkname="rela_id")}
            as assoctext_from,
        {self._langtextsql(colname="rela_assoc_to_from",
                           fkname="rela_id")}
            as assoctext_to,
        {self._listsql(tablename="examples",
                       colname="expl_value",
                       idcol="rela_id")} as examples,
        mode_dc as dc,
        mode_uc as uc,
        mode_um as um,
        mode_dm as dm,
        {self._additionalpropssql(idcol="rela_id")} as additionalProps
        from relations
        join modelelements on mode_id = rela_id
    """
        return self.selelementjson(sql=sql)

    def selbusinessrulejson(self):
        sql = f"""select 'BURU' ||buru_id as elementid,
            {self._langtextsql(colname="buru_name",
                               fkname="buru_id")} as name,
            {self._langtextsql(colname="buru_descr",
                               fkname="buru_id")} as description,
            {self._mapstring(col="buru_type", mapping=self.BURUTYPES)} as type,
            {self._mapstring(col="buru_level", mapping=self.BURULEVEL)} as level,
            buru_rule as rule,
            buru_errormsg as errormessage,
            {self._listsql(tablename="examples",
                           colname="expl_value",
                           idcol="buru_id")} as examples,
            'MODL'||mode_modl_id as modelid,                                                                       
           mode_dc as dc,
            mode_uc as uc,
            mode_um as um,
            mode_dm as dm,
            {self._additionalpropssql(idcol="buru_id")}  as additionalProps
        from main.business_rules    
        join modelelements on mode_id=buru_id
        """
        return self.selelementjson(sql=sql)


class Sql2IMJsonschema(Sql2IMJson):
    """
    extract all elements from the sqldatabase and create a standardjson-schema
    file
    """

    def __init__(self, mydb: DbDML):
        self._mydb: DbDML = mydb
        self.standardjson = dict()

        return

    def _addlist(self,
                 elementname: str,
                 elements = None ):
        if elementname in self.standardjson:
            self.standardjson[elementname].extend(elements)
        else:
            self.standardjson[elementname] = elements

        return

    def generatecategories(self, catgtype: str):
        elements=self.selcategoryjson()
        #STANDARD
        for elem in elements:
            self.movetosubentry(elem=elem,
                            colnames=["uc", "dc", "um", "dm"]
                            )
            elem["categorytype"]=catgtype

        self._addlist(elements=elements,
                      elementname="Categories")
        return

    def generatedomains(self):
        elements=self.seldomainjson()
        for elem in elements:
            self.movetosubentry(elem=elem,
                            colnames=["uc", "dc", "um", "dm"]
                            )

        self._addlist(elements=elements,
                      elementname="Domains")
        return

    def generateentities(self):
        elements=self.selentityjson()
        for elem in elements:
            self.movetosubentry(elem=elem,
                            colnames=["uc", "dc", "um", "dm"]
                            )
        self._addlist(elements=elements,
                      elementname="Entities")
        return

    def generateattributes(self):
        elements = self.selattributejson()
        for elem in elements:
            self.movetosubentry(elem=elem,
                            colnames=["uc", "dc", "um", "dm"]
                            )
        self._addlist(elements=elements, elementname="Attributes")
        return

    def generatekeys(self):
        sql = f"""select 
                keys_name              as name,
                '['||group_concat((select '"'||mode_type||mode_id||'"'
                from modelelements
                where mode_type in ('ATTR','RELA')
                and (mode_id = keys_attr_id
                    or mode_id = keys_rela_id)),
                ',') 
                || ']'as elements
        from keys
        where keys_enti_id=:entiid
        group by name;   
        """
        for enti in self.standardjson.get("Entities"):
            keys = self._mydb.select(sql=sql, entiid=enti.get("elementid")[4:])
            if len(keys) > 0:
                self._str2json(keys)
                enti["keys"] = keys
        return

    def generaterelations(self):
        elements = self.selrelationjson()
        for elem in elements:
            self.movetosubentry(elem=elem,
                            colnames=["uc", "dc", "um", "dm"]
                            )
        for elem in elements:
            for field in ("entityid",
                          "assoctext",
                          "mandatory",
                          "cardinality",
                          "historicised",
                          "arcnumber"
                          ):
                # move rela-end attributes to fwd and bwd
                endfield = field + "_from"
                val = elem.get(endfield)
                if val not in [None, "", {}, []]:
                    elem["fwd"][field] = val
                    del elem[endfield]

                endfield = field + "_to"
                val = elem.get(endfield)
                if val not in [None, "", {}, []]:
                    elem["bwd"][field] = val
                    del elem[endfield]

        self._addlist(elements=elements, elementname="Relations")
        return

    def generatebusinessrules(self):
        elements = self.selbusinessrulejson()
        for elem in elements:
            self.movetosubentry(elem=elem,
                            colnames=["uc", "dc", "um", "dm"]
                            )

            buresql = f"""select mode_type || bure_mode_id as elemid,
                            bure_writeable as writeable
                   from businessrule_elements
                   join modelelements on mode_id = bure_mode_id
                    where bure_buru_id={elem.get("elementid")[4:]}
                    """
            bures = self._mydb.select(sql=buresql)
            if len(bures) > 0:
                self._str2json(bures)
                elem["restrictedelements"] = [val.get("elemid") for val in bures]
                affectedelements = [val.get("elemid") for val in bures if val.get("writeable")]
                if len(affectedelements) > 0:
                    elem["affectedelements"] = affectedelements
            else:
                logging.error(f"Business rules must have at least one element they restrict, {elem.get('name')}")

        self._addlist(elements=elements, elementname="BusinessRules")
        return

    def generatebusinessmodel(self):
        self.generateentities()
        self.generateattributes()
        self.generaterelations()
        self.generatebusinessrules()
        self.generatekeys()
        return

    def movetosubentry(self,elem:dict,
                         colnames:list,
                       subentryname="additionalProps"):
        """
        move the namec columns in colname within the element into the subentry in the element
        :param elem: dictionnary to change
        :param colnames: list of columnnames to move (if present)
        :return: nothin, elem object is changed
        """
        for colname in colnames:
            if colname in elem :
                val=elem.get(colname)
                if val not in [None, "", {}, []]:
                    # get or set the subgroup in the element
                    subgroup = elem.setdefault(subentryname, {})
                    # move it to the subgroup if it is not empty
                    subgroup[colname]=val
                del elem[colname] #delete anyway
        return

    def generatejson(self, status=None):
        self.standardjson = dict()
        assert status in ("PUBL", "GTOP", "ALL", None), "status  must be PUBL, GTOP or ALL"

        now = datetime.now().replace(microsecond=0).isoformat()

        models = self.selmodeljson()


        #STANDARD
        for model in models:
            model["targetenvironment"]='???'
            self.movetosubentry(elem=model,
                                colnames=["uc","dc","um","dm"]
                                )
        #TODO Standard list of models
        if len(models)>0:
            self._addlist(elements=models[0],
                      elementname="ModelInfo")

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


class Sql2IMowlschema(Sql2IMJson):
    """
    extract all elements from the sqldatabase and create a standard owl schema
    file
    """



    def __init__(self, mydb: DbDML):
        self._mydb: DbDML = mydb
        self.graph=None

        return

    def _addlist(self,
                 elementname: str,
                 elements: dict):

        if elementname in self.standardjson:
            self.standardjson[elementname].extend(elements)
        else:
            self.standardjson[elementname] = elements

        return

    def generatecategories(self, catgtype: str):

        self._addlist(elements=self.selcategoriejson(),
                      elementname="Categories")
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
            'MODL'||mode_modl_id as modelid,                                                                       
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

    def generateentities(self):
        elements=self.selentityjson()

        for enti in elements:

            entity_class = self.EX[enti.get("name", {}).get("en", '??').replace(' ', '')]
            self.graph.add((entity_class, RDF.type, OWL.Class))
            for lang, val in enti.get("name", {}).items():
                self.graph.add((entity_class, RDFS.label, Literal(val, lang=lang)))
            self.graph.add((entity_class, RDFS.comment, Literal(enti.get("shortname"))))
            for lang, val in enti.get("description", {}).items():
                self.graph.add((entity_class, DCTERMS.description, Literal(val, lang=lang)))
            self.graph.add((entity_class, self.short_descr_prop, Literal(enti.get("shortdescr"))))
            self.graph.add((entity_class, SKOS.altLabel, Literal(enti.get("prefix"))))

            # dcterms:description ist der weltweite Standard für Volltext-Beschreibungen
            # self.graph.add((entity_class, RDFS.tooltip, Literal(enti.get("enti_tooltip"))))
            # self.graph.add((entity_class, RDFS.prefix, Literal(enti.get("enti_prefix"))))


        return

    def generateattributes(self):
        sql = f"""select 'ATTR' ||attr_id as elementid,
            {self._langtextsql(colname="attr_tech_name",
                               fkname="attr_id")} as name,
            {self._langtextsql(colname="attr_descr",
                               fkname="attr_id")} as description,
            'DOMA' || attr_doma_id as domainid,
             case when attr_enti_id is null 
                    THEN 'DOMA' || attr_doma_group_id
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
            'MODL'||mode_modl_id as modelid,                                                                       
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

    def generatekeys(self):
        sql = f"""select 
                keys_name              as name,
                '['||group_concat((select '"'||mode_type||mode_id||'"'
                from modelelements
                where mode_type in ('ATTR','RELA')
                and (mode_id = keys_attr_id
                    or mode_id = keys_rela_id)),
                ',') 
                || ']'as elements
        from keys
        where keys_enti_id=:entiid
        group by name;   
        """
        for enti in self.standardjson.get("Entities"):
            keys = self._mydb.select(sql=sql, entiid=enti.get("elementid")[4:])
            if len(keys) > 0:
                self._str2json(keys)
                enti["keys"] = keys
        return

    def generaterelations(self):
        """

              "relationtype": "SUBTYPE",
      "fwd": {
        "entityid": "ENTI98",
        "assoctext": {
          "de": "ist",
          "en": "is"
        },
        "cardinality": "1",
        "mandator'": true
      },

        """
        sql = f"""select 'RELA' ||rela_id as elementid,
            {self._langtextsql(colname="rela_name",
                               fkname="rela_id")} as name,
            {self._mapstring(col="rela_type", mapping=self.RELATYPES)} as relationtype,
            '{{ }}' as fwd  ,          
            '{{ }}' as bwd  ,
             'ENTI'|| rela_enti_id_from as entityid_from,
             'ENTI'|| rela_enti_id_to as entityid_to,
             rela_hist_from_to as historicised_from, 
             rela_hist_to_from as historicised_to, 
             rela_maptype_from_to as cardinality_from,
             rela_maptype_to_from as cardinality_to,
             rela_mandatory_from_to as mandatory_from,
             rela_mandatory_to_from as mandatory_to,
             rela_arc_no_from as arcnumber_from,
             rela_arc_no_to as arcnumber_to,
             {self._langtextsql(colname="rela_assoc_from_to",
                                fkname="rela_id")} 
                    as assoctext_from,                        
             {self._langtextsql(colname="rela_assoc_to_from",
                                fkname="rela_id")} 
                    as assoctext_to,                       
             {self._listsql(tablename="examples",
                            colname="expl_value",
                            idcol="rela_id")} as examples,
            'MODL'||mode_modl_id as modelid,                                                                       
           mode_dc as dc,
            mode_uc as uc,
            mode_um as um,
            mode_dm as dm,
            {self._additionalpropssql(idcol="rela_id")}  as additionalProps
        from relations    
        join modelelements on mode_id=rela_id
        """

        elements = self._mydb.select(sql=sql)
        self._str2json(elements)
        for elem in elements:
            for field in ("entityid",
                          "assoctext",
                          "mandatory",
                          "cardinality",
                          "historicised",
                          "arcnumber"
                          ):
                # move rela-end attributes to fwd and bwd
                endfield = field + "_from"
                val = elem.get(endfield)
                if val not in [None, "", {}, []]:
                    elem["fwd"][endfield] = val
                    del elem[endfield]

                endfield = field + "_to"
                val = elem.get(endfield)
                if val not in [None, "", {}, []]:
                    elem["bwd"][endfield] = val
                    del elem[endfield]

        self._addlist(elements=elements, elementname="Relations")
        return

    def generatebusinessrules(self):
        sql = f"""select 'BURU' ||buru_id as elementid,
            {self._langtextsql(colname="buru_name",
                               fkname="buru_id")} as name,
            {self._langtextsql(colname="buru_descr",
                               fkname="buru_id")} as description,
            {self._mapstring(col="buru_type", mapping=self.BURUTYPES)} as type,
            {self._mapstring(col="buru_level", mapping=self.BURULEVEL)} as level,
            buru_rule as rule,
            buru_errormsg as errormessage,
            {self._listsql(tablename="examples",
                           colname="expl_value",
                           idcol="buru_id")} as examples,
            'MODL'||mode_modl_id as modelid,                                                                       
           mode_dc as dc,
            mode_uc as uc,
            mode_um as um,
            mode_dm as dm,
            {self._additionalpropssql(idcol="buru_id")}  as additionalProps
        from main.business_rules    
        join modelelements on mode_id=buru_id
        """
        elements = self._mydb.select(sql=sql)
        self._str2json(elements)
        for buru in elements:
            buresql = f"""select mode_type || bure_mode_id as elemid,
                            bure_writeable as writeable
                   from businessrule_elements
                   join modelelements on mode_id = bure_mode_id
                    where bure_buru_id={buru.get("elementid")[4:]}
                    """
            bures = self._mydb.select(sql=buresql)
            if len(bures) > 0:
                self._str2json(bures)
                buru["elements"] = [val.get("elemid") for val in bures]
                affectedelements = [val.get("elemid") for val in bures if val.get("writeable")]
                if len(affectedelements) > 0:
                    buru["affectedelements"] = affectedelements

        self._addlist(elements=elements, elementname="BusinessRules")
        return

    def generatebusinessmodel(self):
        self.generateentities()
        return
        self.generateattributes()
        self.generaterelations()
        self.generatebusinessrules()
        self.generatekeys()
        return

    def generatejson(self, status=None):
        self.standardjson = dict()
        assert status in ("PUBL", "GTOP", "ALL", None), "status  must be PUBL, GTOP or ALL"

        now = datetime.now().replace(microsecond=0).isoformat()

        self.graph= Graph()
        # 2. Namespaces definieren und an den Graphen binden (für schöne Prefixes im TTL)
        self.EX = Namespace("http://information-model.org/model/")
        self.graph.bind("ex", self.EX)
        self.graph.bind("owl", OWL)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("xsd", XSD)
        self.graph.bind("skos", SKOS)
        self.graph.bind("dcterms", DCTERMS)

        # 1. Definiere deine eigene Dokumentations-Eigenschaft (AnnotationProperty)
        self.short_descr_prop = self.EX.shortDescr
        self.graph.add((self.short_descr_prop, RDF.type, OWL.AnnotationProperty))
        self.graph.add((self.short_descr_prop, RDFS.label, Literal("Short Description", lang="en")))
        self.graph.add((self.short_descr_prop, RDFS.label, Literal("Kurzbeschreibung", lang="de")))
        self.graph.add((self.short_descr_prop, RDFS.comment,
               Literal("Eine kurze, prägnante Beschreibung für Benutzeroberflächen.")))

        modelsel = f"""select 'MODL'||modl_id as modelid,                                                                       
                            modl_name as modelname,
                            modl_descr as description,
                            modl_targetenvironment as targetenvironment,
                            case modl_type
                            when "IM" then "Information Model"
                            when "DM" then "Data Model"
                            when "AM" then "Artefact Model"
                            end as modeltype,
                            mode_uc as uc,
                            mode_dc as dc,
                            mode_um as um,
                            mode_dm as dm,
                            lang_iso_code2 as mainlanguage,
                            "0.0" as modelversion,
                            {self._langssql()} as languages,
                            {self._additionalpropssql(idcol="modl_id")}  as additionalProps
                    from models 
                    join modelelements on mode_id=modl_id
                    join model_languages on (mola_modl_id=modl_id
                                            and mola_mainlanguage='TRUE')
                    join languages on lang_id = mola_lang_id
        """
        elements = self._mydb.select(sql=modelsel)

        for model in elements:
            pass


        # self.generatecategories(catgtype="DOMAIN", status=status)
        # self.generatecategories(catgtype="ENTITY")
        # self.generatedomains()
        self.generatebusinessmodel()
        # self.generatederivations(status=status)
        # self.generatemappings(status=status)
        # self.generatetransformations(status=status)
        # self.generatediagrams(status=status)
        # self.generatediagrams(status=status)

        return self.graph


if __name__ == '__main__':
    pass
