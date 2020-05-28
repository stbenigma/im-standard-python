from IM_DB import dbDML,dbDDL
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

        dbDDL.dropView("SPRAATTR");
        dbDDL.createTable("""
                    create view spraattr as
        	        select sptx_text,spra_id,spra_iso_code2,sptx_mode_id,sptx_attrname
        	          from sprachtexte 
        	          join sprachen on spra_id = sptx_spra_id
        	          """);
    #createtable

    @staticmethod
    def delete():
        Baseobject.delete(Sprachtext._tablename)

    @staticmethod
    def select(pwhere=None,porderby=None):
        return Baseobject.select(pclass=Sprachtext
                                ,pwhere=pwhere,porderby=porderby)
    @staticmethod
    def sptxistleer():
        data = dbDML.select("""select count(*) from sprachtexte""")
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


    __translNameEN = {'Anzeige': 'Display'
        , 'Arc': 'Arc'
        , 'Anzeige': 'Display'
        , 'Attribut': 'Attribute'
        , 'Attribut(e)': 'Attribute(s)'
        , 'Attribute': 'Attributes'
        , 'Attributgruppe': 'Attribut group'
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
        , 'Diagramm': 'Diagram'
        , 'Diagramme': 'Diagrams'
        , 'Dokument': 'Document'
        , 'Domäne': 'Domain'
        , 'Einheit': 'Unit'
        , 'Element': 'Element'
        , 'Elemente': 'Elements'
        , 'Entität': 'Entity'
        , 'Entität/Tabelle': 'Entity/Table'
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
        , 'Referenziert von': 'Referenced by'
        , 'Relational Mapping (Tabellen)': 'Relational Mapping (tables)'
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
        , 'Synonyme': 'Synonyms'
        , 'Syntaxregel': 'Syntax rule'
        , 'Systeme': 'Systems'
        , 'Tag': 'day'
        , 'Tabelle': 'Table'
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
        , 'Verwendet in Attributgruppen': 'Used in attribute groups'
        , 'Verwendet von': 'used by'
        , 'Vorkommast.': 'digits before period'
        , 'Wert': 'Value'
        , 'Wertebereich': 'Domain'
        , 'Wertebereichs': 'Domains'
        , 'Werteliste': 'List of values'
        , 'wiederholt': 'repeated'
        , 'Woche': 'week'
        , 'Zeitpunkt': 'Point in Time'
                      }
    __translNameFR = {"Anzeige": "Affichage"
        , "Arc": "Arc"
        , "Attribut": "Attribut"
        , "Attribut(e)": "Attribut(s)"
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
        , "Diagramm": "Diagramme"
        , "Diagramme": "Diagrammes"
        , "Domäne": "Domaine"
        , "Dokument": "Document"
        , "Einheit": "Unité"
        , "Element": "Élément"
        , "Elemente": "Éléments"
        , "Entität": "Entité"
        , "Entität/Tabelle": "Entité/Tableau"
        , "Entitäten": "Entités"
        , "erstellt": "Élaboré"
        , "Film": "Film"
        , "geändert": "changé"
        , "Gruppenattribut": "Attribut de groupe"
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
        , "Pflichtattribut": "Attribut obligatoire"
        , "Quartal": "Trimestre"
        , 'Referenziert von': 'Référencé par'
        , "Relational Mapping (Tabellen)": "Relational Mapping (tables)"
        , "Rundungseinheit": "Unité de l'arrondi"
        , "Schlüssel": "Clef"
        , "Sekunde": "Seconde"
        , "Semester": "Semestre"
        , "Sort": "Sorte"
        , "Stunde": "Heure"
        , "Subentität": "Sous-entité"
        , "Subentitäten": "Sous-entités"
        , "Suchbegriff": "Clef de reherche"
        , "Superentität": "Superentité"
        , "Synonyme": "Synonyme"
        , "Syntaxregel": "Règle syntaxique"
        , "Systeme": "Systèmes"
        , 'Tabelle': 'Table'
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
    def transl(pname):
        if (__greportLang == 'de'):
            return pname
        elif (__greportLang == 'en'):
            try:
                return __translNameEN[pname]
            except:
                return pname
        elif (__greportLang == 'fr'):
            try:
                return __translNameFR[pname]
            except:
                return pname
        else:
            return pname
    # transl


    __greportLang: str = None

    @staticmethod
    def reportLang(newval=None):
        global __greportLang
        if (newval is None):
            return __greportLang
        else:
            __greportLang = newval
    # reportLang

#Sprachtext

