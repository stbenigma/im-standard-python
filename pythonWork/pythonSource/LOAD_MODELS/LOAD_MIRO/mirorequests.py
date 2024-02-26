import urllib
import json

import requests as req

from SSOT_infra import authentification


class MiroAccess:
    API_URL = 'https://api.miro.com/v2/'

    def __init__(self, credentialfile=None,token=None,boardid=None,boardname=None):
        self._username = None
        if credentialfile is not None:
            try:
                self._username,creds=authentification.getcredentials(credentialfile=credentialfile)
                self._token=self._gettoken(creds)
            except:
                raise Exception(f"no token found in file {credentialfile}")
        if token is not None: self._token = token
        #read boards to make sure we have access
        if boardid is not None:
            #read single board by id
            self._boards = [self._requestboard(boardid=boardid)]
        else:
            #read board list, matching the name
            self._boards=self._requestboards(query=boardname)
        return

    @property
    def username(self):
        return self._username

    def getboards(self):
        return self._boards

    def _gettoken(self, credential):
        try:
            if credential is None or credential.get('token') is None:
                raise Exception(f"no proper miro credentials found")
            else:
                return credential["token"]
        except Exception as exp:
            raise exp


    def _buildheader(self,postheader=False):
        header = {
            'accept': "application/json",
            'authorization': f"Bearer {self._token}",
        }
        if postheader:
            header["content-type"]= 'application/json'
        return header

    def _doget(self, request):
        # add http if missing
        if request.startswith(self.API_URL):
            locrequest = request
        else:
            locrequest = MiroAccess.API_URL + request
        response = req.get(locrequest, headers=self._buildheader())
        if response.status_code != 200:
            raise Exception(f"miro api access error {response.text}")
        try:
            retval = json.loads(response.content)
        except:
            retval = None
        return retval

    def _postheader(self):
        return self._buildheader(postheader=True)

    def _dopatch(self,request,data):
        # add http if missing
        if request.startswith(self.API_URL):
            locrequest= request
        else:
            locrequest = MiroAccess.API_URL + request

        response = req.patch(url=locrequest,json=data, headers=self._postheader())
        if response.status_code not in (200,201):
            raise Exception(f"miro api access error {response.text}"+
                            f"\ndata={data}")
        try:
            retval = json.loads(response.content)
        except:
            retval = None
        return retval

    def _dodelete(self,request):
        #locrequest = urllib.parse.quote(request)
        if request.startswith(self.API_URL):
            locrequest = request
        else:
            locrequest = MiroAccess.API_URL + request

        response = req.delete(url=locrequest, headers=self._postheader())
        if response.status_code not in (201, 200,204):
            raise Exception(f"miro api access error {response.text}")
        return

    def _dopost(self,request,data=None):
        # add http if missing
        #locrequest=urllib.parse.quote(request)
        if request.startswith(self.API_URL):
            locrequest = request
        else:
            locrequest = MiroAccess.API_URL + request
        if data is None:
            response = req.post(url=locrequest,headers=self._postheader())
        else:
            response = req.post(url=locrequest, json=data, headers=self._postheader())
        if response.status_code not in (201,200,204):
            raise Exception(f"miro api access error {response.text}"+
                            f"\ndata={data}")
        try:
            retval = json.loads(response.content)
        except:
            retval = None
        return retval

    def _dogetlist(self, request):
        """request a list with a possible limit per request
            calls request until complete list is read"""
        nextrequest = request
        retval = []
        while True:
            jsresponse = self._doget(nextrequest)
            retval += jsresponse["data"]
            nextoffset = jsresponse["offset"] + jsresponse["size"]
            if  nextoffset < jsresponse["total"]:
                nextrequest = request + "&offset="+str(nextoffset)
            else:
                break
        # while
        return retval

    def _requestboard(self,boardid):
        req=f'boards/{boardid}'
        board =self._doget(request=req)
        return board

    def _requestboards(self,query=None):
        req='boards'
        if query is not None:
            req += f"?query={urllib.parse.quote(query)}&sort=alphabetically"
        else:
            req += "?sort=alphabetically"
        boards =self._dogetlist(request=req)
        return boards

    def _requestitems(self, boardid, elemtype=None, itemlimit=20):
        """reads all items on the board with board id"""
        request = f"boards/{boardid}/items?limit={itemlimit}"
        if elemtype is not None:
            request += f"&type={elemtype}"
        return self._dolistrequest(request=request)

    def _dolistrequest(self, request):
        """request a list with a possible limit per request
            calls request until complete list is read"""
        nextrequest = request
        retval = []
        while True:
            jsresponse = self._doget(nextrequest)
            retval += jsresponse["data"]
            if jsresponse["type"] == "cursor-list" and \
                    ("next" in jsresponse["links"].keys()):
                nextrequest = request + "&cursor="+jsresponse["cursor"]
            else:
                break
        # while
        return retval

    def _updateframe(self, boardid,frameid, data):
        request = f"boards/{boardid}/frames/{frameid}"
        return self._dopatch(request=request,data =data)

    def _createframe(self, boardid,data):
        request = f"boards/{boardid}/frames"
        return self._dopost(request=request,data =data)

    def _deleteframe(self, boardid,frameid):
        request = f"boards/{urllib.parse.quote(boardid)}/frames/{frameid}"
        return self._dodelete(request=request)


    def _createshape(self, boardid,data):
        request = f"boards/{urllib.parse.quote(boardid)}/shapes"
        return self._dopost(request=request,data =data)

    def _deleteshape(self, boardid,shapeid):
        request = f"boards/{urllib.parse.quote(boardid)}/shapes/{shapeid}"
        return self._dodelete(request=request)


    def _createconnector(self, boardid,data):
        request = f"boards/{urllib.parse.quote(boardid)}/connectors"
        return self._dopost(request=request,data =data)

    def _changeconnector(self, boardid,connectorid,data):
        request = f"boards/{urllib.parse.quote(boardid)}/connectors/{connectorid}"
        return self._dopatch(request=request,data=data )

    def _requestframes(self, boardid, frameid=None,itemlimit=20):
        request = f"boards/{urllib.parse.quote(boardid)}/frames"
        if frameid is not None:
            request += f"/{frameid}"
        request += f"?limit={itemlimit}"
        return self._dolistrequest(request=request)

    def _requestconnectors(self, boardid, itemlimit=20):
        request = f"boards/{urllib.parse.quote(boardid)}/connectors?limit={itemlimit}"
        return self._dolistrequest(request=request)

    def _requestshapes(self, boardid, frameid=None, itemid=None,itemlimit=20):
        request = f"boards/{urllib.parse.quote(boardid)}/items/"
        if itemid is not None:
            request += f"/{itemid}"
        request+=f"?limit={itemlimit}&type=shape"
        if frameid is not None:
            request += f"&parent_item_id={frameid}"
        return self._dolistrequest(request=request)

    def _requestcards(self, boardid, frameid=None, itemlimit=20):
        request = f"boards/{urllib.parse.quote(boardid)}/items?limit={itemlimit}&type=card"
        if frameid is not None:
            request += f"&parent_item_id={frameid}"
        return self._dolistrequest(request=request)

    def _requestframeitems(self, boardid, frameid, itemlimit=20):
        request = f"boards/{urllib.parse.quote(boardid)}/items?parent_item_id={frameid}?limit={itemlimit}"
        return self._dolistrequest(request=request)

    def _deleteitem(self, boardid,itemid):
        request = f"boards/{urllib.parse.quote(boardid)}/items/{itemid}"
        return self._dodelete(request=request)

    def _updatecard(self, boardid,cardid, data):
        request = f"boards/{urllib.parse.quote(boardid)}/cards/{cardid}"
        return self._dopatch(request=request,data =data)

    def _postcard(self, boardid,data):
        request = f"boards/{urllib.parse.quote(boardid)}/cards"
        return self._dopost(request=request,data=data)


    def _requesttexts(self, boardid, frameid=None, itemlimit=20):
        request = f"boards/{urllib.parse.quote(boardid)}/items?limit={itemlimit}&type=text"
        if frameid is not None:
            request += f"&parent_item_id={frameid}"
        return self._dolistrequest(request=request)

    def _requeststickys(self, boardid, itemlimit=20):
        request = f"boards/{urllib.parse.quote(boardid)}/sticky_notes?limit={itemlimit}"
        return self._dolistrequest(request=request)

    def _poststicky(self, boardid,data):
        request = f"boards/{urllib.parse.quote(boardid)}/sticky_notes"
        return self._dopost(request=request,data=data)

    def _deletesticky(self, boardid,stickyid):
        request = f"boards/{urllib.parse.quote(boardid)}/sticky_notes/{stickyid}"
        return self._dodelete(request=request)

    def _requestitemtags(self, boardid, itemid):
        request = f"boards/{urllib.parse.quote(boardid)}/items/{itemid}/tags"
        return self._doget(request=request)

    def _getalltags(self, boardid):
        request = f"boards/{urllib.parse.quote(boardid)}/tags"
        return self._doget(request=request)["data"]

    def _createtag(self, boardid, data):
        request = f"boards/{urllib.parse.quote(boardid)}/tags"
        return self._dopost(request=request,data=data)

    def _updatetag(self, boardid,tagid, data):
        request = f"boards/{urllib.parse.quote(boardid)}/items/{tagid}"
        return self._dopatch(request=request,data =data)

    def _deletetag(self, boardid, tagid):
        request = f"boards/{urllib.parse.quote(boardid)}/tags/{tagid}"
        return self._dodelete(request=request)

    def _additemtag(self, boardid, itemid,tagid):
        request = f"boards/{urllib.parse.quote(boardid)}/items/{itemid}?tag_id={tagid}"
        return self._dopost(request=request)

