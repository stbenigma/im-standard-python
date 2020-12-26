from IM_OBJECTS import Languagetext,Language,Boolean
from datetime import date
from IM_JSON import JSModel


def langs2js():
    langs = {l.lang_iso_code2: {'name': l.lang_iso_name
        , 'iso3': l.lang_iso_code3
        , 'modellanguage': Boolean.str2bool(l.lang_is_base_lang)
        , 'replacementlang': None if l.lang_lang_id is None else Language().getbyid(l.lang_lang_id).lang_iso_code2
                                }
             for l in Language.select()
             }
    return langs
#languages

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

def langs2sql(pmodel:JSModel):
    """   "languages": {
      "de": {
         "name": "Deutsch",
         "iso3": "deu",
         "modellanguage": true,
         "replacementlang": null
      }"""
    for iso2, jlang in pmodel.jsmodel['languages'].items():
        lang = Language()
        lang.lang_iso_code2 = iso2
        lang.lang_iso_code3 = jlang['iso3']
        lang.lang_iso_name = jlang['name']
        lang.lang_uc = None
        lang.lang_dc = date.today()
        lang.lang_is_base_lang = Boolean.bool2str(jlang['modellanguage'])
        if jlang['modellanguage']:
            if pmodel.modellanguage() is not None:
                error(pmsg="more than one model language defined", pelem=jlang)
            else:
                pmodel.setmodellanguage (lang.lang_iso_code2)
            # fi
        # fi
        lang.lang_is_text_lang = Boolean.FALSE
        try:
            langid = lang.insert()
        except Exception as err:
            error(pmsg=err, pelem=lang.tostring())
            continue
        pmodel.languages[langid] = iso2
    # for
    try:
        Language.setallreplacementlang()
    except Exception as err:
        error(pmsg=err, pelem=pelem)

    if pmodel.modellanguage() is None:
        error(pmsg="No model language defined", pelem=None)
    # print([l.tostring() for l in Language.select()])
#langs2sql


