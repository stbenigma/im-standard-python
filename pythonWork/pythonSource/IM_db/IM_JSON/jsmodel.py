from datetime import datetime
from IM_JSON import *
from IM_OBJECTS import Project, Modelelemtype
from IM_DB import parameters,dbConnect


def lastupd():
    return datetime.today().__str__()

import copy

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
    for k, v in new_model.items():
        new_model[k] = make_hash(v)
    return hash(tuple(frozenset(sorted(new_model.items()))))


def sql2json(pdbname, pemptymodel=False):
    jsmodel = {}
    jsmodel['model'] = proj2js(pemptymodel)
    jsmodel['languages'] = langs2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.ENTI)] = entities2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.DOMA)] = domains2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.ATTR)] = attributes2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.RELA)] = relations2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.ARCS)] = arcs2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.KEYS)] = keys2js(pemptymodel)
    #jsmodel[JSModel.elemtype2label(Modelelemtype.KEYS)] = businessrules2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.DOCU)] = documents2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.ORGU)] = orgUnits2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.INTF)] = systems2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.TABL)] = tables2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.COLU)] = columns2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.DIAG)] = diagrams2js(pemptymodel=pemptymodel, pmodelname=jsmodel['model']['name'])
    jsmodel[JSModel.elemtype2label(Modelelemtype.UDPR)] = udps2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.PHYU)] = physicalunits2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.DATY)] = datatypes2js(pemptymodel)
    jsmodel[JSModel.elemtype2label(Modelelemtype.STFO)] = storageformats2js(pemptymodel)

    modelhash = make_hash(jsmodel)
    jsmodel['_imprint_'] = {"database": "None" if pemptymodel else pdbname if pdbname != "" else ":in-memory:"
        , "created": str(datetime.today())
        ,"Modelversion" : "" if pemptymodel else dbConnect.getversion()
        , "hashvalue": modelhash
        ,
                            "comment": "Entries ending with + represent denormalized data and are not checked for consistency while reading back"}
    return jsmodel


# sql2json

def proj2js(pemptymodel: bool):
    model = ['name', 'type', 'language', 'uc', 'dc', 'um', 'dm']
    if pemptymodel:
        entries = ['' for i in range(len(model))]
    else:
        projs = Project.select()
        if len(projs)== 0:
            """empty db no project found"""
            entries = [None for i in range(len(model))]
        else:
            proj = projs[0]
            entries = [proj.proj_name, Project.LOGICALTYPE
                , '' if proj.proj_curr_lang is None else proj.proj_curr_lang.lower()
                , proj.proj_uc, proj.proj_dc, proj.proj_um, proj.proj_dm]
        #fi
    #fi
    return fillmodel(pmodel=model, pentries=entries)

# proj2js

def js2proj(pkey, pelem):
    proj = Project()
    proj.proj_name = pelem["name"]
    proj.proj_type = pelem["type"]
    proj.proj_curr_lang = pelem["language"]
    proj.proj_uc = pelem["uc"]
    proj.proj_dc = pelem["dc"]
    proj.proj_um = pelem["um"]
    proj.proj_dm = pelem["dm"]
    return proj


def proj2sql(presult, podmjson:JSModel, pdbjson:JSModel,pwithextsrcref):
    elem = podmjson.jsmodel['model']
    try:
        """insert if nonexistent, otherwise don't touch"""
        projs = Project.select()
        if len(projs)== 0:
            proj = js2proj(pkey=None,pelem=elem)
            proj.insert()
    except Exception as err:
        presult.errors.append("""*** DB-Error {}\{}""".format(err, pelem))

    return
