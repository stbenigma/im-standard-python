from datetime import datetime
from requests.exceptions import HTTPError
from functools import reduce
import markupsafe
import logging
import html
from colorama import Fore, Style


class ContextLogger(logging.LoggerAdapter):

    def __init__(self, logger, topic: str, key: str):
        super().__init__(logger, {'topic': topic, 'key': key})
        self.topic = topic
        self.key = key

    def process(self, msg, kwargs):
        return '[{topic}:{key}] - {message}'.format(topic=self.topic, key=self.key, message=msg), kwargs


class Publisher:
    """
    The publisher contains mapping information of IM elements.
    Helper methods to translate content from IM json to Confluence.
    """
    logger = logging.getLogger(__name__)
    log = logger

    def __init__(self, config, data, confluence, space_key, root_page_id,
                 languages=['de'], version_comment=None):

        self.config = config
        self.json_data = data
        self.confluence = confluence
        self.space_key = space_key
        self.root_page_id = root_page_id

        self.minor_edit = True
        self.languages = languages if languages else data['languages']
        assert len(self.languages) > 0, 'Expecting at least one language to translate to'

        # dictionary with key = element_key ('E233322', 'A132452', ...)
        # value = map with a page entry per language ( { 'de': page_de, 'en': page_en } )
        self.content_map = {}

        # dictionary containing page name as key, value = content_map:key
        self.page_name_map = {}

        stamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.version_comment = version_comment if version_comment else 'Update ' + str(stamp_now)

        # default translation language: first in self.languages
        # this is an operational state -> factor out
        self.language = languages[0]

    def set_context(self, topic: str, key: str):
        self.log = ContextLogger(self.logger, topic, key)


    def tr(self, field, language=None) -> str:
        if language is None:
            language = self.language

        if isinstance(field, dict):
            text = field.get(language)
            if not text:
                # fallback, use whatever present
                text = field.get(self.languages[0], '-no-fallback-')
            if not text:
                return ''
            return text

        if isinstance(field, str):
            self.log.debug('Untranslated string "{}"'.format(field))
            return field

        self.log.debug('No text for field "{}"'.format(field))
        return ''

    def translate(self, field, language=None) -> markupsafe.Markup:
        return markupsafe.Markup(self.tr(field, language))

    def translate_text(self, field, language=None) -> markupsafe.Markup:
        text = html.escape(self.tr(field, language))
        linebreaks = text.replace('\n', '<br/>\n')
        return markupsafe.Markup(linebreaks)

    def page_title(self, key: str) -> str:
        """Returns the page title of an element. This will be used to reference elements"""
        return self.translation_title(key, self.language)

    def translation_title(self, key: str, lang: str) -> str:
        """Returns the page title of an element. This will be used to reference elements"""
        pages = self.content_map[key]
        if pages:
            same_language_page = pages.get(lang)
            if not same_language_page.get('title'):
                self.log.warning('No title for key {} in language {}'.format(key, lang))
                return '*missing title for key "{key}" in language {lang}*'.format(key=key, lang=lang)
            return same_language_page['title']

    def order_topic_tree(self, topics: dict):
        """Flatten topic tree to process form roots to leaves"""
        topic_list = list(topics)
        result = []

        roots = filter(lambda x: x['parent'] is None, topic_list)
        topic_list.remove(roots)

        for child in topic_list:
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

        for language in list(self.languages):
            self.language = language
            for topic in list(topics):
                self.log.debug('Processing ' + topic + ' for language ' + language)
                for key in self.json_data[topic]:
                    entry = self.json_data[topic][key]
                    title_safe = self.translate(entry['name']).strip()

                    if topic == 'attributes':
                        title_safe = '{} - {}'.format(title_safe,
                                                      self.translate(
                                                          self.json_data['entities'][entry['entity']]['name']))

                    if topic == 'tables':
                        title_safe = '{} - {}'.format(title_safe,
                                                      self.translate(
                                                          self.json_data['systems'][entry['interface-id']]['name']))

                    if topic == 'columns':
                        title_safe = '{} - {}'.format(title_safe,
                                                      self.translate(
                                                          self.json_data['tables'][entry['table-id']]['name']))

                    title_safe = self.lang_specific(title_safe)

                    is_taken = self.page_name_map.get(self.confluence_stem(title_safe))
                    if is_taken:
                        title_safe = title_safe + ' [' + key + ']'
                        self.log.debug(
                            'Extending title to {} to ensure uniqueness for {} {}'.format(title_safe, topic, key))

                        is_taken = self.page_name_map.get(self.confluence_stem(title_safe))
                        while is_taken:
                            title_safe = title_safe + '+'
                            is_taken = self.page_name_map.get(self.confluence_stem(title_safe))

                    pages = self.content_map.get(key, {})
                    pages[self.language] = {'title': title_safe, 'data': entry, 'topic': topic}
                    self.content_map[key] = pages

                    self.page_name_map[self.confluence_stem(title_safe)] = key

        return self.content_map

    def register_page_id(self, key: str, page_id: str):
        element = self.content_map.get(key)
        if not element:
            self.log.debug('New element {}'.format(key))
            element = {self.language: {}}
        else:
            current = element.get(self.language)
            if not current:
                self.log.debug('Adding page {} for key {} for language {}'.format(page_id, key, self.language))
                element[self.language] = {}
            else:
                previous = current.get('pageid')
                if previous:
                    assert page_id == previous, 'Altering page id from {} to {} for key {}'.format(previous, page_id,
                                                                                                   key)
        element[self.language]['pageid'] = page_id
        self.content_map[key] = element
        element['filtered'] = False
        return element

    def page_for_key(self, key: str):
        """Returns the page object of an element or None if there is no page yet.
        A page object is a dictionary containing 'pageid' and 'name'.
        """
        element = self.content_map.get(key)
        if element and element.get(self.language):
            assert element[self.language].get('pageid'), 'No page id on element ' + str(element)
            return element.get(self.language)
        raise RuntimeError('No page found for key {} in language {}'.format(key, self.language))

    def stub(self, key: str, title: str, parent_page_id, content='+[stub]+', labels=[]):
        """Create a stub page to obtain the page id for the title"""
        if self.confluence.page_exists(self.space_key, title):
            page_id = self.confluence.get_page_id(self.space_key, title)
            current = self.confluence.get_page_by_id(page_id, expand='body.storage,ancestors,version,history')
            current_parent = None
            ancestors = current['ancestors']
            if len(ancestors) > 0:
                current_parent = ancestors[-1]['id']
            if current_parent != parent_page_id:
                self.log.warning(
                    'Moving page {title} from {source} to {destination}'.format(title=title, source=current_parent,
                                                                                destination=parent_page_id))
                self.confluence.move_page(self.space_key, page_id, target_id=parent_page_id)
            page = self.register_page_id(key, page_id)
            page[self.language]['current_confluence_content'] = current
            self.set_page_labels(page_id, labels)
            return {'id': page_id, 'current': current}

        create_result = self.confluence.create_page(self.space_key, title=title, parent_id=parent_page_id,
                                                    body=content)
        self.log.info(
            'Created new page {} for title {} below parent {}'.format(create_result['id'], title, parent_page_id))

        self.register_page_id(key, create_result['id'])
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
            return self.confluence.update_page(meta['pageid'], meta['title'], body, minor_edit=minor_edit,
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

    def column_lineage(self, column_key: str):
        """Collects columns that are mapped with the column provided via the IM"""
        column = self.json_data['columns'][column_key]
        result = []
        for attribute_key in column['attributesmapped']:
            attribute = self.json_data['attributes'][attribute_key]
            columns_mapped = attribute['columnsmapped+']
            all_columns = map(lambda entry: columns_mapped[entry], columns_mapped)
            cols = reduce(lambda e, l: e + l, list(all_columns), [])
            result.extend(cols)
        try:
            result.remove(column_key)
        except ValueError:
            # fine if it is not in the list
            pass
        return result

    def attribute_lineage(self, attribute_key: str):
        """Collects columns that are mapped to the provided attribute"""
        attribute = self.json_data['attributes'][attribute_key]
        columns_mapped = attribute['columnsmapped+']
        all_columns = map(lambda entry: columns_mapped[entry], columns_mapped)
        cols = reduce(lambda e, l: e + l, list(all_columns), [])
        return cols

    def soft_link(self, key: str, item_class: str = None, title: str = None):
        """Returns a link to the element denoted by key"""
        if not key:
            return ''

        pages = self.content_map[key]
        if pages and pages.get(self.language):
            same_language_page = pages.get(self.language)
            if same_language_page.get('title') and not pages.get('filtered', False):
                page_title = self.page_title(key)
                title_text = title if title else page_title
                return markupsafe.Markup(
                    ('<ac:link><ri:page ri:content-title="{reference}" /><ac:plain-text-link-body>'
                     '<![CDATA[{title_text}]]></ac:plain-text-link-body></ac:link>').format(
                        reference=html.escape(page_title), title_text=title_text)
                )

        just_name = title if title else key
        if not item_class:
            item_class = self.find_class_for_key(key)

        if item_class:
            just_name = self.translate(self.json_data[item_class][key].get('name'))

        return just_name

    def find_class_for_key(self, key: str) -> str:
        """
            Reverse look up te entity class of a key.
            Known entity classes are domains, entities, attributes, systems, ...
            :returns: None, if unable to find the entity class
        """
        if not key:
            return None

        # scan top level classes for the key
        for class_key in self.json_data:
            node = self.json_data[class_key]
            if node.get(key):
                return class_key

        return None

    def entity_icon(self, entity: object):
        return markupsafe.Markup(
            '<img width="50px" align="right" ' +
            'src="' +
            'https://res.cloudinary.com/foryouandyourcustomers/image/upload/fyayc_icon_library/svg/ChannelOverview/f-icon_channeloverview_0099_product.svg' +
            '" />'
        )

    def lang_specific(self, text: str) -> str:
        if self.is_default_language():
            return text
        return text + ' ' + self.language

    def is_default_language(self) -> bool:
        return self.language == self.languages[0]

    def other_languages(self) -> [str]:
        others = list(self.languages)
        others.remove(self.language)
        return others

    def set_language(self, language: str):
        assert language in self.languages, 'Language ' + language + ' not in known list: ' + str(self.languages)
        self.language = language


def print_http_error_details(e: HTTPError):
    print(Fore.RED + e.response.content.decode('utf-8'))
    from pprint import pprint
    print(Fore.YELLOW + str(vars(e)))
    pprint(vars(e.response))
    result = e.response.raw
    pprint(vars(result))
    print(Style.RESET_ALL)
