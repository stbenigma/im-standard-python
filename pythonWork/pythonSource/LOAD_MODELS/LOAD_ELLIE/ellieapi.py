import json
import re
from datetime import datetime

from SSOT_infra import nvl
from SSOT_db.IM_OBJECTS import  *
from SSOT_db import IM_JSON

SOURCE_ELLIE: str = 'ELLIE'

def ellie2proj(pmodel, pmodellng):
    proj = Project()
    proj.proj_name = pmodel['name']
    proj.proj_type = pmodel['level']
    proj.proj_curr_lang = pmodellng
    proj.proj_uc = 'loadellie'
    proj.proj_dc = pmodel["createdAt"]
    proj.proj_um = 'loadellie'
    proj.proj_dm = pmodel["updatedAt"]
    return IM_JSON.proj2js(pprojs=[proj])


def ellie2lang(pmodellng):
    lang = Language(lang_iso_code2=pmodellng,
                    lang_is_base_lang = True)
    return IM_JSON.langs2js(plangs=[lang])


nvlkey = lambda x, m: m[x] if x in m else None

attributes = []


def ellie2attr(pentiid, pattrid, pellieattr, pmodellng) -> Attribute:
    attr = Attribute(pname=pellieattr, pentiid=pentiid
                     , psrcname=SOURCE_ELLIE, psrcid=pellieattr['id'])
    attr.attr_dc = pellieattr['created_at']
    attr.attr_id = pattrid
    attr.attr_displ_name = pellieattr['name']
    attr.attr_displ_name_l = {pmodellng: pellieattr['name']}
    attr.attr_doma_id = None
    attr.attr_tech_name = pellieattr['name']
    attr.attr_displ_seq = pellieattr['order']
    attr.attr_tooltip = None
    attr.attr_tooltip_l = None
    descr = nvlkey('description', pellieattr['metadata'])
    attr.attr_descr = descr
    attr.attr_descr_l = {pmodellng: descr}
    attr.attr_is_descriptive = None
    attr.attr_is_mandatory = None
    attr.attr_is_historicised = None
    attr.attr_is_repeated = None
    attr.attr_is_translated = None
    attr.attr_is_encrypted = None
    attr.attr_uc = None
    attr.attr_um = None
    attr.attr_dm = None
    # save attribute for later generation as attribute
    attributes.append(attr)
    return attr


entitransl = {}


def ellie2entities(pinjson, pmodellng):
    entis = []
    for entiid, inenti in enumerate(pinjson):
        metadata = inenti["metadata"]
        entitransl[inenti["id"]] = entiid
        enti = Entity(psrcname=SOURCE_ELLIE, psrcid=inenti["id"])
        enti.enti_id = entiid
        enti.enti_name = inenti['name']
        enti.enti_name_l = {pmodellng: inenti['name']}
        enti.enti_short_name = None
        enti.enti_descr = nvlkey("Description", metadata)
        enti.enti_descr_l = {pmodellng: nvlkey("Description", metadata)}
        enti.enti_tooltip = None
        enti.enti_tooltip_l = None
        enti.enti_enca_id = None
        enti.enti_exp_tuplecnt = None
        enti.enti_prefix = None
        enti.enti_enca_id = None
        enti.enti_um = None
        enti.enti_dm = None
        enti.enti_uc = None
        enti.enti_dc = None
        insynos = nvlkey("Synonyms", metadata)
        synos = []
        if insynos is not None and insynos != '':
            for synoid, s in enumerate(insynos.split(',')):
                syno = Synonym()
                syno.syno_id = (100 * entiid) + synoid
                syno.syno_name = s
                syno.syno_name_l = {pmodellng: s}
                syno.syno_enti_id = entiid
                synos.append(syno)
            # for
        # fi
        enti.setsynonyms(synos)

        inexpl = nvlkey("Examples", metadata)
        expls = []
        if inexpl is not None and inexpl != '':
            for explid, e in enumerate(re.split('\n', inexpl)):
                expl = Example()
                expl.expl_id = (100 * entiid) + explid
                expl.expl_value = e
                expl.expl_value_l = {pmodellng: e}
                expl.expl_enti_id = entiid
                expl.expl_attr_id = None
                expls.append(expl)
            # for
        enti.setexamples(expls)

        attrs = []
        inattrs = nvlkey("attributes", inenti)
        if inattrs is not None:
            for attrid, a in enumerate(inattrs):
                attrs.append(ellie2attr(pentiid=entiid, pattrid=(100 * entiid) + attrid, pellieattr=a,
                                        pmodellng=pmodellng))
            # for
        # fi
        enti.setattributes(attrs)

        enti.setschluessel([])

        entis.append(enti)
    # for
    return IM_JSON.entities2js(pentis=entis)


def ellie2relations(pinjson,pmodellng):
    def getenti(pinjson):
        return {'entiid':entitransl[pinjson['id']],'type':nvl(nvlkey('startType',pinjson))+nvl(nvlkey('endType',pinjson))}

    for r in pinjson:
        srcenti = getenti(r["sourceEntity"])
        targenti = getenti(r["targetEntity"])
        assocs = r['description']
        #print (srcenti,targenti,assocs)
        if srcenti[type = 'superType']:
            pass
        elif srcenti[type = 'subType']:
            pass
        else:
            pass
    return {}


def elliejson2json(pelliejson: str) -> str:
    modellng = 'en'
    outjson = {}
    model = pelliejson['model']
    outjson[IM_JSON.JSModel.elemtype2label(IM_JSON.JSModel.ELEMTYPE_PROJ)] = ellie2proj(pmodel=model,
                                                                                        pmodellng=modellng)
    outjson[IM_JSON.JSModel.elemtype2label(IM_JSON.JSModel.ELEMTYPE_LANG)] = ellie2lang(pmodellng=modellng)
    outjson[IM_JSON.JSModel.elemtype2label(Modelelemtype.ENTI)] = ellie2entities(pinjson=model["entities"],
                                                                                 pmodellng=modellng)
    outjson[IM_JSON.JSModel.elemtype2label(Modelelemtype.ATTR)] = IM_JSON.attributes2js(pattrs=attributes)
    outjson[IM_JSON.JSModel.elemtype2label(Modelelemtype.RELA)] = ellie2relations(pinjson=model["relationships"],
                                                                                  pmodellng=modellng)
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.ARCS)] = arcs2js(pemptymodel=True)
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.KEYS)] = keys2js(pemptymodel=True)
    # #IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.KEYS)] = businessrules2js(pemptymodel=True)
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.DOCU)] = documents2js(pemptymodel=True)
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.ORGU)] = orgUnits2js(pemptymodel=True)
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(IM_JSON.JSModel.ELEMTYPE_CATG)] = categories2js(pemptymodel=True)
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.INTF)] = systems2js(pemptymodel=True)
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.TABL)] = tables2js(pemptymodel=True)
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.COLU)] = columns2js(pemptymodel=True)
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.DIAG)] = diagrams2js(pemptymodel=pemptymodel, pmodelname=IM_JSON.JSModel['pmodel']['name'])
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.UDPR)] = udps2js(pemptymodel=True)
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.PHYU)] = physicalunits2js(pemptymodel=True)
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.DATY)] = datatypes2js(pemptymodel=True)
    # IM_JSON.JSModel[IM_JSON.JSModel.elemtype2label(Modelelemtype.STFO)] = storageformats2js(pemptymodel=True)

    modelhash = IM_JSON.make_hash(outjson)
    outjson['_imprint_'] = {"database": "None"
        , "created": str(datetime.today())
        , "Modelversion": ""
        , "hashvalue": modelhash
        ,
                            "comment": "Entries ending with + represent denormalized data and are not checked for consistency while reading back"}

    return outjson


if __name__ == '__main__':
    import sys

    infile = sys.argv[1]
    with open(infile, 'r') as inf:
        elliejson = json.loads(inf.read())
    with open("/Users/stb/Downloads/ellitest.json", 'w') as f:
        f.write(json.dumps(elliejson2json(pelliejson=elliejson), indent=4))
        print("~/Downloads/ellitest.json created")
