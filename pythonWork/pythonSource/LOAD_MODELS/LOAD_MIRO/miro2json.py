from LOAD_MODELS.LOAD_MIRO import *
from SSOT_db.IM_JSON import jsondiagram, JSModel, jsonproject, jsonlanguage, jsoncategory, UIElement, jsonimprint, \
    jsonarc, jsonrelation, jsonrelationend, jsondiagrela, jsondiagelem, defaultlinesegements, \
    multilangstring, jsonlineseg
from SSOT_db.IM_OBJECTS import Relation
from SSOT_infra import Parameter, colorhex, version, nvl

DUMMYENTITYMARKER = "dummyrecursive-"


def roundposition(pos: str):
    lpos = float(pos) if type(pos) == str else pos

    return round(lpos, 1)


def mirodiag2jsdiag(diag: MiroFrame, entis, relas):
    retval = jsondiagram(name=diag.name, diagtype="Entity", uc=diag.uc, dc=diag.dc,
                         sourceref={miromergemodel.SPODMIROSOURCE: [diag.id, str(datetime.today())]},
                         width=str(round(float(diag.width()), 1)), height=round(diag.height()),
                         elements={"attribute": [],
                                   "entity": diagentis(diag=diag, entis=entis)},
                         relationships=diagrelas(diagid=diag.id, relas=relas, entis=entis)
                         )
    return retval


def miroenti2jsenti(lang, enti: MiroEntity):
    return jsonentity(name=jslang.multilangstring(lang=lang, string=enti.name),
                      uc=enti.uc, dc=enti.dc, shortname=enti.name,
                      descr=jslang.multilangstring(lang=lang, string=enti.description),
                      tooltip=jslang.multilangstring(lang=lang, string=""),
                      category=None if enti.category is None else enti.category.id,
                      supertypeentity=enti.superentiid,
                      sourceref={miromergemodel.SPODMIROSOURCE: [enti.id, str(datetime.today())]}
                      )


def entibyid(entis, entiid):
    enti = [e for e in entis if e.id == entiid]
    if len(enti) == 0:
        return None
    else:
        return enti[0]


def diagrelas(diagid, relas, entis):
    retval = {r.id: jsondiagrela(start_connector="M" if r.toenti["many"] else "1",
                                 end_connector="M" if r.fromenti["many"] else "1",
                                 startedge=r.fromenti.get("position").get('edge'),
                                 startposition=r.fromenti.get("position").get('percentage'),
                                 endedge=r.toenti.get("position").get('edge'),
                                 endposition=r.toenti.get("position").get('percentage'),
                                 linesegments=linesegments(rela=r, entis=entis))
              for r in relas if r.relatype() != Relation.ISASUBTYPE and diagid == r.frame.id
              }
    return retval


def diagentis(diag, entis):
    retval = []
    for e in filter(lambda e: diag.id in e.getentityframeids(), entis):
        # replaced by filter if diag.id not in e.getentityframeids(): continue
        # correct center-position to upper left positions
        retval.append(jsondiagelem(element=e.id,
                                   pos_x=str(roundposition(e.x(diag))),
                                   pos_y=str(roundposition(e.y(diag))),
                                   index=0, color=colorhex(color=e.fillcolor, withhashtag=False),
                                   width=str(roundposition(e.width(diag))),
                                   height=str(roundposition(e.height(diag))))
                      )

    return retval


def linesegments(rela, entis):
    def linetype(mandatory):
        if mandatory:
            return "SOLID"
        else:
            return "DASHED"

    def directionoffset(x):
        if x <= 2 : return -minlength
        if x >= 99: return minlength
        return 0

    linesegs = []
    feid = rela.fromenti["entiid"]
    fe = entibyid(entis=entis, entiid=feid)
    few = fe.width(rela.frame)
    feh = fe.height(rela.frame)
    fex = fe.x(rela.frame)
    fey = fe.y(rela.frame)
    feedge = rela.fromenti["position"].get("edge")
    frex = rela.fromenti["position"].get("x")
    frey = rela.fromenti["position"].get("y")
    frm = rela.fromenti["mandatory"]

    teid = rela.toenti["entiid"]
    te = entibyid(entis=entis, entiid=teid)
    tew = te.width(rela.frame)
    teh = te.height(rela.frame)
    tex = te.x(rela.frame)
    tey = te.y(rela.frame)
    teedge = rela.toenti["position"].get("edge")
    trex = rela.toenti["position"].get("x")
    trey = rela.toenti["position"].get("y")
    trm = rela.toenti["mandatory"]

    startposx = roundposition(fex + nvl(frex, 0.0) * few / 100)
    startposy = roundposition(fey + nvl(frey, 0.0) * feh / 100)
    endposx = roundposition(tex + nvl(trex, 0.0) * tew / 100)
    endposy = roundposition(tey + nvl(trey, 0.0) * teh / 100)
    minlength = 60

    # start at start entity
    linesegs.append(jsonlineseg(x=startposx, y=startposy, linetype=linetype(frm)))
    # go straight N,S,W or E
    nextx, nexty = max(startposx + directionoffset(frex), 0), max(startposy + directionoffset(frey), 0)
    linesegs.append(jsonlineseg(x=nextx, y=nexty, linetype=linetype(frm)))

    if ((feedge == Linesegment.NORTH and endposy <= nexty) or \
        (feedge == Linesegment.SOUTH and endposy >= nexty)) and \
            ((teedge == Linesegment.WEST and endposx >= nextx) or \
             (teedge == Linesegment.EAST and endposx <= nextx)
            ):
        nextx, nexty = nextx, endposy
    elif ((feedge == Linesegment.WEST and endposx <= nextx) or \
          (feedge == Linesegment.EAST and endposx >= nextx)) and \
            ((teedge == Linesegment.SOUTH and endposy <= nexty) or \
             (teedge == Linesegment.NORTH and endposy >= nexty)):
        nextx, nexty = endposx, nexty
    # same direction ends
    elif feedge == teedge:
        if feedge in (Linesegment.NORTH, Linesegment.SOUTH):
            nextx, nexty = endposx, nexty
        else:
            nextx, nexty = nextx, endposy
            # enter intermediate point
        linesegs.append(jsonlineseg(x=nextx, y=nexty, linetype=linetype(frm)))
        nextx, nexty = max(endposx + directionoffset(trex), 0), max(endposy + directionoffset(trey), 0)
    #North<->South or East<->West
    elif (feedge == Linesegment.NORTH and teedge== Linesegment.SOUTH) or\
         (feedge == Linesegment.SOUTH and teedge== Linesegment.NORTH):
        nextx, nexty = nextx, max(endposy + directionoffset(trey), 0)
        # enter intermediate point
        linesegs.append(jsonlineseg(x=nextx, y=nexty, linetype=linetype(frm)))
        nextx, nexty = max(endposx + directionoffset(trex), 0), max(endposy + directionoffset(trey), 0)
    elif (feedge == Linesegment.EAST and teedge == Linesegment.WEST) or \
         (feedge == Linesegment.WEST and teedge == Linesegment.EAST):
        nextx, nexty = max(endposx + directionoffset(trex), 0), nexty
        # enter intermediate point
        linesegs.append(jsonlineseg(x=nextx, y=nexty, linetype=linetype(frm)))
        nextx, nexty = max(endposx + directionoffset(trex), 0), max(endposy + directionoffset(trey), 0)
    else:
        # go slanted from starting limb to to ending limb
        nextx, nexty = max(endposx + directionoffset(trex), 0), max(endposy + directionoffset(trey), 0)

    linesegs.append(jsonlineseg(x=nextx, y=nexty, linetype=linetype(trm)))

    # go straight N,S,E,W towards end-entity
    linesegs.append(jsonlineseg(x=endposx, y=endposy, linetype=linetype(trm)))

    # TODO replace creation by this code, edge is missing
    xedge, percentage = rela._position2edgeposition(xpercent=rela.fromenti["position"].get("x"),
                                                    ypercent=rela.fromenti["position"].get("y"))

    defaultlinesegements(startx=startposx, starty=startposy,
                         startedge=Linesegment.SOUTH,
                         startmandatory=rela.fromenti["mandatory"],
                         endx=endposx, endy=endposy,
                         endedge=Linesegment.NORTH,
                         endmandatory=rela.toenti["mandatory"])
    return linesegs


def miroarc2jsarc(arc: MiroArc):
    structarc = arc.structarc()
    return jsonarc(name=structarc["name"], entity=structarc["entity"], relations=structarc["relations+"],
                   uc="sys", dc=str(datetime.today()),
                   sourceref={miromergemodel.SPODMIROSOURCE: [structarc['id'], str(datetime.today())]})


def mirorela2jsrela(lang: str, rela: MiroRelation) -> dict:
    retval = jsonrelation(name=miromergemodel.SPODMIROSOURCE + rela.id, uc=rela.uc, dc=rela.dc,
                          relatype=rela.relatype(),
                          relafrom=jsonrelationend(enti=rela.fromenti["entiid"],
                                                   assoc=multilangstring(string=rela.fromenti["text"], lang=lang),
                                                   maptype=Relation.MANY if rela.fromenti["many"] else Relation.ONE,
                                                   hist=False, mandatory=rela.fromenti["mandatory"],
                                                   arc=rela.fromenti["arc"]),
                          relato=jsonrelationend(enti=rela.toenti["entiid"],
                                                 assoc=multilangstring(string=rela.toenti["text"], lang=lang),
                                                 maptype=Relation.MANY if rela.toenti["many"] else Relation.ONE,
                                                 hist=False, mandatory=rela.toenti["mandatory"],
                                                 arc=rela.toenti["arc"]),
                          sourceref={miromergemodel.SPODMIROSOURCE: [rela.id, str(datetime.today())]})
    return retval


def miroboard2json(board: MiroBoardModel, lang: str = "en") -> JSModel:
    jsmodel = JSModel(pmodel=JSModel.emptyjsonmodel(), pwithversioncheck=False)
    jsmodel.jsmodel["model"] = jsonproject(name=board.boardname, modeltype="logical"
                                           , language=lang, uc=board.boarduc, dc=board.boarddc)
    assert lang in Parameter.SUPPORTEDLANGUAGES, f"language {lang} not in {list(Parameter.SUPPORTEDLANGUAGES.keys())}"
    jsmodel.jsmodel["languages"] = {lang: jsonlanguage(isoname=Parameter.SUPPORTEDLANGUAGES[lang][0],
                                                       iso3=Parameter.SUPPORTEDLANGUAGES[lang][1],
                                                       modellanguage=True)}
    catgs = board.categories()
    jsmodel.jsmodel["categories"] = {cat.id: jsoncategory(name=cat.name,
                                                          uc=board.boarduc,
                                                          dc=board.boarddc,
                                                          ui=UIElement(color=colorhex(color=cat.fillcolor,
                                                                                      withhashtag=False)).js()
                                                          ) for cat in catgs
                                     }
    entis = board.entities()
    relas = board.relations()
    # handle recursive relationships moved to board
    removeentis = []
    for rela in relas:
        fromenti = board.getitembyid(rela.fromenti["entiid"])
        toenti = board.getitembyid(rela.toenti["entiid"])
        if fromenti.name.startswith(DUMMYENTITYMARKER):
            rela.fromenti["entiid"] = rela.toenti["entiid"]  # point to yourself
            removeentis.append(fromenti)
        elif toenti.name.startswith(DUMMYENTITYMARKER):
            rela.toenti["entiid"] = rela.fromenti["entiid"]  # point to yourself
            removeentis.append(toenti)
    for e in set(removeentis):
        entis.remove(e)

    jsmodel.jsmodel["entities"] = {enti.id: miroenti2jsenti(lang=lang, enti=enti) for enti in entis}
    jsmodel.jsmodel["relations"] = {rela.id: mirorela2jsrela(lang=lang, rela=rela) for rela in relas}

    arcs = board.arcs()
    jsmodel.jsmodel["arcs"] = {key: miroarc2jsarc(arc) for key, arc in arcs.items()}
    jsmodel.jsmodel["attributes"] = {}
    jsmodel.jsmodel["documents"] = {}
    jsmodel.jsmodel["domains"] = {}
    diags = board.diagrams()
    jsmodel.jsmodel["diagrams"] = {diag.id: mirodiag2jsdiag(diag=diag,
                                                            relas=relas, entis=entis)
                                   for diag in diags}
    jsmodel.jsmodel["_imprint_"] = jsonimprint(dbname="",
                                               created="2023-04-03 10:36:28.392947",
                                               modelversion=version().get("DBVERSION"),
                                               jsonversion=version().get("JSONVERSION"),
                                               hashvalue=None,
                                               gitrevision="48e71ce")

    return jsmodel
