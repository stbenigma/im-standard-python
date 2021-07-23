import xml.etree.ElementTree as et
from IM_DB import logmessages
from pathlib import Path

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
