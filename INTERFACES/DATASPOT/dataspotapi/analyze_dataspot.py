import sys

from LOAD_MODELS.LOAD_INFRA import mergedbs
from SSOT_db.IM_JSON import *
from SSOT_infra import nvl
from LOAD_MODELS.LOAD_DATASPOT import *

DATASPOTSRCNAME = "imstandard_dataspot"


def translatestatus(status):
    if status in ("Veröffentlicht"):  # TODO
        return "PUBL"
    elif status in ("Abgenommen"):  # TODO
        return "GTOP"
    else:
        return "DRAFT"

newdsmodel:DSTenant = None
modelenties = dict()
modelrelas = dict()
modeldomas = dict()
modelattrs = dict()
modelarcs = dict()
modeldiags = dict()


def entiidbyname(name):
    nameid = {elem["shortName"]: lkey for lkey, elem in modelenties.items()}
    retval = nameid[name]
    return retval


def attridbyname(name):
    nameid = {elem["techname"]: lkey for lkey, elem in modelattrs.items()}
    retval = nameid[name]
    return retval


def domainidbyname(name):
    nameid = {elem["name"]["en"]: lkey for lkey, elem in modeldomas.items()}
    retval = nameid.get(name)
    return retval


def enti2js(enti: dict,lang) -> dict:
    """{
  "_type" : "BusinessObject",
  "id" : "63ecebc7-6f44-4b57-8ac6-6dd2c0729afe",
  "href" : "/web/foryouandyourcustomers-ch/classifiers/63ecebc7-6f44-4b57-8ac6-6dd2c0729afe",
  "label" : "Produktinstanz",
  "description" : "einzelnes, weltweit identifizierbares Exemplar eines Produktes.\n\nMit oder ohne IOT.",
  "inCollection" : "Produkte",
  "favorite" : true,
  "status" : "WORKING",
  "createdBy" : "sberner",
  "dateCreated" : 1683900399504
}"""
    catg = newdsmodel.getcategorybyname(name=enti.get('inCollection'))
    if catg is None:
        catgid=None
    else:
        catgid=catg.elemid

    retval = jsonentity(
        name=multilangstring(string=nvl(enti.get('title'), enti.get('label')),lang=lang),
        shortname=enti.get('label'),
        uc=enti.get('createdBy'), dc=enti.get('dateCreated'),
        publstatus=translatestatus(enti.get("status")),
        descr=multilangstring(string=enti.get('description'),lang=lang), tooltip=multilangstring(string="",lang=lang),
        category=catgid,
        supertypeentity=enti.get('subtypeOf'),
        icon=dict(),
        synonyms=[] if enti.get("synonyms") is None else [multilangstring(string=s,lang=lang)
                                                          for s in enti.get("synonyms")],
        examples=[] if enti.get("examples") is None else [multilangstring(string=s,lang=lang)
                                                          for s in enti.get("examples")],
        sourceref={DATASPOTSRCNAME: [enti.get('id'), str(datetime.today())]},
        referencedby=[], userdefprops=dict()
    )
    return retval


def rela2js(rela: dict,lang):
    """
{
  "_type" : "Relationship",
  "id" : "b23a541a-0ef3-4f9e-ad7a-3a28af22424a",
  "href" : "/web/foryouandyourcustomers-ch/associations/b23a541a-0ef3-4f9e-ad7a-3a28af22424a",
  "hasDomain" : "Gebiet",
  "name" : "unterteilt",
  "hasRange" : "Gebiet",
  "stereotype" : "many2many",
  "status" : "WORKING",
  "createdBy" : "sberner",
  "dateCreated" : 1683902278832,
  "required" : "OPTIONAL",
  "cardinality" : "MANY",
}
    """

    def relaend(many, name, mand, entiid, arcid):
        return jsonrelationend(enti=entiid,
                               arc=arcid,
                               assoc=multilangstring(string=name,lang=lang),
                               maptype="M" if many == "MANY" else "1",
                               hist=False,
                               mandatory=mand.upper() != 'OPTIONAL')

    def translrelatype(dstype):
        if dstype == "many2many":
            return "M:N"
        elif dstype == "one2one":
            return "1:1"
        elif dstype == "role":
            return "ISAR"
        elif dstype == "subtype":
            return "ISAS"
        elif dstype == "one2many":
            return "M:1"
        else:
            logging.error(f"illegal sterotype for relation: {dstype}")
            return None

    retval = jsonrelation(name=rela.get("id"),
                          relatype=translrelatype(dstype=rela.get("stereotype")),
                          relafrom=relaend(many=rela.get('cardinality'),
                                           name=rela.get("name"), mand=rela['required'],
                                           entiid=entiidbyname(rela.get("hasDomain")),
                                           arcid=arcname(arcno=rela.get("ARC"),
                                                         entiid=entiidbyname(rela.get("hasDomain")))),
                          relato=relaend(many=rela.get("BCKWCARDINALITY"),
                                         name=rela.get("inverseName"),
                                         mand=rela.get("BCKWOPTIONALITY"),
                                         entiid=entiidbyname(rela.get("hasRange")),
                                         arcid=arcname(arcno=rela.get("BCKWARC"),
                                                       entiid=entiidbyname(rela.get("hasRange")))),
                          sourceref={DATASPOTSRCNAME: [rela.get('id'), str(datetime.today())]},
                          uc=rela.get('createdBy'), dc=rela.get('dateCreated'),
                          publstatus=translatestatus(rela.get("status"))
                          )

    return retval


def doma2js(doma: dict, lang,values=[]) -> dict:
    """{
  "_type" : "DataDomain",
  "id" : "e60eed5f-c787-4340-b1c2-cce7dfcd23b0",
  "href" : "/web/foryouandyourcustomers-ch/datatypes/e60eed5f-c787-4340-b1c2-cce7dfcd23b0",
  "label" : "Betrag",
  "inCollection" : "Allgemeine Domänen",
  "status" : "WORKING",
  "createdBy" : "stb@foryouandyourcustomers.com",
  "dateCreated" : 1690633179296,
  "baseType" : "DECIMAL",
  "integerDigits" : 8,
  "fractionDigits" : 2

  "baseType" : "STRING",
  "minLength" : 0,
  "maxLength" : 250,
  "pattern" : "Zeichen"

  "baseType" : "BOOLEAN",
  "baseType" : "DATETIME",

}"""

    def translatedomatypes(dstype):
        if dstype == "DECIMAL":
            return Domain.NUM
        elif dstype == ("STRING", "BOOLEAN"):
            return Domain.TXT
        elif dstype in ("DATETIME", "DATE", "TIME"):
            return Domain.DAT
        else:
            return Domain.BIN

    if doma.get("_type") == "ReferenceObject":
        # LOV type
        basetype = Domain.TXT
        domavals = [jsondomainvalue(value=val["timeSeries"][0]["code"], sort=idx,
                                    displ=val["timeSeries"][0].get("shortText"),
                                    descr=val["timeSeries"][0].get("longText"),
                                    uc=val.get("createdBy"), dc=val.get("dateCreated"),
                                    mappedto=[],mappedfrom=[])
                    for idx, val in enumerate(values)]
    else:  # non lov type
        basetype = translatedomatypes(doma.get("baseType"))
        domavals = [jsondomainvalue(value=val[0], sort=val[1], displ=val[2],
                                    uc=doma.get("createdBy"), dc=doma.get("dateCreated"))
                    for val in [["TRUE", 1, "True,"],
                                ["FALSE", 2, "False,"]]
                    ] if doma.get("baseType") == "BOOLEAN" else []

    retval = jsondomain(name=multilangstring(string=doma.get("label"),lang=lang), domtype=basetype,
                        domorigin=Domain.DOMAIN, uc=doma.get("createdBy"), dc=doma.get("dateCreated"),
                        descr=multilangstring(string=nvl(doma.get("descr"), doma.get("title")),lang=lang),
                        totaldigits=(nvl(doma.get("integerDigits"), 0) +
                                     nvl(doma.get("fractionDigits"), 0)) if basetype == Domain.NUM else None,
                        fractdigits=nvl(
                            doma.get("fractionDigits"), 0) if basetype == Domain.NUM else None,
                        roundvalue=None,
                        minvalue=doma.get("fractionDigits") if basetype in (Domain.NUM, Domain.DAT) else None,
                        maxvalue=doma.get("fractionDigits") if basetype in (Domain.NUM, Domain.DAT) else None,
                        unit=None,
                        maxlng=doma.get("maxLength") if basetype == Domain.TXT else None,
                        syntaxrule=doma.get("pattern") if basetype == Domain.TXT else None,
                        granularity=Domain.MINUTE if basetype in Domain.DAT else None,
                        elements=[],  # groups not yet handled
                        values=domavals,
                        contenttype=Domain.OTHER if basetype == Domain.BIN else None,
                        sourceref={DATASPOTSRCNAME: [doma.get('id'), str(datetime.today())]}
                        )
    return retval


def attr2js(attr: dict,lang):
    """{
  "_type" : "BusinessAttribute",
  "id" : "2bc8a266-78dc-4b48-b203-ada12634ce0c",
  "href" : "/web/foryouandyourcustomers-ch/attributes/2bc8a266-78dc-4b48-b203-ada12634ce0c",
  "hasDomain" : "Land",
  "label" : "ISO-2",
  "order" : 1,
  "title" : "Name translated",
  "hasRange" : "/CRM/ISO-Land",
  "status" : "WORKING",
  "createdBy" : "sberner",
  "dateCreated" : 1683899079955,
  "required" : "MANDATORY",
  "cardinality" : "ONE",
  "identifying" : true
  "multilingual" : true
  "temporal" : true
}"""
    retval = jsonattribute(
        name=multilangstring(string=nvl(attr.get('label')),lang=lang),
        techname=attr.get('label'),
        uc=attr.get('createdBy'), dc=attr.get('dateCreated'),
        publstatus=translatestatus(attr.get("status")),
        descr=multilangstring(string=attr.get('description'),lang=lang),
        tooltip=multilangstring(string=nvl(attr.get('title')),lang=lang),
        examples=[] if attr.get("examples") is None else [multilangstring(string=s,lang=lang)
                                                          for s in attr.get("examples")],
        seq=attr.get("order"),
        entity=entiidbyname(attr.get("hasDomain")),
        domain=nvl(domainidbyname(attr.get("hasRange")),
                   domainidbyname("Unknown")),
        # descriptive= attr.get("") ,
        mandatory=attr.get("required") == "MANDATORY",
        historicised=attr.get("temporal"),
        repeated=attr.get("cardinality") != "ONE",
        translated=attr.get("multilingual"),
        # encrypted= attr.get("") ,
        # minzoomlevel= attr.get("") ,
        # maxzoomlevel= attr.get("") ,
        sourceref={DATASPOTSRCNAME: [attr.get('id'), str(datetime.today())]},
    )
    return retval


def attr2diag(attrid, attr) -> dict:
    return dict()


def arcname(arcno, entiid):
    return None if arcno is None else f"{str(entiid)}-{str(arcno)}"


def do1arc(entiid, relaid, arcno, arcs):
    aname = arcname(arcno=arcno, entiid=entiid)
    if aname not in arcs:
        arcs[aname] = jsonarc(name=aname,
                              entity=entiid,
                              relations=[],
                              sourceref={DATASPOTSRCNAME: [aname, str(datetime.today())]},
                              uc="SYS",
                              dc=str(datetime.today()))
    arcs[aname]["relations+"].append(relaid)
    return


def extractarc(arcs, rela):
    """extract any arc from rela and create the element
    """
    if rela.get("ARC") is not None:
        do1arc(arcs=arcs,
               entiid=entiidbyname(rela.get("hasDomain")),
               relaid=rela.get("id"),
               arcno=rela.get("ARC")
               )
    if rela.get("BCKWARC") is not None:
        do1arc(arcs=arcs,
               entiid=entiidbyname(rela.get("hasRange")),
               relaid=rela.get("id"),
               arcno=rela.get("BCKWARC"))
    return


def transfer2mymodel(readmodel, mymodel):
    for entry in readmodel:
        typ = entry["_type"]
        if typ not in mymodel:
            mymodel[typ] = []
        mymodel[typ].append(entry)
    return

def createsubtyperelation(supertypes: dict,lang):
    """create an arc for all ISAS-Relations
        then create a relation for every subtype
    """
    for superentiid, subentiids in supertypes.items():
        aname = f"SUPERTYPE{superentiid}"
        modelarcs[aname] = jsonarc(name=aname,
                                   entity=superentiid,
                                   relations=[],
                                   sourceref={DATASPOTSRCNAME: [aname, str(datetime.today())]},
                                   uc="SYS", dc=str(datetime.today()))
        # create a relation for every subtype
        for subentiid in subentiids:
            relaid = f"{subentiid[3:13]}-{superentiid[3:13]}"
            modelarcs[aname]["relations+"].append(relaid)

            modelrelas[relaid] = jsonrelation(name=relaid,
                                              relatype=Relation.ISASUBTYPE,
                                              relafrom=jsonrelationend(enti=subentiid,
                                                                       arc=None,
                                                                       assoc=multilangstring(string="",lang=lang),
                                                                       maptype="1",
                                                                       hist=False,
                                                                       mandatory=True),
                                              relato=jsonrelationend(enti=superentiid,
                                                                     arc=aname,
                                                                     assoc=multilangstring(string="",lang=lang),
                                                                     maptype="1",
                                                                     hist=False,
                                                                     mandatory=True),
                                              sourceref={DATASPOTSRCNAME: [relaid, str(datetime.today())]},
                                              uc=modelenties[subentiid].get("uc"), dc=modelenties[subentiid].get("dc"),
                                              publstatus=modelenties[subentiid].get("publstatus")
                                              )
    return


def main(argv):
    global newdsmodel
    raise Exception(f"analyze dataspot-json file is currently not active")
    mymodel = dict()
    imfilename = Path(argv[1])
    lang="en"

    with open(imfilename, 'r') as src:
        dsmodel = json.load(src)
        transfer2mymodel(readmodel=dsmodel, mymodel=mymodel)

    if len(argv) > 1:
        domainfilename = Path(argv[2])
        with open(domainfilename, 'r') as src:
            domainmodel = json.load(src)
            transfer2mymodel(readmodel=domainmodel, mymodel=mymodel)
    else:
        domainfilename = None
        domainmodel = []

    if len(argv) > 2:
        dmfilename = Path(argv[3])
        with open(dmfilename, 'r') as src:
            datamodel = json.load(src)
            transfer2mymodel(readmodel=datamodel, mymodel=mymodel)
    else:
        dmfilename = None
        datamodel = []

    if len(argv) > 3:
        refmodelfilename = Path(argv[4])
        with open(refmodelfilename, 'r') as src:
            refmodel = json.load(src)
            transfer2mymodel(readmodel=refmodel, mymodel=mymodel)
    else:
        refmodelfilename = None
        refmodel = []

    newdsmodel=DSTenant(lang="de",tenantname="testfiles")
    newdsmodel.loadfile(filepath=imfilename,modeltype=DSAccess.BusinessDataModel)
    newdsmodel.loadfile(filepath=domainfilename,modeltype=DSAccess.DataDomainModel)
    newdsmodel.loadfile(filepath=dmfilename,modeltype=DSAccess.UmlModel)
    newdsmodel.loadfile(filepath=refmodelfilename,modeltype=DSAccess.ReferenceDataModel)

    for enti in mymodel["BusinessObject"]:
        modelenties[enti["id"]] = enti2js(enti=enti,lang=lang)

    for rela in mymodel["Relationship"]:
        extractarc(arcs=modelarcs, rela=rela)
        modelrelas[rela["id"]] = rela2js(rela=rela,lang=lang)

    supertypes = dict()
    for enti in mymodel["BusinessObject"]:
        subtypeof = enti.get('subtypeOf')
        if subtypeof is not None:
            mainentiid = entiidbyname(subtypeof)
            if mainentiid not in supertypes:
                supertypes[mainentiid] = list()
            supertypes[mainentiid].append(enti.get("id"))
            modelenties[enti.get("id")]["supertypeentity"] = mainentiid
    # for enti in mymodel[""]:
    createsubtyperelation(supertypes=supertypes,lang=lang)

    modeldomas["UNKNOWN"] = jsondomain(name=multilangstring(string="Unknown",lang=lang),
                                       domtype="TXT", domorigin=Domain.DOMAIN,
                                       sourceref={DATASPOTSRCNAME: ["UNKNOWN", str(datetime.today())]
                                                  },
                                       uc="SYS", dc=str(datetime.today()),
                                       descr=multilangstring(string="Dummy-domain for unknown domain",
                                                             lang=lang))

    for doma in mymodel["DataDomain"]:
        modeldomas[doma["id"]] = doma2js(doma=doma,lang=lang)

    for doma in mymodel["ReferenceObject"]:
        modeldomas[doma["id"]] = doma2js(doma=doma,
                                         values=[val for val in mymodel["ReferenceValue"]
                                                 if val["literalOf"] == doma.get("label")],
                                         lang=lang)

    for attr in mymodel["BusinessAttribute"]:
        modelattrs[attr["id"]] = attr2js(attr,lang=lang)

    # for key, val in modeldomas.items(): print(key, val)
    # for key, val in modelenties.items(): print(key, val)
    # for key, val in modelarcs.items():    print(key, val)
    # for key, val in modelrelas.items():   print(key, val)
    # for key, val in modeldomas.items():    print(key, val)
    # for key, val in modelattrs.items():    print(key, val)
    # for key, val in modeldiags.items():    print(key, val)

    jsmodel = JSModel()
    for key, value in jsmodel._elemtype2label.items():
        jsmodel.jsmodel[value] = dict()

    jsmodel.jsmodel["model"] = jsonproject(name="Fachdatenmodell",
                                           modeltype="logical",
                                           language="en",
                                           uc="stb",
                                           dc="2018-03-07 06:15:36 UTC",
                                           um="SYS",
                                           dm="2023-04-03 10:36:20.947053")
    jsmodel.jsmodel["languages"] = {'en': jsonlanguage(isoname="English", iso3="eng",
                                                       modellanguage=True)}
    jsmodel.jsmodel["categories"] = {cat.elemid : cat.spodjson() for cat in newdsmodel.categories() }
    jsmodel.jsmodel["entities"] = modelenties
    jsmodel.jsmodel["relations"] = modelrelas
    jsmodel.jsmodel["domains"] = modeldomas
    jsmodel.jsmodel["attributes"] = modelattrs
    jsmodel.jsmodel["arcs"] = modelarcs
    jsmodel.jsmodel["diagrams"] = modeldiags
    jsmodel.jsmodel["_imprint_"] = jsmodel.jsonimprint(dbname="",
                                               created=str(datetime.today()),
                                               modelversion="2.0",
                                               jsonversion="1.0",
                                               hashvalue=None,
                                               gitrevision="0")

    outputfile = imfilename.with_name(imfilename.stem + "_loaded" + imfilename.suffix)
    jsmodel.write_json(outputfile)
    print(f"loaded json file created in {outputfile}")
    mergedbs.checkjsonfile(pjsonfilepath=outputfile, pverbose=True)

    jsmodel.write_json(outputfile)

    # Create pure spod version with our id's
    jsmodel.jsmodel = mergedbs.jsonviadbtojson(pmodel=jsmodel, psrcname=DATASPOTSRCNAME)
    spodjsonfile = imfilename.with_name(imfilename.stem + "_spod" + imfilename.suffix)
    jsmodel.write_json(spodjsonfile)
    print(f"spod json file written to {spodjsonfile}")
    return spodjsonfile

    # listWebdoku.webmain(pjsonfilepath=spodjsonfile, pwebdirec=spodjsonfile.parent,
    #                    pmodelname="dstest", pfiletype="html", singlefile=True)

    # result = mergejson2sql(pmodel=jsmodel, psrcname=DATASPOTSRCNAME, pverbose=True)
    # print(result)


if __name__ == '__main__':
    # make sure 1. argument in sysargv exists as file
    if len(sys.argv) > 1 and Path(sys.argv[1]).exists():
        main(argv=sys.argv)
    else:
        print("ERROR: no infile found")
