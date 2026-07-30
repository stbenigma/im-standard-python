from SSOT_db.IM_JSON import jsondiagram,JSModel,jsondiagelem,jsondiagrela,\
                Linesegment,defaultlinesegements
from datetime import datetime

def diagenties(jsonmodel: JSModel,entities):
    retval = []
    entiwidth, entiheight = 120, 80
    posx, posy = 20, 100
    categories = jsonmodel.getelements("categories")
    linewidth = 5 * (entiwidth + 20) if len(entities) < 20 else 15 * (entiwidth + 20)
    for entiid, enti in entities.items():
        catgid = enti.get("category")
        enticolor = None if catgid is None else categories[catgid]["ui"]["color"]
        retval.append(jsondiagelem(element=entiid,
                                   index=0,
                                   pos_x=posx, pos_y=posy,
                                   width=entiwidth,
                                   height=entiheight,
                                   color=enticolor))
        posx += entiwidth + 20
        if posx > linewidth:
            posx = 20
            posy += entiheight + 20
    # for
    return retval, linewidth + 100, posy + entiheight + 100


def adddsdiagram(jsonmodel: JSModel, diagname,categoryId=None):
    """add a dummy diagram to the jsonmodel
        containing all entities in a grid and all relationships going from south to north
    """

    diag = jsondiagram(name=diagname, diagtype="Entity", uc='Testuser', dc=str(datetime.now()))
    diag["sourceref"] = {"DATSPOT": [diagname, str(datetime.today())]}

    diagentities = {key:val for key,val in jsonmodel.getelements("entities").items()
                    if categoryId is None or val["category"]==categoryId
                    }
    entis, diagwidth, diagheight = diagenties(jsonmodel=jsonmodel,
                                              entities=diagentities)
    diag["elements"] = {"attribute": [], "entity": entis}


    for relaid, rela in jsonmodel.getelements("relations").items():
        if not (rela["from-to"]["enti"] in list (diagentities.keys())
            and rela["to-from"]["enti"] in list (diagentities.keys())):
            continue #skip relationships whose entities are not on diagram
        # define start and endposition of relation to generate linesegs between them
        startentix, startentiy, startentiwidth, startentiheight = \
        [(e["pos_x"], e["pos_y"], e["ui"]["width"], e["ui"]["height"]) for e in entis
         if e["element"] == rela["from-to"]["enti"]
         ][0]
        endentix, endentiy, endentiwidth, endentiheight = \
        [(e["pos_x"], e["pos_y"], e["ui"]["width"], e["ui"]["height"]) for e in entis
         if e["element"] == rela["to-from"]["enti"]
         ][0]
        startx = startentix + startentiwidth / 2
        starty = startentiy + startentiheight  # start south of the entity
        endx = endentix + endentiwidth / 2
        endy = endentiy  # start north of the entity
        diag["relationships"][relaid] = jsondiagrela(start_connector=rela["from-to"]["maptype"],
                                                     startedge=Linesegment.SOUTH, startposition=50,
                                                     end_connector=rela["to-from"]["maptype"],
                                                     endedge=Linesegment.NORTH, endposition=50,
                                                     linesegments=defaultlinesegements(startx=startx, starty=starty,
                                                                                       startedge=Linesegment.SOUTH,
                                                                                       startmandatory=rela["from-to"][
                                                                                           "mandatory"],
                                                                                       endx=endx, endy=endy,
                                                                                       endedge=Linesegment.NORTH,
                                                                                       endmandatory=rela["to-from"][
                                                                                           "mandatory"]
                                                                                       )
                                                     )

    diag["width"] = diagwidth
    diag["height"] = diagheight
    jsonmodel.jsmodel["diagrams"][diagname] = diag
    return

