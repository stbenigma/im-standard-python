import copy

from SSOT_db.IM_JSON import JSModel
from SSOT_db.IM_OBJECTS import Modelelement

""" filter a model-json structure by diagram and publication status

    returns a json structure only with elements fullfilling the filter criteria
    or having no status but being referenced in ones fullfilling the criteria
    
    call
    filter_json(pmodel:JSModel                  
                ,ppubl_status:str = None         
                ,pIMdiagrams = None) -> JSMODEL:
    
    pmodel      model to be filtered
    ppubl_status DRAFT (all elements, including those with no publ_status)
                GTOP (all elements with GTOP or PUBL as publ_status)
                PUBL (all elements with PUBL as publ_status)
    pIMdiagrams []  all elements
                ["name",] all entities on one of the IM diagrams identified by its names

"""


def removediagrams(pmodel, pIMdiagrams):

    return pmodel


def filter_json(pmodel: JSModel
                , ppubl_status: str = None
                , pIMdiagrams: list = None) -> JSModel:
    #defaults change nothing
    if ppubl_status is None and pIMdiagrams is None:
        return pmodel

    assert ppubl_status is None \
           or ppubl_status in (Modelelement.DRAFT, Modelelement.GTOP, Modelelement.PUBL)
    assert pIMdiagrams is None or type(pIMdiagrams) == list

    newmodel = copy.deepcopy(pmodel)
    removediagrams(pmodel=newmodel, pIMdiagrams=pIMdiagrams)
    return newmodel
