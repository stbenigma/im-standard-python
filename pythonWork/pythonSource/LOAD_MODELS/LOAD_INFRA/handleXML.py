import xml.etree.ElementTree as et
from xml.dom import minidom

from SSOT_infra import nvl
from pathlib import Path
import os
import logging
import re
from typing import List
from LOAD_MODELS.LOAD_ODM import ODMParameter

"""EA-Specific"""
def findColumn(xmlelem, name):
    try:
        return findField(xmlelem.find(f"Column[@name='{name}']"), 'value')
    except Exception as ex:
        raise ex


def findRefGuid(xmlelem, name):
    """looks for field in a xml-tag "Extension
       in EA_native xml-files
    """
    try:
        return findField(xmlelem.find("Extension"), name)
    except Exception as ex:
        raise ex

"""================="""

def findText(xmlelem, name):
    try:
        return xmlelem.find(name).text
    except Exception as ex:
        return None


def findField(xmlelem, name):
    try:
        return xmlelem.get(name)
    except Exception as ex:
        return None

def findorcreateelement(xmlelem,elemname,**attribs):
    """ find the element name
        if not  found, create it, with arguments in attribs
        return the found or created element
        """
    elem = xmlelem.find(elemname)
    if elem is None:
        elem = createsubelement(xmlelem,elemname,**attribs)
    return elem

def createsubelement(xmlelem,elemname,**attribs):
    """ create a subelement , with arguments in attribs
        return the found or created element
        """
    if len(attribs)==0:
        elem = et.SubElement(xmlelem, elemname)
    else:
        elem = et.SubElement(xmlelem, elemname,attrib=attribs)
    return elem

def searchfile(pfilename, pdefaultdirec):
    my_file = Path(pfilename)
    if my_file.is_file():
        infile = pfilename
    else:
        my_file = Path(pdefaultdirec + pfilename)
        if my_file.is_file():
            infile = os.path.join (pdefaultdirec, pfilename)
        else:
            raise Exception("File {} not found".format(pfilename))
    # fi
    return infile


def parseXML(pfilename):
    try:
        tree = et.parse(pfilename)
    except Exception as err:
        logging.error(f"XML-File ({pfilename}) could not be parsed")
        print(f"********XML-File ({pfilename}) could not be parsed")
        raise
    # try
    return tree


def extractlngcomments(ptext):
    """extracts text and language comments (XX_ENTI_COMMENT, XX_ATTR_COMMENT...)
       from a multilinetext (usually a note)
        text
        [DE_ENTI_COMMENT[
            text
        ]DE_ENTI_COMMENT]
        [EN_ENTI_COMMENT[
        ]EN_ENTI_COMMENT]"""
    retval = dict()
    if ptext is not None:
        props = re.finditer(r'\[(([A-Z]{2})_[A-Z_]+)\[(.*?)(?=\]\1\])', ptext, re.DOTALL)

        # liefert group1 name,group2 sprache, group3 text
        for prop in props:
            retval[prop.group(2).lower()] = {prop.group(1).strip("\n"): prop.group(3).strip("\n")}
        # for
    # fi
    return retval


def separateExamples(pstr: str):
    """look for Examples in a text:
        Beispiel(e):, Example(s):, Ejemplo(s):, Esempi(o):...
        ex1
        ex2
        ...
        returns a list of texts
        0-> original text without trailing examples
        1..2 examples, each on a line
    """
    commentstruct = []
    if pstr is None:
        commentstruct.append(None)
    else:
        text = re.search('(([\w\W]*)('
                         + 'Beispiel'
                         + '|Example'
                         + '|Exemple'
                         + '|Ejemplo'
                         + '|Esempi'
                         + ')[eso]?\s*:)\s*\n([\w\W]*)'
                         , pstr, re.MULTILINE)
        if text is None:
            commentstruct.append(pstr)
        else:
            commentstruct.append(text.group(2))
            commentstruct.extend(text.group(4).split("\n"))
            commentstruct = list(filter(lambda a: a != "", commentstruct))
            # print(text.group(4).split("\n"))
            # for i in range(text.lastindex+1): print (i,"=>|",text.group(i),"|")
        # fi
    # fi
    descr = nvl(commentstruct[0]).strip()
    examples = [s.strip() for s in commentstruct[1:]]

    return (descr,examples)

def stable_file_list(folder: str,removehidden=True) -> List[str]:
    assert os.path.isdir(folder), f"Path '{folder}' is not a valid folder"
    result = list(os.listdir(folder))
    if removehidden:
        for f in result:
            if f.startswith('.'):
                result.remove(f)

    result.sort()
    return result


def doxmlfiles(pdirec, phandlefunc, ppattern=r".*", pmandatorydirec=True,**kwargs):
    """
        looks in pdirec for the non hidden files matching the pattern
        applies phandlecunt(filespec) for each of them
        if directory does not exist, there is a warning logged, wi pmandatorydirec is True
    """
    try:
        listdir = stable_file_list(pdirec)
    except Exception as ex:
        if pmandatorydirec:
            logging.warning(f'dosxmlfiles: directory "{pdirec}" not found.')
        return
    # try
    for file in listdir:
        if re.match(ppattern, file):
            filename=os.path.join(pdirec, file)
            XMLtree = parseXML(pfilename=filename)
            phandlefunc(filename,XMLtree,**kwargs)
        # fi
    # for
    return


def dosegfiles(pdirec, phandlefunc,
               ppattern=r'{}.xml'.format(ODMParameter.GUIDPATTERN),
               pmandatoryfile=True,**kwargs):
    """
        ODM-specific
        searches in pdirec for subdirectories seg_n
        calls doxmlfiles for each directory found
            which calls alle
        issues a warning, is pdirec is not found an pmandatory is True
    """
    try:
        listdir = stable_file_list(pdirec)
    except Exception as ex:
        if pmandatoryfile:
            logging.warning(f'dosSEGfiles: directory "{pdirec}" not found.')
        return
    # try
    for el in listdir:
        if re.match('seg_\d+', el):
            doxmlfiles(pdirec=os.path.join(pdirec, el),
                       phandlefunc=phandlefunc,
                       ppattern=ppattern,
                       **kwargs)
    # for
    return

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = et.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
