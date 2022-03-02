import copy

from SSOT_db.IM_OBJECTS import Modelelement, Modelelemtype
from .jsbase import JSModel

class JSFILTER:
    #Model element types which apply to filtering
    FILTEREDTYPES = (Modelelemtype.ENTI, Modelelemtype.ATTR, Modelelemtype.RELA,
                     Modelelemtype.DOCU, Modelelemtype.DOMA, Modelelemtype.DATY,
                     Modelelemtype.STFO, Modelelemtype.ORGU, Modelelemtype.ARCS,
                     Modelelemtype.KEYS, Modelelemtype.PHYU, Modelelemtype.DIAG
                     )

    def __init__(self, ppublstatus: str = None, pimdiagrams: list = None, pmodel: JSModel = None):
        assert ppublstatus in (None, Modelelement.DRAFT, Modelelement.GTOP, Modelelement.PUBL)
        assert pimdiagrams is None or type(pimdiagrams) == list
        self._publstatus = ppublstatus
        self._imdiagram = pimdiagrams
        self.setJSModel(pmodel)

    def setJSModel(self, pmodel: JSModel):
        self._JSModel = pmodel
        if self._JSModel is not None:
            self._buildfilteredidlist()
        else:
            self._filteredidlist = None
        return

    def getsJSMdel(self) -> JSModel:
        return self._JSModel

    def getfilteredidlist(self) -> list:
        return self._filteredidlist

    """ is the pelement publishable accorging to its publstats and the set filter 
    """
    def _publishable(self, pelement):
        # no publ status set or element does not have the attribute => take it,
        if (self._publstatus is None) or ("publstatus" not in pelement):
            retval = True
        else:
            elempubstatus = pelement["publstatus"]
            # PUBL-element is always published
            # None or DRAFT as filter includes all
            # GTOP filter requires GTOP or PUBL element
            # PUBL filter requires PUBL element
            retval = (elempubstatus in (None, Modelelement.PUBL))  \
                     or (self._publstatus in  (None,Modelelement.DRAFT)) \
                     or (self._publstatus == Modelelement.GTOP
                         and elempubstatus in (Modelelement.GTOP,
                                                Modelelement.PUBL)
                         ) \
                    or (self._publstatus == Modelelement.PUBL
                        and elempubstatus == Modelelement.PUBL
                        )
        # fi
        return retval

    """ builds a list of all top level keys fullfilling the publischable criteriy (publstatus) 
    """
    def _buildpublishedidlist(self)->set:
        idlist = set()
        for elemtype in JSFILTER.FILTEREDTYPES:
            for key, value in self._JSModel.jsmodel[JSModel.elemtype2label(elemtype)].items():
                if self._publishable(value):
                    idlist.add(key)
            # for
        return idlist

    """ remove a key from the filteredidlist it the condition is met
        pelemtype  (ENTI, ATTR ...)
        pcondition : lambda elem,filteridlist:   
        pfilteredidlist : 
    """
    def _removeelement(self, pelemtype, pcondition):
        for id, elem in self._JSModel.getelements(pelemtype=pelemtype, pfiltered=False).items():
            if pcondition(elem,self._filteredidlist):
                self._filteredidlist.discard(id)
            # fi
        # for
        return

    """ build a list of ID's remaining after applying the filter"""

    def _buildfilteredidlist(self):
        #start with publishable top level keys
        self._buildpublishedidlist()
        # remove diagrams not in the filter list
        if self._imdiagram is not None:
            for diagid, diag in self._JSModel.getelements(pelemtype=Modelelemtype.DIAG
                    , pfiltered=False).items():
                if diag["name"] not in self._imdiagram:
                    self._filteredidlist.discard(diagid)
                # fi
            # for
        # fi
        # remove entities shown on no remaining diagrams
        self._removeelement(pelemtype=Modelelemtype.ENTI,
                            pcondition=lambda elem,ref : not set (elem["diagrams+"]).intersection(ref))

        # for entiid, enti in self._JSModel.getelements(pelemtype=Modelelemtype.ENTI
        #         , pfiltered=False).items():
        #
        #     if set(enti["diagrams+"]).intersection(filteredidlist):
        #         filteredidlist.discard(entiid)
        #     # fi
        # # for
        # assert testlist == filteredidlist

        # remove attributes of not shown entities
        self._removeelement(pelemtype=Modelelemtype.ATTR,
                            pcondition=lambda elem,ref : elem["entity"] not in ref)

        # remove relationships of not shown entities
        self._removeelement(pelemtype=Modelelemtype.RELA,
                            pcondition=lambda elem,ref : elem["from-to"]["enti"] not in ref \
                                            or elem["to-from"]["enti"] not in ref)
        # remove arcs of not shown entities
        self._removeelement(pelemtype=Modelelemtype.ARCS,
                            pcondition=lambda elem,ref : elem["entity"] not in ref)
        # remove arcs of not shown entities
        self._removeelement(pelemtype=Modelelemtype.KEYS,
                            pcondition=lambda elem,ref : elem["entity"] not in ref)
        # remove domains of not used by attributes
        self._removeelement(pelemtype=Modelelemtype.DOMA,
                            pcondition=lambda elem,ref : len(elem["usedinattrs+"]) > 0 \
                                            and not set(elem["usedinattrs+"]).intersection(ref))
        # remove domains of not used in domaingroups (second step including removed basic domains)
        self._removeelement(pelemtype=Modelelemtype.DOMA,
                            pcondition=lambda elem,ref : len(elem["usedingrps+"]) > 0 \
                                            and not set(elem["usedingrps+"]).intersection(ref)

        # remove org-units not referenced by any remaining elements
        self._removeelement(pelemtype=Modelelemtype.ORGU,
                            pcondition=lambda elem,ref : len(elem["references+"]) > 0 \
                                            and not set(elem["references+"]).intersection(ref))
        # remove documents not referenced by any remaining elements
        self._removeelement(pelemtype=Modelelemtype.DOCU,
                            pcondition=lambda elem,ref : len(elem["references+"]) > 0 \
                                            and not set(elem["references+"]).intersection(ref))

        return

    """ filters all entries out of reference-lists (all entries with a + at the end of the key"""
    def _filterreferences(pmodel,pelemtype):
        elements = pmodel[pelemtype]
        for key in elements.keys():
            if key.endswith("+"):
                elements[key]= list(set(elements[key]).intersection(self._filteredidlist))
        return

    """ returns the json structured with filters applied
    """

    def filtered_json(self) -> dict:
        if self._JSModel is None:
            return None

        newmodel = copy.deepcopy(self.getjsmodel().jsmodel)
        #remove all top level elements, not in the filteredidlist
        for elemtype in JSFILTER.FILTEREDTYPES:
            elements = newmodel[JSModel.elemtype2label(elemtype)]
            #list of keys of that element to be removed (= all those not in the filtereslist
            elemstoremove = set(elements.keys()).difference(self._filteredidlist)
            for key in elemstoremove:
                del elements[key]
        """ for all remaining elements in the filtered structure, remove all 
            references from the list of reverenced elements.
        """
        for elemtype in self.FILTEREDTYPES:
            self._filterreferences(pmodel=newmodel,pelemtype=elemtype)

        return newmodel
