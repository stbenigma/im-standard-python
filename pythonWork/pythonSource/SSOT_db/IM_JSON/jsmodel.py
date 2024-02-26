import copy
from datetime import datetime

from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import Project, Modelelemtype
from SSOT_db.SQL_INFRA import dbConnect
from SSOT_infra import parameters



def lastupd():
    return datetime.today().__str__()


def make_hash(pmodel):
    """
    Makes a hash from a dictionary, list, tuple or set to any level, that contains
    only other hashable types (including any lists, tuples, sets, and
    dictionaries).
    """

    if isinstance(pmodel, (set, tuple, list)):
        return tuple([make_hash(e) for e in pmodel])
    elif not isinstance(pmodel, dict):
        return hash(pmodel)

    new_model = copy.deepcopy(pmodel)
    for k, v in filter (lambda nm : nm[0] not in ("dc", "dm", "uc", "um", "_imprint_"),
                        new_model.items()):
        # exclude non-fix dict entries
        #replaced by filter if k in ("dc", "dm", "uc", "um", "_imprint_"): continue
        new_model[k] = make_hash(v)
    return hash(tuple(frozenset(sorted(new_model.items()))))


def jsonimprint(dbname, created, modelversion, jsonversion, hashvalue, gitrevision):
    return {"database": dbname,
            "created": created,
            "Modelversion": modelversion,
            "JSONversion": jsonversion,
            "hashvalue": hashvalue,
            "git-revision": gitrevision,
            "comment": "Entries ending with + represent denormalized data and are not checked for consistency while reading back"
            }


def sql2json(pdbname=None, pemptymodel=False):
    jsmodel = {}
    jsmodel[JSModel.elemtype2label(JSModel.ELEMTYPE_PROJ)] = proj2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(JSModel.ELEMTYPE_LANG)] = langs2js(pemptymodel)
    logging.info("Processing entities")
    jsmodel[JSModel.elemtype2label(Modelelemtype.ENTI)] = entities2js(pemptymodel)
    logging.info("Processing domains")
    jsmodel[JSModel.elemtype2label(Modelelemtype.DOMA)] = domains2js(pemptymodel)
    logging.info("Processing attributes")
    jsmodel[JSModel.elemtype2label(Modelelemtype.ATTR)] = attributes2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.RELA)] = relations2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.ARCS)] = arcs2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.KEYS)] = keys2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.BURU)] = businessrules2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.DOCU)] = documents2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.ACTR)] = actorroles2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.ORGU)] = orgUnits2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(JSModel.ELEMTYPE_CATG)] = categories2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.DATM)] = datamodels2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.TABL)] = tables2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.COLU)] = columns2js(pemptymodel)
    logging.info("Processing diagrams")
    jsmodel[JSModel.elemtype2label(Modelelemtype.DIAG)] = diagrams2js(pemptymodel=pemptymodel,
                                                                      pmodelname=jsmodel['model']['name'])
    logging.info("Processing user defined properties")
    jsmodel[JSModel.elemtype2label(Modelelemtype.UDPR)] = udps2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.PHYU)] = physicalunits2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.DATY)] = datatypes2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.STFO)] = storageformats2js(pemptymodel)

    modelhash = make_hash(jsmodel)

    jsonversion = parameters.jsonversion()
    if jsonversion:
        jsonversion = parameters.jsonversion().base_version
    if pemptymodel:
        dbname, dbversion = "None", ""
        git_revision = '<emptymodel>'
    else:
        dbversion = dbConnect.getversion()
        git_revision = dbConnect.read_git_revision(dbConnect.getdbcon())
        if pdbname == "":
            dbname = ":in-memory:"
        elif pdbname is None:
            dbname = dbConnect.getDBname()
        else:
            dbname = pdbname

    jsmodel['_imprint_'] = jsonimprint(dbname=dbname,
                                       created=lastupd(),
                                       modelversion=dbversion,
                                       jsonversion=jsonversion,
                                       hashvalue=modelhash,
                                       gitrevision=git_revision)
    logging.info(f"JSModel for git revision '{git_revision}' generated")
    return jsmodel


PROJECTMODEL = ['name', 'type', 'language', 'uc', 'dc', 'um', 'dm']


def jsonproject(name, modeltype, language, uc, dc, **kwargs):
    model = dict()
    initjselement(model=model, refmodel=PROJECTMODEL)
    model["name"] = name
    model["type"] = modeltype
    model["language"] = language
    model["uc"] = uc
    model["dc"] = dc

    fillargs(model=model, refmodel=PROJECTMODEL, **kwargs)
    return model


def proj2js(pemptymodel: bool):
    if pemptymodel:
        entries = ['' for i in range(len(PROJECTMODEL))]
    else:
        projs = Project.select()
        if len(projs) == 0:
            """empty db no project found"""
            entries = [None for i in range(len(PROJECTMODEL))]
        else:
            proj = projs[0]
            entries = [proj.proj_name, Project.LOGICALTYPE,
                       '' if proj.proj_curr_lang is None else proj.proj_curr_lang.lower(),
                       proj.proj_uc, proj.proj_dc, proj.proj_um, proj.proj_dm]
        # fi
    # fi
    return fillmodel(pmodel=PROJECTMODEL, pentries=entries)


def js2proj(pkey, pelem, pmodellang=None):
    proj = Project()
    proj.proj_name = pelem["name"]
    proj.proj_type = pelem["type"]
    proj.proj_curr_lang = pelem["language"]
    proj.proj_uc = pelem["uc"]
    proj.proj_dc = pelem["dc"]
    proj.proj_um = pelem["um"]
    proj.proj_dm = pelem["dm"]
    return proj


def proj2sql(presult, pjson: JSModel, pwithextsrcref):
    inscnt = 0
    elem = pjson.jsmodel['model']
    try:
        """insert if nonexistent, otherwise don't touch"""
        projs = Project.select()
        if len(projs) == 0:
            proj = js2proj(pkey=None, pelem=elem)
            proj.insert()
            inscnt += 1
    except Exception as err:
        presult.markdberror(perr=err, pelem=elem)
    return inscnt
