import copy
import logging

from LOAD_MODELS.LOAD_MIRO import MiroFrame, MiroEntity, MiroRelation, MiroCard, MiroSticky, MiroArc, MiroInterface, MiroCategory
from SSOT_infra import nvl


class MiroBoardModel():
    """ contains the model and all its interpreted forms."""

    def __init__(self, mirointerface, board, framenames=None, reportback2miro=False, withload=True):
        assert (withload and (framenames is not None)) or not withload, \
            "need frame to load from miro, call MiroBoardModel with proper parameters"
        self._mirointerface: MiroInterface = mirointerface
        self._board = board
        self.reportback2miro = reportback2miro
        self._entities = []
        self._relations = []
        self._frames = []
        self._categories = []
        self._cards = []
        self._arcs = dict()
        self._itemtranslateids = {}

        if withload: self._selectmodelitems(framenames=framenames)
        return

    @property
    def boardid(self):
        return self._board["id"]

    @property
    def boardname(self):
        return self._board["name"]

    @property
    def boarddc(self):
        return self._board["createdAt"]

    @property
    def boarduc(self):
        return self._board["createdBy"]["name"]

    @property
    def boarddescr(self):
        return self._board["description"]

    def getitembyname(self, name, itemtype):
        items = []
        if itemtype == "frame":
            elems = self._frames
        elif itemtype == "category":
            elems = self._categories
        elif itemtype == "card":
            elems = self._cards
        elif itemtype == "relation":
            elems = self._frames + self._categories + self._cards + self._relations + self._entities
        elif itemtype == "entity":
            elems = self._entities
        else:
            raise Exception(f"Illegal item type {itemtype}")
        for elem in elems:
            if elem.name == name:
                items.append(elem)
        if len(items) == 0:
            return None
        elif len(items) > 1:
            raise Exception(f"Too many items found with name {name}")
        else:
            return items[0]

    def getitembyid(self, id):
        retval = None
        for elem in self._frames + self._categories + self._relations + self._entities + self._cards:
            if elem.id == id:
                retval = elem
        return retval

    def renameframes(self, framenames):
        frames = self._mirointerface._requestframes(boardid=self.boardid)
        retval = {}
        for f in frames:
            if f["data"]["title"] in framenames:
                retval[f["data"]["title"]] = {"x": f["position"]["x"],
                                              "y": f["position"]["y"]
                                              }

                self._mirointerface.updateframe(boardid=self.boardid, frameid=f["id"],
                                                title=f["data"]["title"] + "_old",
                                                x=f["position"]["x"], y=f["position"]["y"],
                                                color="#FFFFFF" if "style" not in f else f["style"]["fillColor"])

        return retval


    def _frameidisIM(self, frameid):
        return frameid in [f.id for f in self._frames]


    def _entiparentid(self, enti):
        parent = enti.get("parent")
        if parent is None:
            return None
        else:
            return parent["id"]


    def _isenti(self, enti):
        entidata = enti.get("data")
        if entidata is None: #shapes that are not supported
            return False
        return entidata["shape"] == MiroEntity.ELEMTYPE_ENTITY and \
               self._frameidisIM(self._entiparentid(enti))


    def _isproperrela(self,rela):
        retval = False
        if "startItem" in rela and "captions" in rela:
            if "position" in rela.get("startItem"):
                retval = True
            if "endItem" not in rela or ("position" in  rela.get("endItem")):
                retval = True
        if not retval:
            logging.error(f"malformed relation {rela.get('startItem'), rela.get('captions')}")
        return retval

    def _isrelation(self, rela):
        # connector has 2 endpoints and these are in the list of r
        if "startItem" in rela and \
                rela["startItem"]["id"] in self._itemtranslateids:
            # there is a starting point at an entity
            if "endItem" in rela and \
                    rela["endItem"]["id"] in self._itemtranslateids:
                isrela = self._isproperrela(rela)
            elif self._isproperrela(rela) and ("endItem" not in rela) and \
                    (len(rela["captions"]) == 2):
                # one entry but 2 captions treat this as recursive
                isrela = self._isproperrela(rela)
            else:
                isrela = False
        else:
            isrela = False
        return isrela


    def _handleduplicateentity(self, enti):
        """ if entity name already exists on the same frame, add X to it"""
        samenameentis = [compenti for compenti in self._entities
                         if compenti.name == enti.name and
                         compenti.id != enti.id]
        # I get at most 1 duplicate entity
        newentiframe = enti.frames[0]  # a new entity has exactly one frame as father
        if len(samenameentis) == 1:
            sameenti = samenameentis[0]

            if newentiframe.id in sameenti.getentityframeids():
                # I have duplicate on same frame
                logging.warning(f"Duplicate entity name '{enti.name}' " +
                                f"on frame '{newentiframe.name}'. Added X to it")
                if self.reportback2miro:
                    self._mirointerface.putsticky(boardid=self.boardid,
                                                  data=MiroSticky(parentid=newentiframe.id).duplicateentitysticky(
                                                      enti=enti))
                enti.name += 'X'
                enti = self._handleduplicateentity(enti)
            else:
                # I have duplicate on different frame, add  only frame of current enti to baseentity
                sameenti.frames.append(enti.frames[0])
                self._itemtranslateids[enti.id] = [sameenti.id, newentiframe.id]
                enti.frames[0].switchentity(oldentiid=enti.id, newenti=sameenti)
                enti = None  # enti is no longer needed
        else:
            # translate enti-id to itself
            self._itemtranslateids[enti.id] = [enti.id, newentiframe.id]

        return enti


    def _handleduplicateentities(self):
        locentities = copy.copy(self._entities)
        self._entities = []  # I rebuild original list with single shots
        for enti in locentities:
            enti = self._handleduplicateentity(enti)
            if enti is not None:
                self._entities.append(enti)
        return


    def createsupertypearcs(self):
        supertypes = set(e.superentiid for e in self._entities if e.superentiid is not None)
        for st in supertypes:
            arcid = f"{st}-ISAS-ARC"
            if arcid in self._arcs:
                logging.error(f"supertype arcid \"{arcid}\" already in arcs. This should not happen")
            self._arcs[arcid] = MiroArc(arcid=arcid, entiid=st, name=arcid)
        return

    def addsupertyperelas(self):
        """create an ISAS relation for all arcs of subtype-entities"""
        for arcid, arc in filter(lambda a : a[0].endswith("-ISAS-ARC") , self._arcs.items()):
            subentis = [enti for enti in self.entities() if enti.superentiid == arc.structarc()["entity"]]
            for enti in subentis:
                relaid = f"{arc.structarc()['entity']}-{enti.id}"
                rela = MiroRelation(relation={"id": relaid,
                                              "createdAt": enti.dc,
                                              "modifiedAt": enti.dm,
                                              "createdBy": {"id": None, "type": enti.uc},
                                              "modifiedBy": {"id": None, "type": enti.um},
                                              "style": {}
                                              },
                                    frame=enti.frames[0], #take first frame of entity
                                    fromenti=MiroRelation.structrelaend(entiid=self._translateid(enti.id),
                                                                      text='',
                                                                        mandatory=True,many=False,
                                                                        arc=None),
                                    toenti=MiroRelation.structrelaend(entiid=self._translateid(arc.structarc()['entity']),
                                                                      text='',
                                                                        mandatory=True,many=False,
                                                                      arc=arcid),

                                    )

                arc.addrelation(relaid)
                self._relations.append(rela)
        return

    def createarcsoutofrelations(self):
        for rela in self._relations:

            arcid,arcentiid = rela.toenti["arc"],rela.toenti["entiid"]
            if arcid is None:
                arcid, arcentiid = rela.fromenti["arc"], rela.fromenti["entiid"]

            if arcid is None: continue # no arc

            if arcid in self._arcs.keys():
                #add relation to existing arc
                self._arcs[arcid].addrelation(rela.id)
            else:
                #add Arc
                self._arcs[arcid] = MiroArc(arcid=arcid, entiid=arcentiid,
                                            name=arcid,
                                            relations=[rela.id])
        return


    def _selectmodelitems(self, framenames):
        self._frames = [MiroFrame(frame=f, createdBy=self.boarduc)
                        for f in self._mirointerface.getframes(boardid=self.boardid)
                        if f["data"]["title"] in framenames]
        shapes = self._mirointerface.getshapes(boardid=self.boardid)
        self._entities = [MiroEntity(entity=e, frame=self.getitembyid(self._entiparentid(e)), createdBy=self.boarduc)
                          for e in shapes if self._isenti(e)]

        # mark duplicate entities (on the same frame)
        # bring same entities from different frames together
        self._handleduplicateentities()

        # find superentities (entity in entity) within every frame and mark them properly
        MiroEntity.resolvesuperentities(self._frames)

        self._relations = [MiroRelation(relation=r,
                                        frame=self.getitembyid(self._translateframeid(r["startItem"]["id"])),
                                        enti1id=self._translateid(r["startItem"]["id"]),
                                        enti2id=None if "endItem" not in r else self._translateid(r["endItem"]["id"]),
                                        createdBy=self.boarduc)
                           for r in self._mirointerface.getconnectors(boardid=self.boardid) if self._isrelation(r)]

        self.createarcsoutofrelations()
        self.createsupertypearcs()
        self.addsupertyperelas()

        # get all tags from board
        self._tags = self._mirointerface._getalltags(boardid=self.boardid)

        #add all cards with entity-names,
        for cardname,card in self.getallcards().items():
            enti: MiroEntity = self.getitembyname(name=cardname,itemtype="entity")
            # test if card has name like an entity and entity is still without card
            if enti is None: continue
            if enti.card is not None:
                if self.reportback2miro:
                    entiframe = enti.frames[0]
                    self._mirointerface.putsticky(boardid=self.boardid,
                                                  data=MiroSticky(childid=entiframe.id,
                                                                  x=enti.x(entiframe),
                                                                  y=enti.y(entiframe)).duplicatecardsticky(
                                                      cardname=cardname))
            else:
                self._cards.append(card)
                enti.addcard(card)

                # add category derived from card
                catg = MiroCategory.getcatgfromtags(tags=card.gettags())
                if catg is not None:
                    if self.getitembyid(catg.id) is None:
                        self._categories.append(catg)  # add if none was found so far
                    enti.category = catg

        return


    def _translateid(self, itemid):
        retval = nvl(self._itemtranslateids.get(itemid)[0], itemid)
        return retval


    def _translateframeid(self, itemid):
        retval = nvl(self._itemtranslateids.get(itemid)[1], itemid)
        return retval


    def diagrams(self):
        return self._frames


    def creatediagram(self, title, x, y, width, height, color=None):
        return self._mirointerface.createframe(boardid=self.boardid, title=title,
                                               x=x, y=y, color=color, width=width, height=height)


    def categories(self):
        return self._categories


    def entities(self, diagid=None):
        return self._entities if diagid is None else self.getitembyid(diagid).getentities()


    def createentity(self, frameid, name, x, y, width, height, color, textalignh, textalignv):
        return self._mirointerface.createentity(boardid=self.boardid, frameid=frameid, name=name,
                                                x=x, y=y, color=color,
                                                width=width, height=height,
                                                textalignh=textalignh, textalignv=textalignv)


    def deleteentity(self, entiid):
        self._mirointerface._deleteshape(boardid=self.boardid, shapeid=entiid)
        return


    def relations(self, diagid=None):
        return self._relations if diagid is None else self.getitembyid(diagid).getrelations()

    def arcs(self):
        return self._arcs

    def createrelation(self, startitem, enditem, linetype="normal"):
        return self._mirointerface.createrelation(boardid=self.boardid,
                                                  startitem=startitem, enditem=enditem, linetype=linetype)


    def changerelation(self, relaid, data):
        return self._mirointerface._changeconnector(boardid=self.boardid, connectorid=relaid, data=data)


    def cards(self):
        return self._cards


    def getallcards(self):
        cards = dict()
        for c in self._mirointerface.getcards(boardid=self.boardid):
            card = MiroCard(c)
            if card.name in cards.keys():
                logging.warning(f"more than one card found with identical name {card.name}" +
                                "\nFirst used, rest ignored")
            else:
                card.settags(self._mirointerface.gettags(boardid=self.boardid, itemid=card.id))
                cards[card.name] = card
        # for

        return cards


    def createcard(self, card):
        return self._mirointerface.createcard(boardid=self.boardid, card=card)


    def updatecard(self, card):
        return self._mirointerface.updatecard(boardid=self.boardid, cardid=card.id,
                                              text=card.description, tags=card.gettags())
