import json
import logging
import re
from datetime import datetime

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD, SKOS, DCTERMS

from IM_STANDARD import nvl,normalize_booleans,remove_empty_values, StandardSchema
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
    DOMATYPESREV = {val: key for key, val in DOMATYPES.items()}

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

    def _listsql(self, tablename: str,
                 colname: str,
                 idcol: str) -> str:
        return f"""(select {self._mydb.listgroup(colname=colname)}  
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
        defaultsql = f"""(select  {self._dictgroup(keycolname=keycolname,
                                                   valcolname='defaultvalue')}
                    from translatedvalues
                   where lgtx_attrname='{colname}'  
                   and lgtx_mode_id={fkname})"""

        realsql = f"""(select {self._dictgroup(keycolname=keycolname,
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
        return f"""(select {self._mydb.listgroup(colname="lang_iso_code2")}  
               from languages
               join model_languages on mola_lang_id=lang_id               
                where mola_modl_id=modl_id)"""

    def _additionalpropssql(self,
                            idcol: str) -> str:
        return self._dictsql(tablename="user_defined_props",
                             keycolname="udpv_name",
                             valcolname="udpv_value",
                             idcol=idcol)

    def _dictgroup(self, keycolname: str, valcolname: str):
        return self._mydb.dictgroup(keycolname=keycolname,
                                    valcolname=valcolname)

    def _dictsql(self, tablename: str,
                 keycolname: str,
                 valcolname: str,
                 idcol: str) -> str:
        return f"""(select {self._dictgroup(keycolname=keycolname,
                                            valcolname=valcolname)} 
               from {tablename}
                where {self.FKCOLS[tablename]}={idcol})"""

    def selelementjson(self, sql):
        elements = self._mydb.select(sql=sql,aslist=True)
        #liefert eine liste von tupeln von json strings
        return json.loads(elements[0][0])

    def selmodeljson(self):
        sql = f"""select 'MODL'||modl_id as elementId,                                                                       
                            modl_name as modelname,
                            modl_descr as description,
                            modl_targetenvironment as targetenvironment,
                            case modl_type
                            when 'IM' then 'Information model'
                            when 'DM' then 'Data model'
                            when 'AM' then 'Artefact model'
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
        sql = """select json_group_array(
                        json_object('elementId', 'MODL' || modl_id,
                   'modelName', modl_name,
                   'description', modl_descr,
                   'targetEnvironment', modl_targetenvironment,
                   'modelType', case modl_type
                                    when 'IM' then 'Information model'
                                    when 'DM' then 'Data model'
                                    when 'AM' then 'Artefact model'
                       end,
                   'uc', mode_uc,
                   'dc', mode_dc,
                   'um', mode_um,
                   'dm', mode_dm,
                   'mainLanguage', lang_iso_code2,
                   'modelVersion', '0.0',
                   'languages', (select json_group_array(lang_iso_code2)
                                 from languages
                                    join model_languages on mola_lang_id = lang_id
                                 where mola_modl_id = modl_id),
                   'additionalProps', (select json_group_object(udpv_name, udpv_value)

                                       from user_defined_props
                                       where udpv_mode_id = modl_id)
           ))as models
            from models
                     join modelelements on mode_id = modl_id
                     join model_languages on (mola_modl_id = modl_id
                            and mola_mainlanguage = 'TRUE')
                     join languages on lang_id = mola_lang_id"""
        elements = self.selelementjson(sql=sql)
        return elements

    def selcategoryjson(self):
        sql = f"""select json_group_array(
        json_object('elementId','CATG' ||enca_id,
            'name',{self._langtextsql(colname="enca_name", fkname="enca_id")},
            'description',{self._langtextsql(colname="enca_descr",
                                             fkname="enca_id")},
            'modelId',case when enca_enca_id is null then null
                                    else 'CATG' || enca_enca_id
                                    end,
           'modelId', 'MODL' ||mode_modl_id ,
            'dc',mode_dc ,
            'uc',mode_uc ,
            'um',mode_um ,
            'dm',mode_dm,
            'additionalProps', {self._additionalpropssql(idcol="enca_id")}
            ))as catgs
        from entity_categories
        join modelelements on mode_id=enca_id"""

        return self.selelementjson(sql=sql)

    def seldomainjson(self):
        sql = f"""select json_group_array(
            json_object('elementId','DOMA' ||doma_id ,
            'name',{self._langtextsql(colname="doma_name",
                                      fkname="doma_id")},
            'description',{self._langtextsql(colname="doma_descr",
                                             fkname="doma_id")} ,
            'domainType',{self._mapstring(col="doma_type", mapping=self.DOMATYPES)} ,
            'maxLength',doma_txt_maxlng ,
            'minLength',doma_txt_minlng ,
            'syntaxRule',doma_txt_syntaxrule,
            'minValue',case 
                when doma_num_minvalue is null then doma_dat_minvalue 
                else doma_num_minvalue 
            end ,
            'maxValue',case 
                when doma_num_maxvalue is null then doma_dat_maxvalue 
                else doma_num_maxvalue 
            end,
            'fractDigits',doma_num_fract_digits ,
            'totalDigits',doma_num_total_digits ,
            'roundto',doma_num_round_value ,
            'physunit',doma_num_physunit,
            'granularity',doma_dat_granularity ,
            'examples',{self._listsql(tablename="examples",
                                      colname="expl_value",
                                      idcol="doma_id")} ,
            'modelId','MODL'||mode_modl_id ,                                                                       
            'dc',mode_dc,
            'uc',mode_uc ,
            'um',mode_um ,
            'uc',mode_dm ,
            'values',(select json_group_array(json_object('value', lovv_value,
                                                        'displayValue', lovv_displ,
                                                        'sortOrder', lovv_sort_order,
                                                        'description', lovv_descr)
                                                    )
                                     from lov_values
                                     where lovv_doma_id = doma_id
                                     order by lovv_sort_order
                                ) ,
            'additionalProps',{self._additionalpropssql(idcol="doma_id")}
            )) as domas 
        from domains    
        join modelelements on mode_id=doma_id
        """

        elements = self.selelementjson(sql=sql)

        return elements

    def selentityjson(self):
        sql = f"""select json_group_array(
        json_object(
        'elementId','ENTI' || enti_id,
        'name', {self._langtextsql(colname="enti_name",
                                   fkname="enti_id")} ,
        'description',{self._langtextsql(colname="enti_descr",
                                         fkname="enti_id")} ,
        'shortDescr', enti_tooltip,
        'prefix',enti_prefix,
        'shortName',enti_short_name,                         
        'categoryId', case when enti_enca_id is null then null else 'CATG' || enti_enca_id end ,
         'synonyms',{self._listsql(tablename="synonyms",
                                   colname="syno_name",
                                   idcol="enti_id")},
        'examples',{self._listsql(tablename="examples",
                                  colname="expl_value",
                                  idcol="enti_id")},
        'keys',(SELECT json_group_array(
                   json_object(
                       'name', keys_name,
                       'elements', json(elements))
                    )
                FROM (
                    SELECT
                        keys_name ,
                        json_group_array(mode_type || mode_id) AS elements
                    FROM keys 
                    LEFT JOIN modelelements 
                        ON mode_type IN ('ATTR', 'RELA')
                        AND (mode_id = keys_attr_id OR mode_id = keys_rela_id)
                 WHERE keys_enti_id = enti_id
                    GROUP BY keys_name
                )),                                  
        'modelId', 'MODL'||mode_modl_id,                                                                       
        'dc',mode_dc,
        'uc',mode_uc,
        'um',mode_um,
        'dm',mode_dm,
        'additionalProps',{self._additionalpropssql(idcol="enti_id")} 
        )) as entis
        from entities    
        join modelelements on mode_id=enti_id
        """
        return self.selelementjson(sql=sql)

    def selattributejson(self):
        sql = f"""select json_group_array(
                json_object('elementId','ATTR' ||attr_id ,
            'name',            attr_tech_name, 
            'description',        {self._langtextsql(colname="attr_descr",
                                                     fkname="attr_id")} ,
            'domainId',            'DOMA' || attr_doma_id,
            'parentId',         case when attr_enti_id is null 
                            THEN 'DOMA' || attr_doma_group_id
                            else 'ENTI' || attr_enti_id 
                    end ,
            'displname',        {self._langtextsql(colname="attr_displ_name",
                                                   fkname="attr_id")} ,
        'tooltip',            attr_tooltip,
            'sortOrder',            attr_displ_seq,
            'mandatory',            attr_is_mandatory,
            'descriptive',            attr_is_descriptive,
            'temporal',            attr_is_historicised,
            'multilang',            attr_is_translated,
            'repeated',            attr_is_repeated,
            'encrypted',            attr_is_encrypted,
            'examples',        {self._listsql(tablename="examples",
                                              colname="expl_value",
                                              idcol="attr_id")} ,
            'uc',            mode_uc,
            'um',                            mode_um,
            'dm',                            mode_dm,
            'dc',                            mode_dc,
            'additionalProps',        {self._additionalpropssql(idcol="attr_id")} 
            )) as attrs
        from attributes    
        join modelelements on mode_id=attr_id
        """

        return self.selelementjson(sql=sql)

    def selrelationjson(self):
        """
        "relationType": "SUBTYPE",
        "fwd": {
            "entityId": "ENTI98",
            "assocText": {
                "de": "ist",
                "en": "is"
            },
            "cardinality": "1",
            "mandator'": true
        },

        """
        sql = f"""
        select json_group_array(
                json_object('elementId',        'RELA' || rela_id,
    'name',    {self._langtextsql(colname="rela_name",
                                  fkname="rela_id")},
    'relationType',    {self._mapstring(col="rela_type", mapping=self.RELATYPES)} ,
    'fwd',        '',
    'bwd',        '',
    'entityid_from',        'ENTI' || rela_enti_id_from,
    'entityid_to',        'ENTI' || rela_enti_id_to,
    'historicised_from',        rela_hist_from_to,
    'historicised_to',        rela_hist_to_from,
    'cardinality_from',        rela_maptype_from_to,
    'cardinality_to',        rela_maptype_to_from,
    'mandatory_from',        rela_mandatory_from_to,
    'mandatory_to',        rela_mandatory_to_from,
    'arcnumber_from',        rela_arc_no_from,
    'arcnumber_to',        rela_arc_no_to,
    'assoctext_from',    {self._langtextsql(colname="rela_assoc_from_to",
                                            fkname="rela_id")},
    'assoctext_to',    {self._langtextsql(colname="rela_assoc_to_from",
                                          fkname="rela_id")},
    'examples',    {self._listsql(tablename="examples",
                                  colname="expl_value",
                                  idcol="rela_id")},
    'dc',        mode_dc,
    'uc',        mode_uc,
    'um',        mode_um,
    'dm',        mode_dm,
    'additionalProps',        {self._additionalpropssql(idcol="rela_id")}
    )) as relas
        from relations
        join modelelements on mode_id = rela_id
    """
        return self.selelementjson(sql=sql)

    def selbusinessrulejson(self):
        sql = f"""select json_group_array(
           json_object(
            'elementId','BURU' ||buru_id,
            'name',        {self._langtextsql(colname="buru_name",
                                              fkname="buru_id")} ,
            'description',        {self._langtextsql(colname="buru_descr",
                                                     fkname="buru_id")},
            'type',            {self._mapstring(col="buru_type", mapping=self.BURUTYPES)},
            'level',            {self._mapstring(col="buru_level", mapping=self.BURULEVEL)},
            'rule',            buru_rule,
            'errormessage',            buru_errormsg,
            'examples',        {self._listsql(tablename="examples",
                                              colname="expl_value",
                                              idcol="buru_id")}  ,
            'restrictedElements',(select json_group_array(mode_type || bure_mode_id)
                                       from businessrule_elements
                                    join modelelements on mode_id = bure_mode_id
                                    where bure_buru_id=buru_id),
            'affectedElements',(select json_group_array(mode_type || bure_mode_id)
                                       from businessrule_elements
                                    join modelelements on mode_id = bure_mode_id
                                    where bure_buru_id=buru_id
                                    and bure_writeable='TRUE'),
            'modelId',            'MODL'||mode_modl_id,                                                                       
            'dc',           mode_dc,
            'uc',            mode_uc,
            'um',            mode_um,
            'dm',            mode_dm,
            'additionalProps',            {self._additionalpropssql(idcol="buru_id")} 
        )) as burus
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
                 elements=None):
        if elementname in self.standardjson:
            self.standardjson[elementname].extend(elements)
        else:
            self.standardjson[elementname] = elements

        return

    def generatecategories(self, catgtype: str):
        elements = self.selcategoryjson()
        # STANDARD
        for elem in elements:
            self.movetosubentry(elem=elem,
                                colnames=["uc", "dc", "um", "dm"]
                                )
            elem["categoryType"] = catgtype

        self._addlist(elements=elements,
                      elementname="Categories")
        return

    def generatedomains(self):
        elements = self.seldomainjson()
        for elem in elements:
            self.movetosubentry(elem=elem,
                                colnames=["uc", "dc", "um", "dm"]
                                )

        self._addlist(elements=elements,
                      elementname="Domains")
        return

    def generateentities(self):
        elements = self.selentityjson()
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

    def generaterelations(self):
        elements = self.selrelationjson()
        for elem in elements:
            self.movetosubentry(elem=elem,
                                colnames=["uc", "dc", "um", "dm"]
                                )
        for elem in elements:
            elem["fwd"] = {}
            elem["bwd"] = {}
            for field in ("entityId",
                          "assocText",
                          "mandatory",
                          "cardinality",
                          "historicised",
                          "arcNumber"
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
            if elem.get('restricted') in (None,[]):
                logging.error(f"Business rules must have at least one element they restrict, {elem.get('name')}")

        self._addlist(elements=elements, elementname="BusinessRules")
        return

    def generatebusinessmodel(self):
        self.generateentities()
        self.generateattributes()
        self.generaterelations()
        self.generatebusinessrules()
        return

    def movetosubentry(self, elem: dict,
                       colnames: list,
                       subentryname="additionalProps"):
        """
        move the namec columns in colname within the element into the subentry in the element
        :param elem: dictionnary to change
        :param colnames: list of columnnames to move (if present)
        :return: nothin, elem object is changed
        """
        for colname in colnames:
            if colname in elem:
                val = elem.get(colname)
                if val not in [None, "", {}, []]:
                    # get or set the subgroup in the element
                    subgroup = elem.setdefault(subentryname, {})
                    # move it to the subgroup if it is not empty
                    subgroup[colname] = val
                del elem[colname]  # delete anyway
        return

    def generatejson(self, status=None,notnullonly:bool=True):
        self.standardjson = dict()
        assert status in ("PUBL", "GTOP", "ALL", None), "status  must be PUBL, GTOP or ALL"

        now = datetime.now().replace(microsecond=0).isoformat()

        models = self.selmodeljson()

        # STANDARD
        for model in models:
            model["targetEnvironment"] = '???'
            self.movetosubentry(elem=model,
                                colnames=["uc", "dc", "um", "dm"]
                                )
        # TODO Standard list of models
        if len(models) > 0:
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
        self.standardjson=normalize_booleans(self.standardjson)
        if notnullonly:
            self.standardjson=remove_empty_values(self.standardjson)
        return self.standardjson


class Sql2IMowlschema(Sql2IMJson):
    """
    extract all elements from the sqldatabase and create a standard owl schema
    file
    """

    def __init__(self, mydb: DbDML):
        self._mydb: DbDML = mydb
        self.graph = None

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
        sql = f"""select 'DOMA' ||doma_id as elementId,
            {self._langtextsql(colname="doma_name",
                               fkname="doma_id")} as name,
            {self._langtextsql(colname="doma_descr",
                               fkname="doma_id")} as description,
            {self._mapstring(col="doma_type", mapping=self.DOMATYPES)} as domaintype,
            doma_txt_maxlng as maxlength,
            doma_txt_minlng as minlength,
            doma_txt_syntaxrule as syntaxrule,
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
        """        subtypeproperties["domainType"] = domaintypes[domaintype]
        elif domaintype == "DATETIME":
            subtypeproperties["granularity"] = "MINUTE"
        elif domaintype == "DATE":
            subtypeproperties["granularity"] = "DAY"
            """
        elements = self._mydb.select(sql=sql)
        self._str2json(elements)

        for doma in elements:
            lovvalsql = f"""select lovv_value as value,
                            lovv_displ as displayvalue,
                         lovv_sort_order as sortorder,
                         lovv_descr as description
                   from lov_values
                    where lovv_doma_id={doma.get("elementId")[4:]}
                    order by lovv_sort_order
                    """
            lovvals = self._mydb.select(sql=lovvalsql)
            if len(lovvals) > 0:
                self._str2json(lovvals)
                doma["values"] = [{key2: val2 for key2, val2 in val.items()
                                   if (nvl(val2) != "")}
                                  for val in lovvals]

        self._addlist(elements=elements, elementname="Domains")

        return

    def generateentities(self):
        elements = self.selentityjson()

        for enti in elements:

            entity_class = self.EX[enti.get("name", {}).get("en", '??').replace(' ', '')]
            self.graph.add((entity_class, RDF.type, OWL.Class))
            for lang, val in enti.get("name", {}).items():
                self.graph.add((entity_class, RDFS.label, Literal(val, lang=lang)))
            self.graph.add((entity_class, RDFS.comment, Literal(enti.get("shortName"))))
            for lang, val in enti.get("description", {}).items():
                self.graph.add((entity_class, DCTERMS.description, Literal(val, lang=lang)))
            self.graph.add((entity_class, self.short_descr_prop, Literal(enti.get("shortDescr"))))
            self.graph.add((entity_class, SKOS.altLabel, Literal(enti.get("prefix"))))

            # dcterms:description ist der weltweite Standard für Volltext-Beschreibungen
            # self.graph.add((entity_class, RDFS.tooltip, Literal(enti.get("enti_tooltip"))))
            # self.graph.add((entity_class, RDFS.prefix, Literal(enti.get("enti_prefix"))))

        return

    def generateattributes(self):
        sql = f"""select 'ATTR' ||attr_id as elementId,
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


    def generaterelations(self):
        """

              "relationType": "SUBTYPE",
      "fwd": {
        "entityId": "ENTI98",
        "assocText": {
          "de": "ist",
          "en": "is"
        },
        "cardinality": "1",
        "mandator'": true
      },

        """
        sql = f"""select 'RELA' ||rela_id as elementId,
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
            for field in ("entityId",
                          "assocText",
                          "mandatory",
                          "cardinality",
                          "historicised",
                          "arcNumber"
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
        sql = f"""select 'BURU' ||buru_id as elementId,
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
                    where bure_buru_id={buru.get("elementId")[4:]}
                    """
            bures = self._mydb.select(sql=buresql)
            if len(bures) > 0:
                self._str2json(bures)
                buru["elements"] = [val.get("elemid") for val in bures]
                affectedelements = [val.get("elemid") for val in bures if val.get("writeable")]
                if len(affectedelements) > 0:
                    buru["affectedElements"] = affectedelements

        self._addlist(elements=elements, elementname="BusinessRules")
        return

    def generatebusinessmodel(self):
        return

        self.generateentities()
        self.generateattributes()
        self.generaterelations()
        self.generatebusinessrules()
        return

    def generatejson(self, status=None):
        self.standardjson = dict()
        assert status in ("PUBL", "GTOP", "ALL", None), "status  must be PUBL, GTOP or ALL"

        now = datetime.now().replace(microsecond=0).isoformat()

        self.graph = Graph()
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
                            when "IM" then "Information model"
                            when "DM" then "Data model"
                            when "AM" then "Artefact model"
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
