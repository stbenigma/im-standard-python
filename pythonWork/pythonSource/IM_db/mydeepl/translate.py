
import requests
import json

g_authid:str = None
g_deeplurl:str = 'https://api.deepl.com/v2/translate'
g_deeplpath:str = '/Users/stb/Documents/deeplauthid'

LANGUAGES = {
    'auto': 'Auto',
    'DE': 'German',
    'EN': 'English',
    'FR': 'French',
    'ES': 'Spanish',
    'IT': 'Italian',
    'NL': 'Dutch',
    'PL': 'Polish'
}

def setauthid():
    global g_authid
    if g_authid is not None:
        return
    # Open a file
    try:
        with open(g_deeplpath, 'r') as af:
        # Reading text
            lauthid = af.read()
    except:
        lauthid = ''
    #
    #print (lauthid)
    g_authid = lauthid
#setauthid

def translate(p_text,p_tolang,p_fromlang):
    #print(p_text,p_tolang,p_fromlang)
    if g_authid is None:
        raise Exception("DeepL not authenticated. See parameter deeplauthid in parameterfile.")
    if (LANGUAGES.get(str.upper(p_tolang)) is None):
        raise Exception("To language ({}) not allowed".format(p_tolang))
    if LANGUAGES.get(str.upper(p_fromlang)) is None:
        raise Exception("From language ({}) not allowed".format(p_fromlang))

    param = {'auth_key': g_authid
            , 'text': p_text
            , 'target_lang': None if p_tolang is None else str.upper(p_tolang)
            , 'source_lang': None if p_fromlang is None else str.upper(p_fromlang)
            , 'preserve_formatting': 1}

    r = requests.post(g_deeplurl, data=param)
    if (r.status_code == 200):
        rj = r.json()
        #print (rj)
        result = rj['translations'][0]['text']

    elif (r.status_code == 403):
        result = "*{}* {}".format(str.upper(p_tolang),p_text)
    else:
        raise Exception("Translation failed with statuscode '{}'".format(r.status_code))
    #fi
    return result
#translate

if __name__ == '__main__':
    import sys
    setauthid()
    text = sys.argv[1]
    transl = translate(p_text= text
         , p_tolang=sys.argv[2] if (len(sys.argv) > 2) else None
         , p_fromlang=sys.argv[3] if (len(sys.argv) > 3) else None
         )
    print (text,'=',transl)
