from datetime import date
from IM_JSON import *
from IM_OBJECTS import Languagetext, Language, Boolean,Project
from IM_DB import dbConnect

def langs2js(pemptymodel):
    model = ['name', 'iso3', 'modellanguage', 'replacementlang']
    if pemptymodel:
        langs ={'en': fillmodel(pmodel=model, pentries=['' for idx in range(len(model))])}
    else:
        langs = {l.lang_iso_code2: fillmodel(pmodel=model
                                             , pentries=[l.lang_iso_name, l.lang_iso_code3
                                                    , Boolean.str2bool(l.lang_is_base_lang)
                                                     , None if l.lang_lang_id is None else Language().getbyid(l.lang_lang_id).lang_iso_code2]
                                             )
                 for l in Language.select()
                 }
        # langs = {l.lang_iso_code2: {'name': l.lang_iso_name
        # , 'iso3': l.lang_iso_code3
        # , 'modellanguage': Boolean.str2bool(l.lang_is_base_lang)
        # , 'replacementlang': None if l.lang_lang_id is None else Language().getbyid(l.lang_lang_id).lang_iso_code2
        #                         }
        #      for l in Language.select()
        #      }
    # fi
    return langs


# languages

def inslgtx(pmodel, pmodeid, pattr, ptexts):
    for langid, lang in pmodel.languages.items():
        lgtx = Languagetext()
        lgtx.lgtx_attrname = pattr
        lgtx.lgtx_text = ptexts[lang]
        lgtx.lgtx_lang_id = langid
        lgtx.lgtx_mode_id = pmodeid
        lgtx.lgtx_uc = "sys"
        lgtx.lgtx_dc = date.today()
        try:
            lgtx.insert()
        except Exception as err:
            pmodel.markerror(pmsg=err, pelemstr=lgtx.tostring())
            continue
    # for


# inslgtx

def js2lang(pkey, pelem):
    lang = Language()
    lang.lang_iso_code2 = pkey
    lang.lang_iso_code3 = pelem['iso3']
    lang.lang_iso_name = pelem['name']
    lang.lang_is_base_lang = Boolean.bool2str(pelem['modellanguage'])
    lang.lang_is_text_lang = Boolean.FALSE
    return lang

def langs2sql(presult, podmjson:JSModel, pdbjson:JSModel,pwithextsrcref):
    assert dbConnect.isopenDB()
    """   "languages": {
      "de": {
         "name": "Deutsch",
         "iso3": "deu",
         "modellanguage": true,
         "replacementlang": null
      }"""
    fromodm2db(presult=presult,podmjson=podmjson,pdbjson=pdbjson,pelemtype='LANG',pjs2obj=js2lang,pwithextsrcref=pwithextsrcref)
    # for iso2, jlang in podmjson.getelements('LANG').items():
    #     lang = js2lang(pkey=iso2,pelem=jlang)
    #     try:
    #         langid = lang.insert()
    #     except Exception as err:
    #         presult.markdberror(perr=err, pelem=lang.tostring())
    #         continue
    # # for

    try:
        deflang =  Language.getdefaultlang()
        if deflang is None: presult.errors.append("""*** No modellanguage defined""")
        pdbjson.setmodellanguage(deflang.lang_iso_code2)
    except:
        presult.errors.append("""*** more then one default modellanguage defined""")

    """update proj_languages field with all languages found"""
    for iso2, jlang in podmjson.getelements('LANG').items():
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
        # for

    try:
        Language.setallreplacementlang()
    except Exception as err:
        presult.markdberror(perr=err, pelem=pelem)

    return

# langs2sql
