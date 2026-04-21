import json
import logging
from datetime import datetime
from pathlib import Path

from IM_STANDARD import JsonSchema, nvl


class DiagramLayout:
    DIAGMINWIDTH = 300.0
    DIAGMINHEIGHT = 200.0
    ENTITYWIDTH = 170.0
    ENTITYHEIGHT = 110.0
    CATEGORYWIDTH = 250.0
    CATEGORYHEIGHT = 30.0
    ENTITYGAP = 30.0
    STARTY = 30.0
    STARTX = 30.0

    def __init__(self, entitycnt):
        self.diagwidth = self.DIAGMINWIDTH
        self.diagheight = self.DIAGMINHEIGHT
        self.gridwidth = self._hcount(entitycnt)
        self.gridh = self.gridv = 1
        self.startx = self.STARTY
        self.starty = self.STARTX

        return

    @staticmethod
    def _hcount(enticnt):
        from math import sqrt
        return max(round(sqrt(enticnt) * 0.6), 3)

    def _incgridv(self, gap, heigth=0):
        self.gridh = 1
        self.gridv += 1
        self.startx = gap
        self.diagheight = max(self.diagheight, self.starty + heigth + gap)
        self.starty += heigth + gap
        return

    def _nextbox(self, width, heigth, gap):
        self.diagwidth = max(self.diagwidth, self.startx + width + gap)
        self.startx += width + gap
        self.gridh += 1
        if self.gridh > self.gridwidth:
            self._incgridv(gap=gap, heigth=heigth)
        return

    def _nextentity(self):
        self._nextbox(width=self.ENTITYWIDTH, heigth=self.ENTITYHEIGHT, gap=self.ENTITYGAP)
        return

    def _nextcatg(self):
        self._nextbox(width=self.CATEGORYWIDTH, heigth=self.CATEGORYHEIGHT, gap=self.ENTITYGAP)
        return


class GenericUiRessource():
    def __init__(self, stdmodel, destjson=None):
        self._stdmodel = stdmodel
        self._destjson = destjson
        self._lang = None
        self._defaultlang = None
        self.destentities = []
        self.destrelationships = []
        self.destcategories = []
        self.destsystems = []
        self.destdataflows = []
        return

    def _mlvalue(self, value):
        return JsonSchema._mlvalue(value=value, lang=self._lang, defaultlang=self._defaultlang)

    def modeljson(self, modelid, name, ui, **kwargs):
        assert False, f"function must be implemented in subobject"

    def _getitems(self, elements: list, condition):
        return [e for e in elements if condition(e)]

    def catgjson(self, catgid, name, ui, **kwargs):
        assert False, f"function must be implemented in subobject"

    def entijson(self, entityid, name, ui, **kwargs):
        assert False, f"function must be implemented in subobject"

    def relajson(self, relaid, name, ui, **kwargs):
        assert False, f"function must be implemented in subobject"

    def uijson(self, id, name, ui, **kwargs):
        assert False, f"function must be implemented in subobject"

    def relaendjson(self, id, name, ui, **kwargs):
        assert False, f"function must be implemented in subobject"


class UiRessource(GenericUiRessource):

    def __init__(self, stdmodel, destjson=None):
        super().__init__(stdmodel=stdmodel, destjson=destjson)
        return

    def _getdestelements(self, elementname, condition):
        if self._destjson is None:
            return []
        return self._getitems(elements=self._destjson.get("elements").get(elementname, list()),
                              condition=condition)

    def _getdestelement(self, elementname, condition):
        if self._destjson is None:
            retval = []
        else:
            retval = self._getdestelements(elementname=elementname, condition=condition)
        if len(retval) == 0:
            return None
        if len(retval) == 1:
            return retval[0]
        raise Exception("too many entries found")

    def _existselement(self, elementname, name, link):
        return self._getdestelement(elementname=elementname,
                                    condition=lambda x: (x.get("name") == name or
                                                         x.get("srclink") == link
                                                         )
                                    ) is not None

    def _updatecatgui(self):
        catgbyname = dict() if self._destjson is None \
            else {catg.get("name"): catg for catg in self._destjson.get("elements", dict()).get("categories", [])}
        for catg in self.destcategories:
            try:
                samelink = self._getdestelement("categories",
                                                lambda e: e.get("srclink") ==
                                                          self._href(catg)
                                                )
                if samelink is None:
                    # handle not yet linked element
                    # check wether the name is already here
                    samelink = catgbyname.get(self._mlvalue(catg.get("name")))
                    if samelink is not None:
                        # the name was found:
                        if samelink.get("srclink") is None:
                            # found category with same name but not yet an src link
                            # mark it as dataspot entiry
                            samelink["srclink"] = self._href(catg)
                        # else:
                        #     logging.warning(f'category name present with different dataspot link: {byname.get("name")}')
                else:
                    # handle linked element
                    samelink["name"] = self._mlvalue(catg.get("name"))

                samelink["dm"] = str(datetime.now())
                samelink["um"] = "generated"
                self.diaglayout.starty = max(self.diaglayout.starty, float(samelink.get("ui", dict()).get("height")))
            except:
                logging.error(
                    f'multiple categories for the same datatspot link: {self._href(catg)}')
        return

    def _updateentiui(self):
        entibyname = dict() if self._destjson is None \
            else {enti.get("name"): enti for enti in self._destjson.get("elements", dict()).get("elements")}
        for enti in self.destentities:
            try:
                samelink = self._getdestelement("entities",
                                                lambda e: e.get("srclink") ==
                                                          self._href(enti)
                                                )
                if samelink is None:
                    # handle not yet linked element
                    # check wether the name is already here
                    samelink = entibyname.get(self._mlvalue(enti.get("name")))
                    if samelink is not None:
                        # the name was found:
                        if samelink.get("srclink") is None:
                            # found category with same name but not yet an src link
                            # mark it as dataspot entiry
                            samelink["elementid"] = self._structid(enti)
                            samelink["srclink"] = self._href(enti)
                        else:
                            logging.warning(f'entity name present with different dataspot link: {samelink.get("name")}')
                else:
                    # handle linked element
                    samelink["name"] = self._mlvalue(enti.get("name"))
                samelink["dm"] = str(datetime.now())
                samelink["um"] = "generated"
                self.diaglayout.starty = max(self.diaglayout.starty, float(samelink.get("ui", dict()).get("height")))

            except:
                logging.error(
                    f'multiple entities for the same datatspot link: {self._href(enti)}')
        return

    def _updaterelaui(self):
        relabyname = dict() if self._destjson is None \
            else {self._relaname(rela): rela for rela in
                  self._destjson.get("elements", dict()).get("relationships", [])}
        for rela in self.destrelationships:
            try:
                samelink = self._getdestelement("relationships",
                                                lambda e: e.get("srclink") ==
                                                          self._href(rela))
                if samelink is None:
                    # handle not yet linked element
                    # check wether the name is already here
                    samelink = relabyname.get(self._relaname(rela))
                    if samelink is not None:
                        # the name was found:
                        if samelink.get("srclink") is None:
                            # found realtioship with same name but not yet an src link
                            # mark it as dataspot entiry
                            samelink["elementid"] = self._structid(rela)
                            samelink["srclink"] = self._href(rela)
                            samelink["dm"] = str(datetime.now())
                            samelink["um"] = "generated"
                        else:
                            logging.warning(
                                f'relationship name present with different dataspot link: {samelink.get("name")}')
                else:
                    # handle linked element
                    samelink["name"] = self._mlvalue(rela.get("name"))
                    samelink["dm"] = str(datetime.now())
                    samelink["um"] = "generated"
            except Exception as exp:
                logging.error(
                    f'multiple relationships for the same datatspot link: {self._href(rela)}')
        return

    def _catgsui(self):
        catgs = []
        donecatg = False
        for catg in self.destcategories:
            # skip createion if already in destination
            if not self._existselement(elementname="categories",
                                       name=self._mlvalue(catg.get("name")),
                                       link=self._href(catg)):
                category = self.catgjson(
                    catgid=self._structid(catg),
                    name=self._mlvalue(catg.get("name")),
                    pos_x=self.diaglayout.startx,
                    pos_y=self.diaglayout.starty,
                    srclink=self._href(catg),
                    ui=self.uijson(
                        width=DiagramLayout.CATEGORYWIDTH,
                        height=DiagramLayout.CATEGORYHEIGHT
                    )
                )
                catgs.append(category)
                self.diaglayout._nextcatg()
                logging.info(f'category "{category.get("name")}" added')
                donecatg = True

        if donecatg and self.diaglayout.gridh > 1:
            # add gap after last category, if line is not full
            self.diaglayout._incgridv(gap=self.diaglayout.ENTITYGAP,
                                      heigth=self.diaglayout.CATEGORYHEIGHT)
        return catgs

    def _linktods(self, url, name):
        return f"<p><a href=\"{url}\">{name}</a></p>"

    def _relaend(self, card: str, mand: bool):
        endshapes = {"MT": "erd_many",
                     "1F": "oval",
                     "MF": "erd_zero_or_many",
                     "1T": "none"}
        return endshapes[card + ("T" if mand else "F")]

    def _entitiesui(self):
        entities = []
        for enti in self.destentities:
            # skip createion if already in destination
            if not self._existselement(elementname="entities",
                                       name=self._mlvalue(enti.get("name")),
                                       link=self._href(enti)):
                entity = self.entijson(entityid=self._structid(enti),
                                       name=self._mlvalue(enti.get("name")),
                                       displname=self._linktods(url=self._href(enti),
                                                                name=self._mlvalue(enti.get("name"))),
                                       elemtype="Entity",
                                       examples=enti.get("examples"),
                                       pos_x=self.diaglayout.startx,
                                       pos_y=self.diaglayout.starty,
                                       srclink=self._href(enti),
                                       ui=self.uijson(width=DiagramLayout.ENTITYWIDTH,
                                                      height=DiagramLayout.ENTITYHEIGHT
                                                      )
                                       )
                entities.append(entity)
                self.diaglayout._nextentity()
                logging.info(f'Entität "{entity.get("name")}" hinzugefügt')

        return entities

    def _systemsui(self):
        systems = []
        for syst in self.destsystems:
            parts = syst.split("/")
            # skip createion if already in destination
            if not self._existselement(elementname="systems",
                                       name=parts[-1],
                                       link=None):
                system = self.entijson(entityid=syst,
                                       name=parts[-1],
                                       pos_x=self.diaglayout.startx,
                                       pos_y=self.diaglayout.starty,
                                       srclink=None,
                                       ui=self.uijson(width=DiagramLayout.ENTITYWIDTH,
                                                      height=DiagramLayout.ENTITYHEIGHT
                                                      )
                                       )
                systems.append(system)
                self.diaglayout._nextentity()
                logging.info(f'System "{syst}" hinzugefügt')

        return systems

    def _dataflowsui(self):
        dataflows = []
        for syst in self.destdataflows:
            pass

        return dataflows

    def _getentity(self, entiid):
        enti = [e for e in self.destentities if e.get("elementid") == entiid]
        return enti[0] if len(enti) == 1 else None

    def _getentity_dest(self, entiid, entiname=None):
        enti = [e for e in self._destjson.get("elements", {}).get("entities", [])
                if e.get("elementid") == entiid or
                e.get("miroid") == entiid or
                entiname == e.get("name")]
        return enti[0] if len(enti) == 1 else None

    def _structid(self, struct):
        return struct.get("additionalProps", dict()).get("SOURCE-ID", struct.get("elementid"))

    def _href(self, struct):
        return struct.get("additionalProps", dict()).get("SOURCE-HREF")

    def _getentityname(self, entiid):
        enti = self._getentity(entiid=entiid)
        if enti is None:
            enti = self._getentity_dest(entiid)
        return self._mlvalue(enti.get("name")) if enti is not None else None

    def _relaendui(self, relaend, edge):
        edgeval = lambda d, v: v if d == "E" else 100 - v
        relaendui = self.relaendjson(
            entityid=self._structid(self._getentity(relaend.get("entityid"))),
            edge=edge,
            position=50,
            connector=relaend.get("cardinality"),
            mandatory=relaend.get("mandatory"),
            captiontext=self._mlvalue(value=relaend.get("assoctext")),
            captionposition=edgeval("E", 15)
        )

        if "arcnumber" in relaend:
            relaendui["arc"] = {"no": relaend.get("arcnumber"),
                                "position": edgeval("E", 5)}
        return relaendui

    def _relaname(self, rela):
        """ build a 'name' for a relation
            enti-name1->assoc from to->enti-name2
            """
        fwd = rela.get("fwd")
        bwd = rela.get("bwd")
        fwdname = fwd.get("entity") if "entity" in fwd else self._getentityname(
            fwd.get("entityid"))  # depends what sourcejson
        bwdname = bwd.get("entity") if "entity" in bwd else self._getentityname(
            bwd.get("entityid"))  # depends what sourcejson
        fwdcaption = self._mlvalue(fwd.get("assoctext")) if "assoctext" in fwd else fwd.get("caption", {}).get("text")
        return f'{fwdname}->{fwdcaption}->{bwdname}'

    def _captions(self, fwd: dict, bwd: dict):
        captions = []
        fwdarc = fwd.get("arcnumber")
        startpos = 15
        endpos = 85
        if fwdarc:
            captions.append({"content": "/" * int(fwdarc), "position": startpos})
            startpos += 15
        if self._mlvalue(bwd.get("assoctext")) in (None, ""):
            startpos = 50  # only one text

        captions.append({"content": self._mlvalue(fwd.get("assoctext")), "position": startpos})

        bwdarc = bwd.get("arcnumber")
        if bwdarc:
            captions.append({"content": "/" * int(bwdarc), "position": endpos})
            endpos -= 15

        if self._mlvalue(bwd.get("assoctext")) not in (None, ""):
            # two texts
            captions.append({"content": self._mlvalue(bwd.get("assoctext")), "position": endpos})
        return captions

    def _relationsui(self):
        relations = []
        for rela in self.destrelationships:
            if not self._existselement(elementname="relationships",
                                       name=self._relaname(rela),
                                       link=self._href(rela)
                                       ):
                # TODO Subtype relations are not on a project in dataspot how to capture them anyway
                fwd, bwd = rela.get("fwd"), rela.get("bwd")

                """                  "caption": {
                      "text": kwargs.get("captiontext"),
                      "position": kwargs.get("captionposition")
                  }"""
                relation = self.relajson(relaid=self._structid(rela),
                                         name=self._relaname(rela),
                                         fromElement=self._structid(self._getentity(fwd.get("entityid"))),
                                         toElement=self._structid(self._getentity(bwd.get("entityid"))),
                                         startposition={"x": 50, "y": 100},
                                         endposition={"x": 0, "y": 50},
                                         captions=self._captions(fwd=fwd, bwd=bwd),
                                         shape="elbowed",
                                         style={
                                             "startStrokeCap": self._relaend(card=fwd.get("cardinality"),
                                                                             mand=fwd.get("mandatory")),
                                             "endStrokeCap": self._relaend(card=bwd.get("cardinality"),
                                                                             mand=bwd.get("mandatory")),
                                             "strokeWidth": "1.0",
                                             "strokeStyle": "normal",
                                             "strokeColor": "#000000",
                                             "color": "#1a1a1a",
                                             "textOrientation": "horizontal",
                                             "fontSize": "10"
                                         },
                                         fwd=self._relaendui(relaend=fwd, edge="E"),
                                         bwd=self._relaendui(relaend=bwd, edge="W")
                                         )
                relations.append(relation)
                logging.info(f'Beziehung "{relation.get("name")}" hinzugefügt')

        return relations

    def _checkproblems(self):
        """
        Params:
         List of elements chosen for this miro frame

        check: no duplicates for
            Entitiies (name,srclink)
            Categories (name,srclink)
            Relations (fwd caption, from entitiy (name) and to entity (name)
        list of names in dest, no longer in source
        :return: logging of warnings and errors
        """
        srcentinames = [self._mlvalue(e.get("name")) for e in self.destentities]
        srccatgnames = [self._mlvalue(e.get("name")) for e in self.destcategories]
        srcrelas = [self._relaname(e) for e in self.destrelationships]
        srcentilinks = [self._href(e) for e in self.destentities]
        srccatglinks = [self._href(e) for e in self.destcategories]

        destentinames = [e.get("name") for e in self._destjson.get("elements").get("entities", [])]
        destcatgnames = [e.get("name") for e in self._destjson.get("elements").get("categories", [])]
        destrelas = [self._relaname(e) for e in self._destjson.get("elements").get("relationships", [])]
        destentilinks = [e.get("srclink") for e in self._destjson.get("elements").get("entities", []) if "srclink" in e]
        destcatglinks = [e.get("srclink") for e in self._destjson.get("elements").get("categories", []) if
                         "srclink" in e]
        destrelalinks = [e.get("srclink") for e in self._destjson.get("elements").get("relationships", []) if
                         "srclink" in e]

        for n in list(set([name for name in destentinames if destentinames.count(name) > 1])):
            if n is not None: logging.warning(f'Duplicate entity name in destination "{n}"')
        for n in list(set([name for name in destcatgnames if destcatgnames.count(name) > 1])):
            if n is not None: logging.warning(f'Duplicate category name in destination "{n}"')
        for n in list(set([name for name in destentilinks if destentilinks.count(name) > 1])):
            if n is not None: logging.warning(f'Duplicate entity dataspotlink in destination "{n}"')
        for n in list(set([name for name in destcatglinks if destcatglinks.count(name) > 1])):
            if n is not None: logging.warning(f'Duplicate category dataspotlink in destination "{n}"')
        for n in set(destentilinks).difference(srcentilinks):
            logging.warning(f'dataspotlink in destination entity but no longer in source "{n}"')
        for n in set(destentinames).difference(srcentinames):
            logging.warning(f' destination entity no longer in source "{n}"')
        for n in set(destcatglinks).difference(srccatglinks):
            logging.warning(f'dataspotlink in destination category but no longer in source "{n}"')
        for n in set(destcatgnames).difference(srccatgnames):
            logging.warning(f' destination category no longer in source "{n}"')

        return

    def modeljson(self, modelid, name, **kwargs):
        retval = {"elementid": modelid,
                  "name": name,
                  "type": "Entity"}
        for key, val in kwargs.items():
            retval[key] = val
        return retval

    def catgjson(self, catgid, name, ui, **kwargs):
        retval = {"elementid": catgid,
                  "name": name,
                  "pos_x": kwargs.get("pos_x"),
                  "pos_y": kwargs.get("pos_y"),
                  "srclink": kwargs.get("srclink"),
                  "ui": ui
                  }
        return retval

    def entijson(self, entityid, name, ui, **kwargs):
        retval = {
            "elementid": entityid,
            "name": name
        }
        for key, val in kwargs.items():
            if key == "index":
                val = nvl(val, 0)
            if key == "displname":
                val = nvl(val, name)
            retval[key] = val
        retval["ui"] = ui
        return retval

    def relajson(self, relaid, name, fwd, bwd, **kwargs):
        retval = {
            "elementid": relaid,
            "name": name,
            "fwd": fwd,
            "bwd": bwd
        }
        for key, val in kwargs.items():
            if key == "index":
                val = nvl(val, 0)
            if key == "displname":
                val = nvl(val, name)
            retval[key] = val
        return retval

    def uijson(self, width, height, **kwargs):
        retval = {
            "width": width,
            "height": height,
            "opacity": kwargs.get("opacity", "1.0"),
            "color": kwargs.get("color", "a4e1ff"),
            "marginwidth": kwargs.get("marginwidth", 2),
            "marginopacity": kwargs.get("marginopacity", 0),
            "margincolor": kwargs.get("margincolor", "0000ff"),
            "fontsize": kwargs.get("fontsize", 14),
            "fontcolor": kwargs.get("fontcolor", "0000ff")
        }
        return retval

    def relaendjson(self, entityid, edge, connector, mandatory, **kwargs):
        retval = {"entityid": entityid,
                  "entity": self._getentityname(id),
                  "edge": edge,
                  "position": kwargs.get("position", 50),
                  "connector": connector,
                  "mandatory": mandatory,
                  "caption": {
                      "text": kwargs.get("captiontext"),
                      "position": kwargs.get("captionposition")
                  }
                  }
        return retval

    def generate_uiressource(self, diagname: str,
                             uitype,
                             lang=None,
                             injson=None) -> dict:

        mainlang = self._stdmodel.get("ModelInfo").get("mainlanguage")
        self._lang = nvl(lang, mainlang)
        # set defaultlanguage for replacement of missing translations
        if self._lang == mainlang:
            self._defaultlang = None
        else:
            self._defaultlang = mainlang

        self._destjson = injson

        # get one and only diagram
        diagrams = [diag for diag in self._stdmodel.get("Diagrams", []) if diag.get("name") == diagname]
        assert len(diagrams) == 1, f"Diagram '{diagname} not found in standard json"
        diagram = diagrams[0]

        self.destentities = [elem for elem in self._stdmodel.get("Entities", []) if
                             elem.get("elementid") in diagram.get("elements")]
        self.destrelationships = [elem for elem in self._stdmodel.get("Relations", []) if
                                  elem.get("elementid") in diagram.get("elements")]
        self.destcategories = [elem for elem in self._stdmodel.get("Categories", []) if elem.get("elementid") in \
                               [enti.get("categoryid") for enti in self.destentities]]
        self.destsystems = [elem for elem in self._stdmodel.get("Systems", []) if
                            elem.get("elementid") in diagram.get("elements")] + \
                           [elem[len("Systems:"):] for elem in diagram.get("elements") if elem.startswith("Systems:")]

        self.destdataflows = [elem for elem in self._stdmodel.get("Systems", []) if
                              elem.get("elementid") in diagram.get("elements")] + \
                             [elem[len("Systems:"):] for elem in diagram.get("elements") if elem.startswith("Systems:")]
        self.diaglayout = DiagramLayout(entitycnt=max(len(self.destentities), len(self.destsystems)))
        if self._destjson is None:
            self._destjson = self.modeljson(modelid=self._structid(diagram),
                                            name=diagram.get("name"),
                                            width=DiagramLayout.DIAGMINWIDTH,
                                            height=DiagramLayout.DIAGMINHEIGHT,
                                            dc=str(datetime.now()),
                                            srclink=self._href(diagram),
                                            elements={"categories": [],
                                                      "elements": [],
                                                      "relationships": []
                                                      }
                                            )
        else:
            assert self._destjson["name"] == diagram.get("name"), \
                f'diagram names do not match {self._destjson["name"]} != {diagram.get("name")}'
            self.diaglayout.diagwidth = self._destjson.get("width")
            self.diaglayout.diagheight = self._destjson.get("height")
            self._destjson["dm"] = str(datetime.now())
            self._destjson["srclink"] = self._href(diagram)

        self._checkproblems()
        # existingcags=c.get("name")[self._destjson["elements"]["categories"]
        self._updatecatgui()
        self._updateentiui()
        self._updaterelaui()
        # TODO self._updatesystui()
        # TODO self._updatedataflowui()
        # add new categories and entities to destjson

        # new elements below the existing ones
        if self.diaglayout.starty > self.diaglayout.STARTY:
            self.diaglayout.starty += self.diaglayout.CATEGORYHEIGHT

        if "categories" in self._destjson["elements"]:
            self._destjson["elements"]["categories"].extend(self._catgsui())
        self._destjson["elements"]["elements"].extend(self._entitiesui())
        self._destjson["elements"]["relationships"].extend(self._relationsui())

        self._destjson["width"] = self.diaglayout.diagwidth
        self._destjson["height"] = self.diaglayout.diagheight
        return self._destjson


def creatediagramui(infile, diagname, outfile=None, lang=None):
    """
    create an outfile with user interace content
    infile: filepath of json standard file
    diagname: Name of the diagram to output
    outfile: filepath for output. Defulat: infile with "-ui" added to name
    lang: Languagecode for texts. Default mainlanguage of the standardjson
    """
    logging.getLogger().setLevel(logging.INFO)

    assert Path(infile).is_file(), f"not a file {infile}"
    with open(infile) as inputfile:
        stdjson = json.load(inputfile)

    # default outfile
    if outfile is None:
        myoutfile = Path(infile).with_stem(Path(infile).stem + "-ui")
    else:
        myoutfile = Path(outfile)

    # default lang
    if lang is None:
        lang = stdjson.get("ModelInfo").get("mainlanguage")

    uijson = UiRessource(stdmodel=stdjson).generate_uiressource(diagname=diagname,
                                                                uitype="miro",
                                                                lang=lang)
    with open(myoutfile, "w") as outjson:
        json.dump(uijson, outjson, indent=2)

    logging.info(f"jsonfile written : {str(myoutfile)}")

    return uijson
