from copy import deepcopy

from SSOT_db.IM_JSON import *

SPODMIROSOURCE = "MIRO"


def translateentiid(origmodel, entiid, reftype=SPODMIROSOURCE):
    """
        looks up entity ID as sourceref in origmodel.
        if  found return ID of found entity, else return None
    """
    origentiid, origenti = origmodel.getbysrcref(psrcname=reftype, psrcid=entiid)
    return None if origentiid is None else origentiid


def anyentiid(origmodel: JSModel, entiid, reftype=SPODMIROSOURCE):
    """
        looks up entity ID in original model
        if  found return ID
        if not found look up id in sourceref,
            if found return entiid
            else return None
    """
    if entiid in origmodel.getelements("entities").keys():
        origentiid = entiid
    else:
        origentiid, _ = origmodel.getbysrcref(psrcname=reftype, psrcid=entiid)
    if origentiid is None:
        logging.error(f"Entity-id {entiid} not found as json or external ({reftype}) id")
    return origentiid


def anyrelaid(origmodel: JSModel, relaid, reftype=SPODMIROSOURCE):
    """
        looks up relation ID in original model
        if  found return ID
        if not found look up id in sourceref,
            if found return relaid
            else return None
    """
    if relaid in origmodel.getelements("relations").keys():
        origrelaid = relaid
    else:
        origrelaid, _ = origmodel.getbysrcref(psrcname=reftype, psrcid=relaid)
    if origrelaid is None:
        logging.error(f"Relation-id {relaid} not found as json or external ({reftype}) id")
    return origrelaid


def mergeentities(original, newjson, lang):
    miromergelogger = logging.getLogger("miromerge")
    for entiid, enti in newjson.getelements("entities").items():
        origentiid = translateentiid(origmodel=original, entiid=entiid)
        # entiid not found in sourceref
        if origentiid is None:
            # entity not found via sourceref-id, but could have same entity-name
            samenameentities = original.getbyfield(ptype="entities", pvalue=enti['name'][lang], plang=lang)
            if len(samenameentities) == 0:
                # entity is new, add it to the original file with the new entiid (for reference in diagram)
                original.jsmodel["entities"][entiid] = deepcopy(enti)
                origenti = enti  # for later sourcerefupdate
                miromergelogger.info(f"Entity: added \"{enti['name'][lang]}\"")
            else:
                # entity with same name found
                origentiid, origenti = samenameentities[0]
                # map to entity found in MIRO
                origenti["sourceref"][SPODMIROSOURCE] = enti["sourceref"][SPODMIROSOURCE]
                miromergelogger.info(f"Entity: mark \"{origenti['name'][lang]}\" as miro-referenced")
        else:
            # original entity found
            origenti = original.getbyid(pjsid=origentiid, ptype="entities")
            if origenti["name"][lang] != enti["name"][lang]:
                miromergelogger.info(f"Entity: name \"{origenti['name'][lang]}\" changed to " + \
                                     f"\"{enti['name'][lang]}\"")
                origenti["name"][lang] = enti["name"][lang]

        # if supertypeenti exists, replace reference to original
        superentiid, superenti = original.getbysrcref(psrcname=SPODMIROSOURCE, psrcid=enti["supertypeentity"])
        if superentiid is not None:
            origenti["supertypeentity"] = superentiid

    return

def whitespace(s:str)->str:
    return None if s is None else s.replace("\n"," ").strip()


def equalassoc(origrela: dict, newrela: dict, lang: str) -> bool:

    # true if both assocs (from<->to) in this language are equal
    # or both are in a role or subtype and both assocs are allowed for roles or subtypes
    return (origrela["type"] in (Relation.ISAROLE, Relation.ISASUBTYPE) and
            origrela["to-from"]["assoc"][lang] in ROLEASSOCIATIONS and
            newrela["to-from"]["assoc"][lang] in ROLEASSOCIATIONS and
            origrela["from-to"]["assoc"][lang] in ROLEASSOCIATIONS and
            newrela["from-to"]["assoc"][lang] in ROLEASSOCIATIONS
            ) or \
           (whitespace(origrela["to-from"]["assoc"][lang]) == whitespace(newrela["to-from"]["assoc"][lang]) and
            whitespace(origrela["from-to"]["assoc"][lang]) == whitespace(newrela["from-to"]["assoc"][lang])
            )

def differentrelas(origrela, newrela, lang) -> bool:
    return not (origrela["type"] == newrela["type"] and
            origrela["from-to"]["maptype"] == newrela["from-to"]["maptype"] and
            origrela["from-to"]["mandatory"] == newrela["from-to"]["mandatory"] and
            origrela["to-from"]["maptype"] == newrela["to-from"]["maptype"] and
            origrela["to-from"]["mandatory"] == newrela["to-from"]["mandatory"] and
            equalassoc(origrela=origrela, newrela=newrela, lang=lang)
            )
"""abc
d
ef""".replace("\n"," ")

def differententilayouts(origentry, newentry) -> bool:
    # print(origenti["pos_x"], "  =  ", newentry["pos_x"],
    #       origenti["pos_y"], "  =  ", newentry["pos_y"],
    #       origenti["pos_x"], "  =  ", newentry["pos_x"],
    #       origenti["ui"]["width"], "  =  ", newentry["ui"]["width"],
    #       origenti["ui"]["height"], "  =  ", newentry["ui"]["height"],
    #       origenti["ui"]["color"], "  =  ", newentry["ui"]["color"])
    return not (origentry["pos_x"] == newentry["pos_x"] and
                origentry["pos_y"] == newentry["pos_y"] and
                origentry["pos_x"] == newentry["pos_x"] and
                origentry["ui"]["width"] == newentry["ui"]["width"] and
                origentry["ui"]["height"] == newentry["ui"]["height"] and
                origentry["ui"]["color"] == newentry["ui"]["color"]
                )


def mergerelations(original, newjson, lang):
    miromergelogger = logging.getLogger("miromerge")
    for relaid, rela in newjson.getelements("relations").items():
        newfromentiid = rela["from-to"]["enti"]
        newtoentiid = rela["to-from"]["enti"]
        origrelaid, origrela = original.getbysrcref(psrcname=SPODMIROSOURCE, psrcid=relaid)
        if origrelaid is None:
            # relation is new, add it to the original file with the miroid (for reference in diagram)
            original.jsmodel["relations"][relaid] = deepcopy(rela)
            miromergelogger.info(
                f"Relation: added \"{whitespace(newjson.getelemdescr(pjsid=relaid, plang=lang, ptype='relations'))}\"")
        else:
            fromentiid = anyentiid(origmodel=original, entiid=newfromentiid)
            toentiid = anyentiid(origmodel=original, entiid=newtoentiid)
            if differentrelas(origrela=origrela, newrela=rela, lang=lang) or \
                    anyentiid(origmodel=original, entiid=origrela["from-to"]["enti"]) != fromentiid or \
                    anyentiid(origmodel=original, entiid=origrela["to-from"]["enti"]) != toentiid:
                origrela["from-to"]["enti"] = fromentiid
                origrela["to-from"]["enti"] = toentiid
                miromergelogger.info("Relation: changed from \"" + \
                                     f"{whitespace(original.getelemdescr(pjsid=origrelaid, plang=lang, ptype='relations'))}\"  " + \
                                     f"  to  \"{whitespace(newjson.getelemdescr(pjsid=relaid, plang=lang, ptype='relations'))}\""
                                     )

                origrela["type"] = rela["type"]
                origrela["from-to"]["assoc"][lang] = rela["from-to"]["assoc"][lang]
                origrela["from-to"]["maptype"] = rela["from-to"]["maptype"]
                origrela["from-to"]["mandatory"] = rela["from-to"]["mandatory"]
                origrela["to-from"]["assoc"][lang] = rela["to-from"]["assoc"][lang]
                origrela["to-from"]["maptype"] = rela["to-from"]["maptype"]
                origrela["to-from"]["mandatory"] = rela["to-from"]["mandatory"]
    return


def replaceelementsproperties(original: JSModel):
    """
    in the merged original:
    replaces new id's by existing ones, if they exist
    replaces color of entities by ther category-color
    """
    for rela in original.getelements("relations").values():
        rela["from-to"]["enti"] = anyentiid(origmodel=original, entiid=rela["from-to"]["enti"])
        rela["to-from"]["enti"] = anyentiid(origmodel=original, entiid=rela["to-from"]["enti"])

    # replace originial entiid and color for diagramentry
    for diag in original.getelements("diagrams").values():
        for enti in diag["elements"]["entity"]:
            enti["element"] = anyentiid(origmodel=original, entiid=enti["element"])
            enti["ui"]["color"] = nvl(original.getentitycolor(enti["element"]), enti["ui"]["color"])
        relationdict = dict()  # cannot change keys of entries in loop
        for relaid, rela in diag["relationships"].items():
            relationdict[anyrelaid(origmodel=original, relaid=relaid)] = rela
        diag["relationships"] = relationdict

    return


def handlediagentities(original, newjson, origdiag, newdiag):
    miromergelogger = logging.getLogger("miromerge")
    for newdiagenti in newdiag["elements"]["entity"]:
        newentiid = newdiagenti["element"]
        newenti = newjson.getbyid(newentiid, ptype="entities")
        newentiname = newjson.getlangtext(newenti["name"], newjson.modellanguage())
        origentiid, origenti = original.getbysrcref(psrcname=SPODMIROSOURCE, psrcid=newentiid)
        if origentiid is None:
            # entity of this entry is new, add entity to diagram
            newdiagenti["ui"]["color"] = original.getentitycolor(newentiid)
            origdiag["elements"]["entity"].append(newdiagenti)
            miromergelogger.info(f"Entity: Added \"{newentiname}\" to \"{newdiag['name']}\"")
        else:
            # search original entry in list of entities for diagram
            continue
            # TODO
            newdiagenti["element"] = origentiid
            newdiagenti["ui"]["color"] = original.getentitycolor(origentiid)
            if differententilayouts(origentry=origdiagenti, newentry=newdiagenti):
                origdiagenti = deepcopy(newdiagenti)
            origdiagenti["element"] = origentiid
            origdiagenti["pos_x"] = newdiagenti["pos_x"]
            origdiagenti["pos_y"] = newdiagenti["pos_y"]
            origdiagenti["pos_x"] = newdiagenti["pos_x"]
            origdiagenti["ui"]["width"] = newdiagenti["ui"]["width"]
            origdiagenti["ui"]["height"] = newdiagenti["ui"]["height"]
            origdiagenti["ui"]["color"] = original.getentitycolor(origentiid)
            miromergelogger.info(
                f"Diagram: Changed layout for entity \"{newentiname}\" on diagram \"{newdiag['name']}\"")
    return


def handlediagrelations(original, newjson, origdiag, newdiag, lang=None):
    miromergelogger = logging.getLogger("miromerge")
    for newrelaid, newreladiag in newdiag["relationships"].items():
        if newrelaid in origdiag["relationships"]:
            # relation is on diagram in original diagram
            origreladiag = origdiag["relationships"][newrelaid]
            if not (origreladiag["startedge"] == newreladiag["startedge"] and
                    origreladiag["startposition"] == newreladiag["startposition"] and
                    origreladiag["start_connector"] == newreladiag["start_connector"] and
                    origreladiag["endedge"] == newreladiag["endedge"] and
                    origreladiag["endposition"] == newreladiag["endposition"] and
                    origreladiag["end_connector"] == newreladiag["end_connector"]
            ):
                miromergelogger.info(
                    f"Diagram: relation \"{whitespace(newjson.getelemdescr(pjsid=newrelaid, plang=lang, ptype='relations'))}\"" +
                    f" updated on \"{newdiag['name']}\"")
                origdiag["relationships"][newrelaid] = deepcopy(newreladiag)
        else:
            # relation not found on original diagram
            miromergelogger.info(
                f"Diagram: relation \"{whitespace(newjson.getelemdescr(pjsid=newrelaid, plang=lang, ptype='relations'))}\"" +
                f" added to \"{newdiag['name']}\"")
            origdiag["relationships"][newrelaid] = deepcopy(newreladiag)
    return


def mergediags(original: JSModel, newjson: JSModel):
    miromergelogger = logging.getLogger("miromerge")
    for newdiagid, newdiag in newjson.getelements("diagrams").items():
        # handle a new diagram
        origdiagid, origdiag = original.getbysrcref(psrcname=SPODMIROSOURCE, psrcid=newdiagid)
        if origdiagid is None:
            samenamediags = original.getbyfield(ptype="diagrams", pvalue=newdiag["name"])
            if len(samenamediags) > 0:
                origdiagid, origdiag = samenamediags[0]

        if origdiagid is None:
            # diagram is new, add it to the original file with the miroid (for reference in diagram)
            # first replace ID's and colors of original elements
            # replaceelementsproperties(original=original, newdiag=newdiag)
            original.jsmodel["diagrams"][newdiagid] = deepcopy(newdiag)
            miromergelogger.info(f"Diagram: added \"{newdiag['name']}\"")
            miromergelogger.info(f"\t {len(newdiag['elements']['entity'])} Entities")
            for diagenti in newdiag["elements"]["entity"]:
                enti = newjson.getbyid(pjsid=diagenti["element"], ptype="entities")
                miromergelogger.info(f"\t  {enti['name'][newjson.modellanguage()]}")
            miromergelogger.info(f"\t {len(newdiag['relationships'])} Relations")
            for diagrelaid in newdiag["relationships"].keys():
                rela = newjson.getbyid(pjsid=diagrelaid, ptype="relations")
                miromergelogger.info(f"\t  {newjson.getelemdescr(pjsid=diagrelaid, ptype='relations')}")
        else:
            # update  existing diagram
            if origdiag["width"] != newdiag["width"] or origdiag["height"] != newdiag["height"]:
                # diagram attributes changed
                origdiag["width"] = newdiag["width"]
                origdiag["height"] = newdiag["height"]
                origdiag["sourceref"][SPODMIROSOURCE] = newdiag["sourceref"][SPODMIROSOURCE]
                miromergelogger.info(f"Diagram: changed size for \"{newdiag['name']}\"")

            # handle all diagram entities
            handlediagentities(original=original, newjson=newjson,
                               origdiag=origdiag, newdiag=newdiag)

            # handle all relationships on the diagram
            handlediagrelations(original=original, newjson=newjson,
                                origdiag=origdiag, newdiag=newdiag)
    # for


def mergeintooriginaljson(original: JSModel, newjson: JSModel, verbose=False) -> JSModel:
    """ merges newjson into original jsong

        existing entities: update name if they are old entities
        new entities: create
        existing relationships update
        new relationships create
        redirect dummy entities back to the original
        DO NOT DELETE ANYTHING FROM ORIGINAL
        diagelements:
        Entity update position and size
        Relationship update start and end point connection to entity
        Diagram adjust size
        """
    # logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.ERROR)
    miromergelogger = logging.getLogger("miromerge")
    miromergelogger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    miromergelogger.addHandler(ch)

    lang = original.getdefaultlang()
    miromergelogger.info(f"{datetime.now()} - Merge miro-export into json")

    mergeentities(original=original, newjson=newjson, lang=lang)
    mergerelations(original=original, newjson=newjson, lang=lang)
    mergediags(original=original, newjson=newjson)
    replaceelementsproperties(original=original)

    return newjson
