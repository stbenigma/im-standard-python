import csv
import json
import os
import tempfile
from pathlib import Path

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.field_creation_information import FieldCreationInformation
from office365.sharepoint.files.file_system_object_type import FileSystemObjectType

# {
#   "username": "bue@foryouandyourcustomers.com",
#   "password": "****",
#   "site": "https://fyayc.sharepoint.com/sites/CoPInformation-Data-Governance",
#   "list": "ListSandboxBue",
#   "ssot": "../../../testenvironment/testmodels/riddle/DB/riddle.json"
# }
with open('fyayc-sharepoint.json', 'r') as src:
    config = json.load(src)

# Verify ssot
ssot = Path(config['ssot'])
if not ssot.is_file():
    ssot = Path.cwd() / ssot

assert ssot.is_file(), f"Invalid path to ssot: {ssot.resolve()}"

with open(str(ssot), 'r') as src:
    model = json.load(src)

print(f"Working with ssot {model['model']}")
assert len(model['entities']) > 0, f"Cannot find 'entities' in model {ssot}"

credentials = UserCredential(config['username'], config['password'])
ctx = ClientContext(config['site']).with_credentials(credentials)

def filter_json(tuple) -> (str, str):
    key = tuple[0]
    value = tuple[1]
    if type(value) == str or type(value) == int:
        return (str(key), str(value))
    return None

filelist = []
doc_lib = ctx.web.lists.get_by_title("Documents")
items = doc_lib.items.select(["FileSystemObjectType"]).expand(["File", "Folder"]).get().execute_query()
for item in items:  # type: ListItem
    if item.file_system_object_type == FileSystemObjectType.Folder:
        print("Folder url: {0}".format(item.folder.serverRelativeUrl))
        filelist.append({ 'name': item.folder.name, 'path': item.folder.serverRelativeUrl, 'type': 'folder'})
    else:
        print("File url: {0}".format(item.file.serverRelativeUrl))
        filelist.append({ 'name': item.file.name, 'path': item.file.serverRelativeUrl, 'type': 'file' })

with open('filelist.json', 'w') as dst:
    json.dump(filelist, dst)
    
entity_list = ctx.web.lists.get_by_title(config['list'])
print(f"Successfully logged in to {config['site']}")



def print_progress(items_read):
    print("Items read: {0}".format(items_read))


# fetch in batches of 100
list_items = entity_list.items.top(50).get().execute_query()
list_items.page_loaded += print_progress

if len(list_items) == 0:
    print("No data found")

sp_entities = {}

# Column structure should be read from configuration file
entity_columns = [
    ('Title', {'value': lambda e: tr(e['name']), 'properties': {'CanBeDeleted': False}}),
    ('Description', {'value': lambda e: tr(e['descr']), 'properties': {'CanBeDeleted': False}}),
    ('Synonyms', {'value': lambda e: tr(e['synonyms']), 'properties': {}}),
    ('Diagrams', {'value': lambda e: tr(e['diagrams+']), 'properties': {}}),
    ('Key', {'value': 'KEY', 'properties': {
        'Description': 'SSOT ID',
        'CanBeDeleted': False,
        'Filterable': True,
        'Sortable': True,
        'Indexed': True,
        'Sortable': True,
        'FieldType': 2,
        'MaxLength': 10,
        'Required': True,
    }}),
    ('Documentation Link', {'value': lambda e: './bla.html', 'properties': {'FieldType': 11}})
]

# https://fyayc.sharepoint.com/sites/CoPInformation-Data-Governance/Shared%20Documents/Forms/AllItems.aspx
# ?id=%2Fsites%2FCoPInformation%2DData%2DGovernance%2FShared%20Documents%2FInformation%20Cadastre%20%28Sandbox%29%2Fwebcontent%2Fraetsel%2D3lang%5Fde%2Ehtm
# l&parent=%2Fsites%2FCoPInformation%2DData%2DGovernance%2FShared%20Documents%2FInformation%20Cadastre%20%28Sandbox%29%2Fwebcontent
#
# https://fyayc.sharepoint.com/sites/CoPInformation-Data-Governance/Shared Documents/Forms/AllItems.aspx
# ?id=/sites/CoPInformation-Data-Governance/Shared Documents/Information Cadastre (Sandbox)/webcontent/raetsel-3lang_de.html
# &parent=/sites/CoPInformation-Data-Governance/Shared Documents/Information Cadastre (Sandbox)/webcontent
#

existing_fields = {}
column_map = dict(entity_columns)

fields = entity_list.fields.get().execute_query()
print(f"List {config['list']} has {len(fields)} fields")

field_collection = []
for field in fields:
    name = field.properties['EntityPropertyName']
    print(f"Field {name}: {vars(field)}")
    existing_fields[name] = field
    field_collection.append(field.properties)

with open('current-fields.json', 'w') as out:
    json.dump(field_collection, out)

existing_fields_keys = set(existing_fields.keys())
missing_fields_keys = set(column_map.keys()) - existing_fields_keys
print(f"Missing list fields: {missing_fields_keys}")

update = False
for key in missing_fields_keys:
    configuration = column_map[key]
    assert configuration is not None, f"Missing configuration for column {key}"
    properties = configuration.get('properties', {})
    description_text = properties.get('Description') if properties.get('Description') is not None else f"{key} field"

    field_type_kind = properties.get('FieldType', 3)  # default 3 = Long text
    create = FieldCreationInformation(
        title=key, field_type_kind=field_type_kind,
        description=description_text,
    )
    for col_key, value in properties.items():
        if 'Description' == col_key: continue
        if 'FieldType' == col_key: continue
        create.set_property(col_key, value, True)

    entity_list.fields.add(create)
    update = True

if update:
    print(f"Updating structure")
    ctx.execute_batch()

existing_items_count = len(list_items)
if existing_items_count > 0:
    path = os.path.join(tempfile.mkdtemp(), "Entities.csv")
    with open(path, 'w') as fh:
        fields = list_items[0].properties.keys()
        w = csv.DictWriter(fh, fields)
        w.writeheader()
        index = 0
        for item in list_items:
            print("{0}: {1} = {2}".format(index, item.properties['Title'], item.properties))
            w.writerow(item.properties)
            index += 1
            sp_entities[item.properties['Key']] = item

    print(f"Wrote items to: {path}")
else:
    print("No items, skip write")

# merge with SSOT
# item.set_property("Title", "Value").update()

# 2. read & upload attachment for a list item
# path = "../../data/report #123.csv"
# with open(path, 'rb') as fh:
#    file_content = fh.read()
# attachment_file_info = AttachmentfileCreationInformation(os.path.basename(path), file_content)
# task_item.attachment_files.add(attachment_file_info).execute_query()

def tr(element: dict, lang: str = 'en') -> str:
    if element is None or len(element) < 1:
        return ''
    return element.get(lang, '')


def update_values(item, values: dict, context: str) -> []:
    touched = False
    for key, new_value in values.items():
        current_value = item.properties.get(key)
        if (current_value is None or current_value != new_value) \
                and not (current_value is None and new_value == ''):  # None and '' are treated equal
            print(f"Updating value {key} {current_value} -> {new_value} in context {context}")
            item.properties[key] = new_value
            touched = True
    return touched


new = []
updated = []
for key, entity in model['entities'].items():
    existing = sp_entities.get(key)
    values = {
        'Title': tr(entity['name']),
        'Description': tr(entity['descr']),
        'Synonyms': tr(entity['synonyms']),
        'Key': key
    }
    if not existing:
        # add new item
        print(f"Adding new item {key}: {values}")
        list_item = entity_list.add_item(values)
        new.append(list_item)
    else:
        # update existing
        if update_values(existing, values, key):
            updated.append(existing)

print(f"Summay: existing: {existing_items_count}, updated={len(updated)}, new={len(new)}."
      f" Model contains {len(model['entities'])} entities.")

# process the update as batch
if False:
    print(f"Publishing to Sharepoint")
    ctx.execute_batch()
    print(f"Successfully processed batch")
