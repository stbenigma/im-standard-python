import argparse
import logging
import os.path
import re
import sys
from pathlib import Path

from LOAD_MODELS.LOAD_INFRA import handleXML
from LOAD_MODELS.LOAD_ODM import ODMParameter
from SSOT_db.IM_JSON import JSModel
from SSOT_infra import transl, nvl

""" 
    writes information back into ODM-XML-files
"""


def getmodellang(pmodelfile):
    dmdxml = handleXML.parseXML(pmodelfile)
    root = dmdxml.getroot()
    comment = root.find('comment').text
    lang = re.search('currentLang=(\w+)', comment)
    if lang:
        return lang.group(1)
    else:
        return lang


def getelembyodmguid(pjson: JSModel, pelemtype, pguid):
    elems = pjson.getelements(pelemtype=pelemtype)
    for key, elem in elems.items():
        odmref = elem.get('sourceref').get('ODM')
        if odmref and (odmref[0] == pguid):
            return key, elem
    return None, None


def udpname(lang, name):
    return f"{lang.upper()}_{name}"


def do1Attribute(lfnr, attrxml, jsstruct: JSModel, cnt, langs, dryrun):
    changed = False
    attrguid = handleXML.findField(attrxml, 'id')
    attrid, jsattr = getelembyodmguid(pjson=jsstruct, pelemtype='attributes', pguid=attrguid)
    if attrid is None: return  # Attribute from ODM not found in json

    """<propertyMap>
        <property name="DE_ATTR_NAME" value="."/>
        <property name="EN_ATTR_NAME" value="."/>
        </propertyMap>
    """
    propmap = handleXML.findorcreateelement(attrxml, "propertyMap")
    for lang in langs:

        fieldname = udpname(lang, "ATTR_NAME")
        newval = jsstruct.getlangtext(pelem=jsattr['name'], plang=lang
                                      , preplacement=False)
        if updproperty(propmap=propmap, udpname=fieldname, newval=newval):
            if dryrun:
                logging.info(f"attr {attrid}: field={fieldname}  newval={newval}")
            changed = True
            # for

    noteelem = findorinitialisenote(elemxml=attrxml, type='ATTR_COMMENT', langs=langs)
    if updnote(noteelem=noteelem, langs=langs, descrs=jsattr['descr'],
               examples=jsattr['examples'], jsstruct=jsstruct, dryrun=dryrun):
        changed = True

    if changed:
        cnt['attr'] += 1
    return changed


def updproperty(propmap, udpname: str, newval: str) -> bool:
    changed = False
    newval = nvl(newval)
    prop = propmap.find(f"property[@name='{udpname}']")
    if (prop is None):
        prop = handleXML.createsubelement(propmap, "property", name=udpname, value=newval)
        changed = (newval != "")  # empty map is considered unchanged
    else:
        if prop.get('value') != newval:
            prop.set('value', newval)
            changed = True
    # fi
    return changed


def findorinitialisenote(elemxml, type, langs):
    """ finds the <notes> element in elemxml
        if not found, create it
        """
    note = handleXML.findorcreateelement(elemxml, 'notes')
    if note.text is None:
        note.text = "<![CDATA[\n]]>"
    for lang in langs:
        lang = lang.upper()
        commtag = f"[{lang}_{type}["
        if not re.search(re.escape(commtag), note.text, re.MULTILINE):
            note.text += f"[{lang}_{type}[\n]{lang}_{type}]\n"
    return note


def updnote(noteelem, langs, descrs, examples, jsstruct, dryrun):
    """ fill the translated descriptions into the note with examples at the end to
        the ODM's note field
        examples are a list of language-text dicts
        """
    changed = False

    lngcomments = handleXML.extractlngcomments(ptext=noteelem.text)
    for lang, lngitems in filter (lambda l : l[0] in langs, lngcomments.items()):
        #replaced by filter if lang not in langs: continue  # skip modellanguage
        for name, text in filter (lambda l : l[0].endswith("_COMMENT"),
                                  lngitems.items()):
            #replaced by filter if name.endswith("_COMMENT"):
            """separate examples from description"""
            lngdescr, lngexamples = handleXML.separateExamples(text)
            newlngdescr = jsstruct.getlangtext(pelem=descrs, plang=lang
                                               , preplacement=False)
            if len(examples) > 0:
                newexamples = joinlistoflang(joinchar='\n', elems=examples,
                                             lang=lang, jsstruct=jsstruct)
                newexamplstr = f"\n\n{transl(ptext='Beispiele', plang=lang)}:\n  " \
                               + newexamples
                newlngdescr = newlngdescr + newexamplstr
            # fi
            if newlngdescr != text:
                if dryrun:
                    logging.info(f"note: field={name} " +
                                 f" newval={newlngdescr}")
                changed = True
                # replace part  between [xx_yyyy_COMMENT[ and ]xx_yyyy_COMMENT] with the new comment
                noteelem.text = re.sub(r'(\[{attrname}\[)([\S\n\t\v ]*)(\]{attrname}\])'.format(attrname=name),
                                       r'\1\n{}\n\3'.format(newlngdescr),
                                       noteelem.text)
            # fi
        # for
    # for
    return changed


def joinlistoflang(joinchar, elems, lang, jsstruct):
    """ returns a joined list of strings out of a list of language-text-entries"""
    return joinchar.join(jsstruct.getlangtext(pelem=s, plang=lang, pidx=idx
                                              , preplacement=False) for idx, s in enumerate(elems))


def do1entity(filename, XMLtree, jsstruct: JSModel, cnt, langs, dryrun):
    changed = False

    entixml = XMLtree.getroot()
    # there are sometimes strange files in the directories
    if (handleXML.findField(entixml, "class") != "oracle.dbtools.crest.model.design.logical.Entity"): return
    entiguid = handleXML.findField(entixml, 'id')
    entiid, jsenti = getelembyodmguid(pjson=jsstruct, pelemtype='entities', pguid=entiguid)
    if entiid is None: return  # Entity from ODM not found in json

    """<propertyMap>
        <property name="DE_ATTR_NAME" value="."/>
        <property name="EN_ATTR_NAME" value="."/>
        </propertyMap>
    """
    propmap = handleXML.findorcreateelement(entixml, "propertyMap")
    for lang in langs:
        fieldname = udpname(lang, "ENTI_NAME")
        newval = jsstruct.getlangtext(pelem=jsenti['name'], plang=lang, preplacement=False)
        if updproperty(propmap=propmap, udpname=fieldname, newval=newval):
            if dryrun:
                logging.info(f"enti {entiid}: field={fieldname} " +
                             f" newval={newval}")
            changed = True

        fieldname = udpname(lang, "ENTI_SYNONYM")
        newval = joinlistoflang(joinchar=', ', elems=jsenti['synonyms'], lang=lang, jsstruct=jsstruct)
        if updproperty(propmap=propmap, udpname=fieldname, newval=newval):
            if dryrun:
                logging.info(f"enti {entiid}: field={fieldname} " +
                             f" newval={newval}")
            changed = True
    # for

    fieldname = 'ENTI_COMMENT'
    noteelem = findorinitialisenote(elemxml=entixml, type=fieldname, langs=langs)
    if updnote(noteelem=noteelem, langs=langs, descrs=jsenti['descr'],
               examples=jsenti['examples'], jsstruct=jsstruct, dryrun=dryrun):
        changed = True

    attrs = entixml.find('attributes')
    if attrs is not None:
        for idx, attr in enumerate(attrs, start=1):
            guid = attr.get('id')
            if do1Attribute(lfnr=idx, attrxml=attr, jsstruct=jsstruct, cnt=cnt,
                            langs=langs, dryrun=dryrun):
                changed = True
    if changed:
        if not dryrun:
            XMLtree.write(filename, encoding='unicode')
            # XMLtree.write('/Users/stb/Downloads/test.xml',encoding='unicode')
        cnt['enti'] += 1
    return


def do1domain(filename, XMLtree, jsstruct: JSModel, cnt, langs, dryrun):
    changed = False

    domaxml = XMLtree.getroot()
    # there are sometimes strange files in the directories
    if (handleXML.findField(domaxml, "class") != "oracle.dbtools.crest.model.design.DomainFileWrapper"): return
    ##not yet translated in ODM
    cnt['doma'] += 1 if changed else 0
    return


def do1relation(filename, XMLtree, jsstruct: JSModel, cnt, langs, dryrun):
    changed = False

    relaxml = XMLtree.getroot()
    # there are sometimes strange files in the directories
    if (handleXML.findField(relaxml, "class") != "oracle.dbtools.crest.model.design.logical.Relation"): return
    relaguid = handleXML.findField(relaxml, 'id')
    relaid, jsrela = getelembyodmguid(pjson=jsstruct, pelemtype='relations', pguid=relaguid)
    if relaid is None: return  # Relation from ODM not found in json

    """<propertyMap>
        <property name="EN_RELA_TEXT_FROM" value="goes with"/>
        <property name="EN_RELA_TEXT_TO" value="follows"/>
        <property name="FR_RELA_TEXT_FROM" value="va avec"/>
        <property name="FR_RELA_TEXT_TO" value="suit"/>
        </propertyMap>
        """
    propmap = handleXML.findorcreateelement(relaxml, "propertyMap")
    for lang in langs:
        fieldname = udpname(lang, "RELA_TEXT_FROM")
        newval = jsstruct.getlangtext(pelem=jsrela['from-to']['assoc'], plang=lang,
                                      preplacement=False)
        if updproperty(propmap=propmap, udpname=fieldname, newval=newval):
            if dryrun:
                logging.info(f"rela {relaid}: field={fieldname}  newval={newval}")
            changed = True

        fieldname = udpname(lang, "RELA_TEXT_TO")
        newval = jsstruct.getlangtext(pelem=jsrela['to-from']['assoc'], plang=lang,
                                      preplacement=False)
        if updproperty(propmap=propmap, udpname=fieldname,
                       newval=newval):
            if dryrun:
                logging.info(f"rela {relaid}: field={fieldname}  newval={newval}")
            changed = True
    # for

    if changed:
        if not dryrun:
            XMLtree.write(filename, encoding='unicode')
            # XMLtree.write('/Users/stb/Downloads/test.xml', encoding='unicode')
        cnt['rela'] += 1
    return


def writetranslations(pIMdirec, pmodelname, pjson: JSModel, pdryrun=False):
    """ make sure the ODM has the same baselanguage as is defined in the jsonmodel
        replace in ODM-files all translations (this means without the values of the base language)
        we treat all translated elements as defined in  Languagetext.ODMtranslAttributes
        pdryrun = True, do not write files back. only count changes
        consider dryrun as verbose
    """
    modelmasterfile = pIMdirec / (pmodelname + ODMParameter.imextension())
    defaultlang = getmodellang(modelmasterfile).lower()
    model = pjson.getelements(JSModel.ELEMTYPE_PROJ)
    jsonlang = model.get('language')
    if defaultlang != jsonlang:
        logging.error(f"Model {pmodelname}, language in ODM ({defaultlang}) and jsonfile ({jsonlang}) differ")
        print(f"Model {pmodelname}, language in ODM {defaultlang} and jsonfile {jsonlang} differ")
        exit(1)

    langs = [key for key, val in pjson.getelements('languages').items() if not val['modellanguage']]
    odmparam = ODMParameter(modelname=pmodelname, imdirec=pIMdirec, defaultlang=jsonlang, )
    cnt = {'enti': 0, 'doma': 0, 'rela': 0, 'attr': 0}
    handleXML.dosegfiles(pdirec=odmparam.entitydirec(),
                         phandlefunc=do1entity, cnt=cnt, jsstruct=pjson, langs=langs, dryrun=pdryrun)
    handleXML.dosegfiles(pdirec=odmparam.relationdirec(),
                         phandlefunc=do1relation, cnt=cnt, jsstruct=pjson, langs=langs, dryrun=pdryrun)
    """domains are not yet translated in ODM """
    if False:
        handleXML.doxmlfiles(pdirec=odmparam.domainsdirec(), ppattern=r'.*\.xml',
                             phandlefunc=do1domain, cnt=cnt, jsstruct=pjson, langs=langs, dryrun=pdryrun)
        handleXML.doxmlfiles(pdirec=odmparam.defdomainsfilpath().parent, ppattern=odmparam.defdomainsfilname(),
                             phandlefunc=do1domain, cnt=cnt, jsstruct=pjson, langs=langs, dryrun=pdryrun)
    return cnt


def main(sysargs):
    argp = argparse.ArgumentParser(description='Write back foreign language texts into 2 ODM-xmls')
    argp.add_argument('--verbose', '-v', action='store_true',
                      help="Verbose mode")
    argp.add_argument('--dryrun', '-dry', action='store_true',
                      help="Dry Run. Only get response of changed elements, do not change any XML-files")
    argp.add_argument('--destination', '-d', dest="destination",
                      help=f"Path of ODM-model to change.  Default: <path of jsonffile>/../IM ")
    argp.add_argument('--languages', '-l', dest="languages",
                      help=f"List of language to be written back (ex. 'en,fr').  Default: non-model languages found in jsonfile")
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

    cnt = writetranslations(pIMdirec=imdirec, pdryrun=arguments.dryrun, pjson=myjson, pmodelname=myjson.modelname(),
                            plangs=arguments.languages)
    print(
        f"{'Supposed c' if arguments.dryrun else 'C'}hanges in XML: Entities {cnt['enti']},  Attributes {cnt['attr']},  Domains {cnt['doma']}, Relations  {cnt['rela']}")
    return


if __name__ == '__main__':
    main(sys.argv)
