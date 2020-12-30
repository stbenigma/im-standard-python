
from IM_OBJECTS import Project,Entity
from IM_JSON import *
from datetime import datetime

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

def sql2json(pmodelname,pdbname):
    jsmodel = {}
    jsmodel['model'] = proj2js()
    jsmodel['languages'] = langs2js()
    jsmodel['entities'] = entities2js()
    jsmodel['domains'] = domains2js()
    jsmodel['attributes'] = attributes2js()
    jsmodel['relations'] = relations2js()
    jsmodel['arcs'] = arcs2js()
    jsmodel['keys'] = keys2js()
    jsmodel['documents'] = documents2js()
    jsmodel['orgunits'] = orgUnits2js()
    jsmodel['systems'] = systems2js()
    jsmodel['tables'] = tables2js()
    jsmodel['columns'] = columns2js()
    jsmodel['diagrams'] = diagrams2js(pmodelname=pmodelname)
    jsmodel['userdefprops'] = udps2js()
    jsmodel['physicalunits'] = physicalunits2js()
    jsmodel['datatypes'] = datatypes2js()
    jsmodel['storageformats'] = storageformats2js()

    if jsmodel['model']['dm'] is None: jsmodel['model']['dm'] = lastupd()

    modelhash = make_hash(jsmodel)
    jsmodel['_imprint_'] = {"database" : pdbname if pdbname != "" else ":in-memory:"
                        , "created": str(datetime.today())
                        ,"hashvalue": modelhash
                        ,"comment": "Entries ending with + represent denormalized data and are not checked for consistency while reading back"}
    return jsmodel
#sql2json

def proj2js():
    proj = Project.select()[0]
    model = {'name': proj.proj_name
        , 'type': Project.LOGICALTYPE
        , 'language': proj.proj_curr_lang.lower()
        , 'uc': proj.proj_uc
        , 'dc': proj.proj_dc
        , 'um': proj.proj_um
        , 'dm': proj.proj_dm
             }
    return model
#proj2js

def proj2sql(pmodel):
    elem = pmodel.jsmodel['model']
    try:
        proj = Project()
        proj.proj_name = elem["name"]
        proj.proj_languages = elem["type"]
        proj.proj_curr_lang = elem["language"]
        proj.proj_uc = elem["uc"]
        proj.proj_dc = elem["dc"]
        proj.proj_um = elem["um"]
        proj.proj_dm = elem["dm"]
        proj.insert()
    except Exception as err:
        error(pmsg=err, pelem=elem)
