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
# def getelembyodmguid(pjson: JSModel, pelemtype, pguid):
#     elems = pjson.getelements(pelemtype=pelemtype)
#     for key, elem in elems.items():
#         odmref = elem.get('sourceref').get('ODM')
#         if odmref and (odmref[0] == pguid):
#             return key, elem
#     return None, None


# def writetranslations(pIMdirec, pmodelname, pjson: JSModel, pdryrun=False):
#     """ make sure the ODM has the same baselanguage as is defined in the jsonmodel
#         replace in ODM-files all translations (this means without the values of the base language)
#         we treat all translated elements as defined in  Languagetext.ODMtranslAttributes
#         pdryrun = True, do not write files back. only count changes
#         consider dryrun as verbose
#     """
#     modelmasterfile = pIMdirec / (pmodelname + ODMParameter.imextension())
#     defaultlang = getmodellang(modelmasterfile).lower()
#     model = pjson.getelements(JSModel.ELEMTYPE_PROJ)
#     jsonlang = model.get('language')
#     if defaultlang != jsonlang:
#         logging.error(f"Model {pmodelname}, language in ODM ({defaultlang}) and jsonfile ({jsonlang}) differ")
#         print(f"Model {pmodelname}, language in ODM {defaultlang} and jsonfile {jsonlang} differ")
#         exit(1)
#
#     langs = [key for key, val in pjson.getelements('languages').items() if not val['modellanguage']]
#     odmparam = ODMParameter(modelname=pmodelname, imdirec=pIMdirec, defaultlang=jsonlang, )
#     cnt = {'enti': 0, 'doma': 0, 'rela': 0, 'attr': 0}
#     handleXML.dosegfiles(pdirec=odmparam.entitydirec(),
#                          phandlefunc=do1entity, cnt=cnt, jsstruct=pjson, langs=langs, dryrun=pdryrun)
#     handleXML.dosegfiles(pdirec=odmparam.relationdirec(),
#                          phandlefunc=do1relation, cnt=cnt, jsstruct=pjson, langs=langs, dryrun=pdryrun)
#     """domains are not yet translated in ODM """
#     if False:
#         handleXML.doxmlfiles(pdirec=odmparam.domainsdirec(), ppattern=r'.*\.xml',
#                              phandlefunc=do1domain, cnt=cnt, jsstruct=pjson, langs=langs, dryrun=pdryrun)
#         handleXML.doxmlfiles(pdirec=odmparam.defdomainsfilpath().parent, ppattern=odmparam.defdomainsfilname(),
#                              phandlefunc=do1domain, cnt=cnt, jsstruct=pjson, langs=langs, dryrun=pdryrun)
#     return cnt

def do1column(pjson:JSModel,pcoluid:str,pcnt:dict):
    pcnt["columns"] += 1
    return

def do1table(pjson:JSModel,ptabid:str,pcnt:dict):
    pcnt["tables"] += 1
    return

def savemapfile(pIMdirec:Path,pintf:dict,pxml:et.Element):
    return
    intffile=""
    #remove existing files
    outfile = open(intffile, "w")
    outfile.write(handleXML.prettify(pxml))
    outfile.close()
    return

def do1interface(pIMdirec:Path,pjson:JSModel,pintfid:str,pintf:dict)->bool:
    if len(pintf["tables+"]) ==0:
        logging.info(f"""Interface '{pintf["name"]}' has no tables. Not handled.""")
        return False

    #delete mapping files, create new mappingfile for interface
    xml = et.Element("RMExtendedMap", {"class": "oracle.dbtools.crest.model.xtdmapping.RMExtendedMap"})
    mappings = et.SubElement(xml, "mappings",
                                {"itemClass": "oracle.dbtools.crest.model.xtdmapping.ContainerMapping"})

    cnt={"tables":0,"columns":0}
    for tabid in pintf["tables+"]:
        do1table(pjson=pjson,ptabid=tabid,pcnt=cnt)

    savemapfile(pIMdirec=pIMdirec,pintf=pintf,pxml=xml)

    logging.info(f"""Interface '{pintf["name"]}': mappings (tables:{str(cnt["tables"])}, columns:{str(cnt["columns"])} written to ODM""")
    return True

def writemappings(pIMdirec:Path, pjson:JSModel, pintfs:list):
    intfs = {key:val for key, val in pjson.getelements("systems").items() if ((pintfs is None) or (val["name"] in pintfs))}

    writtenback = []

    if len(intfs) ==0:
        logging.info(f"No interfaces found to process.")
        return writtenback

    for intfid,intf in intfs.items():
        written = do1interface(pIMdirec=pIMdirec,pjson=pjson,pintfid=intfid,pintf=intf)
        if written:
            writtenback.append(intf)

    return writtenback


def main(sysargs):
    argp = argparse.ArgumentParser(description='Write back mappings for interfaces into ODM-xmls')
    argp.add_argument('--verbose', '-v', action='store_true',
                      help="Verbose mode")
    argp.add_argument('--destination', '-d', dest="destination",
                      help=f"Path of ODM-model to change.  Default: <path of jsonffile>/../IM ")
    argp.add_argument('--interfaces', '-i', dest="interfaces",
                      help=f"List of interfaces (datamodels)  to be written back ('intf1,intf2').  Default: all interfaces found in jsonfile")
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

    interfaces= writemappings(pIMdirec=imdirec,
                        pjson=myjson, pintfs = arguments.interfaces
                        )
    if len(interfaces)==0:
        logging.info(
            "No mappings recreated")
    else:
        logging.info(
            "Mappings recreated for\n" + '\n'.join(interfaces))
    return

if __name__ == '__main__':
    main(sys.argv)
