#!/usr/bin/env python
# coding: utf-8

# # Publisher Application
# 
# This application produces Confluence content based on an information model. 
# 
# 1. Setup and Configuration 
# 1. Build page tree based on configuration and from information model (SSOT JSON)
# 1. Create content (page, attachments, ...) including translations
# 1. Back up existing content (Optional)
# 1. Upload/_publishable content

# ## Configuration
# 
# Read and validate configuration.
# 
# Be aware not to commit your credentials stored in the configuration files.

# In[ ]:


configuration_file = 'bopt.yaml'
configuration_file = 'geberit.yaml'
configuration_file = 'crm_model.yaml'
configuration_file = 'borr.yaml'
configuration_file = 'raetsel-3lang.yaml'
configuration_file = 'modelmodel.yaml'
configuration_file = 'fyayc-projects.yaml'
configuration_file = 'fyayc-intern.yaml'


# In[ ]:


import os
assert os.path.isfile(configuration_file), "Cannot read file " + configuration_file
print(f"Working with configuration from {configuration_file}")


# ## Read configuration values

# In[ ]:


import os
import yaml
import json
import copy
from datetime import datetime


# In[ ]:


with open(configuration_file) as f:
    config = yaml.safe_load(f)
assert len(config) > 0, f'Config is empty :-(' 


# In[ ]:


json_ssot = config['source']
assert os.path.isfile(json_ssot), "Source file {} not found".format(json_ssot)
print(f"Loading {json_ssot}")
with open(json_ssot, 'r') as source:
     data = json.load(source)


# In[ ]:


data['model']['name'], data['_imprint_']


# In[ ]:


def sanitize_filename(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in ('.', '-', '_', ' ')).rstrip()


# In[ ]:


content_root = f"./confluence-content/{sanitize_filename(data['model']['name'])}"
print(f"Publishing to {os.path.abspath(content_root)}")


# ## Evaluate if we are online (deprecated -> two scripts)

# In[ ]:


confluence = config.get('confluence')
if confluence is not None:
    destination = f"{config['confluence']['apiurl']}/{config['confluence']['space']}/{config['confluence']['rootpage']}"
else:
    destination = f" folder {os.path.abspath(content_root)} only "


# In[ ]:


from IPython.core.display import HTML
HTML('''<p><span style="font-family: Impact; font-size:48px">
Publishing the information model <span style="color: darkorange">{name}
</span></span><br/> 
to <span style="color: darkorange">{dest}</span></p><p>from {source} according to configuration from {config}</p>'''
   .format(name=data['model']['name'], source=config['source'], 
           config=os.path.abspath(configuration_file), dest=destination))
     


# In[ ]:


conf_conf = config.get('confluence')
if confluence is not None:
    assert len(conf_conf['apiurl']) > 0
    space_key = conf_conf['space']
    root_page = conf_conf['rootpage']

    conf_confidential = copy.deepcopy(config)
    conf_confidential['confluence']['password'] = '***'
    print(f"Exporting to confluence {conf_confidential}")

# ## Verify dependencies
# Do this early before processing anything

# In[ ]:


import glob
import sys
from lxml import etree

IM_TOOL_LIB = '../../pythonWork/pythonSource'
sys.path.insert(0, os.path.abspath(IM_TOOL_LIB))
sys.path.insert(0, os.path.abspath(os.path.join(IM_TOOL_LIB, 'IM_db')))

from IM_OBJECTS.modelelement import Modelelemtype
from IM_JSON import JSModel

from IM_WEB.IM_HTML import drawiodiagram
from IM_WEB.IM_HTML import entityenviron


# ## Initialize logging

# In[ ]:


import logging

log = logging.getLogger()
log.setLevel(logging.DEBUG)

LOGFILE = 'target/debug.log'
os.makedirs('target', exist_ok=True)

handler = logging.handlers.RotatingFileHandler(
    LOGFILE, maxBytes=(1048576*5), backupCount=7
)
formatter = logging.Formatter("%(asctime)s [%(threadName)s] - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
log.addHandler(handler)

log.debug('Starting execution')


# # Setup translation
# 
# Requires gettext: `conda install gettext`
# 
# Trigger scan for translatable objects:
#     `xgettext --from-code utf-8 -L python -d scan.pot templates/*`
#     `msgmerge --width --update
# 
# https://phrase.com/blog/posts/translate-python-gnu-gettext/

# ## Internationalisation (i18n)
# 
# Publishing of content in different languages is supported. The GNU `gettext` toolchain is used to translate texts in code and templates.
# 
# Translation files are located in the 'locale' directory structure.
# 
# Use `xgettext --from-code utf-8 -L python -d confluence-publisher templates/*` to scan for content and
# `msgfmt -o ../locale/de/LC_MESSAGES/confluence-publisher.mo ../locale/de/LC_MESSAGES/confluence-publisher.po` to upate the compiled translation files.
# 
# Implemtation in section 'Translation'

# In[ ]:


import subprocess
import glob
from pathlib import Path

try:
    result = subprocess.run("msgfmt -V", shell=True, check=True, capture_output=True)
    message = result.stdout.decode()
    assert message.find('msgfmt') >= 0, 'gettext tool msgfmt is missing. Install it using `brew install gettext`.\n-= Message =-\n' + str(message)
    
    sources = glob.glob('locale/**/*.po', recursive=True)
    try:
        for src in sources:
            source = Path(src)
            destination = source.with_suffix('.mo')
            if source.stat().st_mtime > destination.stat().st_mtime: 
                log.info("Updating compiled translation {0} from {1}".format(destination, source))
                subprocess.run('msgfmt -o {dest} {src}'.format(dest=str(destination), src=str(source)), shell=True, check=True, capture_output=False)
                print("Translation {0} updated".format(src))
    except subprocess.CalledProcessError as e:
        raise Exception('Cannot update translation', e)
except subprocess.CalledProcessError as e:
    print(e)
    log.warning('Cannot update translation inline. But this is ok')
    pass


# In[ ]:


import gettext
locale_folder = config.get('locale', './locale')
gettext.bindtextdomain('confluence-publisher', locale_folder)


# In[ ]:


from pathlib import Path
translations_folders = list(Path(locale_folder).rglob("LC_MESSAGES"))
translations_folders


# ## Translator
# 
# Translation is done using the custom translator
# It uses gettext translate when there is no translation provided in the SSOT.
# 
# 

# In[ ]:


class Translator:
    """Translate strings"""
    logger = logging.getLogger("Translator")
    
    def __init__(self, language: str):
        self.language = language
        self.translator = gettext.translation('confluence-publisher', config.get('locale', './locale'), fallback=True, languages=[language])
        self.title_format = '{title} - [{language}]'
        self.logger = logging.getLogger("Translator " + language)
        
    def tr(self, element) -> str:

        if isinstance(element, dict):
            """If the value provided is a field containing translations, use them"""
            text = element.get(self.language)
            if text is None: #and len(element.values()) > 0:
                text = list(element.values())[0]
                self.logger.warning('Translator: Falling back to {} from {}'.format(text, str(element)))
            if not text:
                return ''
            return text

        # Fallback to gettext if not a dict
        if isinstance(element, str):
            translated = self.translator.gettext(element)
            return translated

        self.logger.warning("Cannot translate element '{0}' of type {1}".format(element, type(element)))
        return None
    
    def gettext(self, text: str):
        result = self.translator.gettext(text)
        if result == text:
            self.logger.warning("No translation for {0}".format(text))
        return result
    
    def translator(self):
        return self.translator
    
    def title_language(self, title: str) -> str:
        """Create unique confluence page title per translation"""
        return self.title_format.format(title = title, language = self.language)
    
    def key_lang(self, key: str) -> str:
        return key + '-' + self.language
    
    def lang(self) -> str:
        return self.language


# In[ ]:


translators = { language: Translator(language) for language in config['languages'] }
translators


# In[ ]:


default_language_translator = translators[config['languages'][0]]
default_language_translator.title_format = '{title}'
'Default language is {}'.format(default_language_translator.lang())


# ### Selftests

# In[ ]:


result = default_language_translator.tr('fadsjfklj4q9u')
assert result == 'fadsjfklj4q9u'


# In[ ]:


default_language_translator.tr('Synonyms')


# In[ ]:


default_language_translator.tr({ 'es': 'hola'} )


# In[ ]:


default_language_translator.tr('Diagram')


# In[ ]:


default_language_translator.gettext('Entities')


# In[ ]:


default_language_translator.gettext('{parent_title} - Documentation')


# ## Load the data
# The **data** is the JSON serialized information model 

# In[ ]:


import json

data = None
with open(config['source'], 'r') as source:
     data = json.load(source)

str(data)[:512]


# In[ ]:


data.get('_imprint_')


# In[ ]:


model_languages = list(data['languages'])
config_languages = list(config['languages'])
'Model languages: {}. Export configuration selected languages: {}'.format(model_languages, config_languages)


# In[ ]:


# Missing languages?
missing_translations = set(config_languages) - set(model_languages)
assert len(missing_translations) == 0, 'Missing languages in model: {}'.format(missing_translations) 


# In[ ]:


categories = list(data)
for category in categories:
    print('{} Elements in category "{}"'.format(len(data[category]), category))

# # Setup structure (page hierarchy) and navigation util

# In[ ]:


disclaimer = config.get('disclaimer', '')

destination_folder = os.path.join(config.get('destpath'),'pages')


# ## Navigator
# The navigator contains the map of all pages. It allows create confluence links from one page to it's translations and to parent pages.
# The internal page map contains:
# 'key': element key without language suffix -> 'page': Confluence page objects

# In[ ]:


class Navigator:
    
    def __init__(self):
        self.page_map = {}
        self.page_uniqueness_map = {}
    
    def register_page(self, key: str, lang: str, page: dict):
        key_lang = self.title_lang(key, lang)
        previous = self.page_map.get(key_lang)
        assert not previous, "There is already a page with key {0}: {1}\n{2}".format(key_lang, previous, page)
        self.page_map[key_lang] = page
        
        page['id'] = key_lang
        
        title = page['title']
        previous_u = self.page_uniqueness_map.get(title)
        self.page_uniqueness_map[title] = page
        assert not previous_u, "There is already a page with title {0}: {1}\n{2}".format(title, previous_u, page)
    
    def title_lang(self, key: str, lang: str) -> str:
        return key + '-' + lang
    
    def page_4_language(self, key: str, lang: str) -> str:
        return self.page_map.get(self.title_lang(key, lang))
    
    def translation_title(self, key: str, lang: str) -> str:
        """Get the title of the page with 'key' for language 'lang'"""
        return self.translation_page(key, lang)['title']

    def pages(self) -> list:
        return list(self.page_map.values())
    
    def page_by_title(self, title: str) -> dict:
        return self.page_uniqueness_map.get(title)  
    
    def page_by_key(self, key: str, lang: str) -> dict:
        return self.page_map[self.title_lang(key, lang)]


# ## Prepare destination structure
# Configuration:
# - content
#   - Entities
#     - Attributes
#   - databases
#     - Tables
#       - Columns
# 
# Rolled out:
# - Topic Entities
#   - Entity First
#       - Attribute1 of first entity
#       - Attribute2 of first entity
#   - Entity Second
#       - Attribute1 of second entity
# - Topic 'databases'
#   - System A
#     - Table A1
#       - Column ID - A1
#       - Colunn Name - A1
#       - Column Value - A1
#     - Table A2
#   - System B
#     - Table B1
#     - Table B2

# In[ ]:


def ensure_unique_page_title(page: dict, navigator: Navigator):
    """Make sure the page title is unique in this Confluence space. This does eventually modify the page element!"""
    title = page['title']
    existing_page_with_same_title = navigator.page_by_title(title)
    if existing_page_with_same_title:
        #print('Page for {}[{}] has same title as {}[{}]\nOld:{}\nNew:{}'.format(
        #    existing_page_with_same_title['key'], existing_page_with_same_title['title'], page['key'], title,
        #    existing_page_with_same_title['item'], page['item']))
        tokens = title.split('-')
        if len(tokens) > 1:
            tokens.insert(len(tokens) - 1, page['key'])
        else:
            tokens.append(page['key'])
        page['title'] = ' - '.join(tokens)
        print('Created unique title {}'.format(page['title']))


def manual_documentation(parent_page: dict, config: dict, navigator: Navigator, translator: Translator):
    """Add a page for manual documentation, if configured"""
    md = config.get('manual-documentation')
    if md:
        page = copy.copy(parent_page)
        page_key = parent_page['key'] + '-manual-documentation'
        page['key'] = page_key
        title_format = translator.gettext(md.get('title-format', "{parent_title} - manual"))
        page['name'] = title_format.format(parent_name=parent_page['name'], key=parent_page['key'], lang=translator.lang(), parent_title=parent_page['title'])
        page['title'] = page['name']
        page['config'] = md
        page['parent'] = parent_page
        page['template'] = translator.gettext(md.get('template', "manual-documentation.templ.html")) #'Manual documentation for {title} [{key}]'.format(title=parent_page['title'], key=page['key'])))
        # register child with parent
        parent_page['manual-documentation-page-title'] = page['title']
        
        labels = set(md.get('labels', []))
        labels.add('manual')
        labels.add(translator.lang())
        page['labels'] = labels
        # keep confluence content
        page['preserve'] = True
        page['level'] = page['level'] + 1
        page['template'] = md.get('template')
        page['path'] = parent_page['path']
        page['file'] = f"{parent_page['key']}-{translator.lang()}-manual.confluence.xml"
        
        ensure_unique_page_title(page, navigator)
        navigator.register_page(page_key, translator.lang(), page)
        return page
    else:
        return None


def prepare_pages(parent_page: dict, config: dict, topic: str, level: int, navigator: Navigator, translator: Translator, data: object):
    elements = data[topic]
    pages = []
    item_filter = config.get('filter')
    filtered = 0
    for element_key in list(elements):
    
        item = data[topic][element_key]
        if item_filter:
            filter_result = eval(item_filter)
            if not filter_result:
                filtered += 1
                continue

        name_translated = translator.tr(item['name']).strip()
        if len(name_translated) > 1:
            log.warning("Strange name for item {0}".format(item))

        title_safe = name_translated
        
        if topic == 'attributes':
            parent_key = item['entity']
        elif topic == 'tables':
            parent_key = item['datamodel-id']
        elif topic == 'columns':
            parent_key = item['table-id']
        else:
            parent_key = parent_page['key']
        
        parent = navigator.page_4_language(parent_key, translator.lang())
        
        assert parent, "Need a parent to process"
        
        parent['child-count'] = parent['child-count'] + 1
        parent_name = parent['name']
        
        item_title_rule = config.get('title_rule')
        if item_title_rule:
            title_by_rule = eval(translator.gettext(item_title_rule))
            if title_by_rule:
                title_safe = title_by_rule
        else:
            # Default naming rule for nested elements: {child_title} - {parent_title}
            title_format = translator.gettext(config.get('title-format', "{child_title} - {parent_name}"))
            if topic in ['attributes', 'tables', 'columns']:
                title_safe = translator.gettext(title_format).format(child_title=name_translated, parent_name=parent['name'],
                                                                     parent_title=parent['title'], lang=translator.lang())
                                              
        title = title_safe
        
        labels = set(config.get('labels', []))
        labels.add(translator.lang())
        page = {
            'key': element_key,
            'topic': topic,
            'name': title,
            'title': translator.title_language(title),
            'parent': parent,
            'labels': list(labels),
            'item': item,
            'config': config,
            'level': level,
            'translator': translator,
            'template': translator.gettext(config.get('template')),
            'child-count': 0,
            'path': os.path.join(destination_folder, topic),
            'file': f"{element_key}-{translator.lang()}.confluence.xml"
        }
        
        ensure_unique_page_title(page, navigator)
        
        navigator.register_page(element_key, translator.lang(), page)
        pages.append(page)
        
        if len(pages) < 2:
            print("Prepared page '{0}' [{1}]".format(page['title'], page['key']))
                
        md = manual_documentation(page, config, navigator, translator)
        if md:
            pages.append(md)
            if len(pages) < 3:
                print("Prepared manual documentation page '{0}' [{1}]".format(md['title'], md['key']))

    print('Added {} pages for topic {}. Filtered out {}'.format(len(pages), topic, filtered))
    
    # Descend into children, if any ...
    child_configurations = config.get('content')
    if child_configurations:
        """Process child types"""
        for child_config_topic in child_configurations:
            if not data[child_config_topic]:
                log.warning('No data for topic "{}"'.format(child_config_topic))
                continue
            child_config = child_configurations[child_config_topic]
            subpages = prepare_pages(page, child_config, child_config_topic, level + 1, navigator, translator, data)

    return pages


def top_level_content(config: dict, navigator: Navigator, translator: Translator, data: dict, base_position: int) -> list:
    """Recurse configuration content structure"""
    content = config.get('content')
    pages = []
    if content:
        position = base_position
        for topic_key in list(content):
            topic_config = content[topic_key]
            labels = set(topic_config.get('labels', []))
            labels.add('im-parent')
            labels.add('im-parent-' + topic_key)            
            labels.add(translator.lang())
            name = translator.gettext(topic_config.get('title')) #+ ' - ' + data['model']['name']
            category_page = {
                'topic': topic_key + '-root',
                'key': topic_key,
                'name': name,
                'title': translator.title_language(name),
                'labels': list(labels),
                'config': topic_config,
                'parent': None,
                'level': 0,
                'position': position,
                'child-count': 0,
                'translator': translator,
                'template': translator.gettext(topic_config.get('index-template', 'parent-page-index.templ.html')),
                'path': os.path.join(destination_folder, topic_key),
                'file': f"{topic_key}-{translator.lang()}.confluence.xml",
            }
            
            ensure_unique_page_title(category_page, navigator)

            navigator.register_page(topic_key, translator.lang(), category_page)
            pages.append(category_page)

            if len(pages) < 2:
                print("Prepared top level page '{0}' [{1}]".format(category_page['title'], category_page['key']))

            print('Processing category {} [{}]'.format(topic_config.get('title'), topic_key))
                        
            sub_pages = prepare_pages(category_page, topic_config, topic_key, 1, navigator, translator, data)
            if len(sub_pages) == 0:
                category_page['skip'] = True
            position += 1
    else:
        log.error('Cannot find content on root level')
    return pages


# In[ ]:


navigator = Navigator()

base_position = 0
for lang in list(config['languages']):
    print('*** Scanning for language {0} ***'.format(lang))
    trans = translators[lang]
    print('Translation => tr:{0} gettext:{1}'.format(trans.tr('Entities [TOC]'), trans.gettext('Entities [TOC]')))
    pages = top_level_content(config, navigator, trans, data, base_position)
    print('---------------------------')
    base_position += 10000
    
total = len(navigator.pages())
'Will produce {} * {} ~= {} pages'.format(len(config['languages']), len(pages), total)


# In[ ]:


level0 = list(filter(lambda page: page['level'] == 0, navigator.pages()))
[ page.get('title') for page in level0 ]


# In[ ]:


skiplist = list(filter(lambda page: page.get('skip', False), navigator.pages()))
'Will skip {} pages: {} ...'.format(len(skiplist), [page.get('title') for page in skiplist[:5]])


# # Create Confluence content
# Render the page content and create graphs and attachments for the respective page.

# In[ ]:


from tqdm.autonotebook import tqdm
from tqdm.notebook import tqdm_notebook


# ## Helper class to simplify template rendering
# 
# This helper is available in jina2 templates with the name 'util'

# In[ ]:


import html
import markupsafe
from functools import reduce
from IM_OBJECTS.modelelement import Modelelemtype

class ConfluenceContentUtil:
    """This util is used in jinja2 scripts to create Confluence content.
    It is designed to provide complex functionality, that does not fit into templates directly."""
    def __init__(self, navigator: Navigator, translator: Translator, languages: list, json_data: dict):
        self.translator = translator
        self.navigator = navigator
        self.language = translator.language
        assert len(self.language) == 2
        self.other_lang = list(languages)
        self.other_lang.remove(self.language)
        assert len(self.other_lang) + 1 == len(languages)
        self.json_data = json_data
    
    def translate(self, text):
        return self.translator.tr(text)
    
    def translate_text(self, field) -> markupsafe.Markup:
        translated = self.translator.tr(field)
        if translated is None:
            translated = ''
        text = html.escape(translated)
        linebreaks = text.replace('\n', '<br/>\n')
        return markupsafe.Markup(linebreaks)
        
    def other_languages(self) -> list:
        return self.other_lang
    
    def soft_link(self, key: str, lang: str = None) -> markupsafe.Markup:
        """Returns a confluence link if the key is represented with a page in the same language context or the language provided"""
        if key:
            language = lang if lang else self.language
            page = self.navigator.page_4_language(key, language)
            if page:
                return markupsafe.Markup('''<ac:link><ri:page ri:content-title="{page_title}"/><ac:plain-text-link-body><![CDATA[{name}]]></ac:plain-text-link-body></ac:link>'''.format(
                    page_title=html.escape(page['title']), name=html.escape(page.get('name'))))
            else:
                if 'DOMA' in key:
                    return translator.tr(self.json_data['domains'][key]['name'])
                elif 'COLUMN' in key:
                    return translator.tr(self.json_data['columns'][key]['name'])
                else:
                    return key
        else:
            return ''
        
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
    
    def icon(self, key: str) -> markupsafe.Markup:
        return markupsafe.Markup(
            '<img width="50px" align="right" ' +
            'src="http://res.cloudinary.com/foryouandyourcustomers/image/upload/fyayc_icon_library/svg/0099.svg" />'
        )
        
    def type_name_from_key(self, key: str) -> str:
        """Return the type of a key. Results are [Entity, Attribute, Document, Organisational Unit, Diagram, ...]"""
        if key.startswith(Modelelemtype.ENTI):
            return "Entity"
        elif key.startswith(Modelelemtype.BURU):
            return "Business rule"
        elif key.startswith(Modelelemtype.ATTR):
            return "Attribute"
        elif key.startswith(Modelelemtype.RELA):
            return "Relation"
        elif key.startswith(Modelelemtype.INTF):
            return "System"
        elif key.startswith(Modelelemtype.DOMA):
            return "Domain"
        elif key.startswith(Modelelemtype.TABL):
            return "Table"
        elif key.startswith(Modelelemtype.DOCU):
            return "Document"
        elif key.startswith(Modelelemtype.COLU):
            return "Column"
        elif key.startswith(Modelelemtype.ORGU):
            return "Organisational unit"
        elif key.startswith(Modelelemtype.DIAG):
            return "Diagram"
        elif key.startswith(Modelelemtype.UDPR):
            return "User defined property"
        elif key.startswith(Modelelemtype.PHYU):
            return "Physical unit"
        elif key.startswith(Modelelement.DATY):
            return "Datatype"
        return "Unknown"


# In[ ]:


de_test_trans = Translator('de')
test = ConfluenceContentUtil(navigator, de_test_trans, ['en','fr','de'], data)
others = test.other_languages()
assert ['en', 'fr'] == others, "Expecting en + fr bot got {}".format(others)


# In[ ]:


nl = test.translate_text({'de': '\n'})
nl


# In[ ]:


from jinja2 import Environment, FileSystemLoader, select_autoescape

def create_jinja2_i18n_env(lang:str) -> Environment:
    jinja_env = Environment(
        loader=FileSystemLoader('./templates'),
        autoescape=select_autoescape(['html', 'xml']),
        extensions=["jinja2.ext.i18n"])
    
    translator = translators[lang]
    jinja_env.install_gettext_translations(translator.translator, newstyle=True)    
    util = ConfluenceContentUtil(navigator, translator, config['languages'], data)
    
    jinja_env.globals.update({ 'util': util, 'disclaimer': disclaimer, 'jinja_env': jinja_env, 'i18n': util })
    return jinja_env

i18n_environments = { lang: create_jinja2_i18n_env(lang) for lang in config['languages'] }


# ## Graph rendering

# In[ ]:


jsmodel = JSModel.readfromfile(pfilename=config['source'])


# In[ ]:


def create_graphs(page: dict) -> str:
    if page.get('topic') == 'entities':
        translator = pmodellang=page['translator']
        env = entityenviron.createentienvironment(pentiid=page['key'], pjson=jsmodel, pmodellang=translator.lang())
        content = entityenviron.generate_drawio_content(penviron=env)
        
        name = f"env-{translator.key_lang(page['key'])}"
        graph_filename = f"{name}.drawio"
        
        graph_folder = os.path.join(content_root, page['path'])
        os.makedirs(folder, exist_ok=True)
        
        file = os.path.join(graph_folder, graph_filename)
        pbar.set_description(f"Generating entity grap for {page['id']} [{lang}] to {file}")
        with open(file, 'w') as out:
            out.write(content)
            
        page['entity-graph-name'] = graph_filename
        page['entity-graph-path'] = graph_folder
                                                   
        attachments = page.get('attachments', [])
        diag = { 
            'path': page['path'], 
            'file': graph_filename, 
            'name': name,
            'content-type': 'application/vnd.jgraph.mxfile',
            'labels': ['drawio'],
        }
        attachments.append(diag)
        page['attachments'] = attachments
        page['diagram'] = diag
        return file


# ## Create diagrams
# And the page holding the diagram.

# # TODO Create diagram overview page

# In[ ]:


with tqdm_notebook(total=len(data['diagrams'].keys())*len(translators), dynamic_ncols=True, unit='Diagram') as pbar:
    for lang, translator in translators.items():
        for key, diagram in data['diagrams'].items():
            path = os.path.join(destination_folder, 'diagrams')            
            folder = os.path.join(content_root, path)
            os.makedirs(folder, exist_ok=True)

            filename = f"{key}-{sanitize_filename(diagram['name'])}-{lang}.drawio"
            file = os.path.join(folder, filename)
            
            pbar.set_description(f"Generating diagram {key} '{diagram['name']}' [{lang}] to {file}")
            draw_io_xml = drawiodiagram.create_diagram(key, jsmodel, translator)
            with open(file, 'wb') as out:
                out.write(etree.tostring(draw_io_xml))

            page = navigator.page_by_key(key, lang)
            attachments = page.get('attachments', [])
            diag = { 
                'path': path, 
                'file': filename, 
                'name': f"{key}-{lang}",
                'content-type': 'application/vnd.jgraph.mxfile',
                'labels': ['drawio'],
            }
            attachments.append(diag)
            page['attachments'] = attachments
            page['diagram'] = diag
            
            pbar.update(1)


# # Generate content

# In[ ]:


import re

def write_page_to_disk(page, content: str):
    folder = os.path.join(content_root, page['path'])
    os.makedirs(folder,  exist_ok=True)
    target_file = os.path.join(folder, page['file'])
    with open(target_file, 'w') as out:
        out.write(content)
    page['content'] = content
    return target_file

pages = list(navigator.pages())
with tqdm_notebook(total=len(pages), dynamic_ncols=True, unit='Page') as pbar:
    for page in pages:
        element_config = page['config']
        
        # todo generate graph here
        create_graphs(page)
        
        template_file_name = page.get('template')
        if template_file_name:
            translator = page['translator']
            jinja_env = i18n_environments[translator.language]
            jinja_template = jinja_env.get_template(template_file_name)
            
            rendered = jinja_template.render(page=page, data=data, key=page.get('key'), item=page.get('item'), 
                config=element_config, update_message = 'update')
            
            content = re.sub('<!--.*?->(\n)*', '', rendered) # strip comment lines
            ondisk = write_page_to_disk(page, content)
            page['filename'] = ondisk

        pbar.update(1)


# ## Prepare tasks for simple upload
# ```
# task = {
# 
# 'url': 'rest/api/content/{page_id}',
# 'data': {
#     'title': page['title'],
#     'id': page['id'],
#     'type': page['type'],
#     'version': { 'number': 1, 'minorEdit': 'true', 'message': change_message },
#     'body': {
#         'storage': {
#             'representation': 'storage',
#             'value': confluence_xml_content_from_file
#         }
#     }
#     'metadata': { 'labels': ['my', 'label'] }
# }
# }
# 
# or in case of attachments
# task = { 'url': 'rest/api/content/{page_id}/child/attachment',
# 'data': { 'type': 'attachment',
#                'fileName': name,
#                'contentType': 'application/octet-stream',
#                'metadata': { 'labels': ['my', 'label'] },
#                'minorEdit': 'true',
#                'comment': 'New attachment',
#              }
# 
# ```
# 
# create page with:
# ```
# requests.put(url, data=json.dumps(data), headers={'Content-Type': 'application/json'}, auth=auth, proxies = proxies, verify=verify)
# ```

# ### Structure to collect publishing tasks 
# List of all tasks to be performed to upload content.
# Steps have to be executet in sequence, starting at 0.
# Tasks in the same step can be executed in parallel.

# In[ ]:


steprange = range(0,8)
publish_tasklists = [ {'step': i, 'tasks': [] } for i in steprange ]
publish_tasklists[0]['first'] = 'This is the first step'
publish_tasklists[-1]['last'] = 'This is the last step'
publish_tasklists


# In[ ]:


print('Writing confluence content to disk: {}'.format(destination_folder))
os.makedirs(destination_folder, exist_ok=True)


# ### Tasks
# Currently on level 0-4 there will be tasks
# On the final level (7), there are attachments

# In[ ]:

for level in steprange:
    level_tasklist = publish_tasklists[level]
    level_pages = list(filter(lambda page: page['level'] == level, navigator.pages()))
    print(f"Adding {len(level_pages)} pages on level {level}")
    for page in level_pages:
        
        page_labels = set(page.get('labels', []))
        page_labels.add('generated')
        label_list = list(map(lambda label_name: { 'prefix': 'global', 'name': label_name }, page_labels))
        
        task = { 'url': 'rest/api/content',
                 'data': { 'title': page['title'],
                    'type': 'page',
                    #'id': page.get('id', None),
                    'space': { 'key': '{space_key}' },
                    #'version': { 'number': 1, 'minorEdit': 'true', 'message': 'Publish' },
                    'body': {
                        'storage': {
                            'representation': 'storage',
                            'value': None,
                        }
                    },
                    'metadata': { 'labels': label_list },
                },
                'source': page['id'],
                'sourcefile': str(os.path.join(page['path'], page['file'])),  # content to body.storage.value
        }
        
        parent_page = page.get('parent')
        if parent_page is not None:
            task['parent'] = parent_page['id']

        task['data']['ancestors'] = [ { 'type': 'page', 'id': '{parent_page_id}' } ]
            
        level_tasklist['tasks'].append(task)
    
    # add all attachments to level 7 
    if level == steprange[-1]:
        pages_with_attachments = list(filter(lambda page: page.get('attachments') is not None, navigator.pages()))
        print(f"Adding attachments of {len(attachments)} pages on final level {level}")
        for page in pages_with_attachments:
            for attachment in page['attachments']:
                
                attachment_labels = set(attachment.get('labels', []))
                attachment_labels.add('generated')
                label_list = list(map(lambda label_name: { 'prefix': 'global', 'name': label_name }, list(attachment_labels)))
 
                task = {
                    'url': 'rest/api/content/{page_id}/child/attachment',
                    'data': { 'type': 'attachment',
                            'fileName': attachment['file'],
                            'contentType': attachment['content-type'],
                            'minorEdit': 'true',
                            'comment': 'New attachment',
                            'metadata': { 'labels': label_list },
                            },
                    'source': page['id'],
                    'sourcefile': str(os.path.join(attachment['path'], attachment['file'])),  # content to body.storage.value
                }
                level_tasklist['tasks'].append(task)
            


# In[ ]:


tasklist_file = os.path.join(content_root, 'tasklist.json')
with open(tasklist_file, 'w') as out:
    json.dump(publish_tasklists, out)
    


# In[ ]:


assert False, f"Aborting here since publishing is not possible without confluence configuration"


# # Confluence integration (if in online mode)
# 
# The [Confluence API](https://github.com/atlassian-api/atlassian-python-api) is embedded as a **git submodule** in the 'lib' folder next to this notebook.
# 
# Use `git submodule update --init` to fetch all submodules after a checkout without `--recursive` option.
# 
# If the next cell fails, install confluence-api submodule from the repository root with:
# `git submodule add -f https://github.com/atlassian-api/atlassian-python-api.git notebooks/contentfactory/lib/atlassian-python-api`

# In[ ]:


# this is the parameter cell. see cell tags. used to overwrite things with tests infrastructure
if confluence is not None:
    confluence_username = config['confluence']['username']
    confluence_password = config['confluence']['password']
    cooldown = config['confluence'].get('cooldown', 0.0)


# In[ ]:


if confluence is not None:
    library = 'lib/atlassian-python-api'
    sys.path.insert(0, os.path.abspath(library))
    
    from atlassian import Confluence
    from atlassian.confluence import ApiError
    
    confluence = Confluence(url=config['confluence']['apiurl'], username=confluence_username, password=confluence_password, cloud=True)
    root_page_id = confluence.get_page_id(space_key, config['confluence']['rootpage'])
    assert root_page_id, "Cannot find documentation root page '{}' in space {} on server {}".format(config['confluence']['rootpage'], space_key, config['confluence']['apiurl'])
    root_page = confluence.get_page_by_id(root_page_id, expand='body.storage,ancestors,version,history')
    print(f"{config['confluence']['apiurl']}{root_page['_links']['tinyui']} = id {root_page_id}")


# In[ ]:


from requests.exceptions import HTTPError
from colorama import Fore, Style
from pprint import pformat

def print_http_error_details(message: str = None, page: dict = None, exception: HTTPError = None):
    result = exception.response.raw
    full_message = Fore.RED + message + '\n' +         Fore.MAGENTA + str(exception.response.raw) +         Fore.YELLOW + str(vars(exception)) + '\n' +         str(vars(exception.response)) + '\n' +         str(vars(result)) +         Style.RESET_ALL
    if page:
        full_message += "Page {title} [{key}]".format(title=page.get('title'), key=page.get('key'))
    log.exception(full_message)
    return full_message


# In[ ]:


from requests import Response
from io import BytesIO
r = Response()
r.raw = BytesIO(b'{}')
e = HTTPError(response=r)
print_http_error_details('Test', { }, e)


# ## Persist page map before upload
# The source.json will contain all information prepared before upload starts.

# In[ ]:


pagelist_copy = copy.deepcopy(navigator.page_map)
for page_key in pagelist_copy:
    page = pagelist_copy[page_key]
    page.pop('translator', None)
    page.pop('_publishable-stamp', None)
    page['labels'] = list(page.get('labels', []))
    page.pop('config', None)

safe = os.path.join(os.path.split(destination_folder)[0], 'source.json')
with open(safe, 'w') as output:
    json.dump(pagelist_copy, output, indent=2, sort_keys=False)

print("Persisted state to {}".format(safe))


# In[ ]:


assert False, f"Stopping here"


# ## Cautious mode
# Scan the space before publishing to prevent overwrite or move of pages

# In[ ]:


archive_folder = os.path.join(content_root, 'archive')
os.makedirs(archive_folder, exist_ok=True)

def preserve_page(page_id: str, page: dict):
    page['confluence-page-id'] = page_id
    try:
        content = confluence.get_page_by_id(page_id, expand='body.storage,ancestors,version,history,metadata.labels,children.attachment,children.comment,history.lastUpdated')
        page['previous'] = content
        ancestors = content.get('ancestors')
        page['version'] = content['version']['number']
        page['ancestors'] = ancestors
        current_content = content['body']['storage']['value']
        page['previous-content'] = current_content
        ancestor_ids = set(map(lambda a: a['id'], ancestors))
        ancestor_titles = list(map(lambda a: a['title'], ancestors))
        if not root_page_id in ancestor_ids:
            log.warning("Will move page with title {title} ID={page_id} from hierarchy:\n{ancestors}".format(title=page['title'], page_id=page_id, ancestors='/'.join(ancestor_titles)))
        with open(os.path.join(archive_folder, page['translator'].key_lang(page['key']) + '.chtml'), 'w') as out:
            out.write(current_content)
    except HTTPError as e:
        print_http_error_details("Cannot preserve current content", page, e)
        
def scan_page(page: dict):
    global space_key
    existing_page = copy.deepcopy(page)
    title = existing_page['title']
    try:
        page_id = confluence.get_page_id(space_key, title)
        if not page.get('preserve', False):
            log.warning("Page with title {title} exists. ID={id}".format(title=title, id=page_id)) 
        preserve_page(page_id, existing_page)
        return existing_page
    except ApiError as e:
        # It is perfectly safe, that a page does not exist
        pass


# In[ ]:


import random

if confluence is not None:
    all_pages = list(filter(lambda p: p['topic'] == 'entities', navigator.pages()))
    random_index = random.randint(0, len(all_pages) - 1)
    specimen = all_pages[random_index]
    x = scan_page(specimen)
    if x:
        print("Element {0} at index {1}".format(x.get('title'), random_index))


# In[ ]:


if x: 
    x.get('content')


# In[ ]:


if x: 
    x.get('previous-content')


# In[ ]:


existing_pages = []

if confluence is not None and confluence.get('cautious', True):
    pages = list(navigator.pages())
    print('Scanning {} pages in confluence space {}'.format(len(pages), space_key))
    with tqdm_notebook(total=len(pages), dynamic_ncols=True, unit='Page', smoothing=0.1) as pbar:
        for page in pages:
            existing_page = scan_page(page)
            if existing_page:
                existing_pages.append(existing_page)
            pbar.update(1)
        
    print('Found {existing} existing pages of {total}'.format(existing=len(existing_pages), total=len(navigator.pages())))


# In[ ]:


def extract_labels(page: dict) -> set:
    content = page['previous']
    labels = content['metadata']['labels']['results']
    result = set(map(lambda l: l['name'], labels))
    return result


# In[ ]:


blocking_pages = []
safe_labels = set(['generated', 'manual'])
for page in existing_pages:
    if len(safe_labels.intersection(extract_labels(page))) == 0:
        blocking_pages.append(page)


# In[ ]:


def warn_blocking():
    if len(blocking_pages) > 0:
        return HTML('''<p><span style="font-family: Impact; font-size:48px">
Beware! There are <span style="color: red">{count}
</span> pages blocking your upload</span><br/>'''.format(count=len(blocking_pages)))
warn_blocking()


# In[ ]:


list(map(lambda page: { 'title': page['title'], 'key': page['key'], 'id': page.get('confluence-page-id') ,
         'url': (page['previous']['_links']['base'] + page['previous']['_links']['webui']) }, blocking_pages))


# In[ ]:


# Abort execution on blocking pages
assert 0 == len(blocking_pages), "Found {} pages blocking the publishing. If you continue, these pages will be overwritten by the publisher!".format(len(existing_pages))


# In[ ]:


import time

def upload_attachments(page: dict, confluence):
    svg_file_name = page.get('entity-graph-name')
    if svg_file_name:
        sourcefile = page.get('entity-graph-path')
        with open(sourcefile, 'rb') as source:
            content = source.read()
            
        try:
            result = confluence.attach_content(content, name=svg_file_name, content_type='image/svg+xml', 
                                               page_id=page['confluence-page-id'], space=space_key, comment="Entity-Graph for {}".format(page.get('key')))
            #print('Attachment {}'.format(result))
            page['entity-graph-attachment_result'] = result
            time.sleep(cooldown)
            return result
        except HTTPError as e:
            print_http_error_details('Failed to upload attachment ' + svg_file_name, page, e)


# In[ ]:


test_page = { 'entity-graph-name': '0593.svg', 'entity-graph-path': 'testdata/0593.svg', 'key': 'tests' }
test_page['confluence-page-id'] = root_page_id
upload_attachments(test_page, confluence)


# In[ ]:


from datetime import datetime

def upload(page: dict, content: str):
    parent = page.get('parent')
    if not parent:
        parent_page_id = root_page_id
    else:
        parent_page_id = parent.get('confluence-page-id')
        
    page_id = None
    title = page['title']
    try:
        page_id = confluence.get_page_id(space_key, title)
    except ApiError as e:
        pass
    
    if page_id is None:
        log.info("Stubbing page '{title}'".format(title=title))
        # Stubbing allowed for manual documentation
        create_result = confluence.create_page(space_key, title=title, parent_id=parent_page_id, body=content)
        page_id = create_result['id']
        stub_labels = set(page.get('labels'))
        stub_labels.add('stub')
        for label in stub_labels:
            confluence.set_page_label(page_id, label)
            
    else:
        if not page.get('previous'):
            log.warning('Page {0} exists. But has not been looked up'.format(title))
            scan_page(page)
        
    assert page_id, "Missing page id for page '{title}'".format(title=page.get('title'))
    page['confluence-page-id'] = page_id
    
    if not page.get('preserve', False):
        try:
            #result = confluence.update_page(page_id, title, body=content, parent_id=parent_page_id, minor_edit=True, representation="storage", version_comment='tests')
            """Rest call bypassing the convenience function: this allows to update the page content and metadata (labels) in one request"""
            current_version = page.get('version', 1) # For stubbed pages
            next_version = current_version + 1
            rest_data = { 'id': page_id, 'type': 'page', 'title': title, 'body': confluence._create_body(content, 'storage') }
            
            rest_data['ancestors'] = [{ 'type': 'page', 'id': parent_page_id }]
            rest_data['version'] = { 'number': next_version, 'minorEdit': True, 'message': 'Update xyz' }

            page_labels = set(page.get('labels', []))
            page_labels.add('generated')
            label_list = list(map(lambda label_name: { 'prefix': 'global', 'name': label_name }, page_labels))
            rest_data["metadata"] = { 'labels': label_list }
            response = confluence.put('rest/api/content/{0}'.format(page_id), data=rest_data)
            log.debug("Updated page {0}".format(page_id))
            page['confluence_result'] = response
            page['version'] = next_version
            page['_publishable-stamp'] = datetime.now()
        except HTTPError as error:
            print_http_error_details('Failed to update content', page, error)
            page['update_fail_count'] = page.get('update_fail_count', 0) + 1
    else:
        log.debug(f"Skipping page {page['title']} marked as 'preserve'")
            
    upload_attachments(page, confluence)
    page['confluence-published'] = True
    
    return page


# ## Upload helpers

# In[ ]:


def _publishable(page):
    if page.get('skip', False):
        log.info('Skipping page {}'.format(page.get('key')))
        return True
    result = None
    content_file = page.get('file')
    if content_file:
        try:
            with open(content_file, 'r') as content:
                result = upload(page, str(content.read()))
        except HTTPError as httpe:
            print_http_error_details("Cannot _publishable", page, httpe)
        except Exception as e:
            log.exception("Cannot _publishable page {0}".format(page['title']))
    else:
        log.warning('No content for page {0} [{1}]'.format(page.get('title'), page.get('key')))
        result = upload(page, page.get('content', 'absent-content-placeholder'))
        
    if result:
        time.sleep(cooldown)
    return result


# # Prepublishing

# ## Publish index pages (Entities, Databases, Documents, Domains, ...) in sequence as defined in the configuration

# In[ ]:


level0_pages = list(filter(lambda page: page['level'] == 0, navigator.pages()))
print('Level 0 titles: {}'.format(list(map(lambda p: p.get('title'), level0_pages))))


# In[ ]:


for p in level0_pages:
    print("Publishing index page {0}".format(p.get('title')))
    result = _publishable(p)


# ## Upload a subset

# In[ ]:


def path_to_page(navigator: Navigator, key: str, lang: str) -> list:
    """Returns a page including parent pages"""
    node = navigator.page_4_language(key, lang)
    if not node:
        log.warning("Cannot find node " + key)
    result = []
    while node:
        result.insert(0, node)
        node = node.get('parent')
    return result

def path_to_page_title(navigator: Navigator, title: str) -> list:
    """Returns a page including parent pages"""
    node = navigator.page_uniqueness_map.get(title)
    if not node:
        log.warning("Cannot find node " + title)
    result = []
    while node:
        result.insert(0, node)
        node = node.get('parent')
        
    return result


# In[ ]:


level_pages = []
level = 6
while len(level_pages) == 0:
    level_pages = list(filter(lambda page: page['level'] == level, navigator.pages()))
    level -= 1

specimen = level_pages[-1]
durchstich = path_to_page_title(navigator, specimen['title'])


# In[ ]:


chain = path_to_page(navigator, specimen['key'], 'de')
len(chain)


# ## Publish one sample hierarchy 

# In[ ]:


for p in durchstich:
    print("Publishing {0} [{1}] Level:{2} Version:{3}".format(p['title'], p['key'], p['level'], p['previous']['version']['number'] if p.get('previous') else '??'))
    _publishable(p)


# ## Move pages to correct position if needed

# In[ ]:


#move = list(filter(lambda page: 'modelmodel' in page['title'], navigator.pages()))

move = list(navigator.pages())
len(move)


# In[ ]:


def fixmove(page):
    page_id = page.get('confluence-page-id')
    if page_id:
        content = confluence.get_page_by_id(page_id, expand='ancestors')
        ancestors = content.get('ancestors')
        ancestor_ids = set(map(lambda a: a['id'], ancestors))
        ancestor_titles = list(map(lambda a: a['title'], ancestors))
        parent = page.get('parent')
        if parent and not parent.get('confluence-page-id') in ancestor_ids:
            log.warning("Need to move {0} from {1} to {2}".format(page['title'], ancestors, page['parent'].get('confluence-page-id')))
            return page

movelist = []
for page in move:
    p = fixmove(page)
    if p:
        movelist.append(p)


# In[ ]:


len(movelist)


# In[ ]:


for p in movelist:
    result = confluence.move_page(space_key, p['confluence-page-id'], target_id=p['parent']['confluence-page-id'])
    print("Moved {}: {}".format(p['title'],result))


# In[ ]:


fix = list(filter(lambda page: page['title'] == 'modelmodel', navigator.pages()))
len(fix)


# In[ ]:


if len(fix) > 0:
    modelmodel = fix[0]
    modelmodel['skip'] = False
    print(modelmodel.get('file'))
    _publishable(modelmodel)


# ## Upload all parallel

# In[ ]:


from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

def upload_parallel(pages: list, threads: int = 8):
    summary = []

    for level in range(0,6):
        level_pages = list(filter(lambda page: page['level'] == level and not page.get('confluence-published', False), navigator.pages()))
        print('Level {} has {} pages'.format(level, len(level_pages)))
        with tqdm_notebook(total=len(level_pages), dynamic_ncols=True, unit='Page', smoothing=0.1) as pbar:

            def parallel_publish_stub(page):
                # Skip if already published
                if page.get('confluence-published'):
                    pbar.update(1)
                    return None
                pbar.set_description('Uploading {title} [{key}]'.format(title=page.get('title'), key=page.get('key')))
                p = _publishable(page)
                pbar.update(1)
                return p

            with ThreadPoolExecutor(max_workers=threads) as executor:
                summary.extend(executor.map(parallel_publish_stub, level_pages))
            
    return summary


# In[ ]:


page_selection = navigator.pages()
print("Uploading {} pages to {} with cooldown of {}s after each page".format(len(page_selection), conf_conf['apiurl'], cooldown))


# In[ ]:


pages_processed = upload_parallel(page_selection)
result = list(filter(None, pages_processed))


# In[ ]:


len(result)


# # Create backup archive

# ## Build code distribution bundle based on the loaded Python modules

# In[ ]:


cwd = Path('.')
project_base = Path(*cwd.absolute().parts[0:-2])
project_base


# In[ ]:


all_modules = list(sys.modules.values())
with open('all_modules_loaded.txt', 'wt') as module_list_file:
    for module in all_modules:
        module_list_file.write(vars(module).get('__name__', ''))
        module_list_file.write('\n')


# In[ ]:


for module in all_modules:
    __import__(module.__name__)


# In[ ]:


from pathlib import PurePath

def local_file(module: dict) -> bool:
    v = vars(module)
    file = v.get('__file__')
    if file:
        try:
            return PurePath(file).relative_to(project_base)
        except ValueError:
            pass
        
custom = list(filter(local_file, sys.modules.values()))
print("Using {0} python files".format(len(custom)))


# In[ ]:


custom_module_files = map(lambda f: str(f.__file__), custom)


# In[ ]:


dependencies = set(custom_module_files)
len(dependencies)


# In[ ]:


vars(sys.modules['IM_DB.parameters'])


# In[ ]:


vars(sys.modules['concurrent.futures.process'])


# In[ ]:


backup_time = datetime.now().strftime("%Y-%m-%d")
backup_file = "_publishable-" + data['model']['name'] + '-' + backup_time + '.zip'
backup_file


# In[ ]:


pagelist_copy = copy.deepcopy(navigator.page_map)
for page_key in pagelist_copy:
    page = pagelist_copy[page_key]
    page.pop('translator', None)
    stamp = page.get('_publishable-stamp')
    if stamp:
        page['_publishable-stamp'] = stamp.strftime("%Y-%m-%d %H:%M:%S")
    labels = page.get('labels')
    if labels:
        page['labels'] = list(labels)

ssot = 'pages.json'
with open(ssot, 'w') as summary:
    json.dump(pagelist_copy, summary)


# In[ ]:


from zipfile import ZipFile

with ZipFile(backup_file, 'w') as zipfile:
    zipfile.write(ssot)
    for dependency in dependencies:
        zipfile.write(dependency)
    print("Wrote {0}".format(backup_file))


# # Publishing completed

# In[ ]:


assert False, "Regular publishing done :-)"


# In[ ]:


# Move pages
wrong_root_pages = list(filter(lambda p: 'TABL' in p['key'] , navigator.page_map.values()))
print(len(wrong_root_pages))


# In[ ]:


wrong_root_page = list(filter(lambda p: 'modelmodel' == p['title'] , navigator.page_map.values()))
print(len(wrong_root_page))


# In[ ]:


wrong_root = wrong_root_page[0]
print(str(wrong_root)) 
try:
    wrong_root.pop('skip')
except KeyError:
    pass
_publishable(wrong_root)


# In[ ]:


for page in wrong_root_pages:
    confluence.move_page("")


# In[ ]:


rest_data = {}
try:
    # http://localhost:8090/rest/api/accessmode
    response = confluence.get('rest/api/accessmode'.format(space_key), data=rest_data)
    print("Response 1: {}".format(response))
    #GET /wiki/rest/api/space/{spaceKey}/watch
    response = confluence.get('rest/api/space/{0}/watch'.format(space_key), data=rest_data)
except HTTPError as e:
    print(print_http_error_details('Cannot get space watchers', None, e))


# In[ ]:


rest_data = {}
try:
    # GET /wiki/rest/api/content/{id}/restriction/byOperation
    response = confluence.get('rest/api/content/{root_page_id}/restriction/byOperation'.format(root_page_id=root_page_id), data=rest_data)
    print(response)
except HTTPError as e:
    print(print_http_error_details('Cannot get space watchers', None, e))


# In[ ]:


try:
    # GET /wiki/rest/api/space/{spaceKey}/watch
    response = confluence.get('rest/api/space/{space_key}/watch'.format(space_key=space_key))
    print(response)
except HTTPError as e:
    print(print_http_error_details('Cannot get restrictions', None, e))


# In[ ]:


rest_data = {}
try:
    # GET /wiki/rest/api/content/{id}/restriction
    # GET /wiki/rest/api/content/{id}/restriction/byOperation
    response = confluence.get('rest/api/content/{root_page_id}/restriction'.format(root_page_id=root_page_id), data=rest_data)
    print(response)
except HTTPError as e:
    print(print_http_error_details('Cannot get restrictions', None, e))


# In[ ]:



# POST /wiki/rest/api/space/{spaceKey}/permission
try:
    # GET /wiki/rest/api/content/{id}/restriction
    # GET /wiki/rest/api/content/{id}/restriction/byOperation
    response = confluence.get('rest/api/content/{root_page_id}/restriction'.format(root_page_id=root_page_id), data=rest_data)
    print(response)
except HTTPError as e:
    print(print_http_error_details('Cannot get restrictions', None, e))


# In[ ]:





# In[ ]:




