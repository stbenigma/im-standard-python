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
MIIEvgIBADANBgkqhkiG9...xgUqZ
-----END PRIVATE KEY-----""",
    'thumbprint': "54986C04948A0B724C8608B41F5F35372A4E97CB",
    'public_certificate': """-----BEGIN CERTIFICATE-----
MIID9zCC...At+QHQ=
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
