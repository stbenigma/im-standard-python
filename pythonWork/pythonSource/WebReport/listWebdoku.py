# -*- coding: latin-1 -*-
import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../IM_db')
from datetime import date
from IM_ODM import odmParam
from IM_DB import dbParam,dbConnect,dbDDL,dbDML,dbErstelleTables,dbInserts,dbLookup
from IM_HTML import printHTML

greportLang:str = ''

translNameEN = {'Attribut': 'Attribute'
                ,'Attribut(e)': 'Attribute(s)'
                ,'Attribute': 'Attributes'
                ,'Author': 'Author'
                ,'Beschreibung': 'Description'
                ,'Beziehung': 'Relationship'
                ,'Beziehung(en)': 'relationship(s)'
                ,'Beziehungen': 'Relationships'
                ,'Binär': 'Binary'
                ,'Datentyp': 'Datatype'
                ,'Domains': 'Domains'
                ,'Entität': 'Entity'
                ,'Entität1': 'Entity1'
                ,'Entität2': 'Entity2'
                ,'Entitäten': 'Entities'
                ,'Erstellt': 'Generates'
                ,'Gruppenattribut': 'Groupattribute'
                ,'Informationsmodell {} (Stand: {})': 'Informationmodel {} (Status: {})'
                ,'Ja': 'Yes'
                ,'Name': 'Name'
                ,'Nein': 'No'
                ,'Nr': 'Nr'
                ,'Numerisch': 'Numerical'
                ,'Schlüssel': 'Key'
                ,'Subentität': 'Subentity'
                ,'Subentitäten': 'Subentities'
                ,'Superentitäten': 'Superentity'
                ,'Synonyme': 'Synonyms'
                ,'Technischer Name': 'Technical Name'
                ,'Text': 'Text'
                ,'Typ': 'Type'
                ,'UDP-Matrix': 'UDP-Matrix'
                ,'Wertebereich': 'Domain'
                ,'Werteliste': 'Valuelist'
                ,'Zeitpunkt': 'Point in Time'
                }

udpThemenSql:str = """select distinct bdeg_thema
                    from benudef_eigenschaft
                    join modelltyp_eigensch on mote_bdeg_id = bdeg_id
                    join modellelem_typ on melt_id = mote_melt_id
                                    and melt_kurzname = 'ATTR'
                                    and bdeg_thema != 'translation'
                    order by bdeg_thema"""

def langText(attrName, sprache, modeId):
   lsql= """select sptx_text
    from spraattr
    where spra_iso_code2 = lower('{}')
     and sptx_mode_id = {}
     and sptx_attrname = '{}'
    """.format(sprache,modeId,attrName)
   ltext = dbDML.select(lsql)[0][0]
   return ltext
#langText
def enti_name(lang,modeId):
    return langText('ENT_NAME', lang, modeId)
def enti_comment(lang,modeId):
    return langName('ENT_COMMENT',lang,modeId)
def attr_name(lang,modeId):
    return langName('ATTR_NAME',lang,modeId)
def attr_comment(lang,modeId):
    return langName('ATTR_COMMENT',lang,modeId)
def bezi_from(lang,modeId):
    return langName('TEXT_FROM',lang,modeId)
def bezi_to(lang,modeId):
    return langName('TEXT_TO',lang,modeId)

def entiAnker(id):
    return 'ENTI'+str(id)
def attrAnker(id):
    return 'ATTR'+str(id)
def beziAnker(id):
    return 'BEZI'+str(id)
def schlAnker(id):
    return 'SCHL'+str(id)
def wrtbAnker(id):
    return 'WRTB'+str(id)
def udpAnker(id):
    return 'UDP'+str(id)

# Main Programm
def nvl(x,default=''):
    if x is None: return default
    else: return x
#nvl

def href(ref,anz):
    return """<a href="#{}" target="details">{}</a>""".format(ref,anz)
#href

def makeAnker(ref,anz):
    return """<a name = "{}" >{}</a>""".format(ref,anz)
#href

def anzDatentyp(dt):
    anzDT = {'BIN': transl('Binär')
             ,'GRP': transl('Gruppenattribut')
             ,'LOV': transl('Werteliste')
             ,'NUM': transl('Numerisch')
             ,'TEXT': transl('Text')
             ,'ZPKT': transl('Zeitpunkt')}
    return anzDT[dt]
#anzDatentyp

def transl(pname):
   if (greportLang == 'de'):
       return pname
   elif (greportLang == 'en'):
       try:
           return translNameEN[pname]
       except:
           return pname
   else:
       return pname
#translate

def formatDatentyp(w):
    dt = anzDatentyp(w[0])
    #print (w)
    return(
    "{}   ({}) {} {}" .format(dt, w[3], nvl(w[1])\
        + ' - ' if w[1] is not None else ''
            , nvl(w[2]), nvl(w[11]), nvl(w[6])) if w[0] == 'ZPKT'\
        else '{}  ({}:{})   {}  {}'\
                .format(dt, nvl(w[8]), nvl(w[9]), nvl(w[7]).__str__() \
            + ' - ' if w[7] is not None else ''
            , nvl(w[10]))     if w[0] == 'NUM'\
        else '{}  ({}) {}'\
            .format(dt, nvl(w[4]), 'CHECK: ' + w[5] if (not (w[5] is None))
                                            else '')   if w[0] == 'TEXT'\
        else '{}  ({})'\
                 .format(dt, nvl(w[4])) if w[0] == 'LOV'\
        else dt
    )
#formatDatentyp

def bool2JN(b):
    return 'Ja' if (b == 'TRUE') else 'Nein'
#bool2JN

def printUDP(meltName, Id):
#    printHTML.startTable('Attribute - User Defined Properties: ' + nvl(thema), udpListe, anker='ATTRUDP')#
#
#
#for at in allattr:
#    values = [href(ref=entiAnker(at[1]), anz=at[0]), href(ref=attrAnker(at[2]), anz=at[3])
#        , nvl(at[4]), nvl(at[6])]

    #    udpTypen = dbDML.select("""select distinct bdeg_thema,bdeg_gruppe
#                                    from benudef_eigenschaft
#                                    join modelltyp_eigensch on mote_bdeg_id = bdeg_id
#                                    join modellelem_typ on melt_id = mote_melt_id
#                                                        and melt_kurzname = '{}' 
#                    """ .format(meltName))
    ludpNamen = """select  bdeg_thema,bdeg_gruppe,group_concat(bdeg_name,',') attrs
                           from modellelem_typ
                           join modelltyp_eigensch on mote_melt_id = melt_id  
                           join benudef_eigenschaft on bdeg_id = mote_bdeg_id
                           where melt_kurzname = '{}'
                             and bdeg_thema != '{}'
                        group by bdeg_thema,bdeg_gruppe
                        order by bdeg_thema,bdeg_gruppe""".format(meltName,odmParam.imTranslationFileName)
    udpNamen = dbDML.select(ludpNamen)
    for udpName in udpNamen:
        lsql = """select  bdwe_wert
                    from benudef_wert
                    join modellelement on mode_id = bdwe_mode_id
                                            and ({} = {}) 
                    join benudef_eigenschaft on bdeg_id = bdwe_bdeg_id
                            and bdeg_thema = '{}' and bdeg_gruppe = '{}'
                    order by bdeg_name
                    """.format("mode_" +
                                ("enti" if meltName == 'ENTI'
                                 else "attr" if meltName == 'ATTR'
                                 else "")
                                + "_id " , Id
                               ,udpName[0],udpName[1]
                               )
        lwerte = dbDML.select(lsql)
        #print(udpName[0],udpName[1],lwerte)
        lw = [];
        for l in lwerte:
            lw.append(nvl(l[0]))
        #rof
        #print (udpName[0],udpName[1],lw)
        namenliste = udpName[2].split(',')
        namenliste.sort() #SQl kann keine sortierte group_concat liefern
        printHTML.startTable('Benutzerdefinerte Werte: {} - {} '.format(udpName[0], udpName[1])
                             , namenliste)

        printHTML.writeTable(lw)
        printHTML.endTable('')
    #rof
#printUDP

def printAttrUDPMatrix(thema=None):
    udpListe = [transl('Entität'),transl('Attribut'),transl('Technischer Name'),transl('Datentyp')]
    lsql = """select  bdeg_name,bdeg_thema,bdeg_gruppe
                    from benudef_eigenschaft
                    join modelltyp_eigensch on mote_bdeg_id = bdeg_id
                    join modellelem_typ on melt_id = mote_melt_id
                                    and melt_kurzname = 'ATTR'
                    where bdeg_thema like '{}'
                    order by bdeg_thema,bdeg_gruppe,bdeg_name
                        """ .format(nvl(thema,'%'))
    udpWerte = dbDML.select(lsql)
    for udpWert in udpWerte:
        udpListe.append(udpWert[0])
    #print ('udpListe=',udpListe)
    allattr = dbDML.select("""select * from 
        (select 
       case when ena.sptx_text is null then enti_name else ena.sptx_text end enti_name
       ,enti_id,attr_id,case when ana.sptx_text is null then attr_anzname else ana.sptx_text end attr_anzname
       ,attr_tech_name,wrtb_name,wrtb_typ
      from attributes 
        join sprachen sp on sp.spra_iso_code2 = '{}'
        join modellelement ma on ma.mode_attr_id = attr_id
        left join spraattr  ana on ana.sptx_attrname = 'ATTR_NAME'
                                    and ana.sptx_mode_id = ma.mode_id
                                    and ana.spra_id = sp.spra_id            
      join entitaeten on enti_id = attr_enti_id
        join modellelement me on me.mode_enti_id = enti_id
        left join spraattr  ena on ena.sptx_attrname = 'ENT_NAME'
                                    and ena.sptx_mode_id = me.mode_id
                                    and ena.spra_id = sp.spra_id            
      join wertebereiche on wrtb_id = attr_wrtb_id
      ) order by enti_name,upper(attr_tech_name)"""
                           .format(greportLang))
    printHTML.startTable('Attribute - User Defined Properties: '+nvl(thema), udpListe,anker=udpAnker(thema))
    for at in allattr:
        values = [href(ref=entiAnker(at[1]), anz=at[0]), href(ref=attrAnker(at[2]), anz=at[3])
                              ,nvl(at[4]),nvl(at[6])]
        lsql = """select  bdwe_wert
                    from benudef_wert
                    join modellelement on mode_id = bdwe_mode_id
                                        and (mode_attr_id = {}) 
                    join benudef_eigenschaft on bdeg_id = bdwe_bdeg_id
                    where bdeg_thema like '{}'
                    order by bdeg_thema,bdeg_gruppe,bdeg_name
                    """.format(at[2],nvl(thema,'%'))
        udpWerte = dbDML.select(lsql)
        for udpWert in udpWerte:
            values.append(nvl(udpWert[0]))
        printHTML.writeTable(values)
    # endFor
    printHTML.endTable('')

#printAttrUDPMatrix


def printSchluessel(entiId):
    printHTML.startTable('Schlüssel', ('Nr', 'Name', 'Attribut(e)', 'Beziehung(en)'))


    schl = dbDML.select("""
    select  schl_id,schl_laufnr,schl_name
                  ,group_concat('<a href="#ATTR'||attr_id||'" target="details">'
                                    ||
                                    case when ana.sptx_text is null then attr_anzname else ana.sptx_text end 
                                    ||'</a>', ', ') attrs
                  ,group_concat('<a href="#BEZI'||bezi_id||'" target="details">'
                                    ||bezi_name||'</a>', ', ') bezis
         from schluessel
         join schluesselelement on scel_schl_id = schl_id
            join sprachen sp on sp.spra_iso_code2 = '{}'
         left join attributes on attr_id = scel_attr_id
            left join modellelement ma on ma.mode_attr_id = attr_id
            left join spraattr  ana on ana.sptx_attrname = 'ATTR_NAME'
                                    and ana.sptx_mode_id = ma.mode_id
                                    and ana.spra_id = sp.spra_id            
         left join beziehungen on bezi_id = scel_bezi_id
         where schl_enti_id = {}
           group by schl_id,schl_laufnr,schl_name
                    """.format(greportLang,entiId))

    for s in schl:
        printHTML.writeTable((s[1],s[2],nvl(s[3]),nvl(s[4])))
    printHTML.endTable('')


#printSchluessel


def printBezi(entiId):
    printHTML.startTable('Beziehungen', ('Name','Entität1','','Beziehung','', 'Entität2','Arc'))
    bezi = dbDML.select("""
          with sprenti as 
          (select enti_id, enti_odm_guid
                ,case when ena.sptx_text is null then enti_name else ena.sptx_text end enti_name
                ,spra_id
             from entitaeten
             join modellelement on mode_enti_id = enti_id
              left join spraattr ena on ena.sptx_attrname = 'ENT_NAME'
                                and ena.sptx_mode_id = mode_id
           )
            select von.enti_id as von_enti_id,von.enti_name as von_name,von.enti_odm_guid as von_guid
                        		,case when bvon.sptx_text is null then  bezi_assoc_von_zu else bvon.sptx_text end  bezi_assoc_von_zu
    							,case bezi_type
                           when '1:1' then 
                            case bezi_pflicht_assoc_von_zu
                                 when 'TRUE' THEN '1'
                                 else '0..1'
                               end
                           when 'M:N' then 
                            case bezi_pflicht_assoc_von_zu
                                 when 'TRUE' THEN '1..N'
                                 else '0..N'
                               end
                           when 'M:1' then 
                                case bezi_pflicht_assoc_von_zu
                                 when 'TRUE' THEN '1'
                                 else '0..1'
                               end         
                            end card1
    						,zu.enti_id as zu_enti_id,zu.enti_name as zu_name,zu.enti_odm_guid as zu_guid
    						,case when bzu.sptx_text is null then  bezi_assoc_zu_von else bzu.sptx_text end bezi_assoc_zu_von
    	                    ,case bezi_type
    	                       when '1:1' then 
    	                          case bezi_pflicht_assoc_zu_von
    	                             when 'TRUE' THEN '1'
    	                             else '0..1'
    	                           end
    	                       when 'M:N' then 
    	                        case bezi_pflicht_assoc_zu_von
    	                             when 'TRUE' THEN '1..N'
    	                             else '0..N'
    	                           end
    	                       when 'M:1' then 
    	                            case bezi_pflicht_assoc_zu_von
    	                             when 'TRUE' THEN '1..N'
    	                             else '0..N'
    	                           end         
    	                        end card2
    						,bezi_id,bezi_type,bezi_pflicht_assoc_von_zu,bezi_pflicht_assoc_zu_von
    						,arcs_name,arcs_odm_guid,bezi_name
                        from   sprachen sp          
                        join sprenti as von on von.spra_id = sp.spra_id
    					join beziehungen on bezi_enti_id_von = von.enti_id
    									and bezi_type != 'ISA'
    					join modellelement on mode_bezi_id = bezi_id
                        left join spraattr bvon on bvon.sptx_attrname = 'TEXT_FROM'
                                and bvon.sptx_mode_id = mode_id
                                and bvon.spra_id = sp.spra_id 
                        left join spraattr bzu on bzu.sptx_attrname = 'TEXT_TO'
                                and bzu.sptx_mode_id = mode_id
                                and bzu.spra_id = sp.spra_id 
                        join sprenti as zu on zu.enti_id = bezi_enti_id_zu
                        left join arcs on arcs_id = bezi_arcs_id
                                   and bezi_enti_id_von = von.enti_id
                        where  sp.spra_iso_code2 = '{}'
                           and von.enti_id = {} or zu.enti_id = {}     
                        order by arcs_name 
                        """.format(greportLang,entiId, entiId))

    #print (bezi)
    for c in bezi:
        if (entiId == c[0]):
            #'Name','Entität1','','Beziehung','', 'Entität2','Arc'
            printHTML.writeTable((nvl(c[16]),c[1], '->',nvl(c[3],'--'),c[4] , '',''))
            printHTML.writeTable(('','', c[9],nvl(c[8],'--'),'<-' , href(ref=entiAnker(c[5]), anz=c[6]),nvl(c[14])))
        else:
            printHTML.writeTable((nvl(c[16]),c[6], '->',nvl(c[8],'--'),c[9] , '',''))
            printHTML.writeTable(('','', c[4],nvl(c[3],'--'),'<-' , href(ref=entiAnker(c[0]), anz=c[1]),''))
        #if
    printHTML.endTable('')
#printBez

def main():
    global greportLang
    limDirec = sys.argv[1] if (len(sys.argv)>1) else None
    greportLang = sys.argv[2] if (len(sys.argv)>2) else None
    lModelName = sys.argv[3] if (len(sys.argv)>3) else None
    lWebDirec = sys.argv[4] if (len(sys.argv)>4) else None


    odmParam.initODMParam(pimDirec=limDirec,pmodelName=lModelName)

    #print(odmParam.imModelName,odmParam.imDirectory);
    printHTML.setWebDirec(pwebDirec=lWebDirec,pbaseDirec =  odmParam.imDirectory if (limDirec is None) else limDirec)
#    print (printHTML.webDirectory,printHTML.webFileName,printHTML.detailDirectory
#    ,printHTML.webFileNameSpec,printHTML.tocFileName,printHTML.contFileName,printHTML.indexFileName);
#    print(printHTML.libSourceDirec);

    dbParam.initDBParam(odmParam.imDirectory
                ,odmParam.imModelName+'.db');
    dbConnect.openDB(dbParam.dbDirectory, dbParam.dbName);
    dbParam.liesDefaultLang()
    greportLang = greportLang.lower() if (greportLang is not None) else dbParam.dbDefaultLang

    printHTML.createIndex ("Informationsmodell {} (Stand: {})"
                           .format(odmParam.imModelName,date.today()));

    enti = dbDML.select( """select * from 
              (select case when ena.sptx_text is null then e1.enti_name else ena.sptx_text end  name,e1.enti_odm_guid,
             case when ebe.sptx_text is null then e1.enti_beschr else ebe.sptx_text end beschr
            ,e1.enti_uc,e1.enti_dc,e1.enti_id 
          ,super_enti_name,super_enti_id,NULL superentity_guid
          ,(select group_concat('<a href="#ENTI'||sub_enti_id||'" target="details">'
                                    ||sub_enti_name||'</a>'
                            ,', ') subent
              from superenti where super_enti_id = e1.enti_id
              ) as subentities
            ,(select group_concat(syno_name,', ') synos
              from synonyme
              where syno_enti_id = e1.enti_id
              ) as subentities
          from entitaeten e1
          join modellelement on mode_enti_id = enti_id
           join sprachen sp on sp.spra_iso_code2 = '{}'         
          left join spraattr ebe on ebe.sptx_attrname = 'ENT_COMMENT'
                                and ebe.sptx_mode_id = mode_id
                                and ebe.spra_id = sp.spra_id
          left join spraattr ena on ena.sptx_attrname = 'ENT_NAME'
                                and ena.sptx_mode_id = mode_id
                                and ena.spra_id = sp.spra_id
          left join superenti on  sub_enti_id = e1.enti_id
          ) order by upper(name)
              """.format(greportLang))
#    for e in enti:
#        print (e)
    printHTML.writeToc("""<div><ol class ="tree"><li><label for="entities">Entitäten</label>
                <input type="checkbox" id="entities" /><ol>
    """)
    for e in enti:
        printHTML.writeToc("""<li class="obj"><a href="{}#{}" \
                target="details">{}</a></li>
                """.format(printHTML.contFileName + ".html", entiAnker(e[5]),e[0]))
    #endfor
    printHTML.writeToc("</ol></ol></div>")

    attr = dbDML.select("""select attr_tech_name || ' ('||enti_name||')' as vollname ,attr_odm_guid,attr_tech_name
            ,attr_anzname,enti_odm_guid,attr_uc
           ,attr_dc,attr_beschr,enti_name
           ,wrtb_id,wrtb_name,wrtb_typ
           ,attr_id,enti_id
           ,(select group_concat('<a href="#SCHL'||schl_id||'" target="details">'
                                    ||schl_laufnr||'</a>',',')
               from schluesselelement 
                join schluessel on schl_id = scel_schl_id
                where scel_attr_id = attr_id
            ) as schluessel
          from (select  attr_tech_name, attr_odm_guid, 
                case when ana.sptx_text is null then attr_anzname else ana.sptx_text end attr_anzname
                , case when abe.sptx_text is null then attr_beschr else abe.sptx_text end  attr_beschr
                ,attr_id,sp.spra_id,
                attr_uc,attr_dc,attr_enti_id,attr_wrtb_id
                 from attributes
                 join modellelement on mode_attr_id = attr_id
                 join sprachen sp on sp.spra_iso_code2 = '{}'
                 left join spraattr  ana on ana.sptx_attrname = 'ATTR_NAME'
                                    and ana.sptx_mode_id = mode_id
                                    and ana.spra_id = sp.spra_id 
                 left join spraattr  abe on abe.sptx_attrname = 'ATTR_COMMENT'
                                    and abe.sptx_mode_id = mode_id 
                                    and abe.spra_id = sp.spra_id
                ) attr         
          join (select case when ena.sptx_text is null then enti_name else ena.sptx_text end enti_name
                    ,enti_id,spra_id spra_id,enti_odm_guid
                 from entitaeten 
                 join modellelement on mode_enti_id = enti_id
                left join spraattr ena on ena.sptx_attrname = 'ENT_NAME'
                                and ena.sptx_mode_id = mode_id 
                ) ent on enti_id = attr_enti_id
                     and ent.spra_id = attr.spra_id
          join wertebereiche on wrtb_id = attr_wrtb_id
          order by upper(attr_tech_name)
          """.format(greportLang))
    printHTML.writeToc("""<div><ol class ="tree"><li><label for="attributes">Attribute</label>
                <input type="checkbox" id="attributes" /><ol>
    """)
    for a in attr:
        printHTML.writeToc("""<li class="obj"><a href="{}#{}" \
                target="details">{}</a></li>
                """.format(printHTML.contFileName + ".html", attrAnker(a[12]), a[3]))
    #endfor
    printHTML.writeToc("</ol></ol></div>")
    wrtb = dbDML.select("""select * from wertebereiche order by upper(wrtb_name)""")
    printHTML.writeToc("""<div><ol class ="tree"><li><label for="objects">Domains</label>
            <input type="checkbox" id="objects" /><ol>
            """)
    for w in wrtb:
        printHTML.writeToc("""<li class="obj"><a href="{}#{}" target="details">{}</a></li>\
           """ .format(printHTML.contFileName + ".html", wrtbAnker(w[0]), w[2]))
    #endfor
    printHTML.writeToc("</ol></ol></div>")

    printHTML.writeToc("""<div><ol class ="tree"><li><label for="objects">UDP-Matrix</label>
            <input type="checkbox" id="objects" /><ol>
            """)
    udpAttrThema = dbDML.select(udpThemenSql)
    for u in udpAttrThema:
        printHTML.writeToc("""<li class="obj"><a href="{}#{}" target="details">{}</a></li>\
           """.format(printHTML.contFileName + ".html", udpAnker(u[0]), u[0]))
    printHTML.writeToc("</ol></ol></div>")

    printHTML.closeToc("""</div></div>""")

    ############################

    for e in enti:
        printHTML.printTable({transl('Entität'): e[0], "Beschreibung":nvl(e[2])
                              ,"Synonyme":nvl(e[10])
        , "Autor":e[3], "Erstellt":e[4], "Superentität":href(entiAnker(e[7]), anz=nvl(e[6]))
                , "Subentitäten":nvl(e[9])}, anker=entiAnker(e[5]))

        eattr = dbDML.select("""select 
           attr_odm_guid,attr_tech_name
           ,case when ana.sptx_text is null then attr_anzname else ana.sptx_text end attr_anzname
           ,wrtb_odm_guid,wrtb_name,attr_pflichtattr
           ,attr_historisiert,attr_wiederholt,attr_sprachabhaengig
           ,attr_verschluesselt,wrtb_typ,attr_deskriptor
           ,attr_id,wrtb_id             
           ,(select group_concat('<a href="#SCHL'||schl_id||'" target="details">'
                                    ||schl_laufnr||'</a>',',')
               from schluesselelement 
                join schluessel on schl_id = scel_schl_id
                where scel_attr_id = attr_id
            ) as schluessel
          from attributes 
                 join modellelement on mode_attr_id = attr_id
                 join sprachen sp on sp.spra_iso_code2 = '{}'
                 left join spraattr  ana on ana.sptx_attrname = 'ATTR_NAME'
                                    and ana.sptx_mode_id = mode_id
                                    and ana.spra_id = sp.spra_id            
                join wertebereiche on wrtb_id = attr_wrtb_id
          where attr_enti_id = {}
          order by upper(attr_tech_name)""" .format(greportLang,e[5]))
        entiId = e[5]
        printUDP(meltName='ENTI', Id=entiId)
        printHTML.startTable('Attribute', ('Name', 'Domäne', 'Typ','in Schlüssel'
                                             , 'Pflichtattribut','Deskriptor','übersetzt','historisiert','wiederholt'
                                             ,'verschlüsselt'))
        for eat in eattr:
            printHTML.writeTable((href(ref=attrAnker(eat[12]), anz=eat[2]), href(ref=wrtbAnker(eat[13]), anz=eat[4])
                                     , anzDatentyp(eat[10]), nvl(eat[14]),bool2JN(eat[5]), bool2JN(eat[11])
                                     , bool2JN(eat[6]), bool2JN(eat[7]), bool2JN(eat[8]), bool2JN(eat[9])))
        #endFor
        printHTML.endTable('')
        printBezi(entiId=entiId)
        printSchluessel(entiId=entiId)
    #endfor


    for a in attr:
            #        select
            #        attr_tech_name || ' ('||enti_name||')' as vollname,attr_odm_guid,attr_tech_name
            #        ,attr_anzname,enti_odm_guid,attr_uc
            #           ,attr_dc,attr_beschr,enti_name
            #           ,wrtb_id,wrtb_name,wrtb_typ
            #           ,attr_id,enti_id,schluessel
        printHTML.printTable({"Attribut": a[3], transl('Entität'): href(ref=entiAnker(a[13]), anz=a[8])
                                     , "Wertebereich": href(ref=wrtbAnker(a[9]), anz=a[10])
                                     , "Datentyp": anzDatentyp(a[11])
                                     , "Beschreibung": nvl(a[7])
                                     , "in Schlüssel": nvl(a[14])
                                     , "Autor": a[5], "Erstellt": a[6]}, anker=attrAnker(a[12]))

        # print (a)
        attrId = a[12]
        printUDP(meltName='ATTR', Id=attrId)
    # rof

    for w in wrtb:
        #print (w)
        printHTML.printTable({"Wertebereich": w[2], "Beschreibung":nvl(w[3])\
                                    ,"Datentyp":formatDatentyp((w[4],w[5],w[6],w[7],w[8],w[9],w[10],w[11],w[12],w[13],w[6],w[10]))
        , "Autor":w[18], "Erstellt":w[19]} \
                             , anker=wrtbAnker(w[0]))
        #print (w)
        doms = dbDML.select("select * from vorgabewerte where vgwt_wrtb_id ={} order by vgwt_sortrhfg" .format(w[0]))
        if doms != []:
            printHTML.startTable('Werteliste', ('Sort', 'Wert', 'Anzeige', 'Beschreibung'))
            #print ("Vorgabewerte",doms)
            for d in doms:
                #print (d)
                printHTML.writeTable((d[2], d[1], d[4], d[5]))
            #endfor
            printHTML.endTable('')
        #endif
        printHTML.startTable('Verwendet von', ('Typ', 'Entität/Tabelle', 'Name'))
        attcols = dbDML.select("""select 'Attribut' as attr ,enti_name,attr_tech_name
                        , attr_id,enti_id
                        from attributes 
                     join sprachen sp on sp.spra_iso_code2 = '{}'         
                      join (select case when ena.sptx_text is null then enti_name else ena.sptx_text end enti_name
                                ,enti_id,spra_id ,enti_odm_guid
                        from entitaeten 
                        join modellelement on mode_enti_id = enti_id
                       left join spraattr ena on ena.sptx_attrname = 'ENT_NAME'
                                and ena.sptx_mode_id = mode_id 
                ) ent on enti_id = attr_enti_id
                     and ent.spra_id = sp.spra_id
                        where attr_wrtb_id = {}""" .format(greportLang,w[0]))
        for c in attcols:
            printHTML.writeTable((c[0], href(ref=entiAnker(c[4]), anz=c[1]), href(ref=attrAnker(c[3]), anz=c[2])))
        printHTML.endTable('')
    #endfor

    for u in udpAttrThema:
        printAttrUDPMatrix(thema=u[0])
    # printAttrUDPMatrix()


    printHTML.closeCont('')
    dbConnect.myDbConn.close()
#end main

if __name__ == '__main__':
    main()