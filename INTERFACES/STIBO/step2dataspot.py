import json
import logging
from pathlib import Path

from DATASPOT.imstandard_dataspot import Json2dataspot
from SSOT_infra import nvl, alwayslist
from STIBO.loadstep import LoadStep


class Step2Dataspot:
    DOMAINTYPES = {"text": "TextDomain",
                   "url": "TextDomain",
                   "URL": "TextDomain",
                   "text_exclude_tags": "TextDomain",
                   "numeric_text_exclude_tags": "TextDomain",
                   "numeric_text": "TextDomain",
                   "embedded_number": "TextDomain",
                   "condition": "TextDomain",
                   "gtin14": "TextDomain",
                   "gtin13": "TextDomain",
                   "gtin": "TextDomain",
                   "gtin8": "TextDomain",
                   "gtin12": "TextDomain",
                   "gln": "TextDomain",
                   "regexp": "TextDomain",
                   "binary": "BinaryDomain",
                   "numberrange": "GroupDomain",
                   "reference": "LOVDomain",
                   "number": "NumericDomain",
                   "fraction": "NumericDomain",
                   "fractionnodecimal": "NumericDomain",
                   "integer": "NumericDomain",
                   "date": "DatetimeDomain",
                   "isodate": "DatetimeDomain",
                   "isodatetime": "DatetimeDomain",
                   "legacyisodatetime": "DatetimeDomain",
                   "boolean": "BooleanDomain"
                   }
    STIBOSTEREOTYPE = "STIBO"

    def __init__(self, loadedstep: LoadStep,
                 dsmodelname: str):
        self.loadedstep = loadedstep
        self.dsmodelname = dsmodelname
        self.referencemodelname = self.dsmodelname + " referencemodel"
        self.domainmodelname = self.dsmodelname + " domainmodel"
        self.datamodelfullname = self.dsmodelname + " datamodel"
        self.standardcollnames = [self.loadedstep.DEFAULTATTRGROUP,
                                  self.loadedstep.DEFAULTOBJECTGROUP,
                                  "EntityCrossReferenceType"]

        # restrict to children of my root(s)
        ##TODO could be done here, with full model from loadstep

    def doinattrgroup(self, groups, attrgroup, source, outmodelname,
                      parent, path,
                      grouptype):
        id = attrgroup.get("@ID")
        mypath = path + self._attrgrppath(attrgroup) + [id]
        children = alwayslist(attrgroup.get(grouptype))
        if self.loadedstep.getelement(groups, id) is not None:
            logging.warning(f"Duplicate {grouptype} {id} from source {source}")

        else:
            group = {"name": attrgroup.get("Name"),
                     "ID": id,
                     "MODEL": outmodelname,
                     "PARENT": parent,
                     "SOURCE": source,
                     "PATH": mypath
                     }
            groups.append(group)

        for subattrgroup in children:
            self.doinattrgroup(groups=groups,
                               attrgroup=subattrgroup,
                               outmodelname=outmodelname,
                               parent=id,
                               source=source,
                               path=mypath,
                               grouptype=grouptype)

    @staticmethod
    def children(struct, idval, parent="PARENT"):
        return [elem for elem in struct if elem.get(parent) == idval]

    # def generateattrgroup(self, jsonstruct, groups,
    #                       attrgroup, collectionpath, parent):
    #     groupjson = self._generate1LOV(refobj={"ID": attrgroup.get("ID"),
    #                                            "Name": attrgroup.get("name")},
    #                                    collectionpath=collectionpath,
    #                                    parent=parent)
    #     jsonstruct.append(groupjson)
    #     for idx, subattrgroup in enumerate(self.children(struct=groups,
    #                                                      idval=attrgroup.get("ID"))):
    #         valuejson = self._generate1value(valueobj={"code": subattrgroup.get("ID"),
    #                                                    "text": subattrgroup.get("name")},
    #                                          parent=attrgroup.get("ID"),
    #                                          idx=idx)
    #         jsonstruct.append(valuejson)
    #
    #         # final children get no extra reference-entry
    #         if len(self.children(struct=groups,
    #                              idval=subattrgroup.get("ID"))) > 0:
    #             self.generateattrgroup(jsonstruct=jsonstruct, groups=groups,
    #                                    attrgroup=subattrgroup,
    #                                    collectionpath=collectionpath,
    #                                    parent=subattrgroup.get("PARENT"))
    #     return
    #
    def generatecollections(self, jsonstruct, coll,
                            parent, withcoll=True):
        lcoll = Json2dataspot.fillstruct(elementtype="Collection",
                                         label=coll.get("ID")
                                         )
        Json2dataspot.optionalprop(destobject=lcoll,
                                   propname="title",
                                   value=self.multilang(coll.get("name"))
                                   )
        # None for top collections, else path of parent
        colpath = None if parent is None else coll.get("PATH")[:-1]
        # (with "_coll" endings if required)
        if withcoll: colpath = self._addcollname(colpath)
        Json2dataspot.optionalprop(destobject=lcoll,
                                   propname="inCollection",
                                   value=self.joinpath(colpath)
                                   )

        jsonstruct.append(lcoll)
        for child in self.children(struct=self.loadedstep.lovgroups,
                                   idval=coll.get("ID")):
            self.generatecollections(jsonstruct=jsonstruct,
                                     coll=child,
                                     parent=coll.get("ID"),
                                     withcoll=False)
        return

    def _collname(self, name):
        # adds _coll to then name for distinction with object of same name
        return None if name is None \
            else name if name in self.standardcollnames \
            else name + "_coll"

    def _addcollname(self, names):
        if names is None: return None
        # adds _coll to all elements in the list
        # except standard domains
        return [a if a in self.standardcollnames
                  else self._collname(a) for a in names]

    def _attrgrppath(self, doma):
        if "AttributeGroupLink" in doma:
            attrgrplinks = alwayslist(doma.get("AttributeGroupLink"))
            attrgroupid = self.loadedstep._getanyid(elem=attrgrplinks[0],
                                                    anyid='@AttributeGroupID')
            attrgroup = self.loadedstep.getelement(elements=self.loadedstep.attrgroups,
                                                   idval=attrgroupid)
            if attrgroup is None:
                attrpath = alwayslist(doma.get("PATH"))[:-1]
            else:
                attrpath = alwayslist(attrgroup.get("PATH"))

        # get first group as collection
        else:
            attrpath = alwayslist(doma.get("PATH"))[:-1]
        retval = self._addcollname(attrpath)
        return retval

    def groupderivation(self, attrgroup, doma):
        return None  # solved with collectionshierarchy in domains
        path = attrgroup.get("PATH")
        if len(path) < 3:
            logging.warning(
                f"TBD: {attrgroup.get('PATH')} in {attrgroup.get('SOURCE')} is too short")
            return None
        elif len(path) > 4:
            pass  # path = path[0:2] + path[-2:] immer vollständige Path
        derivation = Json2dataspot.fillstruct(elementtype="Derivation",
                                              derivedTo=Json2dataspot.fullescapestr(doma.get("ID")),
                                              derivedFrom=self.joinpath([""] + path)
                                              )
        return derivation

    @staticmethod
    def joinpath(elements):
        if elements is None or len(elements) == 0:
            return None
        return "/".join([Json2dataspot.fullescapestr(e) for e in elements])

    @staticmethod
    def multilang(mlvalue, lang="std.lang.all"):
        """
            [{'@QualifierID': 'std.lang.all', '#text': 'BT yes/no'},
            {'@QualifierID': ''en-US'', '#text': 'BT yes/no'}]
            returns text from entry lang in mlvalue
            mlvalue, if nothing is found
        """

        def _qualitext(mlv, lang):
            if type(mlv) == dict and lang == mlv.get("@QualifierID"):
                if "#text" in mlv:
                    return mlv.get("#text")
            else:
                return None

        retval = None
        if type(mlvalue) == list:
            for mlv in mlvalue:
                retval = _qualitext(mlv, lang)
                if retval is not None: break
        elif type(mlvalue) == dict:
            retval = _qualitext(mlvalue, lang)

        return retval if retval is not None else mlvalue.__str__()

    def _getfrommetadata(self, elem, fieldname):
        for member in alwayslist(elem.get("MetaData")):
            value = member.get("Value")
            attrid = self.loadedstep._getanyid(elem=value,
                                               anyid="@AttributeID")
            if attrid is not None and attrid == fieldname:
                return value.get("#text")
        return None

    def generateattribut(self, jsonstruct, attr, idx, parentpath=None):
        # TODO Collections für Attribute (= jeweils 1. Gruppe eines Attributes) falls es eine hat, sonst default
        if nvl(parentpath, []) == []:
            logging.warning(f"illegal umlclasspath {parentpath} for {attr.get('ID')}")
            return
        if "ListOfValueLink" in attr:
            lovattr = self.loadedstep.getelement(elements=self.loadedstep.lovs,
                                                 idval=self.loadedstep._getanyid(
                                                     elem=attr.get("ListOfValueLink")[0],
                                                     anyid="@ListOfValueID"))
            if lovattr is None:
                logging.error(f'lovreference in atatribute {attr.get("ID")} not in lovs')
                return
            rangepath = ["", self.referencemodelname] + lovattr.get("PATH")
        else:
            #domains have coll-endings at collections
            rangepath = ["", self.domainmodelname] + \
                        self._addcollname(attr.get("PATH")[:-1]) +\
                        [attr.get("ID")]

        descr = self._getfrommetadata(elem=attr,
                                      fieldname="AttributeHelpText")
        dsplseq = int(nvl(self._getfrommetadata(elem=attr,
                                                fieldname="DisplaySequence"),
                          idx))
        idx = dsplseq

        attribut = Json2dataspot.fillstruct(elementtype="UmlAttribute",
                                            label=attr.get("ID"),
                                            title=self.multilang(attr.get("Name")).__str__(),
                                            order=str(dsplseq),
                                            description=Json2dataspot.escapestr(descr),
                                            hasDomain=self.joinpath(parentpath),
                                            hasRange=self.joinpath(rangepath),
                                            favorite=idx < 3,
                                            derived=attr.get("Derived") == 'true',
                                            required="MANDATORY" if attr.get("Mandatory") == 'true' else "OPTIONAL",
                                            cardinality="MANY" if attr.get("MultiValued") == 'true' else "ONE"
                                            )

        jsonstruct.append(attribut)

        return

    def _utparents(self, ut):
        """return all parents except myself"""
        return [self.loadedstep._getanyid(elem=p, anyid="@UserTypeID")
                for p in alwayslist(self.loadedstep._getanyid(elem=ut,
                                                              anyid="UserTypeLink"))
                if p.get("@UserTypeID") != ut.get("ID")]

    def getparents(self, ut):
        return [father.get("@UserTypeID") for father in alwayslist(ut.get("UserTypeLink"))
                if father.get("@UserTypeID") in self.loadedstep.myusertypes]

    # def collectionshierarchy(self, path, parent=None):
    #
    #     single = lambda x: None if len(x) != 1 else x[0]
    #     roots = {u.get("ID"): single(self._utparents(u)) for u in self.loadedstep.allusertypes
    #              if u.get("ID").upper().endswith("ROOT")
    #              }
    #     collects = {r: {"PARENT": val,
    #                     "PATH": path + [r]
    #                     }
    #                 for r, val in roots.items() if val == parent}
    #     childcollects = dict()
    #     for key, val in collects.items():
    #         childcollects.update(self.collectionshierarchy(parent=key, path=val.get("PATH")))
    #     collects.update(childcollects)
    #     return collects
    #
    def generatereferences(self):
        """
        @return: call to child with special functions for references
        """
        return GenerateReferences(dsmodelname=self.dsmodelname,
                                  loadedstep=self.loadedstep).generatedsjson()

    def generatedomains(self):
        """
        @return: call to child with special functions for references
        """
        return GenerateDomains(dsmodelname=self.dsmodelname,
                               loadedstep=self.loadedstep).generatedsjson()

    def generatedatatmodel(self):
        """
        @return: call to child with special functions for references
        """
        return GenerateDatamodel(dsmodelname=self.dsmodelname,
                                 loadedstep=self.loadedstep).generatedsjson()


class GenerateReferences(Step2Dataspot):
    def __init__(self, loadedstep: LoadStep,
                 dsmodelname: str):
        super().__init__(loadedstep=loadedstep,
                         dsmodelname=dsmodelname)
        return

    def _generate1LOV(self, refobj, collectionpath, parent):
        lovjson = Json2dataspot.fillstruct("ReferenceObject",
                                           label=refobj.get("ID"),
                                           title=self.multilang(refobj.get("Name")).__str__()
                                           )
        Json2dataspot.optionalprop(lovjson, "inCollection",
                                   self.joinpath(collectionpath))
        Json2dataspot.optionalprop(lovjson, "subordinateOf", parent)
        return lovjson

    def _generate1value(self, valueobj, parent, idx):
        valuejson = Json2dataspot.fillstruct(elementtype="ReferenceValue",
                                             literalOf=Json2dataspot.fullescapestr(parent),
                                             timeSeries=[{
                                                 "validFrom": -2208988800000,
                                                 "validTo": 32503593600000,
                                                 "code": Json2dataspot.escapestr(valueobj.get("code"))
                                             }]
                                             )
        Json2dataspot.optionalprop(valuejson["timeSeries"][0], "shortText",
                                   Json2dataspot.escapestr(self.multilang(valueobj.get("text")).__str__()))
        Json2dataspot.optionalprop(valuejson, "favorite", idx < 3)
        return valuejson

    def _generatelovs(self, jsonstruct):
        for lgroup in self.loadedstep.lovgroups:
            if lgroup.get("PARENT") is None:
                self.generatecollections(jsonstruct=jsonstruct,
                                         coll=lgroup,
                                         parent=None,
                                         withcoll=False)
        for lov in self.loadedstep.lovs:
            lovparent = self.loadedstep._getanyid(elem=lov, anyid="@ParentID")
            mycoll = self.loadedstep.getelement(elements=self.loadedstep.lovgroups,
                                                idval=lovparent)
            jsonstruct.append(
                self._generate1LOV(refobj=lov,
                                   collectionpath=mycoll.get("PATH"),
                                   parent=None))
            values = alwayslist(lov.get("Value"))
            if len(values) == 0:
                values = alwayslist(lov.get("ValueGroup"))
            for idx, value in enumerate(values):
                if type(value) == dict:
                    vid = value.get("@ID")

                    val = value.get("#text")
                    if val is None: val = value.get("Value")
                    valueobj = {"code": val.__str__() if vid is None else vid.__str__(),
                                "text": val.__str__()}
                else:
                    valueobj = {"code": val.__str__(),
                                "text": None}

                jsonstruct.append(self._generate1value(
                    valueobj=valueobj,
                    parent=lov.get("ID"), idx=idx))

        return

    def generatedsjson(self):
        # for modelname, modelval in self.loadedstep.models.items():
        # TODO was tun mit mehrfachmodels?
        # currently all packed into one output
        jsonstruct = []
        self._generatelovs(jsonstruct=jsonstruct)
        return jsonstruct


class GenerateDomains(Step2Dataspot):
    def __init__(self, loadedstep: LoadStep,
                 dsmodelname: str):
        super().__init__(loadedstep=loadedstep,
                         dsmodelname=dsmodelname)
        return

    def generategroupcolls(self, jsonstruct, groups, parentpath=None):
        for attrgroup in groups:
            # all attr group collections can also be attr groups therefor +_coll
            collname = self._collname(attrgroup.get("ID"))
            lcoll = Json2dataspot.fillstruct(elementtype="Collection",
                                             label=collname
                                             )
            Json2dataspot.optionalprop(destobject=lcoll,
                                       propname="title",
                                       value=self.multilang(attrgroup.get("name"))
                                       )
            Json2dataspot.optionalprop(destobject=lcoll,
                                       propname="inCollection",
                                       value=self.joinpath(parentpath)
                                       )
            jsonstruct.append(lcoll)
            self.generategroupcolls(jsonstruct=jsonstruct,
                                    groups=[ag for ag in self.loadedstep.attrgroups
                                            if ag.get("PARENT") == attrgroup.get("ID")],
                                    parentpath=alwayslist(parentpath) + [collname]
                                    )
        return

    def generategroupdomain(self, attrgroup) -> list:
        domains = []
        grpid = attrgroup.get("ID")
        name = attrgroup.get("Name")
        collectionname = self._addcollname(attrgroup.get("PATH"))

        groupchildren = [grpattr for grpattr in self.loadedstep.attributes
                         if grpid in [self.loadedstep._getanyid(elem=agl, anyid="@AttributeGroupID")
                                      for agl in alwayslist(self.loadedstep._getanyid(elem=grpattr,
                                                                                      anyid="@AttributeGroupLink"))]
                         ]
        # skip group attr generation if group has less than 2 attributes in it
        if len(groupchildren) < 2:
            return domains
        # TODO group attr groups into collections instead of references
        domain = Json2dataspot.fillstruct(elementtype="DataDomain",
                                          label=grpid,
                                          title=self.multilang(name).__str__(),
                                          stereotype=self.STIBOSTEREOTYPE,
                                          description=Json2dataspot.escapestr(attrgroup.get("description")),
                                          inCollection=self.joinpath(collectionname),
                                          examples=attrgroup.get("examples")
                                          )
        Json2dataspot.optionalprop(destobject=domain, propname="DIMENSIONREF", value=attrgroup.get("DimensionRef"))
        Json2dataspot.optionalprop(destobject=domain, propname="ATTRGRPREF", value=[agl.get("@AttributeGroupID")
                                                                                    for agl in alwayslist(
                attrgroup.get("AttributeGroupLink"))] if "AttributeGroupLink" in attrgroup else None)
        Json2dataspot.optionalprop(destobject=domain, propname="ATTRCALC", value=attrgroup.get("Derived") == 'true' \
            if "Derived" in attrgroup else None)
        Json2dataspot.optionalprop(destobject=domain, propname="ATTRMAND", value=attrgroup.get("Mandatory") == 'true'
        if "Mandatory" in attrgroup else None)
        Json2dataspot.optionalprop(destobject=domain, propname="ATTRMULTIVALUE",
                                   value=attrgroup.get("MultiValued") == 'true'
                                   if "MultiValued" in attrgroup else None)
        Json2dataspot.optionalprop(destobject=domain, propname="PROCMODE", value=attrgroup.get("ProductMode"))
        Json2dataspot.optionalprop(destobject=domain, propname="ATTRDISPLSEQ", value=attrgroup.get("displ"))

        domains.append(domain)
        # fill group attributes
        idx = 0
        for grpattr in groupchildren:
            range = self._attrgrppath(grpattr)
            path = collectionname + [grpid]
            idx += 1
            attribut = Json2dataspot.fillstruct(elementtype="DataAttribute",
                                                label=grpattr.get("ID"),
                                                description=Json2dataspot.escapestr("see where?"),
                                                order=str(idx),
                                                hasDomain=self.joinpath(path),
                                                hasRange=self.joinpath(range + [grpattr.get("ID")]),
                                                # stereotype=self.STIBOSTEREOTYPE,
                                                favorite=idx < 3,
                                                derived=grpattr.get("Derived") == 'true',
                                                required="MANDATORY" if grpattr.get(
                                                    "Mandatory") == 'true' else "OPTIONAL",
                                                cardinality="MANY" if grpattr.get(
                                                    "MultiValued") == 'true' else "ONE"
                                                )
            domains.append(attribut)
        return domains

    def generatedomain(self, doma):  # donecategories: dict):
        domaid = doma.get("ID")
        name = doma.get("Name")
        collectionname = self._addcollname(doma.get("PATH")[:-1])

        domain = Json2dataspot.fillstruct(elementtype="DataDomain",
                                          label=domaid,
                                          title=self.multilang(name).__str__(),
                                          stereotype=self.STIBOSTEREOTYPE,
                                          description=Json2dataspot.escapestr(doma.get("description")),
                                          inCollection=self.joinpath(collectionname),
                                          examples=doma.get("examples")
                                          )
        validation = doma.get("Validation")
        if validation is not None:
            validation = validation[0]
            domaintype = self.DOMAINTYPES[validation.get("@BaseType")]
            if domaintype == "TextDomain":
                domain["pattern"] = validation.get("@InputMask")
                domain["baseType"] = "STRING"
                Json2dataspot.optionalprop(destobject=domain, propname="maxLength", value=validation.get("@MaxLength"))
                # Json2dataspot.optionalprop(destobject=domainid, propname="minLength", value=validation.get("@MinLength"))
                domain["minInclusive"] = None
                domain["maxInclusive"] = None
                domain["minExclusive"] = None
                domain["maxExclusive"] = None
                domain["integerDigits"] = None
                domain["fractionDigits"] = None
            elif domaintype == "NumericDomain":
                domain["baseType"] = "DECIMAL"
                Json2dataspot.optionalprop(destobject=domain, propname="minInclusive",
                                           value=validation.get("@MinValue"))
                Json2dataspot.optionalprop(destobject=domain, propname="maxInclusive",
                                           value=validation.get("@MaxValue"))
                domain["minLength"] = None
                domain["maxLength"] = None
            else:
                domain["minInclusive"] = None
                domain["maxInclusive"] = None
                domain["minExclusive"] = None
                domain["maxExclusive"] = None
                domain["integerDigits"] = None
                domain["fractionDigits"] = None

        Json2dataspot.optionalprop(destobject=domain, propname="DIMENSIONREF", value=doma.get("DimensionRef"))
        Json2dataspot.optionalprop(destobject=domain, propname="ATTRGRPREF", value=[agl.get("@AttributeGroupID")
                                                                                    for agl in alwayslist(
                doma.get("AttributeGroupLink"))]
        if "AttributeGroupLink" in doma else None)
        Json2dataspot.optionalprop(destobject=domain, propname="ATTRCALC", value=doma.get("Derived") == 'true' \
            if "Derived" in doma else None)
        Json2dataspot.optionalprop(destobject=domain, propname="ATTRMAND", value=doma.get("Mandatory") == 'true'
        if "Mandatory" in doma else None)
        Json2dataspot.optionalprop(destobject=domain, propname="ATTRMULTIVALUE", value=doma.get("MultiValued") == 'true'
        if "MultiValued" in doma else None)
        Json2dataspot.optionalprop(destobject=domain, propname="ATTRFULLTEXT",
                                   value=doma.get("FullTextIndexed") == 'true' \
                                       if "FullTextIndexed" in doma else None)
        Json2dataspot.optionalprop(destobject=domain, propname="PROCMODE", value=doma.get("ProductMode"))
        Json2dataspot.optionalprop(destobject=domain, propname="ATTRDISPLSEQ", value=doma.get("displ"))
        Json2dataspot.optionalprop(destobject=domain, propname="ATTRMULTILANG",
                                   value="Language" in {d.get("@DimensionID") for d in
                                                        alwayslist(doma.get("@DimensionLink"))}
                                   if "@DimensionLink" in doma else None)

        return domain

    def generatedsjson(self):
        # TODO see others generates for modelname, modelval in self.models.items():
        # default collectoin
        jsonstruct = [Json2dataspot.fillstruct(elementtype="Collection",
                                               label=self.loadedstep.DEFAULTATTRGROUP)
                      ]
        # generate top level collections
        self.generategroupcolls(jsonstruct=jsonstruct,
                                groups=[ag for ag in self.loadedstep.attrgroups
                                        if ag.get("PARENT") is None]
                                )

        for doma in self.loadedstep.attributes:
            # TODO if doma.get("MODEL") == self.datamodelfullname:
            jsonstruct.append(self.generatedomain(doma))

            for attrgrplink in alwayslist(doma.get("AttributeGroupLink")):
                attrgroupid = self.loadedstep._getanyid(elem=attrgrplink,
                                                        anyid="@AttributeGroupID")
                if attrgroupid is not None:
                    attrgroup = self.loadedstep.getelement(elements=self.loadedstep.attrgroups,
                                                           idval=attrgroupid)
                    if attrgroup is not None:
                        derivation = self.groupderivation(attrgroup=attrgroup,
                                                          doma=doma)
                        # TODO wer braucht derivation? von der Hierarchie in LOVs
                        if derivation is not None:  # TODO Derivation separated
                            jsonstruct.append(derivation)

        for attrgroup in self.loadedstep.attrgroups:
            # if attrgroup.get("MODEL") == self.domainmodelname:
            # todo skip groups with no usage in any usertype or xref or other attrgrou
            jsonstruct.extend(self.generategroupdomain(attrgroup))

        return jsonstruct


class GenerateDatamodel(Step2Dataspot):
    def __init__(self, loadedstep: LoadStep,
                 dsmodelname: str):
        super().__init__(loadedstep=loadedstep,
                         dsmodelname=dsmodelname)
        return

    def getmycollection(self, collections, usertype):
        coll = None
        utid = usertype.get("ID")
        if utid in collections:
            coll = collections[utid]
        else:
            parents = [self.loadedstep.myusertypes[p] for p in self.getparents(usertype)]
            undefparents = [p for p in parents if p.get("PATH") is None]
            rootparents = [collections[p.get("ID")] for p in parents if p.get("ID").upper().endswith("ROOT")]
            if len(rootparents) == 1:
                coll = rootparents[0]
            elif len(rootparents) > 1:
                coll = collections.get(self.loadedstep.DEFAULTOBJECTGROUP)
            elif len(undefparents) == 0:
                colls = set()
                for undefparent in parents:
                    parcol = self.getmycollection(collections=collections, usertype=undefparent)
                    colls.add(parcol.get("PATH")[-1])
                if len(colls) == 1:
                    coll = [c for c in collections.values() if c.get("PATH")[-1] == list(colls)[0]][0]
                else:
                    coll = collections.get(self.loadedstep.DEFAULTOBJECTGROUP)

        return coll

    def generatedmcollections(self, jsonstruct):
        # jsonstruct.append(Json2dataspot.fillstruct(elementtype="Collection",
        #                                           label=self.loadedstep.DEFAULTOBJECTGROUP,
        #                                           title="Default step top collection"))
        # only roots with no parent and xreftypes as subordinate of the roots are created
        def minpath(colpath):
            """ remove all collections except the first  and standardones"""
            return ([c for c in colpath if c in self.standardcollnames][0], colpath[0])

        allcollids = [(ut.get("PATH")[0], None) for ut in self.loadedstep.myusertypes]
        allcollids += [minpath(ut.get("PATH")) for ut in
                       alwayslist(self.loadedstep.xreftypes.get('EntityCrossReferenceType'))]
        #TODO handle other types
        """AssetCrossReferenceType,ProductCrossReferenceType, ClassificationCrossReferenceType, 
            ClassificationProductLinkType, 
        """
        allcollids = list(set(allcollids))  # get rid of duplicates
        allcollids.sort(key=lambda k: nvl(k[1]))
        for coll in allcollids:
            coll = Json2dataspot.fillstruct(elementtype="Collection",
                                            label=self._collname(coll[0]),
                                            inCollection=self._collname(coll[1]))
            jsonstruct.append(coll)
        return

    def generateusertype(self, jsonstruct, ut,
                         collectionpath):
        if collectionpath in [None, []]:
            logging.error(f"{ut.get('ID')} has no proper collection {collectionpath}")
            return
        usertype = Json2dataspot.fillstruct(elementtype="UmlClass",
                                            label=ut.get("ID"),
                                            title=self.multilang(ut.get("Name")).__str__(),
                                            description=Json2dataspot.escapestr(nvl(ut.get("description"))),
                                            examples=ut.get("examples"),
                                            inCollection=self.joinpath(collectionpath),
                                            favorite=False
                                            )

        # Json2dataspot.optionalprop(usertype, "", None)
        jsonstruct.append(usertype)

        parentpath = collectionpath + [ut.get("ID")]
        attrs = alwayslist(self.loadedstep._getanyid(elem=ut,
                                                     anyid="@AttributeLink"))
        idx = 0
        for attrid in attrs:
            attr = self.loadedstep.getelement(elements=self.loadedstep.attributes,
                                              idval=self.loadedstep._getanyid(elem=attrid,
                                                                              anyid="@AttributeID"))
            if attr is None: continue
            idx += 1
            self.generateattribut(jsonstruct=jsonstruct,
                                  parentpath=parentpath,
                                  idx=idx,
                                  attr=attr)

        attrs = alwayslist(self.loadedstep._getanyid(elem=ut,
                                                     anyid="@AttributeGroupLink"))
        #attrs are groupattrs
        for attrid in attrs:
            attr = self.loadedstep.getelement(elements=self.loadedstep.attrgroups,
                                              idval=self.loadedstep._getanyid(elem=attrid,
                                                                              anyid="@AttributeGroupID"))
            if attr is None: continue
            # if attr.get("MODEL") == self.domainmodelname:

            idx += 1
            #groups are in a collection with their own namen hence
            #path + ID
            rangepath = ["", self.domainmodelname]
            rangepath.extend(self._addcollname(attr.get("PATH")))
            rangepath.append(attr.get("ID"))
            attribut = Json2dataspot.fillstruct(elementtype="UmlAttribute",
                                                label=attr.get("ID"),
                                                title=self.multilang(attr.get("Name")).__str__(),
                                                order=str(idx),
                                                description=Json2dataspot.escapestr(attr.get("Description")),
                                                hasDomain=self.joinpath(parentpath),
                                                hasRange=self.joinpath(rangepath),
                                                favorite=idx < 3,
                                                derived=attr.get("Derived") == 'true',
                                                required="MANDATORY" if attr.get(
                                                    "Mandatory") == 'true' else "OPTIONAL",
                                                cardinality="MANY" if attr.get(
                                                    "MultiValued") == 'true' else "ONE"
                                                )
            jsonstruct.append(attribut)

        utlinks = alwayslist(ut.get("UserTypeLink"))
        for utlink in utlinks:
            utlinkid = self.loadedstep._getanyid(elem=utlink,
                                                 anyid="@UserTypeID")
            destut = self.loadedstep.getelement(elements=self.loadedstep.myusertypes,
                                                idval=utlinkid)
            # destinationtype = "UmlAssociation" if modeltype == "DM" else "Relationship"
            if destut is None:
                logging.warning(f"in relation {utlinkid} usertyperef does not exist.")
            else:
                destpath = self._usertypecollection(destut.get("PATH"))
                rela = Json2dataspot.fillstruct(elementtype="UmlAssociation",
                                                title=f"{utlinkid} contains {ut.get('ID')}",
                                                hasDomain=self.joinpath(destpath + [destut.get("ID")]),
                                                name="contains",
                                                hasRange=self.joinpath(collectionpath + [ut.get("ID")]),
                                                domainMultiplicity="1",
                                                rangeMultiplicity="0..*",
                                                required="OPTIONAL",
                                                cardinality="MANY"
                                                )
                #        return ("0.." if not mand else "1.." if card == "M" else "") + ("*" if card == "M" else "1")
                jsonstruct.append(rela)

        return

    def generatxrefs(self, jsonstruct, xreftype,
                     xref):
        utlinks = alwayslist(xref.get("UserTypeLink"))
        targetlinks = alwayslist(xref.get("TargetUserTypeLink"))
        attrgroups = alwayslist(xref.get("AttributeGroupLink"))
        attributes = alwayslist(xref.get("AttributeLink"))

        metadata = xref.get("MetaData")
        descr = self._getfrommetadata(elem=xref,
                                      fieldname="Purpose"
                                      )
        if xref.get("ID") in [ut.get("label") for ut in jsonstruct
                              if ut.get("_type") in ("UmlClass", "Collection")]:
            logging.warning(f"duplicate crossref element {xref.get('ID')}")
            return
        locjsonstruct = []
        newpath = self._usertypecollection(xref.get("PATH"))
        self.generateusertype(jsonstruct=locjsonstruct,
                              collectionpath=newpath,
                              ut={"ID": xref.get("ID"),
                                  "Name": xref.get("Name"),
                                  "description": descr,
                                  "examples": None,
                                  "AttributeLink": attributes,
                                  "AttributeGroupLink": attrgroups,
                                  "PATH": newpath
                                  })
        relacount = 0
        for utlink in utlinks:
            utlinkid = self.loadedstep._getanyid(elem=utlink,
                                                 anyid="@UserTypeID")
            destut = self.loadedstep.getelement(elements=self.loadedstep.myusertypes,
                                                idval=utlinkid)
            if destut is None:
                logging.warning(
                    f"in xref {xref.get('Name')} usertypref {utlinkid} does not exist.")
            else:
                destutpath = self._usertypecollection(destut.get("PATH"))
                rela = {
                    "_type": "UmlAssociation",
                    "title": f"{utlinkid} {'->'} {xref.get('ID')}",
                    "hasDomain": self.joinpath(destutpath + [destut.get("ID")]),
                    "name": f"{utlinkid} {xreftype} {xref.get('ID')}",
                    "hasRange": self.joinpath(newpath + [xref.get("ID")]),
                    "domainMultiplicity": "0..1",
                    "rangeMultiplicity": "0..*",
                    "required": "OPTIONAL",
                    "cardinality": "MANY"
                }
                locjsonstruct.append(rela)
                relacount += 1
        for targetlink in targetlinks:
            targetid = self.loadedstep._getanyid(elem=targetlink,
                                                 anyid='@UserTypeID')
            target = self.loadedstep.getelement(elements=self.loadedstep.allusertypes,
                                                idval=targetid)
            if target is None:
                logging.warning(f"in xref {xref.get('Name')} usertypref {targetid} does not exist.")
            else:
                targetpath = self._usertypecollection(target.get("PATH"))
                rela = {
                    "_type": "UmlAssociation",
                    "title": f"{xref.get('ID')} {'->'} {targetid}",
                    "hasDomain": self.joinpath(newpath + [xref.get("ID")]),
                    "name": f"{xref.get('ID')} {xreftype} {target.get('ID')}",
                    "hasRange": self.joinpath(targetpath + [target.get("ID")]),
                    "domainMultiplicity": "0..*",
                    "rangeMultiplicity": "0..1",
                    "required": "OPTIONAL",
                    "cardinality": "ONE"
                }
                locjsonstruct.append(rela)
                # destinationtype = "UmlAssociation" if modeltype == "DM" else "Relationship"
                relacount += 1
        if relacount > 0:
            jsonstruct.extend(locjsonstruct)
        return

    def _usertypecollection(self, collpath):
        """extract the usertypecollection
        chosen for this transfer from the full path.
        take first element
        if second element is standard collection, take it as well
        all collection postfixes
        """
        if collpath is None: return None
        if len(collpath) == 0: return collpath
        retval = [collpath[0]]
        retval.extend([c for c in collpath[1:] if c in self.standardcollnames])

        return self._addcollname(retval)

    def generatedsjson(self):
        # TODO for modelname, modelval in self.models.items():
        jsonstruct = []

        self.generatedmcollections(jsonstruct=jsonstruct)
        idx = 0
        for ut in self.loadedstep.myusertypes:
            # only top level collections are used
            collectionpath = self._usertypecollection(ut.get("PATH"))
            self.generateusertype(jsonstruct=jsonstruct,
                                  collectionpath=collectionpath,
                                  ut=ut)
            """ UmlClass.inCollection, line: 30447: Asset AssetCrossReferenceType_coll was not found in Data model BT step datamodel!
Fehler abfangen?        <UserType ID="Entity user-type root" >
          <Name>MANUALLY ADDED, MISSTING UserTyoe in Expoert</Name>
      </UserType>

"""
        for xreftype, xrefs in self.loadedstep.xreftypes.items():
            for xref in xrefs:
                # if xref.get("MODEL") == self.datamodelfullname:
                if xreftype in ("EntityCrossReferenceType"):
                    # TODO handle other types
                    """ AssetCrossReferenceType,ProductCrossReferenceType, ClassificationCrossReferenceType, 
                        ClassificationProductLinkType, 
                    """
                    self.generatxrefs(jsonstruct=jsonstruct,
                                      xreftype=xreftype,
                                      xref=xref)

        return jsonstruct


def generatemodels(outpath,
                   dsmodelname: str,
                   loadedstep: LoadStep):
    """

    @param outpath: path to write the files to
    @param loadedstep:loaded step, with information about model names
    @return: 3 files in the outpath directory
    """
    stepmodel = Step2Dataspot(dsmodelname=dsmodelname,
                              loadedstep=loadedstep)
    outfilepath = Path(outpath, stepmodel.referencemodelname + ".json")
    with open(outfilepath, 'w') as outfile:
        json.dump(stepmodel.generatereferences(), outfile, indent=2)
        logging.info(f"Referencemodel generated into file {str(outfilepath)}")
        print(f"Referencemodel generated into file {str(outfilepath)}")

    outfilepath = Path(outpath, stepmodel.domainmodelname + ".json")
    with open(outfilepath, 'w') as outfile:
        json.dump(stepmodel.generatedomains(), outfile, indent=2)
        logging.info(f"Domains generated into file {str(outfilepath)}")
        print(f"Domains generated into file {str(outfilepath)}")

    outfilepath = Path(outpath, stepmodel.datamodelfullname + ".json")
    with open(outfilepath, 'w') as outfile:
        json.dump(stepmodel.generatedatatmodel(), outfile, indent=2)
        logging.info(f"Datamodel generated into file {str(outfilepath)}")
        print(f"Datamodel generated into file {str(outfilepath)}")
