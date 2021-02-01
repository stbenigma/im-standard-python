from xml.sax.saxutils import escape
from datetime import datetime
import logging

class Publisher:
    '''
    The publisher contains mapping information of IM elements.
    Helper methods to translate content from IM json to Confluence.
    '''

    log = logging.getLogger(__name__)

    def __init__(self, config, data, confluence, space_key, root_page_id, default_language='de'):
        self.config = config
        self.json_data = data
        self.confluence = confluence
        self.space_key = space_key
        self.root_page_id = root_page_id
        self.language = default_language
        self.minor_edit = True

        # dictionary with key = element_key ('E233322', 'A132452', ...)
        self.content_map = {}
        # dictionary containing page name as key, value = content_map:key
        self.page_name_map = {}

        stamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.version_comment = 'Update ' + str(stamp_now)

    def translate(self, field, language=None):
        if language is None: language = self.language
        if field and field.get(language):
            return escape(field[language])
        self.log.warning('No translation for "{}" in language {}'.format(field, language))
        return ''

    def page_title(self, key: str):
        '''Returns the page title of an element. This will be used to reference elements'''
        page = self.content_map[key]
        return page['title']

    def scan_current_content(self):
        '''Scan current content below page-root and fills the content_map accordingly'''
        for topic in self.config['content']:
            for key in self.json_data[topic]:
                entry = self.json_data[topic][key]
                title_safe = self.translate(entry['name']).strip()
                taken = self.page_name_map.get(title_safe)
                if taken:
                    title_safe = title_safe + ' [' + key + ']'
                    self.log.warning('Extending title to {} to ensure uniqueness for {} {}'.format(title_safe, topic, key))
                self.content_map[key] = { 'title': title_safe, 'data': entry }
                self.page_name_map[title_safe] = key

        return self.content_map

    def register_page_id(self, key: str, page_id: str):
        page = self.content_map.get(key)
        if not page:
            self.log.warning('New element {} '.format(key))
            page = {}
            self.content_map[key] = page
        else:
            previous = page.get('pageid')
            assert page_id != previous, 'Altering page id from {} to {} for key {}'.format(previous, page_id, key)
        page['pageid'] = page_id

    def page_for_key(self, key: str):
        '''Returns the page object of an element or None if there is no page yet
        A page object is a dictionary containing 'pageid' and 'name'
        '''
        return self.content_map.get(key)

    def stub(self, title: str, parent_page_id):
        '''Create a stub page to obtain the page id for the title'''
        if self.confluence.page_exists(self.space_key, title):
            page_id = self.confluence.get_page_id(self.space_key, title)
            return { 'id': page_id }
        create_result = self.confluence.create_page(self.space_key, title=title, parent_id=parent_page_id, body=('generated stub'))
        return create_result

    def update_page(self, key: str, body: str, minor_edit=True, version_comment=''):
        meta = self.page_for_key(key)
        self.confluence.update_page(meta['pageid'], meta['title'], body, minor_edit=minor_edit, version_comment=version_comment)

    def relation_self(self, entity_key: str, relation_key: str):
        '''Returns the local end of the relation_key attached to enitity_key'''
        relation = self.json_data['relations'][relation_key]
        if relation['from-to']['enti'] == entity_key:
            return relation['from-to']
        else:
            return relation['to-from']

    def relation_other(self, entity_key: str, relation_key: str):
        '''Returns the remote end of the relation_key'''
        relation = self.json_data['relations'][relation_key]
        if relation['from-to']['enti'] == entity_key:
            return relation['to-from']
        else:
            return relation['from-to']
