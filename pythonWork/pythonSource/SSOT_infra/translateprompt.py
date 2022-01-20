import gettext
import os
import logging

LOCALES_DIREC = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'locales') # "'./SSOT_infra/locales'"
DOMAIN = "prompts"
FALLBACK_LANG = 'de'

transldomain = None #currently active lang domain defaults to de

def plural(ending:str,cnt:int) -> str:
    """returns plural ending of ending if cnt > 1

        return None if any parameter is None
    """
    plurals={'y':'ies'}
    if ending is None or cnt is None:
        retval = None
    elif ending in plurals.keys():
        retval= ending if cnt ==1 else plurals[ending]
    else:
        retval= ''
    return retval

def setlocaltransldomain(plang):
    logging.debug(f"Initializing translation from folder '{LOCALES_DIREC}'")
    return gettext.translation(DOMAIN, localedir=LOCALES_DIREC, languages=[plang, FALLBACK_LANG])

def transl(ptext,plang=None):
    """ptext in currently set domainlanguage
       or in plang if it is not None

       en translation if ptext is not found in language
       ptext if no domain is set
        """
    retval = None
    if plang is not None:
        localdomain = setlocaltransldomain(plang)
        retval = localdomain.gettext(ptext)
    elif transldomain is None:
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
    """
    global transldomain
    transldomain = setlocaltransldomain(plang)
    return
