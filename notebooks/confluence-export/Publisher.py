from xml.sax.saxutils import escape
from datetime import datetime
from requests.exceptions import HTTPError
import logging


class Publisher:
    """
    The publisher contains mapping information of IM elements.
    Helper methods to translate content from IM json to Confluence.
    """

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
        if isinstance(field, dict) and field.get(language):
            return escape(field[language])
        if isinstance(field, str):
            self.log.debug('No translation for "{}" in language {}'.format(field, language))
            return field

        self.log.debug('No text for field "{}"'.format(field))
        return ''

    def page_title(self, key: str):
        """Returns the page title of an element. This will be used to reference elements"""
        page = self.content_map[key]
        if not page.get('title'):
            self.log.error('No title for key {}'.format(key))
        return page['title']

    def order_topic_tree(self, topics: dict):
        """Flatten topic tree to process form roots to leaves"""
        all = list(topics)
        result = []

        roots = filter(lambda x: x['parent'] is None, all)
        remainder = all.remove(roots)

        for child in remainder:
            result.append(child)
            children = self.sort_topics({child: topics[child]})
            result.append(children)

        return result

    def collect_recursive(self, node, parent=None):
        """Collect config nodes in a linked tree"""
        content = node.get('content')
        topics_dict = {}
        if content:
            topics = list(content)
            for topic in topics:
                sub_node = node['content'][topic]
                topics_dict[topic] = sub_node
                sub_node['parent'] = parent
                sub = sub_node.get('content')
                if sub:
                    # recurse children
                    topics_dict.update(self.collect_recursive(sub_node, sub_node))

        return topics_dict

    def confluence_stem(self, page_title: str):
        return page_title.lower()

    def scan_current_content(self):
        """Scan current content below page-root and fills the content_map accordingly"""
        topics = self.collect_recursive(self.config)

        for topic in list(topics):
            self.log.warning('Processing ' + topic)
            for key in self.json_data[topic]:
                entry = self.json_data[topic][key]
                title_safe = self.translate(entry['name']).strip()

                if topic == 'attributes':
                    title_safe = '{} - {}'.format(title_safe, self.content_map[entry['entity']]['title'])

                if topic == 'tables':
                    title_safe = '{} - {}'.format(title_safe, self.content_map[entry['interface-id+']]['title'])

                if topic == 'columns':
                    title_safe = '{} - {}'.format(title_safe, entry['table-name+'])

                is_taken = self.page_name_map.get(self.confluence_stem(title_safe))
                if is_taken:
                    title_safe = title_safe + ' [' + key + ']'
                    self.log.warning(
                        'Extending title to {} to ensure uniqueness for {} {}'.format(title_safe, topic, key))
                self.content_map[key] = {'title': title_safe, 'data': entry, 'topic': topic}
                self.page_name_map[self.confluence_stem(title_safe)] = key

        return self.content_map

    def register_page_id(self, key: str, page_id: str):
        page = self.content_map.get(key)
        if not page:
            self.log.debug('New element {} '.format(key))
            page = {}
            self.content_map[key] = page
        else:
            previous = page.get('pageid')
            if previous:
                assert page_id == previous, 'Altering page id from {} to {} for key {}'.format(previous, page_id, key)
        page['pageid'] = page_id

    def page_for_key(self, key: str):
        """Returns the page object of an element or None if there is no page yet
        A page object is a dictionary containing 'pageid' and 'name'
        """
        return self.content_map.get(key)

    def stub(self, title: str, parent_page_id, content='stub', labels=[]):
        """Create a stub page to obtain the page id for the title"""
        if self.confluence.page_exists(self.space_key, title):
            page_id = self.confluence.get_page_id(self.space_key, title)
            current = self.confluence.get_page_by_id(page_id, expand='body.storage,ancestors,version,history')
            current_parent = None
            ancestors = current['ancestors']
            if len(ancestors) > 0:
                current_parent = content['ancestors'][-1]['id']
            if current_parent != parent_page_id:
                self.log.warning(
                    'Moving page {title} from {source} to {destination}'.format(title=title, source=current_parent,
                                                                                destination=parent_page_id))
                self.confluence.move_page(self.space_key, page_id, target_id=parent_page_id)

            self.set_page_labels(page_id, labels)
            return {'id': page_id, 'current': current}

        create_result = self.confluence.create_page(self.space_key, title=title, parent_id=parent_page_id,
                                                    body=content)
        self.set_page_labels(create_result['id'], labels)
        create_result['current'] = None
        return create_result

    def set_page_labels(self, page_id, labels: list):
        """Add labels to a page"""
        for label in labels:
            self.confluence.set_page_label(page_id, label)

    def update_page(self, key: str, body: str, minor_edit=True, version_comment=''):
        meta = self.page_for_key(key)
        try:
            self.confluence.update_page(meta['pageid'], meta['title'], body, minor_edit=minor_edit,
                                        version_comment=version_comment)
        except HTTPError as error:
            self.log.error('Cannot update page "{page_title}" {page_id}. {response}',
                           page_title=meta['title'], page_id=meta['pageid'],
                           response=error.response.content.decode('utf-8'))
            raise error

    def relation_self(self, entity_key: str, relation_key: str):
        """Returns the local end of the relation_key attached to enitity_key"""
        relation = self.json_data['relations'][relation_key]
        if relation['from-to']['enti'] == entity_key:
            return relation['from-to']
        else:
            return relation['to-from']

    def relation_other(self, entity_key: str, relation_key: str):
        """Returns the remote end of the relation_key"""
        relation = self.json_data['relations'][relation_key]
        if relation['from-to']['enti'] == entity_key:
            return relation['to-from']
        else:
            return relation['from-to']
