import os
import re
import json
from pathlib import Path


class CatenaxFiles:

    @staticmethod
    def findfiles(basepath,elementregexp)->Path:
        retval = []
        try:
            with os.scandir(basepath) as localdirec:
                for locdirec in localdirec:
                    if not locdirec.is_file() and re.match(elementregexp,locdirec.name):
                        retval.append(CatenaxFiles.findfile(basepath=basepath / locdirec.name))
        except Exception as exp:
            raise exp
        return retval

    @staticmethod
    def findfile(basepath, version=None)->Path:
        retval = None
        try:
            with os.scandir(basepath) as localdirec:
                locversion = version if version is not None \
                    else max(
                    [locdirec.name for locdirec in localdirec
                     if (not locdirec.is_file() and
                         re.match(r"^\d+\.\d+\.\d+$", locdirec.name))])
            try:
                realpath=basepath / (locversion + "/gen")
                with os.scandir(realpath) as myversion:
                    for model in myversion:
                        if model.name.endswith("-schema.json"):
                            retval=realpath/model.name
            except Exception as exp:
                pass
        except Exception as exp:
            pass
        return retval

    @staticmethod
    def read1file(filepath:Path)->dict():
        try:
            with open(filepath) as infile:
                myjson = json.load(fp=infile)
        except Exception as exp:
            raise exp
        return myjson