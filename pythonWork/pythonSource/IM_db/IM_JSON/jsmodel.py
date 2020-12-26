
from IM_OBJECTS import Project,Entity
from IM_JSON import *

def lastupd(pmodel):
    dm = lambda  objs: max('0' if val['dm'] is None else val['dm'] for val in pmodel[objs].values())
    return max(dm( 'attributes'), dm( 'domains'), dm( 'entities') , dm('relations')
    , dm('arcs')
    , dm('keys')
    , dm('orgunits')
    , dm('diagrams')
    , dm('systems')
    , dm('tables')
    , dm('columns'),dm('datatypes'),dm('storageformats')
)

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

def sql2json(pmodelname):
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
    jsmodel['diagrams'] = diagrams2js(pmodelname=pmodelname)
    jsmodel['systems'] = systems2js()
    jsmodel['tables'] = tables2js()
    jsmodel['columns'] = columns2js()
    jsmodel['userdefprops'] = udps2js()
    jsmodel['physicalunits'] = physicalunits2js()
    jsmodel['datatypes'] = datatypes2js()
    jsmodel['storageformats'] = storageformats2js()
    jsmodel['model']['dm'] = lastupd(jsmodel)
    return jsmodel
#sql2json

def proj2js():
    proj = Project.select()[0]
    model = {'name': proj.proj_name
        , 'type': Project.LOGICALTYPE
        , 'language': proj.proj_curr_lang.lower()
        , 'uc': proj.proj_uc
        , 'dc': proj.proj_dc
             # , 'dm': None
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
        proj.proj_um = None
        proj.proj_dm = elem["dm"]
        proj.insert()
    except Exception as err:
        error(pmsg=err, pelem=elem)
