import requests

g_authid: str = None
g_deeplurl: str = 'https://api.deepl.com/v2/translate'

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

"""
400	Bad request. Please check error message and your parameters.
403	Authorization failed. Please supply a valid auth_key parameter.
404	The requested resource could not be found.
413	The request size exceeds the limit.
414	The request URL is too long. You can avoid this error by using a POST request instead of a GET request, and sending the parameters in the HTTP body.
429	Too many requests. Please wait and resend your request.
456	Quota exceeded. The character limit has been reached.
503	Resource currently unavailable. Try again later.
529	Too many requests. Please wait and resend your request.
5**	Internal error
"""

def setauthid(pDEELPauthid):
    global g_authid
    g_authid = pDEELPauthid
    return
#temprär mein ID fest verdrahtet


def translate(ptext:str, pfromlang:str, ptolang:str):
    # print(ptext,ptolang,pfromlang)
    assert g_authid is not None,"DeepL not authenticated"
    assert ptolang.upper() in LANGUAGES,f"To language ({ptolang}) not allowed"
    assert pfromlang.upper() in LANGUAGES,  f"From language ({pfromlang}) not allowed"

    param = {'auth_key': g_authid
        , 'text': ptext
        , 'target_lang': None if ptolang is None else str.upper(ptolang)
        , 'source_lang': None if pfromlang is None else str.upper(pfromlang)
        , 'preserve_formatting': 1}

    r = requests.post(g_deeplurl, data=param)
    if (r.status_code == 200):
        rj = r.json()
        # print (rj)
        result = rj['translations'][0]['text']

    else:
        raise Exception(f"Translation failed with statuscode '{r.status_code}'")
    # fi
    return result

