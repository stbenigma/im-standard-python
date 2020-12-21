from IM_OBJECTS import Languagetext
from datetime import date

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
