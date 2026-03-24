import json
import logging
from datetime import datetime
from pathlib import Path

from IM_STANDARD import JsonElement,nvl
from .std2uiressource import DiagramLayout, GenericUiRessource


class UiSimple(GenericUiRessource):

    def __init__(self, stdmodel, destjson=None):
        super().__init__(stdmodel=stdmodel,destjson=destjson)
        return

    def _getitems(self, elements: list, condition):
        return [e for e in elements if condition(e)]

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

    def _updateentiui(self):
        entibyname = dict() if self._destjson is None \
            else {enti.get("name"): enti for enti in self._destjson.get("elements", dict()).get("entities")}
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


    def _entitiesui(self):
        entities = []
        for enti in self.destentities:
            # skip creation if already in destination
            if not self._existselement(elementname="entities",
                                       name=self._mlvalue(enti.get("name")),
                                       link=self._href(enti)):
                entity = self.entijson(id= self._structid(enti),
                    name= self._mlvalue(enti.get("name")),
                    pos_x= self.diaglayout.startx,
                    pos_y= self.diaglayout.starty,
                    ui= self.uijson(width= DiagramLayout.ENTITYWIDTH,
                        height= DiagramLayout.ENTITYHEIGHT)
                                       )
                entities.append(entity)
                self.diaglayout._nextentity()
                logging.info(f'Entität "{entity.get("name")}" hinzugefügt')

        return entities

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
        relaendui = {"entityid": self._structid(self._getentity(relaend.get("entityid"))),
                     "entity": self._getentityname(relaend.get("entityid")),
                     "edge": edge,
                     "position": 50,
                     "connector": relaend.get("cardinality"),
                     "mandatory": relaend.get("mandatory"),
                     "caption": {
                         "text": self._mlvalue(value=relaend.get("assoctext")),
                         "position": edgeval("E", 15)
                     }
                     }

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

    def _relationsui(self):
        relations = []
        for rela in self.destrelationships:
            if not self._existselement(elementname="relationships",
                                       name=self._relaname(rela),
                                       link=self._href(rela)
                                       ):
                # TODO Subtype relations are not on a project in dataspot how to capture them anyway
                fwd, bwd = rela.get("fwd"), rela.get("bwd")
                relation = self.relajson(relaid= self._structid(rela),
                    name= self._relaname(rela),
                    fwd= self._relaendui(relaend=fwd, edge="E"),
                    bwd= self._relaendui(relaend=bwd, edge="W")
                                         )
                relations.append(relation)
                logging.info(f'Beziehung "{relation.get("name")}" hinzugefügt')

        return relations

    def modeljson(self, id, name, elements, **kwargs):
        retval = {"id": id,
                  "name": name,
                  "type": kwargs.get("modeltyp", "Entity")
                  }

        for key,val  in kwargs.items():
            if key=="modeltype":continue
            JsonElement.optionalprop(destobject=retval,propname=key,value=val)

        for key,val in elements.items():
            retval[key]=val
        return retval

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

    def generate_uijson(self, diagname: str,
                        lang=None) -> dict:

        mainlang = self._stdmodel.get("ModelInfo").get("mainlanguage")
        self._lang = nvl(lang, mainlang)
        if self._lang == mainlang:
            self._defaultlang = None
        else:
            self._defaultlang = mainlang

        diagrams = [diag for diag in self._stdmodel.get("Diagrams", []) if diag.get("name") == diagname]
        assert len(diagrams) == 1, f"Diagram '{diagname} not found in standard json"
        diagram = diagrams[0]

        self.destentities = [elem for elem in self._stdmodel.get("Entities", []) if
                             elem.get("elementid") in diagram.get("elements")]
        self.destrelationships = [elem for elem in self._stdmodel.get("Relations", []) if
                                  elem.get("elementid") in diagram.get("elements")]
        self.diaglayout = DiagramLayout(entitycnt=len(self.destentities))
        if self._destjson is None:
            self._destjson = self.modeljson(id= self._structid(diagram),
                              name= diagram.get("name"),
                              dc= str(datetime.now()),
                              elements= {"nodes": [],
                                           "edges": []
                                           }
                                            )
        else:
            assert self._destjson["name"] == diagram.get("name"), \
                f'diagram names do not match {self._destjson["name"]} != {diagram.get("name")}'
            self._destjson["dm"] = str(datetime.now())

        self._checkproblems()

        self._updateentiui()
        self._updaterelaui()
        # add new categories and entities to destjson

        # new elements below the existing ones
        if self.diaglayout.starty > self.diaglayout.STARTY:
            self.diaglayout.starty += self.diaglayout.CATEGORYHEIGHT

        self._destjson["nodes"].extend(self._entitiesui())
        self._destjson["edges"].extend(self._relationsui())

        return self._destjson


def createsimpleui(infile, lang=None):
    logging.getLogger().setLevel(logging.INFO)

    if Path(infile).is_file():
        with open(infile) as infile:
            stdjson = json.load(infile)

    ui = UiSimple(stdmodel=stdjson)
    uijson = ui.generate_uijson(diagname="Visualsierung Astronomie",
                                lang=None)
    return uijson
