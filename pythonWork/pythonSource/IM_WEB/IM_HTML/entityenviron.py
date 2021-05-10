from IM_JSON import JSModel

"""defines the classes and functions to implement an entity-environment representation"""
nvl = lambda str,default='': str if str is not None else default

class EntityCell():
    CENTER = 'center'
    ROLE = 'role'
    SUPER = 'super'
    PARENT = 'parent'
    CHILD = 'child'

    def __init__(self,ptype=None,pentiid=None,pentiname=None,passoc=None):
        self.setentiid(pentiid)
        self.setentiname(pentiname)
        self.setassoc(passoc)
        self.settype(nvl(ptype))

    def getentiid(self):
        return self._entiid

    def setentiid(self,pentiid):
        self._entiid = pentiid

    def gettype(self):
        return self._type

    def settype(self,ptype):
        self._type = ptype

    def getentiname(self):
        return self._entiname

    def setentiname(self,pentiname):
        self._entiname = pentiname

    def getassoc(self):
        return self._assoc
    def setassoc(self,passoc):
        self._assoc = passoc

    def isemptycell(self):
        return self.gettype() == ''

    def __str__(self):
        return ', '.join ((self.gettype(), nvl(self.getentiid()), nvl(self.getentiname()), nvl(self.getassoc())))


class EntityEnvironment():
    """Dictrionary for one entity.
        two-dimensional extensible grid 1. index (vidx)  top down , 2. index (hidx) -> left to right
        0/0 is the center
        1,2,3 are cells to downwards or to the right
        -1,-2,-3 are cells upwards or to the left
        {  ...
          ,-1 : {}   vidx
          ,0 : {'left'
                'center':[entiid,entiname,relationtext]
                right :
                }
          ,1 : {}
          ,...}
    """
    def __init__(self,pentiid,pentiname):
        self._grid = dict()
        self.fillcell (pvidx=0,phidx='center',pcell=EntityCell(ptype=EntityCell.CENTER,pentiid=pentiid,pentiname=pentiname))
        return

    def fillcell(self,pvidx,phidx,pcell:EntityCell):
        if pvidx not in self._grid.keys():
            self._grid[pvidx] = {}
        self._grid[pvidx][phidx] = pcell

    def getcell (self,pvidx,phidx):
        if pvidx not in self._grid.keys():
            return EntityCell() #non existing cell is empty
        if phidx not in  self._grid[pvidx].keys():
            return EntityCell()
        return self._grid[pvidx][phidx]

    def getminvkey(self):
        return min(self._grid.keys())
    def getmaxvkey(self):
        return max(self._grid.keys())

    def getentiid(self, pvidx, phidx):
        cell = self.getcell(pvidx=pvidx, phidx=phidx)
        if len(cell) == 0:
            return None
        else:
            return cell.getentiid()

    def getentiname(self, pvidx, phidx):
        cell = self.getcell(pvidx=pvidx, phidx=phidx)
        if len(cell) == 0:
            return None
        else:
            return cell.getentiname()

    def getassoc(self, pvidx, phidx):
        cell = self.getcell(pvidx=pvidx, phidx=phidx)
        if len(cell) == 0:
            return None
        else:
            return cell.getassoc()

    def togrid(self, pcells: list, ptype):
        #doubleline = len(pcells) > 2
        if ptype == EntityCell.ROLE:
            vidx, hidx = 0, 'right'
        elif ptype == EntityCell.SUPER:
            vidx, hidx = 0, 'left'
        elif ptype == EntityCell.PARENT:
            vidx, hidx = -1, 'center'
        elif ptype == EntityCell.CHILD:
            vidx, hidx = 1, 'center'
        elif ptype == EntityCell.CENTER:
            vidx, hidx = 0, 'center'
        else:
            assert false, "illegal type '{}'".format(ptype)

        for cell in pcells:
            self.fillcell(pvidx=vidx, phidx=hidx,pcell=cell)
            #vidx = switchvidx(vidx, doubleline) moved to display procedure
            vidx += 1 if ptype in (EntityCell.SUPER, EntityCell.CHILD) else -1
        # for
        return

def related(pentiid,prelated,pjson,pcardinality,pmodellang):
    retval = []
    entities:dict = pjson.getelements(pelemtype=Modelelemtype.ENTI)
    for relaid in prelated:
        rela = pjson.getelements(pelemtype=Modelelemtype.RELA)[relaid]
        if rela['type'] in (Relation.ISAROLE, Relation.ISASUBTYPE): continue
        if (rela['from-to']['enti'] == pentiid and rela['to-from']['enti'] != pentiid
            and rela['to-from']['maptype'] == pcardinality):
            parentid=rela['to-from']['enti']
            assoc = rela['from-to']['assoc'][pmodellang]
        elif (rela['to-from']['enti'] == pentiid and rela['from-to']['enti'] != pentiid
            and rela['from-to']['maptype'] == pcardinality):
            parentid = rela['from-to']['enti']
            assoc = rela['to-from']['assoc'][pmodellang]
        else:
            continue # not my relation or I am not a child or I am recursive
        #fi
        retval.append(EntityCell(ptype=EntityCell.PARENT if pcardinality == Relation.ONE else EntityCell.CHILD
                                 ,pentiid=parentid, pentiname=entities[parentid]['name'][pmodellang],passoc=assoc))
    #for
    return retval

def createentienvironment(pentiid,pjson:JSModel,pmodellang):

    """creates an EntityEnvironment for the given entity found in the json-structure"""
    entities:dict = pjson.getelements(pelemtype=Modelelemtype.ENTI)

    if not pentiid in entities.keys(): return None #non existing entity is Nothing

    entienvir = EntityEnvironment(pentiid=pentiid,pentiname=entities[pentiid]['name'][pmodellang])
    enties = [EntityCell(ptype=EntityCell.ROLE,pentiid=entiid, pentiname=entities[entiid]['name'][pmodellang]) for entiid in entities[pentiid]['roles+'] + entities[pentiid]['subtypes+']]
    entienvir.togrid(pcells=enties, ptype=EntityCell.ROLE)

    enties = [EntityCell(ptype=EntityCell.SUPER,pentiid=entiid, pentiname=entities[entiid]['name'][pmodellang]) for entiid in entities[pentiid]['supertypes+']]
    entienvir.togrid(pcells=enties, ptype=EntityCell.SUPER)

    """handle Parents (I am ONE, parent is MANY)"""
    parents = related(pentiid=pentiid,prelated=entities[pentiid]['relations+'], pjson=pjson, pcardinality=Relation.ONE, pmodellang=pmodellang)
    entienvir.togrid(pcells=parents, ptype=EntityCell.PARENT)

    """handle children (I am MANY, Child is ONE or MANY)"""
    children = related(pentiid=pentiid,prelated=entities[pentiid]['relations+'], pjson=pjson, pcardinality=Relation.MANY, pmodellang=pmodellang)
    entienvir.togrid(pcells=children, ptype=EntityCell.CHILD)

    return entienvir

def enti2svg():
    entistart = """
    <g  fill="{}" stroke="{}" fill-opacity="{}" stroke-opacity="{}" 
            transform="translate({},{})" >
        <rect x="0" y="0" width="{}" height="{}" rx="10" ry="10" /><a href="#{}" >
        <text id="{}" x="20" y="13" fill="{}" font-weight="bold"  fill-opacity="1.0" font-size="{}" stroke="none">
        {} </text></a>
    """
    entiende = """</g>"""

    entisvg = entistart
    entisvg += entiende
    return entisvg

ENTIWIDTH = 120
ENTIHEIGHT = 20
FONTSIZE = 9
CELLHEIGHT = 30
CELLWIDTH = ENTIWIDTH *5/4
LINESHORTEN = 20
MAXRELACHARS = 16
MAXENTICHARS = 24


def printenti(pcell:EntityCell,pposx,pposy):
    entistart = """<g  fill="{}" stroke="{}" fill-opacity="{}" stroke-opacity="{}" 
            transform="translate({},{})" >
            <rect x="0" y="0" width="{}" height="{}" rx="10" ry="10" /><a href="#{}" >
            <text id="box{}" x="6" y="13" fill="{}" font-weight="bold"  fill-opacity="1.0" font-size="{}" stroke="none">
            {} </text></a>
            </g>
            """
    entibox = entistart.format('white', 'blue'
                               , 80, 80
                               , pposx, pposy, ENTIWIDTH, ENTIHEIGHT
                               , pcell.getentiid(), pcell.getentiid()
                               ,'black' if pcell.gettype()== EntityCell.CENTER else 'blue', FONTSIZE
                               , nvl(pcell.getentiname())[:MAXENTICHARS])
    return entibox

def printrela(pcell:EntityCell,pposx,pposy):
    textstart = """<g  fill="{}" stroke="{}" fill-opacity="{}" stroke-opacity="{}" 
            transform="translate({},{})" >
            <text id="{}" x="2" y="4" fill="{}" font-weight="bold"  fill-opacity="1.0" font-size="{}" stroke="none">
            {} </text>
            </g>
            """
    textbox = textstart.format('white', 'blue'
                                , 80,80
                                , pposx,pposy,'','black',FONTSIZE
                                , nvl(pcell.getassoc())[:MAXRELACHARS])

    return textbox

def printline(pstartx,pstarty,plenx,pleny):
    DEFAULT_LINEWIDTH: int = 1
    line = """<g stroke-linecap="butt" >
              <path stroke="rgb(0,0,0)" fill="none" stroke-opacity="100"  stroke-width="{}" 
                    d="M{} {} L{} {}" />
                </g>
            """
    return line.format(DEFAULT_LINEWIDTH,pstartx,pstarty,pstartx+plenx,pstarty+pleny)


def entienviro2svg(penviron):
    maincell:EntityCell = penviron.getcell(phidx='center',pvidx=0)
    return '<div id="{}-container">\n{}\n</div>'.format(maincell.getentiid(), generate_svg_content(penviron))


def generate_svg_content(penviron):
    diagramhead ="""
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
                version="1.1" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
        <defs id="dmw_defs" >
        </defs>
    """
    diagramfoot ="""
        </svg>
    """

    maincell:EntityCell = penviron.getcell(phidx='center',pvidx=0)
    minvidx,maxvidx = penviron.getminvkey(), penviron.getmaxvkey()
    maincell = penviron.getcell(phidx='left', pvidx=0)

    rectheight = (maxvidx - minvidx + 1) * CELLHEIGHT
    rectwidth = 3 * CELLWIDTH
    svgtext = diagramhead.format(width=rectwidth, height=rectheight)

    entistarty = (CELLHEIGHT - ENTIHEIGHT) / 2
    parentlinestarty,parentlineendy=None,None
    rolelinestarty,rolelineendy = None,None
    childlinestarty,childlineendy = None,None
    superlinestarty,superlineendy = None,None
    for vkey in range(minvidx, maxvidx + 1):
        entistartx = 0
        linestarty = entistarty + (ENTIHEIGHT / 2)
        relastarty = linestarty - 10

        cellleft = penviron.getcell(phidx='left', pvidx=vkey)
        cellcenter = penviron.getcell(phidx='center', pvidx=vkey)
        cellright = penviron.getcell(phidx='right', pvidx=vkey)

        if cellleft.gettype() == EntityCell.SUPER:
            svgtext += printenti(pcell=cellleft,pposx=entistartx,pposy=entistarty)
            lenx = entistartx+CELLWIDTH-ENTIWIDTH
            if vkey != 0:
                lenx -= LINESHORTEN
            svgtext += printline(pstartx=entistartx+ENTIWIDTH, pstarty=linestarty, plenx=lenx, pleny=0)
            superlineendy = linestarty

        elif cellcenter.gettype() == EntityCell.PARENT:
            svgtext += printenti(pcell=cellcenter,pposx=entistartx,pposy=entistarty)
            linelength = ENTIWIDTH
            svgtext += printline(pstartx=entistartx+ENTIWIDTH, pstarty=linestarty, plenx=linelength, pleny=0)
            parentlinestarty = nvl(parentlinestarty,linestarty)
        else:
            pass
        # fi
        entistartx += CELLWIDTH
        if cellcenter.gettype() == EntityCell.CENTER:
            svgtext += printenti(pcell=cellcenter, pposx=entistartx, pposy=entistarty)
            superlinestarty = linestarty
            rolelineendy = linestarty
            childlinestarty = entistarty + ENTIHEIGHT
            parentlineendy = entistarty
        elif cellcenter.gettype() == EntityCell.PARENT:
            svgtext += printrela(pcell=cellcenter, pposx=entistartx, pposy=relastarty)
        elif cellcenter.gettype() == EntityCell.CHILD:
            svgtext += printrela(pcell=cellcenter, pposx=entistartx+CELLWIDTH-ENTIWIDTH+5, pposy=relastarty)
        else:
            pass
        # fi
        entistartx += CELLWIDTH
        if cellright.gettype() == EntityCell.ROLE:
            svgtext += printenti(pcell=cellright, pposx=entistartx, pposy=entistarty)
            lenx = CELLWIDTH-ENTIWIDTH
            if vkey != 0:
                lenx -= LINESHORTEN
            svgtext += printline(pstartx=entistartx, pstarty=linestarty, plenx=-lenx, pleny=0)
            rolelinestarty = nvl(rolelinestarty,linestarty)
        elif cellcenter.gettype() == EntityCell.CHILD:
            svgtext += printenti(pcell=cellcenter, pposx=entistartx, pposy=entistarty)
            linelength = -ENTIWIDTH
            svgtext += printline(pstartx=entistartx, pstarty=linestarty, plenx=linelength, pleny=0)
            childlineendy = linestarty
        else:
            pass
        # fi
        entistarty += CELLHEIGHT
    #for
    # print vertical lines
    if superlineendy is not None and (superlineendy-superlinestarty > 0):
        svgtext += printline(pstartx=CELLWIDTH - LINESHORTEN, pstarty=superlinestarty
                             , plenx=0, pleny=superlineendy-superlinestarty)
    if parentlinestarty is not None and (parentlineendy - parentlinestarty > 0):
        svgtext += printline(pstartx=2*ENTIWIDTH, pstarty=parentlinestarty
                             , plenx=0, pleny=parentlineendy - parentlinestarty)
    if childlineendy is not None and (childlineendy - childlinestarty > 0):
        svgtext += printline(pstartx=2*CELLWIDTH-ENTIWIDTH, pstarty=childlinestarty
                             , plenx=0, pleny=childlineendy - childlinestarty)
    if rolelinestarty is not None and (rolelineendy - rolelinestarty > 0):
        svgtext += printline(pstartx=(2*CELLWIDTH)-(LINESHORTEN/2), pstarty=rolelinestarty
                             , plenx=0, pleny= rolelineendy - rolelinestarty)

    svgtext += diagramfoot
    return svgtext


from IM_OBJECTS import Modelelemtype,Relation





