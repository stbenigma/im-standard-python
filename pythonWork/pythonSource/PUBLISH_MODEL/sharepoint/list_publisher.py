import csv
import json
import logging
import os
from pathlib import Path
import yaml
from office365.sharepoint.listitems.listItem_collection import ListItemCollection
from tqdm.autonotebook import tqdm

from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.client_request_exception import ClientRequestException
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


def update_structure(sharepoint_list: List, columns: [()], direct_write: bool = False) -> [str]:
    """
    Read structure
    Update structure

    :param sharepoint_list: Name of the list in Sharepoint
    :param columns: Columns definition. See end of this file.
    :param direct_write: Execute changes immediately if <code>True</code>.
        <br/>Changes will be performed on next <code>ctx.update_query()</code> otherwise.
    :return: List of changes
    """

    fields = sharepoint_list.fields.get().execute_query()
    logging.debug(f"Processing {len(fields)} fields. Reference: {len(columns)}")

    existing_fields = {}
    field_collection = []
    for field in fields:
        name = field.properties['EntityPropertyName']  # use this as key
        logging.debug(f"Found field {name}: {vars(field)}\n{type(field._properties_metadata)}")
        existing_fields[name] = field
        field_collection.append(field.properties)

    existing_fields_keys = set(existing_fields.keys())
    missing_fields_keys = set(map(lambda r: r[0], columns)) - existing_fields_keys
    logging.debug(f"Missing fields on list:\n {missing_fields_keys}")

    # need to fetch this if we want the title
    sharepoint_list.get().execute_query()
    message = [
        f"- Synchonizing {len(field_collection)} fields in list '{sharepoint_list.title}' - # columns {len(columns)}\n{columns}"]
    logging.info(message[0])

    for record in columns:
        touched = 0
        key = record[0]
        configuration = record[1]
        properties = configuration.get('properties')
        description_text = properties.get('Description') if properties.get(
            'Description') is not None else f"{key} field"
        field_type_kind = properties.get('FieldTypeKind', 3)  # default 3 = Long text (RichTextFormat?)
        if key not in existing_fields_keys:


            logging.info(f"Creating new column {key}")
            # create new field
            field = FieldCreationInformation(
                title=key, field_type_kind=field_type_kind,
                description=description_text,
                required=properties.get('Required', False)
            )
            message.append(f"Adding new field {key}")
            sharepoint_list.fields.add(field)
            if direct_write:
                sharepoint_list.execute_query()
            touched += 1
            fields = list(filter(lambda f: f.properties.get('EntityPropertyName') == key, sharepoint_list.fields.get().execute_query()))
            assert len(fields) == 1, f"Found {len(fields)} fields with name {key}"
            field = next(iter(fields))
        else:
            field = existing_fields[key]

        logging.debug(f"Processing column {key}\nCurrent: {field.properties}")
        # update structure (if possible)
        current_field_type = field.get_property('FieldTypeKind')
        # See https://docs.microsoft.com/en-us/previous-versions/office/sharepoint-server/ee540543(v=office.15)
        logging.debug(f"Updating field '{key}' with current FieldTypeKind {current_field_type}")
        assert current_field_type == field_type_kind, \
            f"Field type {current_field_type} (current) vs {field_type_kind} (configuration) mismatch" \
            f" on column '{key}'\n{str(field.properties).replace(',', ',' + os.linesep)}"
        updated = update_field_properties(properties, field, parent=sharepoint_list, direct_write=direct_write)
        if len(updated) > 0:
            logging.debug(f"Updated {len(updated)} properties of field {key}\n{field.properties}")
            message.append(f"-- Updating properties of field '{key}'")
            message.extend(updated)
            touched += 1

        if touched > 0 and direct_write:
            change = f"Performing {touched} changes on field '{key}' ..."
            logging.info(change)
            print(change)
            try:
                sharepoint_list.context.execute_query()
            except ClientRequestException:
                print("\n".join(message))
                raise
            logging.debug("done")

    return message


def update_field_properties(properties: dict, field: FieldCreationInformation, parent: List,
                            direct_write: bool = False) -> [str]:
    assert dict is not None
    assert field is not None
    assert parent is not None

    message = []
    for col_key, value in properties.items():
        if 'Description' == col_key: continue
        if 'FieldType' == col_key: continue
        try:
            current = field.get_property(col_key)
            if current != value:
                update_message = f"Changing property {col_key} from {current} to {value} in field '{field.get_property('Title')}' on list {parent.title}"
                logging.info(update_message)
                message.append(update_message)
                field.set_property(col_key, value, True)
                if direct_write:
                    field.update().execute_query()
            else:
                logging.debug(f"No changes for {col_key} on {parent.title}")
        except AttributeError as e:
            logging.warning(f"Cannot change field {col_key} of column {field.get_property('Title')}\n{e}")
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


def load_content(items: ListItemCollection) -> dict:
    """
    Load content into list
    :param items: Sharepoint list to load
    :return: List containing tuples of kind (item['Key'], item)
    """
    content = items.get().execute_query()
    result = {}
    for item in content:
        key = item.properties.get('Key')
        if key is not None:
            result[key] = item
        else:
            logging.warning(f"No key for item {item.properties.get('Id')} {item.properties}")
    return result


def update_content(sp_list: List, mapping: dict, model_content: dict, sp_content: dict, direct_write: bool = False):
    """
    mapping = {
        'Title': tr(entity['name']),
        'Description': tr(entity['descr']),
        'Synonyms': tr(entity['synonyms']),
        'Key': key
    }
    :param sp_list Share point list
    :param mapping Mapping between model_content and sp_content
    :param model_content SPOD list
    :param sp_content Previously fetched sharepoint list
    """
    assert sp_list is not None
    assert mapping is not None
    assert isinstance(model_content, dict)
    assert isinstance(sp_content, dict)

    new = []
    updated = []
    current_items = set(sp_content.keys())
    logging.info(f"List '{sp_list.title}' contains {len(current_items)} rows. New rows count {len(model_content)}.")
    for key, entity in tqdm(model_content.items()):
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
                    f"Cannot map field {tk} of entity {key}: {entity} to column {tk} with function {map_function}.\n",
                    e, exc_info=True)

        assert len(values.keys()) > 0
        if not existing:
            # add new item
            logging.debug(f"Adding new item {key}: {values}")
            list_item = sp_list.add_item(values)
            new.append(list_item)
            if direct_write:
                sp_list.execute_query()

        else:
            logging.debug(f"Updating item {key} {existing}: {values}")
            # update existing
            if update_row(existing, values, key):
                updated.append(existing)
                if direct_write:
                    existing.execute_query()

            current_items.remove(key)

    deleted = []
    for key in current_items:
        item = sp_content[key]
        deleted.append(item)
        print(f"Deleting item {key}")
        item.delete_object()
        if direct_write:
            sp_list.execute_query()

    return new, updated, deleted


def update_row(item, values: dict, context: str) -> []:
    touched = False
    for key, new_value in values.items():
        current_value = item.properties.get(key)
        if (current_value is None or current_value != new_value) \
                and not (current_value is None and new_value == ''):  # None and '' are treated equal
            logging.debug(
                f"Updating value {key} {item.properties['Id']} {current_value} -> {new_value} in context {context} on item {item} {item.properties.get('Id')}")
            item.set_property(key, new_value)
            touched = True
    if touched:
        item.update()
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


# fyayc sharepoint cloud 2022-03-11
example_lookup_person = {
    '_properties': {
        'AutoIndexed': False,
        'CanBeDeleted': False,
        'ClientSideComponentId': '00000000-0000-0000-0000-000000000000',
        'ClientSideComponentProperties': None,
        'ClientValidationFormula': None,
        'ClientValidationMessage': None,
        'CustomFormatter': None,
        'DefaultFormula': None,
        'DefaultValue': None,
        'Description': '',
        'Direction': 'none',
        'EnforceUniqueValues': False,
        'EntityPropertyName': 'Editor',
        'Filterable': True,
        'FromBaseType': True,
        'Group': 'Custom Columns',
        'Hidden': False,
        'Id': 'd31655d1-1d5b-4511-95a1-7a09e9b75bf2',
        'Indexed': False,
        'IndexStatus': 0,
        'InternalName': 'Editor',
        'IsModern': False,
        'JSLink': 'clienttemplates.js',
        'PinnedToFiltersPane': False,
        'ReadOnlyField': True,
        'Required': False,
        'SchemaXml': '<Field ID="{d31655d1-1d5b-4511-95a1-7a09e9b75bf2}" ColName="tp_Editor" RowOrdinal="0" ReadOnly="TRUE" Type="User" List="UserInfo" Name="Editor" DisplayName="Modified By" SourceID="http://schemas.microsoft.com/sharepoint/v3" StaticName="Editor" FromBaseType="TRUE" />',
        'Scope': '/sites/CoPInformation-Data-Governance/Lists/Sandbox_Entities',
        'Sealed': False,
        'ShowInFiltersPane': 0,
        'Sortable': True,
        'StaticName': 'Editor',
        'Title': 'Modified By',
        'FieldTypeKind': 20,
        'TypeAsString': 'User',
        'TypeDisplayName': 'Person or Group',
        'TypeShortDescription': 'Person or Group',
        'ValidationFormula': None,
        'ValidationMessage': None,
        'AllowMultipleValues': False,
        'DependentLookupInternalNames': {},
        'IsDependentLookup': False,
        'IsRelationship': False,
        'LookupField': '',
        'LookupList': '{7d7d471c-ff41-48a5-bacb-6ea0fb5151d6}',
        'LookupWebId': 'e12eff43-dfcf-4ca9-be8c-a94776a320fd',
        'PrimaryFieldId': None,
        'RelationshipDeleteBehavior': 0,
        'UnlimitedLengthInDocumentLibrary': False,
        'AllowDisplay': True,
        'Presence': True,
        'SelectionGroup': 0,
        'SelectionMode': 1,
        'UserDisplayOptions': None
    },
    '_properties_metadata': {
        'AutoIndexed': {},
        'CanBeDeleted': {},
        'ClientSideComponentId': {},
        'ClientSideComponentProperties': {},
        'ClientValidationFormula': {},
        'ClientValidationMessage': {},
        'CustomFormatter': {},
        'DefaultFormula': {},
        'DefaultValue': {},
        'Description': {},
        'Direction': {},
        'EnforceUniqueValues': {},
        'EntityPropertyName': {},
        'Filterable': {},
        'FromBaseType': {},
        'Group': {},
        'Hidden': {},
        'Id': {},
        'Indexed': {},
        'IndexStatus': {},
        'InternalName': {},
        'IsModern': {},
        'JSLink': {},
        'PinnedToFiltersPane': {},
        'ReadOnlyField': {},
        'Required': {},
        'SchemaXml': {},
        'Scope': {},
        'Sealed': {},
        'ShowInFiltersPane': {},
        'Sortable': {},
        'StaticName': {},
        'Title': {},
        'FieldTypeKind': {},
        'TypeAsString': {},
        'TypeDisplayName': {},
        'TypeShortDescription': {},
        'ValidationFormula': {}, 'ValidationMessage': {}, 'AllowMultipleValues': {},
        'DependentLookupInternalNames': {}, 'IsDependentLookup': {}, 'IsRelationship': {},
        'LookupField': {}, 'LookupList': {}, 'LookupWebId': {}, 'PrimaryFieldId': {},
        'RelationshipDeleteBehavior': {}, 'UnlimitedLengthInDocumentLibrary': {},
        'AllowDisplay': {},
        'Presence': {}, 'SelectionGroup': {}, 'SelectionMode': {}, 'UserDisplayOptions': {}
    },
    '_entity_type_name': None,
    '_query_options': None,
    '_parent_collection': """< office365.sharepoint.fields.field_collection.FieldCollection
object
at
0x11301fcd0 >""",
    '_context': """< office365.sharepoint.client_context.ClientContext
object
at
0x1131ce9d0 > """,
    '_resource_path': """/ Lists / GetByTitle('Sandbox_Entities') / Fields / getById(
    'd31655d1-1d5b-4511-95a1-7a09e9b75bf2')""",
    '_namespace': 'SP'}
