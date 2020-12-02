from IM_DB import dbDML,dbDDL
from .baseobject import Baseobject

class Languagetext(Baseobject):
    EN:str='en'
    DE:str='de'
    FR:str='fr'
    ENTI_NAME:str='ENTI_NAME'
    ENTI_COMMENT:str='ENTI_COMMENT'
    ENTI_TOOLTIP:str='ENTI_TOOLTIP'
    ATTR_NAME:str='ATTR_NAME'
    ATTR_COMMENT:str='ATTR_COMMENT'
    ATTR_TOOLTIP:str='ATTR_TOOLTIP'
    DOMA_NAME:str= 'DOMA_NAME'
    DOMA_DESCR:str= 'DOMA_DESCR'
    RELA_TEXT_FROM:str='RELA_TEXT_FROM'
    RELA_TEXT_TO:str='RELA_TEXT_TO'
    SYNO_NAME:str='SYNO_NAME'

    __greportLang:str = None


    _tablename:str ='lang_texts'
    _prefix:str ='lgtx'
    _columnlist:list = ['lgtx_id', 'lgtx_attrname', 'lgtx_text', 'lgtx_lang_id'
                        , 'lgtx_mode_id', 'lgtx_uc', 'lgtx_dc', 'lgtx_um', 'lgtx_dm']

    def __init__(self):
        super().__init__(tablename=Languagetext._tablename, prefix=Languagetext._prefix
                         , columnlist = Languagetext._columnlist)

    @staticmethod
    def createtable():
        Baseobject.createtable(ptablename=Languagetext._tablename
                               , psql="""
CREATE TABLE LANG_TEXTS
    (
     LGTX_ID INTEGER NOT NULL primary key autoincrement ,
     LGTX_ATTRNAME VARCHAR (60) NOT NULL ,
     LGTX_TEXT VARCHAR (4000) NULL ,
     LGTX_LANG_ID integer NOT NULL ,
     LGTX_MODE_ID integer NOT NULL ,
     LGTX_UC VARCHAR(30) NULL  ,
     LGTX_DC VARCHAR (30) NOT NULL ,
     LGTX_UM VARCHAR (30) NULL ,
     LGTX_DM VARCHAR (30) NULL
    ,CONSTRAINT LGTX_UK UNIQUE (LGTX_LANG_ID ASC, LGTX_MODE_ID ASC, LGTX_ATTRNAME ASC)
	,CONSTRAINT LGTX_LANG_FK FOREIGN KEY    (     LGTX_LANG_ID)
    	REFERENCES LANGUAGES    (     LANG_ID )
    ,CONSTRAINT LGTX_MODE_FK FOREIGN KEY    (     LGTX_MODE_ID)
		REFERENCES MODELELEMENT    (     MODE_ID )    ON DELETE CASCADE
)"""
                            )

        dbDDL.dropView("LANGATTR");
        dbDDL.createTable("""
                    create view langattr as
        	        select lgtx_text,lang_id,lang_iso_code2,lgtx_mode_id,lgtx_attrname
        	          from lang_texts 
        	          join languages on lang_id = lgtx_lang_id
        	          """);
    #createtable

    @staticmethod
    def delete():
        Baseobject.delete(Languagetext._tablename)

    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(pclass=Languagetext
                                ,pwhere=pwhere,porderby=porderby)
    @staticmethod
    def sptxistleer():
        data = dbDML.select("""select count(*) from lang_texts""")
        return data[0][0] == 0

    @staticmethod
    def filldefaulttext(plang):
        """füllt sämtliche übersetzten Elemente in die lang_texts der Defaultsprache ein.
           D.h. alle übersetzten Attribute haben mind. in der Defaultsprache einen  Eintrag.
        """
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
                   select 'ENTI_SYNONYM' attrname, syno_name text 
                        ,syno_id,syno_uc,syno_dc
                    from synonyms
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
                )
                cross join (select {} as lang_id)
                   """.format(plang))
    #filldefaulttext

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
            select 'SYNO_NAME' attrname,syno_name,lang_id,syno_id,syno_uc,syno_dc
            from synonyms
        cross join languages 
        where lang_is_base_lang = 'TRUE'"""
        dbDML.exec(lsql)

    # insertlang_texts

    @staticmethod
    def getlang_texts(pattrname,pmodeid):
        lsql = """with lgtx as 
            (select lgtx_lang_id,lgtx_text
             from lang_texts
            where lgtx_attrname = '{}'
            and lgtx_mode_id = {}
            )
        select lang_iso_code2,
            case when lgtx.lgtx_text is not NULL
                then lgtx.lgtx_text
                else lgtxdef.lgtx_text
                end text
        from languages
        left join lgtx as lgtx on lgtx.lgtx_lang_id = lang_id
        left join lgtx as lgtxdef on lgtxdef.lgtx_lang_id = lang_lang_id""".format(pattrname,pmodeid if pmodeid is not None else 'NULL')
        data = dbDML.select(lsql)
        retval = {d[0]:d[1] for d in data}
        return retval
    #getlang_texts


    __translNameEN = {'Anzeige': 'Display'
        , 'Arc': 'Arc'
        , 'Anzeige': 'Display'
        , 'Attribute': 'Attribute'
        , 'Attribute(e)': 'Attribute(s)'
        , 'Attribute': 'Attributes'
        , 'Attributgruppe': 'Attribute group'
        , 'auf Diagramm(en)': 'on diagram(s)'
        , 'Author': 'Author'
        , 'Beschreibung': 'Description'
        , 'Beziehung': 'Relationship'
        , 'Beziehung(en)': 'relationship(s)'
        , 'Beziehungen': 'Relationships'
        , 'Benutzerdefinerte Eigenschaften': 'User defined properties'
        , 'Bild': 'Picture'
        , 'Binär': 'Binary'
        , 'Datentyp': 'Datatype'
        , 'Deskriptor': 'descriptor'
        , 'Domänen': 'Domains'
        , 'Diagram': 'Diagram'
        , 'Diagramme': 'Diagrams'
        , 'Dokument': 'Document'
        , 'Dokumente': 'Documents'
        , 'Domäne': 'Domain'
        , 'Einheit': 'Unit'
        , 'Element': 'Element'
        , 'Elemente': 'Elements'
        , 'Entität': 'Entity'
        , 'Entität/Table': 'Entity/Table'
        , 'Entitäten': 'Entities'
        , 'erstellt': 'created'
        , 'Film': 'Video'
        , 'geändert': 'updated'
        , 'Gruppenattribut': 'Groupattribute'
        , 'Grafik': 'Graphic'
        , 'Granularität': 'Granularity'
        , 'historisiert': 'historicized'
        , 'in Schlüssel': 'within key'
        , 'Informationsmodell {} (Stand: {})': 'Informationmodel {} (Status: {})'
        , 'Informationen': 'Informations'
        , 'Inhaltstyp': 'Content type'
        , 'Ja': 'Yes'
        , 'Jahr': 'year'
        , 'Max. Länge': 'Max. length'
        , 'Max. Wert': 'Max. value'
        , 'Mehr': 'more'
        , 'Millisekunde': 'millisecond'
        , 'Minute': 'minute'
        , 'Min. Wert': 'Min. value'
        , 'Monat': 'month'
        , 'Nachkommast.': 'digits after period'
        , 'Name': 'Name'
        , 'Nein': 'No'
        , 'Nr': 'Nr'
        , 'Numerisch': 'Numerical'
        , 'Pflichtattribut': 'Attribute of duty'
        , 'Quartal': 'quarter'
        , 'Referenziert in': 'Referenced in'
        , 'Referenziert von': 'Referenced by'
        , 'Referenziert': 'References'
        , 'Relational Mapping (Tabellen)': 'Relational Mapping (tables)'
        , "Rollen": "Roles"
        , 'Rundungseinh.': 'rounding unit'
        , 'Schlüssel': 'Key'
        , 'Sekunde': 'second'
        , 'Semester': 'half-year'
        , 'Sort': 'Sort'
        , 'Stunde': 'hour'
        , 'Subentität': 'Subentity'
        , 'Subentitäten': 'Subentities'
        , 'Suchbegriff': 'search key'
        , 'Superentität': 'Superentity'
        , 'Superentitäten': 'Superentities'
        , 'Synonyme': 'Synonyms'
        , 'Syntaxregel': 'Syntax rule'
        , 'Systeme': 'Systems'
        , 'Tag': 'day'
        , 'Table': 'Table'
        , 'Tabellen': 'Tables'
        , 'Technischer Name': 'Technical Name'
        , 'Text': 'Text'
        , 'Ton': 'Sound'
        , 'Tooltip': 'Tooltip'
        , 'Treffer': 'Hits'
        , 'Typ': 'Type'
        , 'UDP-Matrix': 'UDP-Matrix'
        , 'übersetzt': 'translated'
        , 'Übersetzungen': 'Translations'
        , 'Unterdokumente': 'Children'
        , "Vaterdokument": "Parent"
        , 'verschlüsselt': 'encrypted'
        , 'Verwendet für Attribute': 'Used for attributes'
        , 'Verwendet für Columns': 'Used for columns'
        , 'Verwendet in Attributgruppen': 'Used in attribute groups'
        , 'Verwendet von': 'used by'
        , 'Vorkommast.': 'digits before period'
        , 'Wert': 'Value'
        , 'Wertebereich': 'Domain'
        , 'Wertebereiche': 'Domains'
        , 'Werteliste': 'List of values'
        , 'wiederholt': 'repeated'
        , 'Woche': 'week'
        , 'Zeitpunkt': 'Point in Time'
                      }
    __translNameFR = {"Anzeige": "Affichage"
        , "Arc": "Arc"
        , "Attribute": "Attribute"
        , "Attribute(e)": "Attribute(s)"
        , "Attribute": "Attributs"
        , "Attributgruppe": "Groupe d'attributs"
        , "auf Diagramm(en)": "sur ce diagramme(s)"
        , "Autor": "Auteur"
        , "Beschreibung": "Déscription"
        , "Beziehung": "Relation"
        , "Beziehung(en)": "Relation(s)"
        , "Beziehungen": "Relations"
        , "Benutzerdefinerte Eigenschaften": "Propriétés définies par l'utilisateur"
        , "Bild": "Image"
        , "Binär": "Binaire"
        , "Datentyp": "Type de données"
        , "Deskriptor": "Descripteur"
        , "Domänen": "Domaines"
        , "Diagram": "Diagramme"
        , "Diagramme": "Diagrammes"
        , "Domäne": "Domaine"
        , "Dokument": "Document"
        , "Dokumente": "Documents"
        , "Einheit": "Unité"
        , "Element": "Élément"
        , "Elemente": "Éléments"
        , "Entität": "Entité"
        , "Entität/Table": "Entité/Tableau"
        , "Entitäten": "Entités"
        , "erstellt": "Élaboré"
        , "Film": "Film"
        , "geändert": "changé"
        , "Gruppenattribut": "Attribute de groupe"
        , "Grafik": "Graphique"
        , "Granularität": "Granularité"
        , "historisiert": "historisé"
        , "in Schlüssel": "dans une clef"
        , "Informationsmodell {} (Stand {})": "Modèle d'informations {} (État {})"
        , "Informationen": "Informations"
        , "Inhaltstyp": "Type de contenu"
        , "Ja": "Oui"
        , "Jahr": "Année"
        , "Max. Länge": "Longueur max."
        , "Max. Wert": "Valeur max."
        , "Mehr": "Plus"
        , "Millisekunde": "Milliseconde"
        , "Minute": "Minute"
        , "Min. Wert": "Valeur min."
        , "Monat": "Mois"
        , "Nachkommastellen": "Décimales"
        , "Name": "Nom"
        , "Nein": "Non"
        , "Nr": "N°"
        , "Numerisch": "Numérique"
        , "Pflichtattribut": "Attribute obligatoire"
        , "Quartal": "Trimestre"
        , 'Referenziert in': 'Référencé dans'
        , 'Referenziert von': 'Référencé par'
        , 'Referenziert': 'Références'
        , "Relational Mapping (Tabellen)": "Relational Mapping (tables)"
        , "Rundungseinheit": "Unité de l'arrondi"
        , "Rollen": "Rôles"
        , "Schlüssel": "Clef"
        , "Sekunde": "Seconde"
        , "Semester": "Semestre"
        , "Sort": "Sorte"
        , "Stunde": "Heure"
        , "Subentität": "Sous-entité"
        , "Subentitäten": "Sous-entités"
        , "Suchbegriff": "Clef de recherche"
        , "Superentität": "Superentité"
        , 'Superentitäten': 'Superentités'
        , "Synonyme": "Synonyme"
        , "Syntaxregel": "Règle syntaxique"
        , "Systeme": "Systèmes"
        , 'Table': 'Table'
        , 'Tabellen': 'Tables'
        , "Tag": "Jour"
        , "Technischer Name": "Terme technique"
        , "Text": "Texte"
        , "Ton": "Ton"
        , "Tooltip": "Info-bulle"
        , "Treffer": "Occurrence"
        , "Typ": "Type"
        , "UDP-Matrix": "Matrice UDP"
        , "übersetzt": "traduit"
        , "Übersetzungen": "Traductions"
        , 'Unterdokumente': 'Enfants'
        , "Vaterdokument": "Document père"
        , "verschlüsselt": "Chiffré"
        , "Verwendet für Attribute": "Utilisé par les attributs"
        , 'Verwendet für Columns': 'Utilisé par les columns'
        , "Verwendet in Attributgruppen": "Utilisé dans les groupes d'attributs"
        , "Verwendet von": "Utilisé pour"
        , "Vorkommastellen": "Position avant la décimale"
        , "Wert": "Valeur"
        , "Wertebereich": "Domaine des valeurs"
        , "Wertebereiche": "Domaines des valeurs"
        , "Werteliste": "Liste des Valeur"
        , "wiederholt": "répété"
        , "Woche": "Semaine"
        , "Zeitpunkt": "Instant"
                      }
    @staticmethod
    def transl(pname,plang=None):
        lang = Languagetext.__greportLang if plang is None else plang
        if (lang == Languagetext.DE):
            return pname
        elif (lang == Languagetext.EN):
            try:
                return Languagetext.__translNameEN[pname]
            except:
                return pname
        elif (lang == Languagetext.FR):
            try:
                return Languagetext.__translNameFR[pname]
            except:
                return pname
        else:
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

#Languagetext

