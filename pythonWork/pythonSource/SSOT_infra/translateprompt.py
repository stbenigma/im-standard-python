import gettext
import os

LOCALES_DIREC = os.path.dirname(os.path.realpath(__file__)) + '/locales' # "'./SSOT_infra/locales'"
DOMAIN = "prompts"
ORIGINAL_LANG = 'de'

transldomain = None #currently active lang domain defaults to de

def setlocaltransldomain(plang):
    return gettext.translation(DOMAIN, localedir=LOCALES_DIREC, languages=[plang, 'en'])

def transl(ptext,plang=None):
    """ptext in currently set domainlanguage
       or in plang if it is not None

       en translation if ptext is not found in language
       ptext if no domain is set
        """
    retval = None
    if plang is not None and plang != ORIGINAL_LANG:
        localdomain = setlocaltransldomain(plang)
        retval = localdomain.gettext(ptext)
    elif transldomain is None or plang == ORIGINAL_LANG:
            retval = ptext
    else:
        retval = transldomain.gettext(ptext)
    return retval

def resettransldomain():
    """set domain to None -- disabling translation
    """
    global transldomain
    transldomain = None
    return

def settransldomain(plang):
    """sets translation domain for gettext to plang
        
       if de is given, translation is reset, as de is origin language 
       fallbacklanguage is always en
    """
    global transldomain
    if plang == 'de':
        transldomain = None
    else:
        transldomain = setlocaltransldomain(plang)
    return
