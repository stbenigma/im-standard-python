import argparse
import logging
import os.path
import re
import sys
from pathlib import Path
import xml.etree.ElementTree as et


from LOAD_MODELS.LOAD_INFRA import handleXML
from LOAD_MODELS.LOAD_ODM import ODMParameter
from SSOT_db.IM_JSON import JSModel
from SSOT_infra import transl, nvl

""" 
    writes mapping back into by creating new mapping ODM-XML-files
"""


# def getmodellang(pmodelfile):
#     dmdxml = handleXML.parseXML(pmodelfile)
#     root = dmdxml.getroot()
#     comment = root.find('comment').text
#     lang = re.search('currentLang=(\w+)', comment)
#     if lang:
#         return lang.group(1)
#     else:
#         return lang
#
#
# def getelembyodmguid(pjsmodel: JSModel, pelemtype, pguid):
#     elems = pjsmodel.getelements(pelemtype=pelemtype)
#     for key, elem in elems.items():
#         odmref = elem.get('sourceref').get('ODM')
#         if odmref and (odmref[0] == pguid):
#             return key, elem
#     return None, None


# def writetranslations(pIMdirec, pmodelname, pjsmodel: JSModel, pdryrun=False):
#     """ make sure the ODM has the same baselanguage as is defined in the jsonmodel
#         replace in ODM-files all translations (this means without the values of the base language)
#         we treat all translated elements as defined in  Languagetext.ODMtranslAttributes
#         pdryrun = True, do not write files back. only count changes
#         consider dryrun as verbose
#     """
#     modelmasterfile = pIMdirec / (pmodelname + ODMParameter.imextension())
#     defaultlang = getmodellang(modelmasterfile).lower()
#     model = pjsmodel.getelements(JSModel.ELEMTYPE_PROJ)
#     jsonlang = model.get('language')
#     if defaultlang != jsonlang:
#         logging.error(f"Model {pmodelname}, language in ODM ({defaultlang}) and jsonfile ({jsonlang}) differ")
#         print(f"Model {pmodelname}, language in ODM {defaultlang} and jsonfile {jsonlang} differ")
#         exit(1)
#
#     langs = [key for key, val in pjsmodel.getelements('languages').items() if not val['modellanguage']]
#     odmparam = ODMParameter(modelname=pmodelname, imdirec=pIMdirec, defaultlang=jsonlang, )
#     cnt = {'enti': 0, 'doma': 0, 'rela': 0, 'attr': 0}
#     handleXML.dosegfiles(pdirec=odmparam.entitydirec(),
#                          phandlefunc=do1entity, cnt=cnt, jsstruct=pjsmodel, langs=langs, dryrun=pdryrun)
#     handleXML.dosegfiles(pdirec=odmparam.relationdirec(),
#                          phandlefunc=do1relation, cnt=cnt, jsstruct=pjsmodel, langs=langs, dryrun=pdryrun)
#     """domains are not yet translated in ODM """
#     if False:
#         handleXML.doxmlfiles(pdirec=odmparam.domainsdirec(), ppattern=r'.*\.xml',
#                              phandlefunc=do1domain, cnt=cnt, jsstruct=pjsmodel, langs=langs, dryrun=pdryrun)
#         handleXML.doxmlfiles(pdirec=odmparam.defdomainsfilpath().parent, ppattern=odmparam.defdomainsfilname(),
#                              phandlefunc=do1domain, cnt=cnt, jsstruct=pjsmodel, langs=langs, dryrun=pdryrun)
#     return cnt

def do1column(pjson:JSModel,pcoluid:str,pcnt:dict):
    pcnt["columns"] += 1
    return

def do1table(pjson:JSModel,ptabid:str,pcnt:dict):
    pcnt["tables"] += 1
    return

def savemapfile(pIMdirec:Path,pdatm:dict,pxml:et.Element):
    return
    datmfile=""
    #remove existing files
    outfile = open(datmfile, "w")
    outfile.write(handleXML.prettify(pxml))
    outfile.close()
    return

def do1datamodel(pIMdirec:Path,pjson:JSModel,pdatmid:str,pdatm:dict)->bool:
    if len(pdatm["tables+"]) ==0:
        logging.info(f"""Datamodel '{pdatm["name"]}' has no tables. Not handled.""")
        return False

    #delete mapping files, create new mappingfile for datamodel
    xml = et.Element("RMExtendedMap", {"class": "oracle.dbtools.crest.model.xtdmapping.RMExtendedMap"})
    mappings = et.SubElement(xml, "mappings",
                                {"itemClass": "oracle.dbtools.crest.model.xtdmapping.ContainerMapping"})

    cnt={"tables":0,"columns":0}
    for tabid in pdatm["tables+"]:
        do1table(pjson=pjson,ptabid=tabid,pcnt=cnt)

    savemapfile(pIMdirec=pIMdirec,pdatm=pdatm,pxml=xml)

    logging.info(f"""datamodel '{pdatm["name"]}': mappings (tables:{str(cnt["tables"])}, columns:{str(cnt["columns"])} written to ODM""")
    return True

def writemappings(pIMdirec:Path, pjson:JSModel, pdatms:list):
    datms = {key:val for key, val in pjson.getelements("datamodels").items() if ((pdatms is None) or (val["name"] in pdatms))}

    writtenback = []

    if len(datms) ==0:
        logging.info(f"No datamodels found to process.")
        return writtenback

    for datmid,datm in datms.items():
        written = do1datamodel(pIMdirec=pIMdirec,pjson=pjson,pdatmid=datmid,pdatm=datm)
        if written:
            writtenback.append(datm)

    return writtenback


def main(sysargs):
    argp = argparse.ArgumentParser(description='Write back mappings for datamodels into ODM-xmls')
    argp.add_argument('--verbose', '-v', action='store_true',
                      help="Verbose mode")
    argp.add_argument('--destination', '-d', dest="destination",
                      help=f"Path of ODM-model to change.  Default: <path of jsonffile>/../IM ")
    argp.add_argument('--datamodels', '-i', dest="datamodels",
                      help=f"List of datamodels to be written back ('datm1,datm2').  Default: all datamodels found in jsonfile")
    argp.add_argument('jsonfile', nargs=1,
                      help=f"jsonfile to be used.")
    argp.add_argument('--logfile', '-log', dest='logfile',
                      help=f"Filepath for logfile.  Default: <path of jsonffile>/../<jsonfilename>.log")

    arguments = argp.parse_args(sysargs[1:])

    jsonfile = arguments.jsonfile[0]
    assert os.path.isfile(jsonfile), f"Json file not found '{jsonfile}'"

    imdirec = arguments.destination
    if nvl(imdirec) == '':
        imdirec = Path(jsonfile).parent.parent / 'IM'
    assert os.path.isdir(imdirec), f"Modeldirectory not found: '{imdirec}'"

    logfile = arguments.logfile
    if logfile is None:
        logfile = Path(jsonfile).parent / (Path(jsonfile).stem + '.log')
    else:
        logfile = Path(logfile)

    assert Path.is_dir(logfile.parent), f"Path for logfile does not exists: '{logfile.parent}'"

    logging_level = logging.DEBUG if arguments.verbose else logging.INFO
    # logging.basicConfig(filename=logfile, level=logging.INFO)
    console_log_handler = logging.StreamHandler()
    console_log_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    console_log_handler.setLevel(logging.WARNING)
    logging.getLogger().addHandler(console_log_handler)
    fh = logging.FileHandler(logfile)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logging.getLogger().setLevel(logging_level)
    logging.getLogger().addHandler(fh)

    try:
        myjson = JSModel.readfromfile(jsonfile)
    except Exception as e:
        logging.error(e)
        exit(1)

    datamodels= writemappings(pIMdirec=imdirec,
                        pjson=myjson, pdatms = arguments.datamodels
                        )
    if len(datamodels)==0:
        logging.info(
            "No mappings recreated")
    else:
        logging.info(
            "Mappings recreated for\n" + '\n'.join(datamodels))
    return

if __name__ == '__main__':
    main(sys.argv)
