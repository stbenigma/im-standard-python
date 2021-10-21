import xml.etree.ElementTree as et
from IM_DB import logmessages,nvl
from pathlib import Path
import re

"""EA-Specific"""
def findColumn(set, name):
    try:
        return findField(set.find("Column[@name='{}']".format(name)),'value')
    except Exception as ex:
        raise ex

def findRefGuid(set, name):
    try:
        return findField(set.find("Extension"),name)
    except Exception as ex:
        raise ex
"""================="""

def findText(set, name):
    try:
        return set.find(name).text
    except Exception as ex:
        return None
# findText

def findField(set, name):
    try:
        return set.get(name)
    except Exception as ex:
        return None
# findField


def searchfile(pfilename, pdefaultdirec):
    my_file = Path(pfilename)
    if my_file.is_file():
        infile = pfilename
    else:
        my_file = Path(pdefaultdirec + pfilename)
        if my_file.is_file():
            infile = pdefaultdirec + pfilename
        else:
            raise Exception("File {} not found".format(pfilename))
    # fi
    return infile

def parseXML(pfilename):
    try:
        tree = et.parse(pfilename)
    except Exception as err:
        logmessages.writelog("File ({}) could not be handled".format(pfilename))
        print (pfilename)
        raise
    #try
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
        props = re.finditer(r'\[(([A-Z]{2})[^[]+)\[\n([^]]*)\][A-Z]{2}[^]]+\]', ptext, re.DOTALL)
        # liefert group1 name,group2 sprache, group3 text
        for prop in props:
            retval[prop.group(2).lower()] = {prop.group(1): prop.group(3)}
        #for
    #fi
    return retval

def separateExamples(pstr:str):
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
                            +'Beispiel'
                            +'|Example'
                            +'|Exemple'
                            +'|Ejemplo'
                            +'|Esempi'
                            +')[eso]?\s*:)\s*\n([\w\W]*)'
                            , pstr,re.MULTILINE)
        if text is None:
            commentstruct.append(pstr)
        else:
            commentstruct.append(text.group(2))
            commentstruct.extend(text.group(4).split("\n"))
            commentstruct = list(filter(lambda a: a != "", commentstruct))
            #print(text.group(4).split("\n"))
            #for i in range(text.lastindex+1): print (i,"=>|",text.group(i),"|")
        #fi
    #fi
    descr = nvl(commentstruct[0]).strip()
    examples = [s.strip() for s in commentstruct[1:]]

    return (descr,examples)