import json

import requests as req
import yaml


def getcredentials(credentialfile):
    try:
        firstandonlykey,firstcredential = None,None
        with open(credentialfile) as src:
            credentials = yaml.safe_load(src)
            if credentials is not None:
                firstandonlykey=list (credentials.keys())[0]
                firstcredential = credentials.get(firstandonlykey)
            else:
                raise Exception(f"no proper credentials found in file {credentialfile}")
    except Exception as exp:
        raise exp

    return firstandonlykey,firstcredential


def getazuretoken(clientid, username, password):
    locrequest = """https://login.microsoftonline.com/organizations/oauth2/v2.0/token"""
    params = {
        'accept': "application/json",
        'username': username,
        'password': password,
        'client_id': clientid,
        'grant_type': 'password',
        'scope': 'openid'
    }
    response = req.post(url=locrequest, data=params)
    if response.status_code != 200:
        raise Exception(f"api access error {response.status_code}\n{response.text}")
    jsonresp = json.loads(response.content)
    return jsonresp["id_token"]
