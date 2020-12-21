from IM_OBJECTS import Languagetext,Language,Boolean
from datetime import date


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
            pmodel.markerror(pmsg=err, pelem=lgtx.tostring())
            continue
    # for
# inslgtx
from IM_JSON import *
