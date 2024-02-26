import logging

from SSOT_db.IM_JSON import *
from SSOT_db.IM_OBJECTS import Relation
from SSOT_infra import striphtml, colorhex,multiline2spaceseparated,nvl


class MiroIMElement():
    ELEMTYPE_SHAPE = "shape"
    ELEMTYPE_FRAME = "frame"
    ELEMTYPE_CARD = "card"
    ELEMTYPE_TEXT = "text"
    ELEMTYPE_CONNECTOR = "connector"

    def __init__(self, imelement, **kwargs):
        self._imelement = imelement
        self._uc = kwargs.get("createdBy")
        self._dc = kwargs.get("createdAt")
        self._um = kwargs.get("modifiedBy")
        self._dm = kwargs.get("modifiedAt")
        return

    @property
    def mirostruct(self):
        return self._imelement

    @property
    def id(self):
        return self._imelement.get("id")

    @property
    def name(self):
        return striphtml(self._imelement.get("data").get("title"), keeplinebreaks=False)

    @property
    def uc(self):
        return self._uc if self._uc is not None else self._imelement.get("createdBy").get("name")

    @property
    def um(self):
        return self._um if self._um is not None else self._imelement.get("modifiedBy").get("name")

    @property
    def dc(self):
        return self._dc if self._dc is not None else self._imelement.get("createdAt")

    @property
    def dm(self):
        return self._dm if self._dm is not None else self._imelement.get("modifiedAt")

    def getgeometry(self):
        return self._imelement.get("geometry")

    def height(self):
        geom = self.getgeometry()
        return (geom["height"]) if geom else None

    def width(self):
        geom = self.getgeometry()
        return (geom["width"]) if geom else None

    def area(self):
        return self.width() * self.height() if self.getgeometry() else None

    def getposition(self):
        return self._imelement.get("position")

    @property
    def x(self):
        pos = self.getposition()
        return pos["x"] if pos else None

    @property
    def y(self):
        pos = self.getposition()
        return pos["y"] if pos else None


class MiroCard(MiroIMElement):
    def __init__(self, card, **kwargs):
        super().__init__(card, **kwargs)
        self._tags = []
        return

    def gettags(self):
        return self._tags

    def settags(self, tags):
        self._tags = tags

    @property
    def description(self):
        return striphtml(self._imelement["data"]["description"])


class MiroFrame(MiroIMElement):
    IMFRAME_START = "IM-"

    def __init__(self, frame, **kwargs):
        super().__init__(frame, **kwargs)
        self._entities = dict()
        self._relations = []
        return

    def renameframe(self, newname):
        return

    def addentity(self, enti, position, geometry):
        self._entities[enti.id] = [position, geometry, enti]
        return

    def addrelation(self, rela):
        self._relations.append(rela)
        return

    def getentities(self):
        return [frameenti[2] for frameenti in self._entities.values()]

    def getframeentityids(self):
        return [frameenti[2].id for frameenti in self._entities.values()]

    def getrelations(self):
        return self._relations

    def getentiposition(self, entiid):
        enti = self._entities.get(entiid)
        if enti is not None:
            return enti[0]
        else:
            return None

    def getentigeometry(self, entiid):
        enti = self._entities.get(entiid)
        if enti is not None:
            return enti[1]
        else:
            return None

    def switchentity(self, oldentiid, newenti):
        """ switch entity-ID's in list of entitygeometries in the frames entity list"""
        self._entities[newenti.id] = self._entities.pop(oldentiid)  # move entry to new key
        self._entities[newenti.id][2] = newenti  # replace enti-object in list
        return


class MiroEntity(MiroIMElement):
    ELEMTYPE_ENTITY = "round_rectangle"

    def __init__(self, entity, frame: MiroFrame, **kwargs):
        super().__init__(entity, **kwargs)
        frame.addentity(enti=self, position=super().getposition(), geometry=super().getgeometry())
        self._frames = [frame]  # backwards reference
        self._card = None
        self._category = None
        self._superentiid = kwargs.get("superentiid")
        return

    @property
    def superentiid(self):
        return self._superentiid

    @superentiid.setter
    def superentiid(self, val):
        self._superentiid = val

    @property
    def name(self):
        return striphtml(self._imelement.get("data").get("content"))

    @name.setter
    def name(self, val):
        self._imelement.get("data")["content"] = val

    def getposition(self, frame=None):
        if frame is not None:
            return frame.getentiposition(self.id)
        else:
            return super().getposition()

    def x(self, frame=None):
        if frame is not None:
            return self.getposition(frame).get("x") - self.width(frame) / 2
        else:
            return super().x

    def y(self, frame=None):
        if frame is not None:
            return self.getposition(frame).get("y") - self.height(frame) / 2
        else:
            return super().y

    def getgeometry(self, frame=None):
        if frame is not None:
            return frame.getentigeometry(self.id)
        else:
            return super().getgeometry()

    def height(self, frame=None):
        geom = self.getgeometry(frame)
        return (geom["height"]) if geom else None

    def width(self, frame=None):
        geom = self.getgeometry(frame)
        return (geom["width"]) if geom else None

    def area(self, frame=None):
        return self.width(frame) * self.height(frame) if self.getgeometry(frame) else None

    @property
    def frames(self):
        return self._frames

    def getentityframeids(self):
        return [frame.id for frame in self._frames]

    @property
    def description(self):
        if self._card is None:
            retval = None
        else:
            retval = self._card.description
        return retval

    @property
    def card(self):
        return self._card

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @property
    def fillcolor(self):
        color = None if self.category is None else self.category.fillcolor
        if color is None:
            color = getattr(self, "_fillcolor", None)
        return colorhex(color)

    @property
    def textalignh(self):
        return self._imelement.get("style").get("textAlign")

    @property
    def textalignv(self):
        return self._imelement.get("style").get("textAlignVertical")

    def addcard(self, card: MiroCard):
        if self._card is not None:
            raise Exception(f"only one card for Entity {self.name} allowed.")
        else:
            self._card = card

    @classmethod
    def resolvesuperentities(cls, frames):
        def size(enti, frame):
            return enti.area(frame)

        def includes(outerx, outery, outerwidth, outerheight,
                     innerx, innery, innerwidth, innerheight):
            return outerx <= innerx and outery <= innery and \
                   (outerx + outerwidth) >= (innerx + innerwidth) and \
                   (outery + outerheight) >= (innery + innerheight)

        def encirclingenti(frame, enti, superentis):
            mysuperenti = None
            for supent in superentis:
                if includes(outerx=supent.x(frame=frame), outery=supent.y(frame=frame),
                            outerwidth=supent.width(frame=frame), outerheight=supent.height(frame=frame),
                            innerx=enti.x(frame=frame), innery=enti.y(frame=frame),
                            innerwidth=enti.width(frame=frame), innerheight=enti.height(frame=frame)
                            ):
                    mysuperenti = supent
                    break
            # for
            return mysuperenti

        for frame in frames:
            # sort entities by size, start with largest
            sizedentities = [[size(enti, frame), enti] for enti in frame.getentities()]
            sizedentities.sort(key=lambda e: e[0], reverse=True)

            supercandidates = []  # all entities larger than myself
            for enti in sizedentities:
                if enti[1].superentiid is not None:
                    continue  # skip entity if already hast superentity
                # find entities surrounding  current entitiy
                superenti = encirclingenti(frame=frame, enti=enti[1], superentis=supercandidates)
                # found, mark current attrs superentitiy
                if superenti is not None:
                    enti[1].superentiid = superenti.id
                    # print (enti[1]["name"],superenti["name"])
                supercandidates.append(enti[1])
        return


class MiroRelation(MiroIMElement):
    def __init__(self, relation, frame:MiroFrame, enti1id=None, enti2id=None,
                 fromenti=None, toenti=None, **kwargs):
        super().__init__(relation, **kwargs)

        self._frame = frame
        startcap = relation["style"].get("startStrokeCap")
        endcap = relation["style"].get("endStrokeCap")
        arcno1, arcno2, caption1, caption2 = self.resolvecaptions(relation.get("captions"))

        # either entiid's are delivered and I fill the end's structure or the end's structure is given
        self.fromenti = fromenti
        if self.fromenti is None:
            arcname = None if arcno1 is None else f"{enti1id}-ARC-{arcno1}"

            #fill fromenti with basic information
            self.fromenti = self.structrelaend(entiid=enti1id,
                                               text=caption1,
                                               position=self.miropos2int(relation["startItem"]["position"]),
                                               mandatory=self.mandatory(cap=endcap,
                                                                        strokestyle=relation["style"].get(
                                                                            "strokeStyle")),
                                               many=endcap is not None and "many" in endcap,
                                               arc=arcname
                                               )
        self.toenti = toenti
        if self.toenti is None:
            if enti2id is None:
                # treat this as recursive relationship
                targetentiid = self.fromenti["entiid"]
                position = {"x": self.fromenti["position"]["y"],
                            "y": self.fromenti["position"]["x"],
                            "edge":self.fromenti["position"]["edge"],
                            "percentage":self.fromenti["position"]["percentage"]
                            }  # switch positions from start to end
            else:
                # we have an endItem, use it's data
                targetentiid = enti2id
                position = self.miropos2int(relation["endItem"]["position"])
            arcname = None if arcno2 is None else f"{targetentiid}-ARC-{arcno2}"

            self.toenti = self.structrelaend(entiid=targetentiid,
                                             text=caption2,
                                             position=position,
                                             mandatory=self.mandatory(cap=startcap,
                                                                      strokestyle=relation["style"].get("strokeStyle")),
                                             many=startcap is not None and "many" in startcap,
                                             arc=arcname
                                             )

            """style attribute     "textOrientation": "horizontal","""

        if frame is not None:
            frame.addrelation(self)
        return

    @classmethod
    def resolvecaptions(cls,captions):
        def resolveoneend(firstcontent,secondcontent):
            if arccaption.match(firstcontent):
                arcno = len(firstcontent)
                caption = secondcontent
            else:
                arcno = None
                caption = firstcontent
            #replace \n by blanks and remove blanks at ent
            return arcno,multiline2spaceseparated(caption).strip()

        arccaption = re.compile("/+")

        #create dummy captions if captions are missing
        if captions is None or len(captions) == 0:
            captions = [{"content": "?????","position":"10%"}]
        if len(captions) < 2:
            captions.append({"content": "?????","position":"90%"})

        captions.sort(key=lambda x:float(x["position"].strip("%")))

        #resolve startedge --text-----  or --))--text-----
        arcno1,caption1 = resolveoneend (firstcontent=striphtml(captions[0]["content"]),
                                             secondcontent=striphtml(captions[1]["content"]))
        # resolve endedge -----text--  or -----text--((--
        arcno2,caption2 = resolveoneend (firstcontent=striphtml(captions[-1]["content"]),
                                             secondcontent=striphtml(captions[-2]["content"]))

        return arcno1,arcno2,caption1,caption2

    @property
    def uc(self):
        return self._imelement.get("createdBy").get("type")

    @property
    def um(self):
        return self._imelement.get("modifiedBy").get("type")

    @classmethod
    def mandatory(cls, cap, strokestyle):
        return not (strokestyle != "normal" or "zero" in cap or "oval" in cap)

    def _position2edgeposition(self, xpercent, ypercent):
        if nvl(xpercent,0) <= 5:
            edge=Linesegment.WEST
            percentage=ypercent
        elif xpercent >= 95:
            edge = Linesegment.EAST
            percentage=ypercent
        elif nvl(ypercent,0) <= 5:
            edge = Linesegment.NORTH
            percentage=xpercent
        elif ypercent >= 95:
            edge = Linesegment.SOUTH
            percentage=xpercent
        else:
            logging.error(f"illegal combination of relationship ({self.name}) position percentages {xpercent},{ypercent}")
            edge=None
            percentage=None
        return (edge,percentage)

    @classmethod
    def relaxposition(cls, edge, percentage):
        if edge == Linesegment.SOUTH:
            return percentage
        elif edge == Linesegment.NORTH:
            return percentage
        elif edge == Linesegment.WEST:
            return 0
        else:
            return 100

    @classmethod
    def relayposition(cls, edge, percentage):
        if edge == Linesegment.SOUTH:
            return 100
        elif edge == Linesegment.NORTH:
            return 0
        elif edge == Linesegment.WEST:
            return percentage
        else:
            return percentage

    def miropos2int(self, miropos):
        """return int for percentage 100% or 0.0%
            in a structure {"x":100,"y":50.0}
        """
        x=float(miropos["x"][:-1])
        y=float(miropos["y"][:-1])
        edge,percentage=self._position2edgeposition(xpercent=x, ypercent=y)
        retval = {"x": x,
                  "y": y,
                  "edge":edge,
                  "percentage":percentage
                  }
        return retval

    @classmethod
    def structrelaend(cls, entiid, text='', position=dict(), mandatory=True, many=False, arc=None):
        return {"text": text,
                "entiid": entiid,
                "position": position,
                "mandatory": mandatory,
                "many": many,
                "arc": arc}

    @property
    def name(self):
        item=self._imelement.get('startItem')
        if item is not None:
            elemid=item.get("id")
        else: elemid = "?id?"
        captions=self._imelement.get('captions')
        if captions is not None:
            captext=" / ".join(v["content"] for v in captions)
        else: captext = "? / ?"

        return f"RELA: ({self._imelement.get('id')}, Elemid=({elemid}), captions={captext} "

    @property
    def frame(self):
        return self._frame
    
    def relatype(self):
        if self.toenti["many"] and self.fromenti["many"]:
            retval = Relation.MANY2MANY  # both are many
        elif self.toenti["many"] or self.fromenti["many"]:
            retval = Relation.MANY2ONE  # at least one is many
        elif self.toenti["mandatory"] and self.fromenti["mandatory"] and \
                (self.toenti["arc"] is not None or self.fromenti["arc"] is not None):
            # 1:1 both mandatory, one end in Arc
            retval = Relation.ISASUBTYPE
        elif self.toenti["mandatory"] != self.fromenti["mandatory"] \
                and (self.fromenti.get("text") in ROLEASSOCIATIONS
                     and self.toenti.get("text") in ROLEASSOCIATIONS
                ):
            # 1:1 and at exactly one mandatory and labels are "is" or empty
            retval = Relation.ISAROLE
        else:
            retval = Relation.ONE2ONE
        return retval

    @classmethod
    def relaerdtype(cls, many, mandatory, oppositemand=None):
        """ if both sides are not mandatory, don't  put circles
            as line will be dashed
        """
        if many:
            if not mandatory and nvl(oppositemand, True):
                return "erd_zero_or_many"
            else:
                return "erd_many"
        else:
            if not mandatory and nvl(oppositemand, True):
                return "oval"
            else:
                return "none"

    @classmethod
    def relalinetype(cls, mandatory):
        return "normal" if mandatory else "dashed"


class MiroCategory(MiroIMElement):
    def __init__(self, catg, **kwargs):
        super().__init__(catg, **kwargs)
        return

    @property
    def name(self):
        return self._imelement.get("title")

    @property
    def fillcolor(self):
        return colorhex(self._imelement.get("fillColor"))

    @classmethod
    def getcatgfromtags(cls, tags):
        if len(tags) == 0:
            return None
        else:
            if len(tags) > 1:
                logging.warning(
                    f"too many tags in card found. First used, rest ignored '{','.join([t['title'] for t in tags])}'")
            return MiroCategory(catg=tags[0])


class MiroSticky():
    def __init__(self, text='', x=None, y=None, size=40, parentid=None, color="light_yellow"):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.parentid = parentid
        self.color = color
        return

    def stickystruct(self):
        stickynote = {
            "data": {
                "shape": "square",
                "content": self.text,
            },
            "style": {
                "fillColor": self.color,
                "textAlign": "center",
                "textAlignVertical": "middle"
            },
            "geometry": {
                "height": self.size
            },
        }
        if self.x is not None and self.y is not None:
            stickynote["position"] = {
                "origin": "center",
                "x": self.x,
                "y": self.y
            }
        if self.parentid is not None:
            stickynote["parent"] = {
                "id": self.parentid
            }

        return stickynote

    def duplicateentitysticky(self, enti: MiroEntity):
        self.text = f"Entity name duplicate {enti.name}"
        self.x = enti.x() + 30
        self.y = enti.y() + 30
        self.size = 40
        return self.stickystruct()

    def duplicatecardsticky(self, cardname):
        self.text = f"Duplicate description-Card for Entity {cardname} ignored"
        self.size = 40
        return self.stickystruct()


class MiroArc(MiroIMElement):
    """ on miro there are no arcs. they are generated on the fly"""

    def __init__(self, arcid, entiid, name, relations=None):
        super().__init__(imelement={"id": arcid})
        self._entiid = entiid
        self._name = name
        self._relations = nvl(relations, list())

    @property
    def name(self):
        return self._name

    def addrelation(self,rela):
        self._relations.append(rela)

    def structarc(self):
        return {"id": self.id, "name": self.name, "entity": self._entiid, "relations+": self._relations}
