from xml.sax.saxutils import escape
from datetime import datetime
import logging

class Publisher:
    '''
    The publisher contains mapping information of IM elements.
    And helper methods to translate content from IM json to Confluence
    '''

    log = logging.getLogger(__name__)

    def __init__(self, config, data, confluence, space_key, root_page_id, language='de'):
        self.config = config
        self.json_data = data
        self.confluence = confluence
        self.space_key = space_key
        self.root_page_id = root_page_id
        self.language = language

        # dictionary with key = element_key ('E233322', 'A132452', ...)
        self.content_map = {}
        stamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def translate(self, field):
        if field and field.get(self.language):
            return escape(field[self.language])
        return ''

    def page_title(self, key: str):
        '''Returns the page title of an element. This will be used to reference elements'''
        page = self.content_map[key]
        return page['title']

    def scan_current_content(self):
        '''Scan current content below page-root and fills the content_map accordingly'''
        None   # Nothing found

    def register_page(self, key: str, page_id: str, title: str):
        page = self.content_map.get(key)
        if page:
            self.log.warning('Element {} entry {} will be overwritten'.format(key, page))
        page = {}
        page['pageid'] = page_id
        page['title'] = title
        self.content_map[key] = page

    def page_for_key(self, key: str):
        '''Returns the page object of an element or None if there is no page yet
        A page object is a dictionary containing 'pageid' and 'name'
        '''
        return self.content_map.get(key)

    def stub(self, title: str, parent_page_id):
        '''Create a stub page to obtain the page id for the title'''
        if self.confluence.page_exists(self.space_key, title):
            key = self.confluence.get_page_id(self.space_key, title)
            if key:
                return { 'id': str(key) }
            assert false, 'illegal condition, page exists but unable to retreive the id'
        create_result = self.confluence.create_page(self.space_key, title=title, parent_id=parent_page_id, body=('generated stub'))
        return create_result

    def update_page(self, key: str, body: str):
        meta = self.page_for_key(key)
        self.confluence.update_page(meta['pageid'], meta['title'], body)

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
