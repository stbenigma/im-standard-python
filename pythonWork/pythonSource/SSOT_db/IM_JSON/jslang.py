from SSOT_db.IM_JSON import  *
from SSOT_db.IM_OBJECTS import Languagetext, Language, Boolean
from SSOT_db.SQL_INFRA import dbConnect
from datetime import datetime

def replaceprefix(plang):
    return f"*{plang}* "

def langs2js(pemptymodel):
    model = ['name', 'iso3', 'modellanguage', 'replacementlang']
    if pemptymodel:
        langs ={'en': fillmodel(pmodel=model, pentries=['' for idx in range(len(model))])}
    else:
        langs = {l.lang_iso_code2: fillmodel(pmodel=model,
                                             pentries=[l.lang_iso_name, l.lang_iso_code3,
                                                    Boolean.str2bool(l.lang_is_base_lang),
                                                     None if l.lang_lang_id is None else Language().getbyid(l.lang_lang_id).lang_iso_code2]
                                             )
                 for l in Language.select()
                 }
    # fi
    return langs
# languages

def replacelgtx(presult:Mergeresult, pmodeid, pattr, ptexts):
    """Starting Version *******
            delete all texts from this modeid
       Later probably
            delete all texts from all languages in ptexts
       Then
           insert all texts from all languages """

    delcnt = Languagetext.delete(pwhere=("""lgtx_mode_id = ? 
                            and lgtx_attrname = ?""",
                            pmodeid, pattr))
    inscnt =insertlgtx(presult,pmodeid=pmodeid,pattr=pattr,ptexts=ptexts)

    presult.addinscnt(max(0,inscnt - delcnt),f"lang_texts for mode {pmodeid}, attribute {pattr}")
    presult.adddelcnt(max(0,delcnt - inscnt),f"lang_texts for mode {pmodeid}, attribute {pattr}")
    return

# replacelgtx

def insertlgtx(presult,pmodeid, pattr, ptexts):
    inscnt = 0
    baselang = Language.liesdeflangiso2()

    for lang in Language.select():
        iso2 = lang.lang_iso_code2
        if iso2 in ptexts.keys():
            if (iso2 != baselang\
                    and (ptexts[iso2] is None or ptexts[iso2] == ''
                         or ptexts[iso2].startswith(replaceprefix(baselang)))
                ):
                continue  #insert only genuine texts, not replacement or emptytexts
            lgtx = Languagetext()
            lgtx.lgtx_attrname = pattr
            lgtx.lgtx_text = ptexts[iso2]
            lgtx.lgtx_lang_id = lang.lang_id
            lgtx.lgtx_mode_id = pmodeid
            lgtx.lgtx_uc = "sys"
            lgtx.lgtx_dc = datetime.today()
            try:
                lgtx.insert()
                inscnt += 1
            except Exception as err:
                presult.markdberror(perr=err, pelem=lgtx.tostring())
                continue
        #if
    #for
    return inscnt
# replacelgtx

def js2lang(pkey,pelem,psrcname=None,psrcid=None,pmodellang=None):
    lang = Language()
    lang.lang_iso_code2 = pkey
    lang.lang_iso_code3 = pelem['iso3']
    lang.lang_iso_name = pelem['name']
    lang.lang_is_base_lang = Boolean.bool2str(pelem['modellanguage'])
    lang.lang_is_text_lang = Boolean.TRUE
    return lang

def langs2sql(presult:Mergeresult, pjson:JSModel,pwithextsrcref):
    assert dbConnect.isopenDB()
    """   "languages": {
      "de": {
         "name": "Deutsch",
         "iso3": "deu",
         "modellanguage": true,
         "replacementlang": null
      }"""
    """exclude lang_lang_id from semantic compare"""
    fromjson2db(presult=presult,pjson=pjson,pelemtype=JSModel.ELEMTYPE_LANG,pjs2obj=js2lang,pwithextsrcref=pwithextsrcref,pequalexceptlist=['lang_lang_id'])

    try:
        deflang =  Language.getdefaultlang()
        if deflang is None: presult.markdberror("""*** No modellanguage defined""",pelem="defaultlang")
    except:
        presult.markerror("""*** more then one default modellanguage defined""")

    """update proj_languages field with all languages found"""
    for iso2, jlang in pjson.getelements(pelemtype=JSModel.ELEMTYPE_LANG).items():
        newlang:Language = Language().getbyuk(lang_iso_code2=iso2)
        if newlang is not None:
            replacementiso2 = jlang["replacementlang"]
            if replacementiso2 is None:
                replacmentid = None
            else:
                replacmentid = Language().getbyuk(lang_iso_code2 = replacementiso2).getid()
            #fi
            if newlang.lang_lang_id != replacmentid:
                newlang.updatedb()
                presult.addupdcnt(1,f"replacement Language for {newlang.lang_iso_code2} changed")
        # for

    try:
        deflang =  Language.getdefaultlang()
        if deflang is None: presult.markdberror("""*** No modellanguage defined""",pelem="defaultlang")
    except:
        presult.markerror("""*** more then one default modellanguage defined""")

    """check all languages have replacementlanguage"""
    langs = Language.getlangswithillegalreplacement()
    if len(langs) > 0:
        presult.markdberror(f"Illegal replacementlanguage(s) {','.l.lang_iso_code2 for l in langs}")
    return
# langs2sql
