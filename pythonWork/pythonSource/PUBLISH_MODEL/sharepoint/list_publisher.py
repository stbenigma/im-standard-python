import csv
import json
import logging
from pathlib import Path
import yaml

from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.field_creation_information import FieldCreationInformation
from office365.sharepoint.lists.list import List


# Configuration file format:
# {
#   "username": "bue@foryouandyourcustomers.com",
#   "password": "****",
#   "site": "https://fyayc.sharepoint.com/sites/CoPInformation-Data-Governance",
#   "list": "ListSandboxBue",
#   "ssot": "../../../testenvironment/testmodels/riddle/DB/riddle.json"
# }

def update_structure(sharepoint_list: List, columns: [()], write: bool = False) -> [str]:
    """
    Read structure
    Update structure

    :param sharepoint_list: Name of the list in Sharepoint
    :param columns: Columns definition. See end of this file.
    :param write: Execute changes
    :return: List of changes
    """

    fields = sharepoint_list.fields.get().execute_query()
    logging.debug(f"Processing {len(fields)} fields. Reference: {len(columns)}")

    existing_fields = {}
    field_collection = []
    for field in fields:
        name = field.properties['EntityPropertyName']  # use this as key
        logging.debug(f"Found field {name}: {vars(field)}")
        existing_fields[name] = field
        field_collection.append(field.properties)

    existing_fields_keys = set(existing_fields.keys())
    missing_fields_keys = set(map(lambda r: r[0], columns)) - existing_fields_keys
    logging.debug(f"Missing fields on list:\n {missing_fields_keys}")

    # need to fetch this if we want the title
    sharepoint_list.get().execute_query()
    message = [f"- Synchonizing {len(field_collection)} fields in list '{sharepoint_list.title}' -"]
    logging.info(message[0])

    for record in columns:
        touched = False
        key = record[0]
        configuration = record[1]
        properties = configuration.get('properties', {})
        description_text = properties.get('Description') if properties.get(
            'Description') is not None else f"{key} field"
        field_type_kind = properties.get('FieldTypeKind', 3)  # default 3 = Long text (RichTextFormat?)
        if key in existing_fields_keys:
            logging.debug(f"Processing column {key}\nCurrent: {existing_fields[key].properties}")
            # update structure (if possible)
            field = existing_fields[key]
            current_field_type = field.get_property('FieldTypeKind')
            logging.debug(f"Updating field {key} of type {current_field_type}")
            assert current_field_type == field_type_kind, \
                f"Field type {current_field_type} (current) vs {field_type_kind} (configuration) mismatch" \
                f" on column {key}\n{field.properties}"
            updated = update_field_properties(properties, field)
            if len(updated) > 0:
                message.append(f"-- Updating properties of field {key}\n{field.properties}")
                message.extend(updated)
                touched = True
        else:
            # create new field
            field = FieldCreationInformation(
                title=key, field_type_kind=field_type_kind,
                description=description_text,
            )
            update_field_properties(properties, field)
            sharepoint_list.fields.add(field)
            message.append(f"Adding new field {key}")
            touched = True

        if touched and write:
            print(f"Performing change on {key} ...")
            field.execute_query()
            logging.debug("done")

    return message


def update_field_properties(properties: dict, field: FieldCreationInformation) -> [str]:
    message = []
    for col_key, value in properties.items():
        if 'Description' == col_key: continue
        if 'FieldType' == col_key: continue
        try:
            current = field.get_property(col_key)
            if current != value:
                message.append(f"Changing property {col_key} from {current} to {value}")
                field.set_property(col_key, value, True)
        except AttributeError as e:
            logging.warning(f"Cannot access field {col_key}")
    return message


def login(config: dict) -> ClientContext:
    """
# {
#   "credentials": {
#     "username": "bue@foryouandyourcustomers.com",
#     "password": "****"
#   },
#   "site": "https://fyayc.sharepoint.com/sites/CoPInformation-Data-Governance",
#   "list": "ListSandboxBue",
#   "ssot": "../../../testenvironment/testmodels/riddle/DB/riddle.json"
# }
    """
    ccc = config['credentials']
    credentials = UserCredential(ccc['username'], ccc['password'])
    ctx = ClientContext(config['site']).with_credentials(credentials)
    return ctx


# Column structure could be read from configuration file
entity_mapping = [
    ('Title', {'value': lambda e: tr(e['name']), 'properties': {
        'FieldTypeKind': 2,
        'CanBeDeleted': False
    }}),
    ('Description', {'value': lambda e: tr(e['descr']), 'properties': {'CanBeDeleted': False}}),
    ('Synonyms', {'value': lambda e: tr(e['synonyms']), 'properties': {}}),
    ('Diagrams', {'value': lambda e: str(e['diagrams+']), 'properties': {}}),
    ('Key', {'value': 'KEY', 'properties': {
        'Description': 'SSOT ID',
        'EnforceUniqueValues': True,
        'CanBeDeleted': False,
        'Filterable': True,
        'Sortable': True,
        'Indexed': True,
        'FieldTypeKind': 2,
        'MaxLength': 10,
        'Required': True,
    }}),
    #   ('Documentation Link', {'value': lambda e: './bla.html', 'properties': {'FieldType': 11}}),
]

# Column structure could be read from configuration file
attribute_mapping = [
    ('Title', {'value': lambda e: tr(e['name']), 'properties': {
        'FieldTypeKind': 2,
        'CanBeDeleted': False
    }}),
    ('Description', {'value': lambda e: tr(e['descr']), 'properties': {'CanBeDeleted': False}}),
    ('Synonyms', {'value': lambda e: tr(e['synonyms']), 'properties': {}}),
    ('Type', {'value': lambda a: a['basetype+'], 'properties': {
        'Description': 'Datatype of the attribute',
        'CanBeDeleted': False,
        'Filterable': True,
        'Sortable': True,
        'Indexed': True,
        'FieldType': 2,
        'MaxLength': 50,
        'Required': False,
    }}),
    ('Key', {'value': 'KEY', 'properties': {
        'Description': 'SSOT ID',
        'CanBeDeleted': False,
        'EnforceUniqueValues': True,
        'Filterable': True,
        'Indexed': True,
        'Sortable': True,
        'FieldType': 2,
        'MaxLength': 10,
        'Required': True,
    }}),
    #   ('Documentation Link', {'value': lambda e: './bla.html', 'properties': {'FieldType': 11}}),
]


def collect_content(list_items: [], destination: Path) -> [(str, dict)]:
    if len(list_items) < 1:
        return []
    result = []
    index = 0
    with open(destination, 'w') as fh:
        fields = list_items[0].properties.keys()
        w = csv.DictWriter(fh, fields)
        w.writeheader()
        for item in list_items:
            logging.debug("{0}: {1} = {2}".format(index, item.properties['Title'], item.properties))
            w.writerow(item.properties)
            index += 1
            result.append((item.properties['Key'], item))  # add tuple

    logging.info(f"Wrote {index + 1} items to: {destination.resolve()}")
    return result


def update_content(sp_list: List, mapping: dict, model_content: dict, sp_content: dict):
    """
    values = {
        'Title': tr(entity['name']),
        'Description': tr(entity['descr']),
        'Synonyms': tr(entity['synonyms']),
        'Key': key
    }

    :param sp_content
    """
    assert sp_list is not None
    assert mapping is not None
    assert isinstance(model_content, dict)
    assert isinstance(sp_content, dict)

    new = []
    updated = []
    current_items = set(sp_content.keys())
    logging.info(f"List contains {len(current_items)} rows. New rows count {len(model_content)}.")
    for key, entity in model_content.items():
        existing = sp_content.get(key)

        values = {}
        for tuple in mapping:
            tk = tuple[0]
            options = tuple[1]
            map_function = options.get('value')
            try:
                value = None
                if type(map_function) is str:
                    if map_function == 'KEY':
                        value = key
                    else:
                        value = eval(map_function, {'e': entity})
                if callable(map_function):
                    value = map_function(entity)
                if value is not None:
                    values[tk] = value
            except Exception as e:
                print(f"{e}: {map_function}, mapping:{options}, tuple: {tuple}")
                logging.warning(
                    f"Cannot map field {key} of entity {entity} to column {tk} with function {map_function}")

        assert len(values.keys()) > 0
        if not existing:
            # add new item
            print(f"Adding new item {key}: {values}")
            list_item = sp_list.add_item(values)
            new.append(list_item)
        else:
            print(f"Updating item {key} {existing}: {values}")
            # update existing
            if update_row(existing, values, key):
                updated.append(existing)
            current_items.remove(key)

    deleted = []
    for key in current_items:
        item = sp_content[key]
        deleted.append(item)
        print(f"Deleting item {key}")
        item.delete_object()

    return new, updated, list(deleted)


def update_row(item, values: dict, context: str) -> []:
    touched = False
    for key, new_value in values.items():
        current_value = item.properties.get(key)
        if (current_value is None or current_value != new_value) \
                and not (current_value is None and new_value == ''):  # None and '' are treated equal
            logging.debug(f"Updating value {key} {current_value} -> {new_value} in context {context} on item {item}")
            item.set_property(key, new_value).execute_query()
            touched = True
    return touched


def tr(element: dict, lang: str = 'en') -> str:
    if element is None or len(element) < 1:
        return ''
    result = element.get(lang)
    if result is None:
        logging.warning(f"No translation for language {lang} on {element}")
        result = ''
    return result


def main(configuration: str = 'fyayc-sharepoint.yaml', ) -> None:
    with open(configuration, 'r') as src:
        config = yaml.safe_load(src)

    # Verify ssot
    ssot = Path(config['ssot'])
    if not ssot.is_file():
        ssot = Path.cwd() / ssot

    assert ssot.is_file(), f"Invalid path to ssot: {ssot.resolve()}"

    with open(str(ssot), 'r') as src:
        model = json.load(src)

    print(f"Working with ssot {model['model']}")
    assert len(model['entities']) > 0, f"Cannot find 'entities' in model {ssot}"

    ctx = login(config)

    enti_list_name = config['lists'].get('entities')
    entity_list = ctx.web.lists.get_by_title(enti_list_name)
    update_structure(entity_list, entity_mapping)
