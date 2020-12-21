
from IM_OBJECTS import Project
from IM_JSON import *

def lastupd(pmodel):
    dm = lambda  objs: max('0' if val['dm'] is None else val['dm'] for val in pmodel[objs].values())
    return max(dm( 'attributes'), dm( 'domains'), dm( 'entities'))

def sql2json(pmodelname,pwithdata=True):
    jsmodel = {}
    jsmodel['model'] = proj2js()
    jsmodel['languages'] = langs2js()
    jsmodel['entities'] = entities2js()
    jsmodel['attributes'] = attributes2js()
    jsmodel['relations'] = relations2js()
    jsmodel['arcs'] = arcs2js()
    jsmodel['domains'] = domains2js()
    jsmodel['keys'] = keys2js()
    jsmodel['documents'] = documents2js()
    jsmodel['orgunits'] = orgUnits2js()
    jsmodel['diagrams'] = diagrams2js(pmodelname=pmodelname)
    jsmodel['systems'] = systems2js()
    jsmodel['tables'] = tables2js()
    jsmodel['columns'] = columns2js()
    jsmodel['userdefprop'] = udps2js()
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