"""

Requires the python package 'msal'
Install with `conda install msal` or `pip install msal`.

"""

import json
import logging
import requests
import argparse

try:
    import msal
except:
    print("Missing msal library")
    print("Install using `conda install msal` or `pip install msal`")
    exit(-1)

argp = argparse.ArgumentParser(description='Sharepoint API sandbox')
argp.add_argument('--verbose', '-v', action='store_true', help="Verbose mode")
argp.add_argument('--user', '-u', dest='user', help="Interactive login as user")

arguments = argp.parse_args()

logging_level = logging.DEBUG if arguments.verbose else logging.INFO

# setup logging
logging.basicConfig(filename='msgraph_sandbox.log', level=logging.DEBUG)

console_log_handler = logging.StreamHandler()
console_formatter = logging.Formatter("%(levelname)s - %(message)s")
console_log_handler.setFormatter(console_formatter)
console_log_handler.setLevel(logging_level)
logging.getLogger().addHandler(console_log_handler)

# tune library logging
if arguments.verbose:
    logging.getLogger("requests.packages.urllib3").setLevel(logging_level)
    logging.getLogger("msal").setLevel(logging_level)

# logging ready

app_settings_sandbox = {
    'tenant': '4ee0b6db-2682-4f0d-8356-b8b71d6af335',
    'client_id': '6f708579-76a6-4009-8f96-f35c234239e1',
    # 'thumbprint': '54986C04948A0B724C8608B41F5F35372A4E97CB',
}

client_id = app_settings_sandbox['client_id']

authority = f"https://login.microsoftonline.com/{app_settings_sandbox['tenant']}"

"""
{
    "private_key": "...-----BEGIN PRIVATE KEY-----...",
    "thumbprint": "A1B2C3D4E5F6...",
    "public_certificate": "...-----BEGIN CERTIFICATE-----... (Optional. See below.)",
    "passphrase": "Passphrase if the private_key is encrypted (Optional. Added in version 1.6.0)",
}
"""
client_credential = {
    "private_key": """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCit9bnsVglLiyn
fCpA/kS96oy1iK/3a4Hnbrgj9BR9Ov+rcHi3daL0MFteDLyxJZqZTaR+T5+CSlIy
chbyKj+QZ16OBN13LmHv3BLXB8woy1mvGyEmNpXmIQSSxOUe8Af2j3dQkkVZY5LH
YkeSltRJ6F2vUqXxTbAeUjUf5XXRsKBGZSCHZEfY9nfGLTRCjMMQUFZs1tmev8yY
FYAYqx1O/GIri4tfgNlA9eXQs7zvoYeqiPI3ZBbIVyAGTyooHxtlKKdJNV6lapJw
/NQeFGMiajfL6/ZgbmQUfBs8FT7QNviZby7ouo/qyXW1/9nig1lcVBy5lsYrk3VC
TVcgjonlAgMBAAECggEBAIoH/UuqCyXvF340O/vKNjIMx7Qu8WanUhkquRX2tXLO
G5go3p5yMfuHEdqkX2S+i3jEfmePz7XMqhGU6pYe9LDgnztGMUAqnnXEcE7slGl+
puN91g7+ewYuuBxw3hPydi7X4NT+X8nGR/rPCfv16ruPW/mf2Jjr2BzAi8Q0+E8Z
dS1znBcQmWB580ENgbHhxelj1/VWSq3zUm1XHH7otgfGYDjW5VLK2PvOokv3ExoE
qiVARNPZqRcNkONT+WbWCtV0pCO2Nexv9ZTEp34jcQc1qRBCJDUrkRcyF6iRKU/T
vXuakLKmuHuzaqn8gZ1dT5nuwcqUtUYiBMHzgNSz6oECgYEA1Je+N2suUFbscUCJ
XuiGYoFfdF2jgVFKwz8fbYDRgx03TYd3l6BS/Fw1+1rECjh8fe0hzonhEaZTCWXC
vpX3ZOnQmB6ra/0XaA0Xbp4Iv2+IDgFY7jAPWA8I/ycRS7GfhZ21BdMOSMSXtEf6
4APoHWI9/3B+KoQXHjJV2XZzP9UCgYEAw/EkUffIl10clYihLXaFnktaRZUWxs7J
t6CfmqytN4B22EjertLJIQX60fXXrwbKZWmx1poTxcuEIU5ircZzL+51IG6+ZfyX
7wybLMZBX0u93enfUCywPz3he68nNsJ42UcUg8aE1krgc4mYzTZxjAyDYPFHsDTN
LZdwbZe9OdECgYAwNqXGDcG4KK6A1MESzCtGBc8vJdliB5ysARHQlMlvMd4L8DAY
LB0F7Ke1dJVHOB5LtM7Y934asZzdYb2z2XD86uYKydHYsNJxH57z0FVtjQ7PFlEj
27RvJSHGNAcBIqxp8iVOx9nSePtqwHRN/7TRjSlAWDPU0pYnnATKR8nFbQKBgEE4
JLS72yK2tWr4fV2ak8MqpbN/eoNWFUJvznA3hbhxpB09tBFQy+2YBfKY99+kTP4Q
fkdGJcqygRps8t+QrIqJvqa69dkQiKni8kum+d90YJBa5h/ToB6MxF7c4BqUBJGd
3TA3hcOmTKtoY1n7AzRwfdJovUnjaWABhkSUO0HhAoGBAKJUqlxlB126TC/dTsUw
j/MBZlWNZlhizlo2JwYCY/YLahiXNPm7KbHayb+4VIjFSezqghfmo9+UT8wyEOmY
mGxSI5uzAu6L2jrgj6jVx60eCXcyx3FDvbs2I+EVwcEg5Blev7d3mrtaFrrxig6C
4qikXhqtbyqtCT9S0vsxgUqZ
-----END PRIVATE KEY-----""",
    'thumbprint': "54986C04948A0B724C8608B41F5F35372A4E97CB",
    'public_certificate': """-----BEGIN CERTIFICATE-----
MIID9zCCAt+gAwIBAgIUHNDafyg3za7ZhmNtm72tz2SdKW8wDQYJKoZIhvcNAQEL
BQAwgYoxCzAJBgNVBAYTAkNIMQswCQYDVQQIDAJaRzEMMAoGA1UEBwwDWnVnMRUw
EwYDVQQKDAxCb3NzYXJkIEdtYkgxDDAKBgNVBAsMA0lDVDEQMA4GA1UEAwwHSUNU
Q0VSVDEpMCcGCSqGSIb3DQEJARYaaWN0YXp1cmVhZG1pbnNAYm9zc2FyZC5jb20w
HhcNMjIwNTExMTUxOTE5WhcNMjUwMjA0MTUxOTE5WjCBijELMAkGA1UEBhMCQ0gx
CzAJBgNVBAgMAlpHMQwwCgYDVQQHDANadWcxFTATBgNVBAoMDEJvc3NhcmQgR21i
SDEMMAoGA1UECwwDSUNUMRAwDgYDVQQDDAdJQ1RDRVJUMSkwJwYJKoZIhvcNAQkB
FhppY3RhenVyZWFkbWluc0Bib3NzYXJkLmNvbTCCASIwDQYJKoZIhvcNAQEBBQAD
ggEPADCCAQoCggEBAKK31uexWCUuLKd8KkD+RL3qjLWIr/drgeduuCP0FH06/6tw
eLd1ovQwW14MvLElmplNpH5Pn4JKUjJyFvIqP5BnXo4E3XcuYe/cEtcHzCjLWa8b
ISY2leYhBJLE5R7wB/aPd1CSRVljksdiR5KW1EnoXa9SpfFNsB5SNR/lddGwoEZl
IIdkR9j2d8YtNEKMwxBQVmzW2Z6/zJgVgBirHU78YiuLi1+A2UD15dCzvO+hh6qI
8jdkFshXIAZPKigfG2Uop0k1XqVqknD81B4UYyJqN8vr9mBuZBR8GzwVPtA2+Jlv
Lui6j+rJdbX/2eKDWVxUHLmWxiuTdUJNVyCOieUCAwEAAaNTMFEwHQYDVR0OBBYE
FOx+y5w8FW5FORVBmc+wfpMAoJmJMB8GA1UdIwQYMBaAFOx+y5w8FW5FORVBmc+w
fpMAoJmJMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAE7giviZ
Opd6CzPiFT6m34V4ZuZzNOa+Xh5M1KdBhk1d/9k9YSm9XFP7QaAXaLIvw6iFw1cA
IS8gP1hf+fvLOwT5n+0/pDA8e1/Ca47KXly4pTXryz82HEVHzmT8jLHR7FJTC0fI
mPxk51wFz6L2PlSnwA6HcLok7f7tyvmSexyh2YChezB5KV+gmi3cUWCHiBED5Ulu
nGRhhXQ/pDvFCnINiapaBfsKl8gt8QyjOiYyTnMx/4jfTVScpkF9PnPaIqDr9RPP
oVEqUAfVlgzwx93hhMiL/+nfCygU6YGFohoe606tKJSWJVKS+Bs3nSVjxBFI6r8p
JDPLBjjW43cfQHQ=
-----END CERTIFICATE-----""",
}

#with open('/Users/bue/projects/client/sharepoint/secret.json', 'r') as src:
#    client_credential = json.load(src)

scopes_app = ["https://graph.microsoft.com/.default"]

scopes_user = [
    'User.ReadBasic.All'
]

if arguments.user:
    # Use interactive login with user credentials
    # Does not work: AADSTS500113: No reply address is registered for the application
    logging.info("Logging in with user credentials from commandline")
    app = msal.PublicClientApplication(
        client_id=client_id,
        client_credential=None,
        authority=authority)
    uv = arguments.user if len(arguments.user) > 3 else 'bue@foryouandyourcustomers.com'
    token_result = app.acquire_token_interactive(scopes=scopes_user,
                                           login_hint=uv)
else:
    logging.info("Logging in with certificate")
    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        client_credential=client_credential,
        authority=authority,
    )
    token_result = app.acquire_token_silent(scopes=scopes_app, account=None)
    if not token_result:
        logging.info("No suitable token exists in cache. Let's get a new one from Azure Active Directory.")
        token_result = app.acquire_token_for_client(scopes=scopes_app)

if "access_token" in token_result:
    logging.info("Access token is " + token_result["access_token"])
else:
    logging.error(f"No access token received 😨\nresult: {token_result}")
    exit(1)

# How to find the site id?
# Access your site using the humanreadable url: https://bosnet.sharepoint.com/sites/<client>_MasterDataSandbox/_api/site
# and read guid from 'id' field in the result
site_client_master_data = '2ce6a841-f969-4ecc-bc31-1017d1979a8b'
site_client_master_data_sandbox = '888ae301-96b4-4859-9be5-34b5b4b981d0'

site_id = site_client_master_data_sandbox

entity_list_id = 'd70a737a-47a1-4ceb-aa62-11758baa2ebf' if site_id == site_client_master_data else '1d716fd1-cb9b-4457-a663-5db3fad2f160'

# Calling graph using the access token
logging.info(f"Fetching profile")
result = requests.get(f"https://graph.microsoft.com/v1.0/users('bue@foryouandyourcustomers.com')",
                          headers={'Authorization': 'Bearer ' + token_result['access_token']}, ).json()
logging.info("response: %s" % json.dumps(result, indent=2))

# Calling graph using the access token
logging.info(f"Fetching lists in site '{site_id}'")
graph_data = requests.get(f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists",
                          headers={'Authorization': 'Bearer ' + token_result['access_token']}, ).json()
logging.info("Graph API call result: %s" % json.dumps(graph_data, indent=2))

logging.info(f"Fetching specific list 'd70a737a-47a1-4ceb-aa62-11758baa2ebf' in site '{site_id}'")
graph_data = requests.get(
    f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{entity_list_id}",
    headers={'Authorization': 'Bearer ' + token_result['access_token']}, ).json()
logging.info("Graph API call result: %s" % json.dumps(graph_data, indent=2))


logging.info(f"Try reading all elements in list {entity_list_id}.")
list_result = requests.get(f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{entity_list_id}/items",
                           headers={'Authorization': 'Bearer ' + token_result['access_token'], },
                           ).json()
result_file = 'list_result.json'
with open(result_file, 'w') as out:
    json.dump(list_result, out, indent=2)
logging.info(f"Wrote {len(list_result['value'])} to {result_file}")

logging.info(f"Try reading element 10 in the list of entities.")
read_result = requests.get(f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{entity_list_id}/items/10",
                           headers={'Authorization': 'Bearer ' + token_result['access_token'], },
                           ).json()
with open('read_result.json', 'w') as out:
    json.dump(read_result, out, indent=2)

uint = len(list_result['value']) + 1
unique = str(uint)
test_item = {
    'fields': {
        'Title': 'Test Entity ' + unique,
        'Description': 'MS Graph Sandbox created entity ' + unique,
        'Key': f'TST{uint:04}',
        'Synonyms': 'Testentity ' + unique,
        'Diagrams': '<h1>It works 😄</h1>',
    }
}

# Doc: https://docs.microsoft.com/en-us/graph/api/listitem-create?view=graph-rest-1.0&tabs=http
logging.info(f"Try adding new element to list entities.'")
logging.debug(json.dumps(test_item, indent=2))
create_result = requests.post(f"https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{entity_list_id}/items",
                              json=test_item,
                              headers={
                                  'Authorization': 'Bearer ' + token_result['access_token'],
                                  'Content-Type': 'application/json'},
                              ).json()

with open('create_result.json', 'w') as out:
    json.dump(create_result, out, indent=2)
logging.info(f"Item creation result: {json.dumps(create_result, indent=2)}")
