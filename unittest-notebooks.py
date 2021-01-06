#!/usr/bin/python3

import os
import papermill as pm

# the script to be tested
script = './notebooks/Sandbox/confluence-python-api/API-sandbox.ipynb'

base_path = os.path.dirname(os.path.abspath(script))

username = os.environ.get('CONFLUENCE_USERNAME')
password = os.environ.get('CONFLUENCE_PASSWORD')

if username is None:
    username = os.environ.get('USER')

if password is None:
    try:
        # try to read the password from keyring
        import keyring
        password = keyring.get_password('fyayc-confluence', username)
        print('Using password for user {} from keyring'.format(username))
    except Exception:
        print("Cannot to read password from keyring")

print('Starting papermill with confluence_username: {} and {}'.format(username, '{} character password'.format(len(password)) if password else 'no password'))

pm.execute_notebook(
   script,
   'output.ipynb',
   parameters=dict(confluence_username=username, confluence_password=password),
   cwd=base_path
)
