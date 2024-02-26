from SSOT_infra import nvl,text2crtext
from LOAD_MODELS.LOAD_MIRO import MiroAccess


class MiroInterface(MiroAccess):
    def __init__(self, credentialfile=None, token=None,boardid=None,boardname=None):
        super().__init__(credentialfile=credentialfile,token=token,boardid=boardid,boardname=boardname)
        return

    def getboard(self, id=None, name=None):
        #returns board from already read boardlist
        for board in self.getboards():
            if board["id"] == id or board["name"] == name:
                return board
        return None

    def getboardcontent(self, boardid, elemtype=None):
        board = super()._requestitems(boardid=boardid, elemtype=elemtype)
        return board

    def deleteitem(self, boardid, itemid):
        self._deleteitem(boardid=boardid, itemid=itemid)

    def getframes(self, boardid):
        frames = super()._requestframes(boardid=boardid)
        return frames

    def getframe(self, boardid, frameid=None, framename=None):
        if frameid is not None:
            return super()._requestframes(boardid=boardid, frameid=frameid)
        elif framename is not None:
            frames = super()._requestframes(boardid=boardid)
            for frame in frames:
                if frame["data"]["title"] == framename:
                    return frame
        return None

    def deleteframe(self, boardid, frameid, withcontent=False):
        if withcontent:
            #requestframeitems  # TODO
            for item in self._requestitems(boardid=boardid):
                if "parent" in item and item["parent"]["id"] == frameid:
                    self.deleteitem(boardid=boardid, itemid=item["id"])
        self._deleteframe(boardid=boardid, frameid=frameid)

    def updateframe(self, boardid, frameid, title, x=None, y=None, color=None, width=None, height=None):
        data = {
            "data": {
                "format": "custom",
                "title": title,
                "type": "freeform"
            }}
        if x is not None and y is not None:
            data["position"] = {
                "origin": "center",
                "x": x,
                "y": y
            }
            if color is not None:
                data["style"] = {"fillColor": color}
            if width is not None or height is not None:
                data["geometry"] = {
            "height": height,
            "width": width
        }

        self._updateframe(boardid=boardid, frameid=frameid, data=data)

        return

    def createframe(self, boardid, title, x, y, color=None, width=None, height=None):
        data = {
            "data": {
                "format": "custom",
                "title": title,
                "type": "freeform"
            },
            "position": {
                "origin": "center",
                "x": x,
                "y": y
            }}
        if color is not None:
            data["style"] = {"fillColor": color}
        if width is not None or height is not None:
            data["geometry"] = {
                "height": height,
                "width": width
            }

        return self._createframe(boardid=boardid, data=data)


    def createentity(self, boardid, frameid, name, color, x, y, width, height,
                     textalignh, textalignv,fillopacity=1.0):
        data = {
            "data": {
                "shape": "round_rectangle",
                "content": name
            },
            "style": {
                "fillColor": color,
                "fillOpacity": fillopacity,
                "textAlign": textalignh,
                "textAlignVertical": textalignv
            },
            "position": {
                "origin": "center",
                "x": x + width / 2,  # we get top left coordinates
                "y": y + height / 2  # but miro uses center
            },
            "geometry": {
                "height": height,
                "width": width
            },
            "parent": {"id": frameid}
        }

        return self._createshape(boardid=boardid, data=data)


    def createrelation(self, boardid, startitem, enditem, linetype="normal"):

        def captions(startitem,enditem):
            BORDERDISTANCE = 5  # % of line from entity
            NEXTTEXT = 2  # add 5% after arc-labels

            """ builds 2 - 4 captions depending on presence of arc-nop's """
            retval = []

            #Position ist schwierig, da % der Länge der Connection die Mitte der Caption
            #festlegt 1 Zeichen ca 5%  10 Zeichen = 20%  20 Zeichen 30%
            startdistance = BORDERDISTANCE
            if startitem.get("arcs") is not None:
                retval.append(
                    {"content": startitem["arcs"],
                     "position": f"{str(startdistance)}%",
                     "textAlignVertical": "middle"
                     })
                startdistance += NEXTTEXT
            capttext = text2crtext(text=nvl(startitem["text"],''),
                                   maxlines=4,maxwidth=15)
            retval.append({
                "content": capttext,
                "position": f"{str(startdistance + 10*(len(capttext)//10))}%",
                "textAlignVertical": "middle"
            })
            startdistance = BORDERDISTANCE
            if enditem.get("arcs") is not None:
                retval.append(
                    {"content": enditem["arcs"],
                     "position": f"{str(100 - startdistance)}%",
                     "textAlignVertical": "middle"
                     })
                startdistance += NEXTTEXT
            capttext = text2crtext(text=nvl(enditem["text"],''),
                                   maxlines=4,maxwidth=15)
            retval.append({
                "content": capttext,
                "position": f"{str(100 - (startdistance + 10*(len(capttext)//10)))}%",
                "textAlignVertical": "middle"
            })
            return retval


        data = {
            "startItem": {
                "position": {
                    "x": str(startitem["x"]) + "%",
                    "y": str(startitem["y"]) + "%"
                },
                "id": startitem["id"]
            },
            "endItem": {
                "position": {
                    "x": str(enditem["x"]) + "%",
                    "y": str(enditem["y"]) + "%"
                },
                "id": enditem["id"]
            },
            "captions": captions(startitem=startitem,enditem=enditem),
            "style": {
                "startStrokeCap": startitem["type"],
                "strokeStyle": linetype,
                "endStrokeCap": enditem["type"],
                "textOrientation": "horizontal"
            }, "shape": "elbowed"
        }

        return self._createconnector(boardid=boardid, data=data)


    def getshapes(self, boardid, frameid=None):
        shapes = super()._requestshapes(boardid=boardid, frameid=frameid)
        return shapes


    def getshape(self, boardid, itemid):
        shape = super()._requestshapes(boardid=boardid, itemid=itemid)
        return shape


    def getconnectors(self, boardid):
        connectors = super()._requestconnectors(boardid=boardid)
        return connectors


    def getcards(self, boardid, frameid=None):
        cards = super()._requestcards(boardid=boardid, frameid=frameid)
        return cards


    def createcard(self, boardid, card):
        super()._postcard(boardid, card)
        return


    def updatecard(self, boardid, cardid, text=None, tags=[]):
        super()._updatecard(boardid=boardid, cardid=cardid,
                            data={
                                "data": {
                                    "description": text,
                                }
                            })
        for tag in tags:
            super()._additemtag(boardid=boardid, itemid=cardid, tagid=tag.id)

        return


    def gettags(self, boardid, itemid):
        tags = super()._requestitemtags(boardid=boardid, itemid=itemid)
        if len(tags) > 0:
            return tags["tags"]
        else:
            return []


    def settag(self, boardid, itemid, tagid):
        tags = super()._additemtag(boardid=boardid, itemid=itemid, tagid=tagid)
        return tags


    def createtag(self, boardid, tag):
        super()._createtag(boardid, tag)
        return


    def updatetag(self, boardid, tagid, name=None, color=None):
        super()._updatetag(boardid=boardid, tagid=tagid,
                           data={
                               "title": name,
                               "fillColor": color
                           })
        return


    def getstickys(self, boardid):
        stickys = super()._requeststickys(boardid=boardid)
        return stickys


    def putsticky(self, boardid, data):
        # print("====\n", json.dumps(data))
        super()._poststicky(boardid=boardid, data=data)
        return


    def deletesticky(self, boardid, stickyid):
        self._deletesticky(boardid=boardid, stickyid=stickyid)
