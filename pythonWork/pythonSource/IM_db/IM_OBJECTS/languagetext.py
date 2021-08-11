from IM_DB import dbDML
from .baseobject import Baseobject


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
    BURU_ERRORMSG: str = 'BURU_ERRORMSG'
    ODMtranslAttributes = [ENTI_NAME, ENTI_COMMENT, ENTI_TOOLTIP
        , ATTR_NAME, ATTR_COMMENT, ATTR_TOOLTIP
        , ENTI_SYNONYM
        , RELA_TEXT_TO, RELA_TEXT_FROM
        , DOMA_NAME, DOMA_DESCR
        , BURU_NAME, BURU_ERRORMSG
                           ]

    __greportLang: str = None

    _tablename: str = 'lang_texts'
    _prefix: str = 'lgtx'
    _idcolname: str = _prefix + '_id'
    _columnlist: list = []

    def __init__(self):
        super().__init__()

    @staticmethod
    def filldefaulttext(plang):
        """füllt sämtliche übersetzten Elemente in die lang_texts der Defaultsprache ein.
           D.h. alle übersetzten Attribute haben mind. in der Defaultsprache einen  Eintrag.
           Synonyms have been handled beforehand (they are in a comma-separated list...)
        """
        assert plang, "No language provided"
        dbDML.exec("""insert into lang_texts 
                    (lgtx_attrname,  lgtx_text
                   ,lgtx_mode_id, lgtx_uc, lgtx_dc
                   , lgtx_lang_id)
                  select * from 
                    (select 'ENTI_NAME' attrname, enti_name text 
                        ,enti_id,enti_uc,enti_dc
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
                   select 'BURU_ERRORMSG' attrname, buru_errormsg text 
                        ,buru_id,buru_uc,buru_dc
                    from business_rules  
                )
                cross join (select {} as lang_id)
                   """.format(plang))

    # filldefaulttext

    @staticmethod
    def insertlang_texts(pudpthema):
        """übertrage alle lang_texts (ausser in der Default Language aus UDP in die lang_texts
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

    # insertlang_texts

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
                else case when lgtxdef.lgtx_text is not NULL 
                        then "*" || langlang.lang_iso_code2 || "* " || lgtxdef.lgtx_text
                        else lgtxdef.lgtx_text
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

    # getlang_texts

    __translNamen = {'Anzeige': {'en': 'Display', 'fr': 'Affichage'}
                    , 'Arc': {'en': 'Arc', 'fr': 'Arc'}
                     ,'Adresse': {'en': 'Address', 'fr': 'Adresse'}
                     ,'Attribute': {'en': 'Attributes', 'fr': 'Attributs'}
                     ,'Attribute(e)': {'en': 'Attribute(s)', 'fr': 'Attribute(s)'}
                     ,'Attributgruppe': {'en': 'Attribute group', 'fr': "Groupe d'attributs"}
                     ,'auf Diagramm(en)': {'en': 'on diagram(s)', 'fr': 'sur ce diagramme(s)'}
                     ,'Autor': {'en': 'Author', 'fr': 'Auteur'}
                     ,'Beschreibung': {'en': 'Description', 'fr': 'Déscription'}
                     ,'Beziehung': {'en': 'Relationship', 'fr': 'Relation'}
                     ,'Beziehung(en)': {'en': 'relationship(s)', 'fr': 'Relation(s)'}
                     ,'Beziehungen': {'en': 'Relationships', 'fr': 'Relations'}
                     ,'Benutzerdefinerte Eigenschaften': {'en': 'User defined properties'
                                                         ,'fr': "Propriétés définies par l'utilisateur"}
                     ,'Bild': {'en': 'Picture', 'fr': 'Image'}
                    , 'Binär': {'en': 'Binary', 'fr': 'Binaire'}
                     ,'Datentyp': {'en': 'Datatype', 'fr': 'Type de données'}
                     ,'Deskriptor': {'en': 'descriptor', 'fr': 'Descripteur'}
                     ,'Domänen': {'en': 'Domains', 'fr': 'Domaines'}
                    , 'Diagram': {'en': 'Diagram', 'fr': 'Diagramme'}
                     ,'Diagramme': {'en': 'Diagrams', 'fr': 'Diagrammes'}
                     ,'Dokument': {'en': 'Document', 'fr': 'Document'}
                     ,'Dokumente': {'en': 'Documents', 'fr': 'Documents'}
                    , 'Domäne': {'en': 'Domain', 'fr': 'Domaine'}
                     ,'Einheit': {'en': 'Unit', 'fr': 'Unité'}, 'Element': {'en': 'Element', 'fr': 'Élément'}
                     ,'Elemente': {'en': 'Elements', 'fr': 'Éléments'}
                    , 'Entität': {'en': 'Entity', 'fr': 'Entité'}
                     ,'Entität/Table': {'en': 'Entity/Table', 'fr': 'Entité/Tableau'}
                     ,'Entitäten': {'en': 'Entities', 'fr': 'Entités'}, 'erstellt': {'en': 'created', 'fr': 'Élaboré'}
                     ,'Film': {'en': 'Video', 'fr': 'Film'}
                    , 'geändert': {'en': 'updated', 'fr': 'changé'}
                     ,'Gruppenattribut': {'en': 'Groupattribute', 'fr': 'Attribute de groupe'}
                     ,'Grafik': {'en': 'Graphic', 'fr': 'Graphique'}
                     ,'Granularität': {'en': 'Granularity', 'fr': 'Granularité'}
                     ,'historisiert': {'en': 'historicized', 'fr': 'historisé'}
                     ,'in Schlüssel': {'en': 'within key', 'fr': 'dans une clef'}
                     ,'Informationsmodell {} (Stand: {})': {'en': 'Informationmodel {} (Status: {})'
                                                           ,'fr': 'Informationmodel {} (Status: {})'}
                     ,'Informationen': {'en': 'Informations', 'fr': 'Informations'}
                     ,'Inhaltstyp': {'en': 'Content type', 'fr': 'Type de contenu'}
                    , 'Ja': {'en': 'Yes', 'fr': 'Oui'}
                     ,'Jahr': {'en': 'year', 'fr': 'Année'}
                     ,'Klassifikation': {'en': 'Classification', 'fr': 'Classification'}
                    , 'Max. Länge': {'en': 'Max. length', 'fr': 'Longueur max.'}
                     ,'Max. Wert': {'en': 'Max. value', 'fr': 'Valeur max.'}
                    , 'Mehr': {'en': 'more', 'fr': 'Plus'}
                     ,'Millisekunde': {'en': 'millisecond', 'fr': 'Milliseconde'}
                     ,'Minute': {'en': 'minute', 'fr': 'Minute'}
                    , 'Min. Wert': {'en': 'Min. value', 'fr': 'Valeur min.'}
                     ,'Monat': {'en': 'month', 'fr': 'Mois'}
                     ,'Nachkommast.': {'en': 'digits after period', 'fr': 'Décimales'}
                     ,'Name': {'en': 'Name', 'fr': 'Nom'}
                    , 'Nein': {'en': 'No', 'fr': 'Non'}
                     ,'Nr': {'en': 'Nr', 'fr': 'N°'}
                    , 'Numerisch': {'en': 'Numerical', 'fr': 'Numérique'}
                    , 'Org. Einheiten': {'en': 'Org. units', 'fr': 'Unités org.'}
                    ,'Organisationseinheit': {'en': 'Organisational unit', 'fr': 'Unités organisationelles'}
                     ,'Pflichtattribut': {'en': 'Mandatory attribute ', 'fr': 'Attribute obligatoire'}
                     ,'Quartal': {'en': 'quarter', 'fr': 'Trimestre'}
                     ,'Referenziert in': {'en': 'Referenced in', 'fr': 'Référencé dans'}
                     ,'Referenziert von': {'en': 'Referenced by', 'fr': 'Référencé par'}
                     ,'Referenziert': {'en': 'References', 'fr': 'Références'}
                     ,'Relational Mapping (Tabellen)': {'en': 'Relational Mapping (tables)'
                                                       ,'fr': 'Relational Mapping (tables)'}
                     ,'Rollen': {'en': 'Roles', 'fr': 'Rôles'}
                     ,'Rundungseinh.': {'en': 'rounding unit', 'fr': "Unité de l'arrondi"}
                     ,'Schlüssel': {'en': 'Key', 'fr': 'Clef'}
                    , 'Sekunde': {'en': 'second', 'fr': 'Seconde'}
                     ,'Semester': {'en': 'half-year', 'fr': 'Semestre'}
                    , 'Sort': {'en': 'Sort', 'fr': 'Sorte'}
                     ,'Stunde': {'en': 'hour', 'fr': 'Heure'}
                    , 'Subentität': {'en': 'Subentity', 'fr': 'Sous-entité'}
                     ,'Subentitäten': {'en': 'Subentities', 'fr': 'Sous-entités'}
                     ,'Suchbegriff': {'en': 'search key', 'fr': 'Clef de recherche'}
                     ,'Superentität': {'en': 'Superentity', 'fr': 'Superentité'}
                     ,'Superentitäten': {'en': 'Superentities', 'fr': 'Superentités'}
                     ,'Synonyme': {'en': 'Synonyms', 'fr': 'Synonyme'}
                     ,'Syntaxregel': {'en': 'Syntax rule', 'fr': 'Règle syntaxique'}
                     ,'Systeme': {'en': 'Systems', 'fr': 'Systèmes'}
                    , 'Tag': {'en': 'day', 'fr': 'Jour'}
                     ,'Tabelle': {'en': 'Table', 'fr': 'Table'}
                    , 'Tabellen': {'en': 'Tables', 'fr': 'Tables'}
                     ,'Technischer Name': {'en': 'Technical Name', 'fr': 'Terme technique'}
                     ,'Text': {'en': 'Text', 'fr': 'Texte'}
                    , 'Ton': {'en': 'Sound', 'fr': 'Ton'}
                     ,'Tooltip': {'en': 'Tooltip', 'fr': 'Info-bulle'}
                    , 'Treffer': {'en': 'Hits', 'fr': 'Occurrence'}
                     ,'Typ': {'en': 'Type', 'fr': 'Type'}
                    , 'UDP-Matrix': {'en': 'UDP-Matrix', 'fr': 'Matrice UDP'}
                     ,'übersetzt': {'en': 'translated', 'fr': 'traduit'}
                     ,'untergeordnet': {'en': 'subordinated', 'fr': 'subordonné'}
                     ,'übergeordnet': {'en': 'superordinated', 'fr': 'superordonné'}
                     ,'Übersetzungen': {'en': 'Translations', 'fr': 'Traductions'}
                     ,'Unterdokumente': {'en': 'Children', 'fr': 'Enfants'}
                     ,'Vaterdokument': {'en': 'Parent', 'fr': 'Document père'}
                     ,'verschlüsselt': {'en': 'encrypted', 'fr': 'Chiffré'}
                     ,'Verwendet für Attribute': {'en': 'Used for attributes', 'fr': 'Utilisé par les attributs'}
                     ,'Verwendet für Columns': {'en': 'Used for columns', 'fr': 'Utilisé par les columns'}
                     ,'Verwendet in Attributgruppen': {'en': 'Used in attribute groups'
                                                      ,'fr': "Utilisé dans les groupes d'attributs"}
                     ,'Verwendet von': {'en': 'used by', 'fr': 'Utilisé pour'}
                     ,'Vorkommast.': {'en': 'digits before period', 'fr': 'Position avant la décimale'}
                     ,'Wert': {'en': 'Value', 'fr': 'Valeur'}
                     ,'Wertebereich': {'en': 'Domain', 'fr': 'Domaine des valeurs'}
                     ,'Wertebereiche': {'en': 'Domains', 'fr': 'Domaines des valeurs'}
                     ,'Werteliste': {'en': 'List of values', 'fr': 'Liste des Valeur'}
                     ,'wiederholt': {'en': 'repeated', 'fr': 'répété'}
                    , 'Woche': {'en': 'week', 'fr': 'Semaine'}
                     ,'Zeitpunkt': {'en': 'Point in Time', 'fr': 'Instant'}}


    @staticmethod
    def transl(pname, plang=None):
        lang = Languagetext.__greportLang if plang is None else plang
        if (lang == Languagetext.DE):
            return pname
        else:
            try:
                return Languagetext.__translNamen[pname][lang]
            except:
                return pname
    # transl

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

    # translist

    @staticmethod
    def reportLang(newval=None):
        if (newval is None):
            return Languagetext.__greportLang
        else:
            Languagetext.__greportLang = newval
    # reportLang

# Languagetext
