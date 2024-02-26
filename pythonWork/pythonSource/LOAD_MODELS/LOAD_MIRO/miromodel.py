import argparse
import sys
import os
import pathlib
import logging

from LOAD_MODELS.LOAD_INFRA import mergedbs
from LOAD_MODELS.LOAD_MIRO import MiroBoardModel, MiroInterface, MiroRelation, miroboard2json, DUMMYENTITYMARKER, \
    mergeintooriginaljson, miromergemodel
from SSOT_db.IM_JSON import *
from SSOT_infra import nvl, argparseparent


def listboards(credentialfile, boardname=None):
    miro = MiroInterface(credentialfile=credentialfile, boardname=boardname)
    loclistboards(miro)
    return


def loclistboards(miro: MiroInterface):
    visibleboards = miro.getboards()
    print("")
    for board in visibleboards:
        print(f"{board['name']}; owner={board['owner']['name']}; id={board['id']} ")
    print(f"{str(len(visibleboards))} board(s) listed for current {miro.username}")
    return


def listframes(credentialfile, boardid=None, boardname=None):
    assert boardid is not None or  boardname not in (None,""),"Boardname or Boardid must be given"

    miro = MiroInterface(credentialfile=credentialfile, boardid=boardid, boardname=boardname)
    print(f"{len(miro.getboards())} board(s) found for \"{nvl(boardname, boardid)}\"")
    loclistframes(miro=miro)
    return

def listboards(credentialfile, boardid=None, boardname=None):
    miro = MiroInterface(credentialfile=credentialfile, boardname=boardname)
    print(f"{len(miro.getboards())} board(s) found for \"{nvl(boardname)}\"")
    print ("Name".ljust(25)
           +"\t"+"owner".ljust(20)
           +"\t"+"frames".rjust(7)
           +"\t"+"id".ljust(15)
           )
    boards=miro.getboards()
    boards.sort(key=lambda b:b["name"])
    for board in boards:
        print (board['name'].ljust(25)
                     +"\t"+board["owner"].get("name").ljust(20)
                     +"\t"+str(len(miro.getframes(boardid=board["id"]))).rjust(7)
                     +"\t"+board["id"].ljust(15))
                #+"\t" + board["team"].get("name").ljust(20)
    return


def loclistframes(miro:MiroInterface):
    def locprint1frame(miro:MiroInterface, board):
        print(f"Frames for Miro-board \"{board['name']}\" (id={board['id']})")
        frames = miro.getframes(boardid=board["id"])
        print("\t"+"Name".ljust(25)+"\tPosition (x,y)")
        print("\t" + '\n\t'.join([fr['data']['title'].ljust(25)+"\t"+f"{round(fr['position']['x'])}, {round(fr['position']['y'])}" for fr in frames]))
        print(f" ========= {len(frames)} =========")
        return
    for board in miro.getboards():
        locprint1frame(miro=miro, board=board)
    return


def diagram2miro(credentialfile, jsonfile, diagramname,
                 destjsonfile=None, boardid=None,
                 boardname=None, diagx=0, diagy=0,
                 lang=None):
    jsmodel = JSModel.readfromfile(pfilename=jsonfile, pwithcheck=True)
    jsondiagnames = [d["name"] for d in jsmodel.getelements("diagrams").values()]
    if diagramname not in jsondiagnames:
        raise Exception(f"Diagram \"{diagramname}\" not found in modelfile \"{jsonfile}\"")

    miro = MiroInterface(credentialfile=credentialfile, boardid=boardid, boardname=boardname)
    if len(miro.getboards()) == 0:
        raise Exception(f"Miro-Board \"{boardname if boardid is None else boardid}\" not found")
    elif len(miro.getboards()) > 1:
        raise Exception(f"Miro-Boardname {boardname} is not unique. Try with id (see function listboards")

    miroboard = MiroBoardModel(mirointerface=miro, board=miro.getboards()[0], withload=False)
    frames = json2miro(board=miroboard, jsmodel=jsmodel,
                       diagnames=[diagramname], diagx=diagx, diagy=diagy,
                       lang=lang)
    if destjsonfile is not None:
        jsmodel.write_json(destjsonfile)
    return


def miroframe2json(credentialfile: str, jsonfile: str, framename: str, lang: str = "en",
                   checkjsonfile: bool = True, boardid: str = None, boardname: str = None) -> JSModel:
    mirointerface = MiroInterface(credentialfile=credentialfile,
                                  boardname=boardname, boardid=boardid)
    miroboard = mirointerface.getboard(name=boardname)

    assert miroboard is not None, f"\"{boardname}\" not found"
    boardmodel = MiroBoardModel(mirointerface=mirointerface,
                                board=miroboard,
                                framenames=[framename],
                                reportback2miro=False)
    jsmodel = miroboard2json(board=boardmodel, lang=lang)
    jsmodel.write_json(jsonfile)
    if checkjsonfile:
        checkedmodel = mergedbs.jsonviadbtojson(pmodel=jsmodel, psrcname=miromergemodel.SPODMIROSOURCE,
                                                pcheckonly=True, pverbose=True)

        #checkedmodel=JSModel(pmodel=checkedmodel)
        #checkedmodel.write_json(Path(jsonfile).with_stem(Path(jsonfile).stem+"_checked"))
    print(f"jsonfile loaded from miro written to {jsonfile}")

    return jsmodel


def mergemiro2spod(mirojsmodel: JSModel, mergetojsonfile:str, dbfile:str=None, verbose=False):
    mergejsmodel= JSModel.readfromfile(mergetojsonfile)
    mergejsmodel=mergeintooriginaljson(original=mergejsmodel, newjson=mirojsmodel, verbose=verbose)
    mergejsmodel.write_json(mergetojsonfile)
    print(f"Miro-loaded file diagram \"{mirojsmodel.modelname()}\" merged into spod:\"{mergetojsonfile}\"")

    if dbfile is not None:
        # merge loaded json in to sqlite db
        newcompletemodel = mergedbs.mergejs2db(pdbfile=dbfile, pmodel=mergejsmodel,
                                               psrcname=miromergemodel.SPODMIROSOURCE, pverbose=verbose)
        print(f"merged new jsonfile into to database \"{dbfile}\"")

        newjsonfile = Path(dbfile).with_suffix('.json')
        if newjsonfile == mergetojsonfile:
            #don't loose loaded jsonfile, add _loaded to the sourcefile
            os.rename(mergetojsonfile,Path(mergetojsonfile).with_stem(Path(mergetojonfile).stem+"_loaded"))
        newcompletemodel.write_json(newjsonfile)
        print(f"created jsonfile for new db-version in  {newjsonfile}")
    return


def arcstext(arcid, enti):
    if arcid is None:
        retval = None
    else:
        arcsymbol = '/'
        retval = ''.rjust(arcno(enti=enti, arcid=arcid), arcsymbol)
    return retval


def json2miro(board: MiroBoardModel, jsmodel: JSModel,
              diagnames=["*"], diagx=None, diagy=None, lang=None):
    def nonemptyassoc(assoc):
        if nvl(assoc) == "":
            return "is"
        else:
            return assoc

    retval = []
    curlang = lang if lang is not None else jsmodel.modellanguage()
    x, y = 0, 0
    # NOCARDS
    # cardw, cardh = 256, 128
    # miroboardcards = board.getallcards()
    autox = nvl(diagx, 0)
    autoy = nvl(diagy, 0)

    for diagid, diag in jsmodel.getelements("diagrams").items():
        if not (len(diagnames) > 0 and (diagnames[0] == "*" or diag["name"] in diagnames)): continue
        renamedframes = board.renameframes([diag["name"]])
        if diag["name"] in renamedframes:
            x = renamedframes[diag["name"]]["x"]
            y = renamedframes[diag["name"]]["y"] + diag["height"] + 30
        else:
            x, y = autox, autoy
        miroframe = board.creatediagram(title=diag["name"],
                                        x=x, y=y,
                                        width=diag["width"], height=diag["height"])
        autox += diag["width"]
        retval.append(miroframe)
        # mark frame in mirojsmodel
        diag["sourceref"][miromergemodel.SPODMIROSOURCE] = [miroframe["id"], str(datetime.now())]
        # NOCARDS
        # cardx, cardy = -diag["width"] /2, -diag["height"]/2 - 100

        newentities = dict()
        """ Entities without size and position are standardsize positioned at bottom of diagram
            in a grid
        """

        for jsdiagenti in diag["elements"]["entity"]:
            jsentity = jsmodel.getbyid(jsdiagenti["element"])
            entiname = jsentity["name"][curlang]
            miroenti = board.createentity(frameid=miroframe["id"],
                                          name=entiname,
                                          x=jsdiagenti["pos_x"], y=jsdiagenti["pos_y"],
                                          width=jsdiagenti["ui"]["width"],
                                          height=jsdiagenti["ui"]["height"],
                                          color="#" + jsdiagenti["ui"]["color"],
                                          textalignh="center",
                                          textalignv="middle" if len(jsentity["subtypes+"]) == 0 else "top")
            jsentity["sourceref"][miromergemodel.SPODMIROSOURCE] = [miroenti["id"], str(datetime.now())]

            # NOCARDS
            # if entiname in [c.name for c in board.cards()]:
            #     card = board.getitembyname(name=entiname, itemtype="card")
            #     card.description = jsentity["descr"][curlang]
            #     board.updatecard(card=card)
            # else:
            #     board.createcard(card={
            #         "data": {
            #             "description": jsentity["descr"][curlang],
            #             "title": entiname
            #         },
            #         "position": {
            #             "x": cardx,
            #             "y": cardy
            #         },
            #         "geometry": {
            #             "height": cardh,
            #             "width": cardw
            #         }
            #     })
            #     # place them in an arry 5xn above the first frame
            #     if cardx > (5 * cardw):
            #         cardx = -200
            #         cardy = cardy - cardh - 5
            #     else:
            #         cardx += (cardw + 5)

            newentities[jsdiagenti["element"]] = miroenti
        # for attrs

        for relaid, jsdiagrela in diag["relationships"].items():
            """ relationships without linesegments go always from east to west
            """

            jsrela = jsmodel.getbyid(relaid)
            jsstartenti = jsmodel.getbyid(jsrela["from-to"]["enti"])
            startenti = newentities[jsrela["from-to"]["enti"]]
            jsendenti = jsmodel.getbyid(jsrela["to-from"]["enti"])
            endenti = newentities[jsrela["to-from"]["enti"]]
            if startenti["id"] == endenti["id"]:
                # to link dummy entity to the real entity
                startentiname = jsstartenti['name'][curlang]
                dummy = board.createentity(frameid=miroframe["id"],
                                           name=f"{DUMMYENTITYMARKER}{startentiname}",
                                           x=startenti["position"]["x"],
                                           y=startenti["position"]["y"],
                                           width=100, height=40,
                                           color=None, textalignh="center", textalignv="middle")
                # selfconnect is not allowed, try dummy shape and change afterwards
                dummyid = dummy["id"]
            else:
                dummyid = endenti["id"]
            mirorela = board.createrelation(startitem={"x": MiroRelation.relaxposition(edge=jsdiagrela["startedge"],
                                                                                       percentage=jsdiagrela[
                                                                                           "startposition"]),
                                                       "y": MiroRelation.relayposition(edge=jsdiagrela["startedge"],
                                                                                       percentage=jsdiagrela[
                                                                                           "startposition"]),
                                                       "text": nonemptyassoc(jsrela["from-to"]["assoc"][curlang]),
                                                       "arcs": arcstext(arcid=jsrela["from-to"]["arc"],
                                                                        enti=jsstartenti),
                                                       "type": MiroRelation.relaerdtype(
                                                           many=jsrela["to-from"]["maptype"] == "M",
                                                           mandatory=jsrela["to-from"]["mandatory"],
                                                           oppositemand=jsrela["from-to"]["mandatory"]),
                                                       "id": startenti["id"]
                                                       },
                                            enditem={"x": MiroRelation.relaxposition(edge=jsdiagrela["endedge"],
                                                                                     percentage=jsdiagrela[
                                                                                         "endposition"]),
                                                     "y": MiroRelation.relayposition(edge=jsdiagrela["endedge"],
                                                                                     percentage=jsdiagrela[
                                                                                         "endposition"]),
                                                     "text": nonemptyassoc(jsrela["to-from"]["assoc"][curlang]),
                                                     "arcs": arcstext(arcid=jsrela["to-from"]["arc"],
                                                                      enti=jsendenti),
                                                     "type": MiroRelation.relaerdtype(
                                                         many=jsrela["from-to"]["maptype"] == "M",
                                                         mandatory=jsrela["from-to"]["mandatory"],
                                                         oppositemand=jsrela["to-from"]["mandatory"]),
                                                     "id": dummyid
                                                     },
                                            linetype=MiroRelation.relalinetype(
                                                jsrela["from-to"]["mandatory"] or jsrela["to-from"]["mandatory"])
                                            )
            jsrela["sourceref"][miromergemodel.SPODMIROSOURCE] = [mirorela["id"], str(datetime.now())]

            if startenti["id"] == endenti["id"]:
                # recursive connector, change end-item-id and delete dummy entitiy
                # TODO Miro akzeptiert change mit identischen ID nicht mehr, lass dummy stehen
                pass
                # board.changerelation(relaid=mirorela["id"],data={"endItem": {"id": endentiid}})
                # board.deleteentity(entiid=dummyid)
        # for relas

        x += diag["width"] + 50

    # for diags

    return retval


def main(sysargs):
    """
    :param sysargs:
    :return:
    """
    parser = argparse.ArgumentParser(description='miro interface')
    parser.add_argument('jsonfile', nargs='?',
                        help=f"Path of the jsonfile to be used. Default ./{Parameter.SPODDBDIREC}" +
                             f"/<modelname>{Parameter.JSONEXTENSION})")
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('--frommiro', '-fm', action='store_true', help='reads diagram from miro into jsonfile')
    parser.add_argument('--checkjson', '-cj', action='store_true', required=False,
                        help=f"check generated json for consistency.")

    group1.add_argument('--tomiro', '-tm', action='store_true', help='write diagram from jsonfile to miro')
    parser.add_argument('--xpos', '-x', default=0,
                        help=f"x-position of diagram on miroboard. Default: 0")
    parser.add_argument('--ypos', '-y', default=0,
                        help=f"y-position of diagram on miroboard. Default: 0")

    group1.add_argument('--listframes', '-lf', action='store_true', help='list of frames on miroboard')
    group1.add_argument('--listboards', '-lb', action='store_true', help='list of visible miroboards, boardname is used with regexp')
    group1.add_argument('--mergejson', '-mj', action='store_true',
                        help=f"merge jsonfile (loaded from miro) into destinationfile (spod-jsonfile).")
    parser.add_argument('--dbfile', '-df', required=False,
                        help=f"spod db-file. if present merged jsonfile is merged into spod database and new jsonfile is generated")
    parser.add_argument('--destination', '-d', dest="destination",
                        help=f"Filepath to write the downloaded or merged json file to.")

    parser.add_argument('--credentials', '-c',
                        help=f"Filepath of miro-credentialfile (type yaml")
    parser.add_argument('--diagram', '-diag',
                        help=f"diagram names to be up/downloaded.")
    parser.add_argument('--boardid', '-id',
                        help=f"ID of miroboard. Default: None")
    parser.add_argument('--boardname', '-name',
                        help=f"Name of miroboard. Default: None")
    parser.add_argument('--language', '-l', default="en",
                        help=f"language on miro board. Default: Modellanguage from jsonfile")

    parser.add_argument('--logfile', '-log', dest='logfile',
                        help=f"Path for logfile. Default: ./<modelname>{Parameter.LOGFILEEXTENSION}")
    parser.add_argument('--version', '-v', action='store_true')
    argparse.Namespace()

    if (len(sysargs) > 0) and ('.py' in sysargs[0]) and ('ipykernel' not in sysargs[0]):
        arguments: argparse.Namespace = parser.parse_args(sysargs[1:])
        myargs = arguments.__dict__
    else:
        # in jupyter environment
        """set myargs with arguments """
    # fi

    if myargs["version"]:
        argparseparent.showversion()
        exit(0)

    assert myargs["boardid"] is None or myargs["boardname"] is None, "either boardid or boardname must be given"
    #logfilepath = nvl(myargs["logfile"],
    #                  logmessages.defaultlogfilepath(name=nvl(myargs["boardname"], myargs["boardid"]),
    #                                                 suffix=Parameter.LOGFILEEXTENSION))

    if myargs["frommiro"]:
        assert myargs["destination"] is not None, "downloading mirodiagram requires destination file"
        mirojson = miroframe2json(credentialfile=myargs["credentials"],
                                  jsonfile=myargs["destination"],
                                  framename=myargs["diagram"],
                                  checkjsonfile=myargs["checkjson"],
                                  boardid=myargs["boardid"],
                                  boardname=myargs["boardname"],
                                  lang=myargs["language"]
                                  )
    elif myargs["mergejson"]:
        assert myargs["destination"] is not None and myargs["jsonfile"] is not None, "merging requires jsonfile and destination "
        mirojson = JSModel.readfromfile(myargs["jsonfile"])
        mergemiro2spod(mirojsmodel=mirojson, mergetojsonfile=myargs["destination"],
                       verbose=True,dbfile=myargs["dbfile"])

    elif myargs["tomiro"]:
        diagram2miro(credentialfile=myargs["credentials"],
                     jsonfile=myargs["jsonfile"],
                     diagramname=myargs["diagram"],
                     destjsonfile=myargs["destination"],
                     boardid=myargs["boardid"],
                     boardname=myargs["boardname"],
                     diagx=nvl(myargs["xpos"], 0),
                     diagy=nvl(myargs["ypos"], 0),
                     lang=myargs["language"]
                     )
    elif myargs["listframes"]:
        assert (myargs["boardname"] is not None or myargs["boardid"] is not None),f"for listframes boardname or boardid must be given"
        listframes(credentialfile=myargs["credentials"],
                   boardid=myargs["boardid"],
                   boardname=myargs["boardname"])
    elif myargs["listboards"]:
        listboards(credentialfile=myargs["credentials"],
                   boardname=myargs["boardname"])
    else:
        parser.print_usage()
        assert False, "command frommiro | tomiro | listframes missing"

    #print(f"logging written to \"{logfilepath}\"")
    return


if __name__ == "__main__":
    main(sys.argv)
