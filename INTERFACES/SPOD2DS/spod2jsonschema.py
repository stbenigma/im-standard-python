from IM_STANDARD import nvl
from IM_STANDARD.myjsonschema import ElementId, JsonSchema, JsonElement
from .jsbase import JSModel, jsguid2type


class Spod2Jsonschema():
    ORIGINTOOL = "SPOD"

    def __init__(self, jsmodel: JSModel = None):
        if type(jsmodel) is JSModel:
            self._JSModel: JSModel = jsmodel
        else:  # None or dict
            self._JSModel = None
        # set range for new attr-id's
        ElementId.setnextid("ATTR", 99999)
        self.standardjson: JsonSchema = JsonSchema()
        return

    @property
    def jsmodel(self):
        return self._JSModel.jsmodel

    def anylingualtext(self, text, stripblanks=False):
        ismultilingual = self.standardjson.modelismultilingual()
        if ismultilingual and type(text) is dict:
            # dict is fine for multilingual, but kill all-empty strings
            if set(list(text.values())) == set(['']):
                return dict()
            else:
                return text
        elif not ismultilingual and (text is None or type(text) == str):
            # string is fine for non multilingual
            if text == '':
                return None
            else:
                return text.strip() if stripblanks else text
        elif not ismultilingual and type(text) is dict:
            # extract single name for monolingual
            vals = [(v.strip() if stripblanks else v) for v in text.values()]
            return vals[0]
        elif ismultilingual and (text is None or type(text) == str):
            # create multilinugal from text
            if text is None or text == '':
                return None
            else:
                return {self.standardjson.mainlang: (text.strip() if stripblanks else text)}
        else:
            raise Exception(f"unkwown type for text {type(text)} {str(text)[:20]}")

    def modellanguagetexts(self, multilangtexts: dict):
        return [] if multilangtexts is None else [expl[self._JSModel.getdefaultlang()] for expl in multilangtexts]

    def lovvalues(self, element):
        invalues = element.get("values") if "values" in element else []
        invalues.sort(key=lambda val: val["sort"])
        outvalues = [JsonElement().refvaluejson(value=val.get("value"),
                                                displayvalue=val.get("displ"),
                                                description=val.get("descr"),
                                                sortorder=val.get("sort")
                                                ).data for val in invalues]
        return outvalues

    def domainjson(self, key, element):
        domaintypes = {"TXT": "TextDomain",
                       "BIN": "BinaryDomain",
                       "GRP": "GroupDomain",
                       "LOV": "LOVDomain",
                       "NUM": "NumericDomain",
                       "DAT": "DatetimeDomain",
                       "BOOL": "BooleanDomain"
                       }
        domaintype = domaintypes[element.get("type")]
        subelements = element.get("elements") if "elements" in element else []
        subattrs = [{"elementId": ElementId.nextid("ATTR"),
                     "name": elem.get("name").strip(),
                     "mandatory": elem.get("mandatory"),
                     "description": elem.get("descr"),
                     "domainId": elem.get("domainId"),
                     "parentId": key
                     }
                    for elem in subelements]
        subattrs2 = [JsonElement().attributejson(elementId=ElementId.nextid("ATTR"),
                                                 name=nvl(elem.get("name")).strip(),
                                                 mandatory=elem.get("mandatory"),
                                                 description=elem.get("descr"),
                                                 domainid=elem.get("domainId"),
                                                 parentid=key
                                                 )
                     for elem in subelements]
        additionalProps = nvl(self.userdefprops(element.get("userdefprops")), dict())
        for sourcekey, source in nvl(element.get("sourceref"), dict()).items():
            additionalProps["SOURCE-" + sourcekey] = source

        jsonstruct = JsonElement().domainjson(elementId=key,
                                              name=self.anylingualtext(element.get("name"), stripblanks=True),
                                              domaintype=domaintype,
                                              parentid=key,
                                              description=self.anylingualtext(element.get("description")),
                                              maxlength=element.get("maxlng"),
                                              syntaxrule=element.get("syntaxRule"),
                                              minvalue=element.get("minValue"),
                                              maxvalue=element.get("maxValue"),
                                              granularity=element.get("granularity"),
                                              totaldigits=element.get("totalDigits"),
                                              fractdigits=element.get("fractDigits"),
                                              roundvalue=element.get("roundValue"),
                                              unit=None if element.get("unit") is None else {
                                                  "symbol": element.get("unit")},
                                              elements=subattrs,
                                              values=self.lovvalues(element=element),
                                              additionalProps=additionalProps
                                              )
        # self.filldocureferences(element=jsonstruct, reflist=element.get("referencedby"))

        return jsonstruct

    def categoryjson(self, key, element):
        color = element.get("ui").get("color")
        additionalProps = dict() if color is None else {"color": color}
        for sourcekey, source in nvl(element.get("sourceref"), dict()).items():
            additionalProps["SOURCE-" + sourcekey] = source

        jsonstruct = JsonElement().categoryjson(elementId=key,
                                                name=self.anylingualtext(element.get("name"), stripblanks=True),
                                                categorytype="ENTITY",
                                                description=self.anylingualtext(element.get("descr")),
                                                categoryId=element.get("parent"),
                                                additionalProps=additionalProps
                                                )
        return jsonstruct

    def documentjson(self, key, element):
        jsonstruct = {"elementId": key,
                      "name": element.get("name")
                      }
        self.optionalprop(jsonstruct, "description", element.get("content"))
        self.optionalprop(jsonstruct, "source", element.get("reference"))
        self.optionalprop(jsonstruct,
                          "additionalProps",
                          {"parent": element.get("parent"
                                                 ),
                           })

        return jsonstruct

    def attributejson(self, key, element):
        element = self._JSModel.getbyid(key)
        additionalProps = nvl(self.userdefprops(element.get("userdefprops")), dict())
        for sourcekey, source in nvl(element.get("sourceref"), dict()).items():
            additionalProps["SOURCE-" + sourcekey] = source

        return JsonElement().attributejson(elementId=key,
                                           name=self.anylingualtext(element.get("name"), stripblanks=True),
                                           domainid=element.get("domainId"),
                                           parentid=element.get("entity"),
                                           mandatory=element.get("mandatory"),
                                           displaySeq=element.get("seq"),
                                           description=self.anylingualtext(element.get("descr")),
                                           title=self.anylingualtext(element.get("tooptip")),
                                           examples=self.modellanguagetexts(element.get("examples")),
                                           descriptive=element.get("descriptive"),
                                           historicised=element.get("historicised"),
                                           repeated=element.get("repeated"),
                                           translated=element.get("translated"),
                                           encrypted=element.get("encrypted"),
                                           additionalProps=additionalProps
                                           )

        self.filldocureferences(element=jsonstruct, reflist=element.get("referencedby"))

        return jsonstruct

    def keyjson(self, keyid):
        key = self._JSModel.getbyid(keyid)
        keyelems = key.get("key-elements").get("attributes") + key.get("key-elements").get("relations")
        return {"name":key.get("name"),
                "elements":keyelems}

    def filldocureferences(self, element, reflist):
        return  # for minimal model disabled
        if reflist is not None and len(reflist) > 0:
            self.optionalprop(element, "docureference", [docuid for docuid in reflist if jsguid2type(docuid) == "DOCU"])
        return

    def userdefprops(self, userdefprops):
        udps = None
        if userdefprops is not None:
            udps = dict()
            for udp in userdefprops.values():
                for udpgrp in udp.values():
                    for udp2 in udpgrp.values():
                        udps[udp2.get("name")] = udp2.get("value")
        return udps

    def entityjson(self, key, element):
        # if entityname exists as category and entity does not have any attributes or relations
        # skip the entity, it is a placeholder on the diagram
        if len(element.get("attributes+")) == 0 and \
                len(element.get("relations+")) == 0 and \
                element.get("name").get(self._JSModel.getdefaultlang) in \
                [catg["name"] for catg in self.standardjson.jsonschemamodel.get("Categories")]:
            return None
        additionalProps = nvl(self.userdefprops(element.get("userdefprops")), dict())
        for sourcekey, source in nvl(element.get("sourceref"), dict()).items():
            additionalProps["SOURCE-" + sourcekey] = source
        jsonstruct = JsonElement().entityjson(elementId=key,
                                              name=self.anylingualtext(element.get("name"), stripblanks=True),
                                              categoryId=element.get("category"),
                                              synonyms=[self.anylingualtext(syno, stripblanks=True) for syno in
                                                        element.get("synonyms")],
                                              keys=[self.keyjson(keyid) for keyid in element.get("keys+")],
                                              shortname=element.get("shortName"),
                                              description=self.anylingualtext(element.get("descr")),
                                              title=self.anylingualtext(element.get("tooltip")),
                                              examples=self.modellanguagetexts(element.get("examples")),
                                              additionalProps=additionalProps
                                              )
        # self.optionalprop(jsonstruct, "isa+", element.get("supertypes+"))
        # self.optionalprop(jsonstruct, "roles+", element.get("roles+"))
        # self.optionalprop(jsonstruct, "subtypes+", element.get("subtypes+"))
        # self.optionalprop(jsonstruct, "relations+", element.get("relations+"))
        # self.filldocureferences(element=jsonstruct, reflist=element.get("referencedby"))

        return jsonstruct

    def arcnumber(self, arcid):
        arcs = {key: idx + 1 for idx, key in enumerate(self._JSModel.getelements("ARCS").keys())}
        return arcs[arcid]

    def relationendjson(self, relaend):
        arcnumber = None if relaend.get("arc") is None else self.arcnumber(relaend.get("arc"))
        assoctext = relaend.get("assoc")
        if type(assoctext) is dict and len(set([at for at in assoctext.values()]).difference({None, ""})) == 0:
            assoctext = None
        return JsonElement().relationendjson(assoctext=self.anylingualtext(assoctext,stripblanks=True),
                                             cardinality=relaend.get("maptype"),
                                             mandatory=relaend.get("mandatory"),
                                             historicised=relaend.get("hist"),
                                             arcnumber=arcnumber,
                                             entityid=relaend.get("enti"))

    def fillelements(self, elementname, elementjson):
        elements = self._JSModel.getelements(elementname)

        schemaelements = list()
        for key, val in elements.items():
            elemjson = elementjson(key, val)
            if elemjson is not None:
                schemaelements.append(elemjson)
        self.standardjson.addelementinstance(name=elementname.capitalize(), val=schemaelements)
        return

    def fillrelations(self):

        relationtypes = {"1:1": "1:1",
                         "ISAR": "ROLE",
                         "ISAS": "SUBTYPE",
                         "M:1": "M:1",
                         "M:N": "M:N"}

        self.standardjson.addelementinstance(name="Relations", val=[])
        for relaid, rela in self._JSModel.getelements("relations").items():
            additionalProps = nvl(self.userdefprops(rela.get("userdefprops")), dict())
            for sourcekey, source in nvl(rela.get("sourceref"), dict()).items():
                additionalProps["SOURCE-" + sourcekey] = source

            relatype = relationtypes[rela.get("type")]
            fwd = self.relationendjson(relaend=rela.get("from-to"))
            bwd = self.relationendjson(relaend=rela.get("to-from"))
            self.standardjson.jsonschemamodel["Relations"].append( JsonElement().relationjson(elementId=relaid,
                                                                        relationtype=relatype,
                                                                        fwd=fwd.data, bwd=bwd.data,
                                                                        relatype=relatype,
                                                                        examples=self.modellanguagetexts(
                                                                            rela.get("examples")),
                                                                        additionalProps=additionalProps
                                                                        ))

        return

    def generatestandardjson(self, modeltype="Information model",
                             targetenv="", description=None):
        if self.jsmodel is None:
            return
        info = self.jsmodel.get("model")
        self.standardjson.jsonschemamodel["ModelInfo"] = JsonElement().modelinfojson(
            modelname=nvl(info.get("name")).strip(),
            modeltype=modeltype,
            mainlanguage=nvl(info.get("language")).strip(),
            modelversion=self.jsmodel.get("_imprint_").get("Modelversion"),
            languages=[lang.strip() for lang in
                       nvl(self.jsmodel.get("languages"), dict()).keys()],
            description=description,
            targetEnvironment=targetenv,
            origintool="SPOD",
            originref=str(self._JSModel.jsfile),
            datetimecreated=self.jsmodel.get("_imprint_").get("created"),
            additionalProps={
                "SPOD-database": self.jsmodel.get("_imprint_").get("database")}
        )

        self.fillelements(elementname=JSModel.elemtype2label("CATG"), elementjson=self.categoryjson)
        self.fillelements(elementname=JSModel.elemtype2label("DOMA"), elementjson=self.domainjson)
        self.fillelements(elementname=JSModel.elemtype2label("ENTI"), elementjson=self.entityjson)
        self.fillelements(elementname=JSModel.elemtype2label("ATTR"), elementjson=self.attributejson)
        self.fillrelations()
        # self.generateentities(elementname=JSModel.elemtype2label("DOCU"), elementjson=self.documentjson)
        return self.standardjson

    def __str__(self):
        return self.model
