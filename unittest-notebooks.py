#!/usr/bin/python3

import os
import papermill as pm

# the script to be tested
scripts = [
    {'script': './notebooks/confluence-export/Publisher application.ipynb'},
    #    './notebooks/Sandbox/confluence-python-api/API-sandbox.ipynb',
    #    './notebooks/confluence-export/Render and _publishable.ipynb',
    #    './notebooks/Sandbox/stbtest.ipynb',
    #    './notebooks/iconlibrary/Confluence producer.ipynb',
]

#(confluence_username=username, confluence_password=password)

destination = os.path.join('build', 'unittest')

os.makedirs(destination, exist_ok=True)

username = os.environ.get('CONFLUENCE_USERNAME')
password = os.environ.get('CONFLUENCE_PASSWORD')

if username is None:
    username = os.environ.get('USER')

keyring_password_label = 'fyayc-confluence'
if password is None:
    try:
        # try to read the password from keyring
        import keyring

        password = keyring.get_password(keyring_password_label, username)
        print('Using password for user {} from keyring'.format(username))
    except Exception:
        print('Cannot read password with label "{}" from keyring'.format(keyring_password_label))

print('Starting papermill with confluence_username: {} and {}'.format(username, '{} character password'.format(
    len(password)) if password else 'no password'))

for notebook in scripts:
    script_file = notebook['script']
    base_path = os.path.dirname(os.path.abspath(script_file))
    result_path = os.path.join(base_path, destination)
    os.makedirs(result_path, exist_ok=True)
    result_output = os.path.join(result_path, os.path.basename(script_file))
    print('Executing {}. Results in {}'.format(script_file, result_output))
    pm.execute_notebook(
        script_file,
        result_output,
        parameters=notebook.get('parameters'),
        cwd=base_path
    )
