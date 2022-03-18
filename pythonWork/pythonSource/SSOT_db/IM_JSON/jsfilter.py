import copy

from SSOT_db.IM_OBJECTS import Modelelement, Modelelemtype
from .jsbase import JSModel


class FILTEREDJSModel(JSModel):
    # Model element types which apply to filtering
    FILTEREDTYPES = (Modelelemtype.ENTI, Modelelemtype.ATTR, Modelelemtype.RELA,
                     Modelelemtype.DOCU, Modelelemtype.DOMA, Modelelemtype.DATY,
                     Modelelemtype.STFO, Modelelemtype.ORGU, Modelelemtype.ARCS,
                     Modelelemtype.KEYS, Modelelemtype.PHYU, Modelelemtype.DIAG
                     )

    def __init__(self, pmodel: dict, ppublstatus: str = None, pimdiagrams: list = None):
        assert ppublstatus in (None, Modelelement.DRAFT, Modelelement.GTOP, Modelelement.PUBL)
        assert pimdiagrams is None or type(pimdiagrams) == list
        assert type(pmodel) == dict
        super().__init__(pmodel=copy.deepcopy(pmodel))  # make copy as we might change an objects passed as parameter
        self._publstatus = ppublstatus
        self._imdiagram = pimdiagrams
        self._filteredidlist = set()
        if self._publstatus in (None, Modelelement.DRAFT) and self._imdiagram is None:
            self._buildpublishedidlist()
        else:
            self._buildfilteredidlist()
            self._filter_json()

    def getfilteredidlist(self) -> list:
        return self._filteredidlist

    """ is the pelement publishable according to its publstats and the set filter 
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
            retval = (elempubstatus in (None, Modelelement.PUBL)) \
                     or (self._publstatus in (None, Modelelement.DRAFT)) \
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

    def _buildpublishedidlist(self):
        for elemtype in self.FILTEREDTYPES:
            for key, value in self.getelements(elemtype).items():
                if self._publishable(value):
                    self._filteredidlist.add(key)
            # for
        return

    """ remove a key from the filteredidlist it the condition is met
        pelemtype  (ENTI, ATTR ...)
        pcondition : lambda elem,filteridlist:   
        pfilteredidlist : 
    """

    def _removeelement(self, pelemtype, pcondition):
        for id, elem in self.getelements(pelemtype=pelemtype).items():
            if pcondition(elem, self._filteredidlist):
                self._filteredidlist.discard(id)
            # fi
        # for
        return

    """ build a list of ID's remaining after applying the filter"""

    def _buildfilteredidlist(self):
        # start with publishable top level keys
        self._buildpublishedidlist()
        # remove diagrams not in the filter list
        if self._imdiagram is not None:
            for diagid, diag in self.getelements(pelemtype=Modelelemtype.DIAG).items():
                if diag["name"] not in self._imdiagram:
                    self._filteredidlist.discard(diagid)
                # fi
            # for
        # fi
        # remove entities if diagrams are filtered, entity is not on remaining diagrams
        self._removeelement(pelemtype=Modelelemtype.ENTI,
                            pcondition=lambda elem, ref: (self._imdiagram is not None \
                                                              and not set(elem["diagrams+"]).intersection(ref))
                            )

        # for entiid, enti in self.getelements(pelemtype=Modelelemtype.ENTI
        #         , pfiltered=False).items():
        #
        #     if set(enti["diagrams+"]).intersection(filteredidlist):
        #         filteredidlist.discard(entiid)
        #     # fi
        # # for
        # assert testlist == filteredidlist

        # remove attributes of not shown entities
        self._removeelement(pelemtype=Modelelemtype.ATTR,
                            pcondition=lambda elem, ref: elem["entity"] not in ref)

        # remove relationships of not shown entities
        self._removeelement(pelemtype=Modelelemtype.RELA,
                            pcondition=lambda elem, ref: elem["from-to"]["enti"] not in ref \
                                                         or elem["to-from"]["enti"] not in ref)
        # remove arcs of not shown entities
        self._removeelement(pelemtype=Modelelemtype.ARCS,
                            pcondition=lambda elem, ref: elem["entity"] not in ref)
        # remove arcs of not shown entities
        self._removeelement(pelemtype=Modelelemtype.KEYS,
                            pcondition=lambda elem, ref: elem["entity"] not in ref)

        #remove tables not referenced by entities
        #remove columns not referenced by attributes
        #remove systems no longer having any elements

        # remove domains of not used by attributes
        self._removeelement(pelemtype=Modelelemtype.DOMA,
                            pcondition=lambda elem, ref: not (set(elem["usedinattrs+"]).intersection(ref)\
                                                              or set(elem["usedincols+"]).intersection(ref)
                                                              )
                                                         )
        # remove domains of not used in domaingroups (second step including removed basic domains)
        self._removeelement(pelemtype=Modelelemtype.DOMA,
                            pcondition=lambda elem, ref: len(elem["usedingrps+"]) > 0 \
                                                         and not set(elem["usedingrps+"]).intersection(ref))

        # remove org-units not referenced by any remaining elements
        self._removeelement(pelemtype=Modelelemtype.ORGU,
                            pcondition=lambda elem, ref: len(elem["references+"]) > 0 \
                                                         and not set(elem["references+"]).intersection(ref))
        # remove documents not referenced by any remaining elements
        self._removeelement(pelemtype=Modelelemtype.DOCU,
                            pcondition=lambda elem, ref: len(elem["references+"]) > 0 \
                                                         and not set(elem["references+"]).intersection(ref))

        return

    """ filters all entries out of reference-lists (all entries with a + at the end of the key"""

    @staticmethod
    def _filterreferences(pelements, pfilteredidlist):
        for elemkey, elem in pelements.items():
            for key in elem.keys():
                if key.endswith("+") and type(elem[key]) in (set, list):
                    try:
                        elem[key] = list(set(elem[key]).intersection(pfilteredidlist))
                        if key == "references+" and "referencecnt+" in elem:
                            elem["referencecnt+"] = len(elem[key]).__str__()
                    except:
                        # one value in the val-list is of structured type (dict), ignore the error
                        pass
        return

    def removeelements(self,pelements):
        # list of keys of that element to be removed (= all those not in the filtereslist
        l = len(pelements)
        for idx in range(l,0,-1): #loop ends with idx > final idx
            if pelements[idx-1]["element"] not in self._filteredidlist:
                del pelements[idx-1]
        # for
        return

    def removekeys(self,pelements):
        # list of keys of that element to be removed (= all those not in the filtereslist
        elemstoremove = set(pelements.keys()).difference(self._filteredidlist)
        for key in elemstoremove:
            del pelements[key]
        # for
        return

    """ returns the json structured with filters applied
    """

    def _filter_json(self):
        if self.jsmodel is None:
            return

        # remove all top level elements, not in the filteredidlist
        for elemtype in self.FILTEREDTYPES:
            self.removekeys(self.getelements(elemtype))
        # for

        """ for all remaining elements in the filtered structure, remove all 
            references from the list of referenced elements.
        """
        for elemtype in self.FILTEREDTYPES:
            self._filterreferences(pelements=self.getelements(elemtype), pfilteredidlist=self._filteredidlist)
        #for

        """ for all remaining diagrams, remove elements (arcs, attributes, entities, relationships)
           which are not to be shown
        """
        for diag in  self.getelements(Modelelemtype.DIAG).values():
            self.removekeys(pelements=diag["arcs"])
            self.removekeys(pelements=diag["relationships"])
            self.removeelements(pelements=diag["elements"]["attribute"])
            self.removeelements(pelements=diag["elements"]["entity"])
        #for
        return
