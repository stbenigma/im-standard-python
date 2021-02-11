#!/usr/bin/python3

import os
import papermill as pm

# the script to be tested
scripts = [
    './notebooks/confluence-export/Render and publish.ipynb',
    './notebooks/Sandbox/confluence-python-api/API-sandbox.ipynb',
    './notebooks/Sandbox/stbtest.ipynb'
]

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

for notebook in scripts:
    base_path = os.path.dirname(os.path.abspath(notebook))
    print('Executing {}'.format(notebook))
    pm.execute_notebook(
       notebook,
       os.path.splitext(notebook)[0] + '.test.out.ipynb',
       parameters=dict(confluence_username=username, confluence_password=password),
       cwd=base_path
    )
