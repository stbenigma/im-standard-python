from SSOT_db.IM_JSON import *

MAPPINGMODEL = ['name', 'type',
                'fromelemids', 'toelemids',
                'rulefrwd', 'rulebckw',
                'descr',
                'uc', 'dc', 'um', 'dm',
                'sourceref'
                ]


def jsonmapping(name, maptype, fromelemids, toelemids, uc, dc, **kwargs):
    mapping = dict()
    initjselement(mapping, MAPPINGMODEL)
    mapping["name"] = name
    mapping["uc"] = uc
    mapping["dc"] = dc
    mapping["type"] = maptype
    mapping['fromelemids'] = fromelemids
    mapping['toelemids'] = toelemids

    fillargs(model=mapping, refmodel=MAPPINGMODEL, **kwargs)
    return mapping
#TODO proper solution for complex mappings
MAPPINGELEMENTMODEL = ['name', 'mappingid',
                'fromelemids', 'toelemids',
                'rulefrwd', 'rulebckw',
                'descr',
                'uc', 'dc', 'um', 'dm',
                'sourceref'
                ]

