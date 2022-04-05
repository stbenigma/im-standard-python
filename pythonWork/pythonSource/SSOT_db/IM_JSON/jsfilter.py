import copy

from SSOT_db.IM_OBJECTS import Modelelement, Modelelemtype
from SSOT_infra import nvl
from .jsbase import JSModel


class FILTEREDJSModel(JSModel):
    # Model element types which apply to filtering
    FILTEREDTYPES = (Modelelemtype.ENTI, Modelelemtype.ATTR, Modelelemtype.RELA,
                     Modelelemtype.DOCU, Modelelemtype.DOMA, Modelelemtype.DATY,
                     Modelelemtype.STFO, Modelelemtype.ORGU, Modelelemtype.ARCS,
                     Modelelemtype.KEYS, Modelelemtype.PHYU, Modelelemtype.DIAG,
                     Modelelemtype.TABL, Modelelemtype.INTF, Modelelemtype.COLU,
                     Modelelemtype.DIAG
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

    def getfilteredidlist(self) -> set:
        return self._filteredidlist

    @property
    def filtered(self):
        """ Returns a copy of the internal model with a 'filters' section in the header describing the applied filters
        """
        model_clone = copy.deepcopy(self.jsmodel)
        model_clone['_imprint_']['filters'] = {
            'publish_status': self._publstatus,
            'diagrams': self._imdiagram,
            'filtered_ids': list(self._filteredidlist),
        }
        return model_clone

    def _publishable(self, pelement):
        # no publ status set or element does not have the attribute => take it,
        if "publstatus" not in pelement:
            retval = True
        else:
            elempubstatus = pelement["publstatus"]
            # PUBL-element is always published
            # None or DRAFT as filter includes all
            # GTOP filter requires GTOP or PUBL element
            # PUBL filter requires PUBL element
            retval = (self._publstatus in (None, Modelelement.DRAFT)) \
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
        for key, elem in self.getelements(pelemtype=pelemtype).items():
            if pcondition(elem, self._filteredidlist):
                self._filteredidlist.discard(key)
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
                            pcondition=lambda elem, ref: not (self._imdiagram is None
                                                              or set(elem["diagrams+"]).intersection(ref))
                            )

        # remove attributes of not shown entities
        self._removeelement(pelemtype=Modelelemtype.ATTR,
                            pcondition=lambda elem, ref: not (elem["entity"] in ref
                                                              and (self._imdiagram is None
                                                                   or set(elem["diagrams+"]).intersection(ref))
                                                              )
                            )

        # remove relationships of not shown entities
        self._removeelement(pelemtype=Modelelemtype.RELA,
                            pcondition=lambda elem, ref: not (elem["from-to"]["enti"] in ref
                                                              and elem["to-from"]["enti"] in ref))
        # remove arcs of not shown entities
        self._removeelement(pelemtype=Modelelemtype.ARCS,
                            pcondition=lambda elem, ref: not (elem["entity"] in ref))

        # remove keys of not shown entities
        self._removeelement(pelemtype=Modelelemtype.KEYS,
                            pcondition=lambda elem, ref: not (elem["entity"] in ref))

        # remove tables not referenced by entities filteredonly if diagrams are filtered too
        self._removeelement(pelemtype=Modelelemtype.TABL,
                            pcondition=lambda elem, ref: not (self._imdiagram is None
                                                              or (set(elem["entitiesmapped"]).intersection(ref)
                                                                  or set(elem["relationsmapped"]).intersection(ref))
                                                              )
                            )

        # remove columns of removed tables and not referenced by attributes
        self._removeelement(pelemtype=Modelelemtype.COLU,
                            pcondition=lambda elem, ref: not (elem["table-id"] in ref
                                                              and set(elem["attributesmapped"]).intersection(ref)
                                                              )
                            )

        # remove systems no longer having any elements or we have not filter set at all
        self._removeelement(pelemtype=Modelelemtype.INTF,
                            pcondition=lambda elem, ref: not ((self._imdiagram is None
                                                               and self._publstatus is None)
                                                              or set(elem["tables+"]).intersection(ref))
                            )

        # remove domains of not used by attributes
        self._removeelement(pelemtype=Modelelemtype.DOMA,
                            pcondition=lambda elem, ref: not (set(elem["usedinattrs+"]).intersection(ref)
                                                              or set(elem["usedincols+"]).intersection(ref)
                                                              or len(elem["usedingrps+"]) > 0
                                                              )
                            )
        # remove domains if not used in domaingroups (second step including removed basic domains)
        self._removeelement(pelemtype=Modelelemtype.DOMA,
                            pcondition=lambda elem, ref: not (len(elem["usedingrps+"]) == 0
                                                              or set(elem["usedingrps+"]).intersection(ref)))

        # remove org-units not referenced by any remaining elements
        self._removeelement(pelemtype=Modelelemtype.ORGU,
                            pcondition=lambda elem, ref: not (len(elem["references+"]) == 0
                                                              or set(elem["references+"]).intersection(ref)))
        # remove documents not referenced by any remaining elements
        self._removeelement(pelemtype=Modelelemtype.DOCU,
                            pcondition=lambda elem, ref: not (len(elem["references+"]) == 0
                                                              or set(elem["references+"]).intersection(ref)))

        return

    """ filters all entries out of reference-lists (all entries with a + at the end of the key"""

    @staticmethod
    def _filterreferences(pelements, pfilteredidlist):
        for elemkey, elem in pelements.items():
            for key in elem.keys():
                if ((key.endswith("+")
                        or key in ("entitiesmapped", "relationsmapped","attributesmapped"))
                    and type(elem[key]) in (set, list)):
                    try:
                        elem[key] = list(set(elem[key]).intersection(pfilteredidlist))
                        if key == "references+" and "referencecnt+" in elem:
                            elem["referencecnt+"] = len(elem[key]).__str__()
                    except:
                        # one value in the val-list is of structured type (dict), ignore the error
                        pass
        return

    def removeelements(self, pelements):
        # list of keys of that element to be removed (= all those not in the filtereslist
        for idx in range(len(pelements), 0, -1):  # loop ends with idx > final idx
            if pelements[idx - 1]["element"] not in self._filteredidlist:
                del pelements[idx - 1]
        # for
        return

    def removekeys(self, pelements):
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
        # for

        """ for all remaining diagrams, remove elements (arcs, attributes, entities, relationships)
           which are not to be shown
        """
        for diagkey, diag in self.getelements(Modelelemtype.DIAG).items():
            self.removekeys(pelements=diag["arcs"])
            self.removekeys(pelements=diag["relationships"])
            self.removeelements(pelements=diag["elements"]["attribute"])
            self.removeelements(pelements=diag["elements"]["entity"])
            # remove all diagrams having no more entity and not being in the diagram filterlist
            if len(diag["elements"]["entity"]) == 0 \
                    and diag["name"] not in nvl(self._imdiagram, []):
                self._filteredidlist.discard(diagkey)
        # for
        # remove all diagrams no longer in filteredliste
        diagkeys = list(self.getelements(Modelelemtype.DIAG).keys())
        for key in diagkeys:
            if key not in self._filteredidlist:
                del self.jsmodel["diagrams"][key]

        return
