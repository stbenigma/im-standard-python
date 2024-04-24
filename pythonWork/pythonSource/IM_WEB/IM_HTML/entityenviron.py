import re
from lxml import etree
from datetime import datetime
from uuid import uuid4

from matplotlib import colors

from SSOT_db.IM_JSON import JSModel
from SSOT_db.IM_OBJECTS import Modelelemtype, Relation
from SSOT_infra import nvl
from .svggeneration import hex2rbg,DEFAULT_LINEWIDTH
from .drawiodiagram import verify_dom, translate_and_encode

"""
    defines the classes and functions to implement an entity-environment representation
    """


class EntityCell():
    CENTER = 'center'
    ROLE = 'role'
    SUPER = 'super'
    PARENT = 'parent'
    CHILD = 'child'

    def __init__(self, ptype=None, pentiid=None, pentiname=None, passoc=None, pbgcolor=None, pfontcolor=None,
                 pdescr=None, precursiveenti=False, pindirrectassoc=False):
        self.setentiid(pentiid)
        self.setentiname(pentiname)
        self.setentidescr(pdescr)
        self.setassoc(passoc)
        self.settype(nvl(ptype))
        self.setbgcolor(nvl(pbgcolor, "rgb(255,255,255)"))
        self.setfontcolor(nvl(pfontcolor, "rgb(0,0,0)"))
        self._entirecursive = precursiveenti
        self._asscocindirect = pindirrectassoc

    def getentiid(self):
        return self._entiid

    def setentiid(self, pentiid):
        self._entiid = pentiid

    def getbgcolor(self):
        return self._bgcolor

    def setbgcolor(self, pbgcolor):
        self._bgcolor = pbgcolor

    def getfontcolor(self):
        return self._fontcolor

    def setfontcolor(self, pfontcolor):
        self._fontcolor = pfontcolor

    def gettype(self):
        return self._type

    def settype(self, ptype):
        self._type = ptype

    def getentidescr(self):
        return self._entidescr

    def setentidescr(self, pentidescr):
        self._entidescr = pentidescr

    def getentiname(self):
        return self._entiname

    def setentiname(self, pentiname):
        self._entiname = pentiname

    def getassoc(self):
        return self._assoc

    def setassoc(self, passoc):
        self._assoc = passoc

    def getentirecursive(self):
        return self._entirecursive

    def getassocindirect(self):
        return self._asscocindirect

    def isemptycell(self):
        return self.gettype() == ''

    def __str__(self):
        return ', '.join((self.gettype(), nvl(self.getentiid()), nvl(self.getentiname()), nvl(self.getassoc())))


class EntityEnvironment():
    """Dictionary for one entity.
        two-dimensional extensible grid 1. index (vidx)  top down , 2. index (hidx) -> left to right
        0/0 is the center
        1,2,3 are cells to downwards or to the right
        -1,-2,-3 are cells upwards or to the left
        {  ...
          ,-1 : {}   vidx
          ,0 : {'left'
                'center': EntityCell
                right :
                }
          ,1 : {}
          ,...}
    """

    def __init__(self, pentiid, pentiname, pbgcolor,precursiveenti=False):
        self._grid = dict()
        self.fillcell(pvidx=0, phidx='center',
                      pcell=EntityCell(ptype=EntityCell.CENTER, pentiid=pentiid, pentiname=pentiname,
                                       pbgcolor=pbgcolor, precursiveenti=precursiveenti))
        return

    def fillcell(self, pvidx, phidx, pcell: EntityCell):
        if pvidx not in self._grid.keys():
            self._grid[pvidx] = {}
        self._grid[pvidx][phidx] = pcell

    def getcell(self, pvidx, phidx):
        if pvidx not in self._grid.keys():
            return EntityCell()  # non existing cell is empty
        if phidx not in self._grid[pvidx].keys():
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
        # doubleline = len(pcells) > 2
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
            assert False, "illegal type '{}'".format(ptype)

        for cell in pcells:
            self.fillcell(pvidx=vidx, phidx=hidx, pcell=cell)
            # vidx = switchvidx(vidx, doubleline) moved to display procedure
            vidx += 1 if ptype in (EntityCell.SUPER, EntityCell.CHILD) else -1
        # for
        return


def hexcolor(pcolor):
    return hex2rbg(nvl(pcolor, "000000"))


def related(pentiid, pjson: JSModel, pcardinality, pmodellang, pentities):
    retval = []
    relas = pentities[pentiid]['relations+'] + pentities[pentiid]['inheritedrelations+']
    for relaid in relas:
        isindirec = False
        rela = pjson.getbyid(relaid)
        if rela['type'] in (Relation.ISAROLE, Relation.ISASUBTYPE): continue
        if (rela['from-to']['enti'] == pentiid and rela['to-from']['enti'] == pentiid):
            # rekursiv, wird nicht hier gezeichnet
            continue
        elif (rela['from-to']['enti'] == pentiid  # and rela['to-from']['enti'] != pentiid
              and rela['to-from']['maptype'] == pcardinality):
            parentid = rela['to-from']['enti']
            assoc = rela['from-to']['assoc'][pmodellang]
        elif (rela['to-from']['enti'] == pentiid  # and rela['from-to']['enti'] != pentiid
              and rela['from-to']['maptype'] == pcardinality):
            parentid = rela['from-to']['enti']
            assoc = rela['to-from']['assoc'][pmodellang]
        elif rela['to-from']['enti'] != pentiid and rela['from-to']['enti'] != pentiid:
            if pjson.issupertype(rela['to-from']['enti'], pentiid) \
                    and rela['to-from']['maptype'] == pcardinality:
                # inherited entity
                parentid = rela['from-to']['enti']
                assoc = rela['to-from']['assoc'][pmodellang]
                isindirec = True
            elif pjson.issupertype(rela['from-to']['enti'], pentiid) \
                    and rela['from-to']['maptype'] == pcardinality:
                # inherited entity
                parentid = rela['to-from']['enti']
                assoc = rela['from-to']['assoc'][pmodellang]
                isindirec = True
            else:
                continue
        else:
            continue
        # fi
        retval.append(EntityCell(ptype=EntityCell.PARENT if pcardinality == Relation.ONE else EntityCell.CHILD
                                 , pentiid=parentid, pentiname=pentities[parentid]['name'][pmodellang], passoc=assoc
                                 , pbgcolor=hexcolor(pjson.getentitycolor(pentiid=parentid, pcolortype="color"))
                                 , pindirrectassoc=isindirec))
    # for
    return retval


def createentienvironment(pentiid, pjson: JSModel, pmodellang):
    """creates an EntityEnvironment for the given entity found in the json-structure"""
    entities: dict = pjson.getelements(pelemtype=Modelelemtype.ENTI)

    if not pentiid in entities.keys(): return None  # non existing entity is Nothing

    entienvir = EntityEnvironment(pentiid=pentiid, pentiname=entities[pentiid]['name'][pmodellang],
                                   pbgcolor=hexcolor(pjson.getentitycolor(pentiid=pentiid, pcolortype="color")),
                                  precursiveenti=pjson.isrecursive(pentiid))
    enties = [EntityCell(ptype=EntityCell.ROLE, pentiid=entiid, pentiname=entities[entiid]['name'][pmodellang]
                         , pdescr=entities[entiid]['descr'][pmodellang]
                         , pbgcolor=hexcolor(pjson.getentitycolor(pentiid=entiid, pcolortype="color"))
                         ) for entiid in entities[pentiid]['roles+'] + entities[pentiid]['subtypes+']]
    entienvir.togrid(pcells=enties, ptype=EntityCell.ROLE)

    enties = [EntityCell(ptype=EntityCell.SUPER, pentiid=entiid, pentiname=entities[entiid]['name'][pmodellang]
                         , pdescr=entities[entiid]['descr'][pmodellang]
                         , pbgcolor=hexcolor(pjson.getentitycolor(pentiid=entiid, pcolortype="color"))
                         ) for entiid in entities[pentiid]['supertypes+']]
    entienvir.togrid(pcells=enties, ptype=EntityCell.SUPER)

    """handle Parents (I am ONE, parent is MANY)"""
    parents = related(pentiid=pentiid,
                      pjson=pjson, pcardinality=Relation.ONE,
                      pmodellang=pmodellang,
                      pentities=entities)
    entienvir.togrid(pcells=parents, ptype=EntityCell.PARENT)

    """handle children (I am MANY, Child is ONE or MANY)"""
    children = related(pentiid=pentiid,
                       pjson=pjson,
                       pcardinality=Relation.MANY, pmodellang=pmodellang,
                       pentities=entities)
    entienvir.togrid(pcells=children, ptype=EntityCell.CHILD)

    return entienvir


ENTIWIDTH = 120
ENTIHEIGHT = 20
FONTSIZE = 9
CELLHEIGHT = 30
CELLWIDTH = ENTIWIDTH * 5 / 4
LINESHORTEN = 20
MAXRELACHARS = 16
MAXENTICHARS = 21
MAXDESCRCHARS = 300


def printenti(pcell: EntityCell, pposx, pposy,precursive=False):
    recursive = f"""<path d="M {ENTIWIDTH*0.9} -1 A 3 3 0 0 1 {ENTIWIDTH} 7" stroke="black" fill="none"/>"""\
                if precursive else ""

    entistart = """<g  fill="{color}" stroke="{stroke}" fill-opacity="{fopacity}" stroke-opacity="{sopacity}" 
            transform="translate({posx},{posy})" >
            <rect x="0" y="0" width="{width}" height="{height}" rx="10" ry="10" >{title}</rect>
            <a href="{href}" >
            <text x="6" y="13" fill="{fillcolor}" font-weight="bold"  fill-opacity="1.0" font-size="{fontsize}" stroke="none">
            {name} </text>{title}
            </a>{recursive}
            </g>
            """
    entibox = entistart.format(color=pcell.getbgcolor(), stroke='blue'
                               , fopacity=0.3, sopacity=0.8
                               , posx=pposx, posy=pposy, width=ENTIWIDTH, height=ENTIHEIGHT
                               ,href=f"#{pcell.getentiid()}"
                               , element=pcell.getentiid()
                               , fillcolor='black' if pcell.gettype() == EntityCell.CENTER else 'blue',
                               fontsize=FONTSIZE
                               , name=nvl(pcell.getentiname())[:MAXENTICHARS]
                               , recursive = recursive
                               , title=f"<title>{' ' if pcell.getentidescr() in (None, '') else pcell.getentidescr()[:MAXDESCRCHARS]}</title>"
                               )
    return entibox


def printrela(pcell: EntityCell, pposx, pposy):
    textstart = f"""<g  fill="{'white'}" stroke="{'blue'}" fill-opacity="{80}" stroke-opacity="{80}" 
            transform="translate({pposx},{pposy})" >
            <text x="2" y="4" fill="{'black'}" font-weight="bold"  fill-opacity="1.0" font-size="{FONTSIZE}" stroke="none">
            {nvl(pcell.getassoc())[:MAXRELACHARS]} </text></g>"""

    return textstart


blacklinecolor = "rgb(0,0,0)"
graylinecolor = "rgb(160,160,160)"


def linecolor(pindirect: bool) -> str:
    return graylinecolor if pindirect else blacklinecolor


def printline(pstartx, pstarty, plenx, pleny, plinecolor=blacklinecolor):
    line = f"""<g stroke-linecap="butt" >
              <path stroke="{plinecolor}" fill="none" stroke-opacity="100"  stroke-width="{DEFAULT_LINEWIDTH}" 
                    d="M{pstartx} {pstarty} L{pstartx + plenx} {pstarty + pleny}" />
                </g>
            """
    return line


def printlinedio(pstartx, pstarty, plenx, pleny, prelatext=None, plinecolor=blacklinecolor):
    uuid = uuid4()
    line = f"""<mxCell id="{uuid}" value="" 
                style="stroke={plinecolor};endArrow=none;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" 
                edge="1" parent="1" >
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="{pstartx}" y="{pstarty}" as="sourcePoint" />
            <mxPoint x="{pstartx + plenx}" y="{pstarty + pleny}" as="targetPoint" />
            <Array as="points" />
          </mxGeometry>
        </mxCell>
            """
    # source="{srcid}"
    if prelatext is not None:
        relatext = f"""<mxCell id="{str(uuid) + "xx"}" value="{translate_and_encode(prelatext[:MAXRELACHARS])}" 
        style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];" vertex="1" connectable="0" 
        parent="{uuid}">
          <mxGeometry x="-0.5672" relative="1" as="geometry">
            <mxPoint x="14" y="-10" as="offset" />
          </mxGeometry>
        </mxCell>"""
        line += relatext
    # fi
    return line


def entienviro2svg(penviron,pentiid=None):
    return '<div>\n{}\n</div>'.format(generate_svg_content(penviron=penviron))


def generate_svg_content(penviron):
    diagramhead = """
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
                version="1.1" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
    """
    diagramfoot = """
        </svg>
    """

    if penviron is None:
        print("Penviron is None: ")
        return None

    minvidx, maxvidx = penviron.getminvkey(), penviron.getmaxvkey()

    rectheight = (maxvidx - minvidx + 1) * CELLHEIGHT
    rectwidth = 3 * CELLWIDTH
    svgtext = diagramhead.format(width=rectwidth, height=rectheight)

    entistarty = (CELLHEIGHT - ENTIHEIGHT) / 2
    parentlinestarty, parentlineendy = None, None
    rolelinestarty, rolelineendy = None, None
    childlinestarty, childlineendy = None, None
    superlinestarty, superlineendy = None, None
    for vkey in range(minvidx, maxvidx + 1):
        entistartx = 0
        linestarty = entistarty + (ENTIHEIGHT / 2)
        relastarty = linestarty - 10

        cellleft: EntityCell = penviron.getcell(phidx='left', pvidx=vkey)
        cellcenter: EntityCell = penviron.getcell(phidx='center', pvidx=vkey)
        cellright: EntityCell = penviron.getcell(phidx='right', pvidx=vkey)

        if cellleft.gettype() == EntityCell.SUPER:
            svgtext += printenti(pcell=cellleft, pposx=entistartx, pposy=entistarty)
            lenx = entistartx + CELLWIDTH - ENTIWIDTH
            if vkey != 0:
                lenx -= LINESHORTEN
            svgtext += printline(pstartx=entistartx + ENTIWIDTH, pstarty=linestarty, plenx=lenx, pleny=0,
                                 plinecolor=linecolor(cellleft.getassocindirect()))
            superlineendy = linestarty

        elif cellcenter.gettype() == EntityCell.PARENT:
            svgtext += printenti(pcell=cellcenter, pposx=entistartx, pposy=entistarty)
            linelength = ENTIWIDTH
            svgtext += printline(pstartx=entistartx + ENTIWIDTH, pstarty=linestarty, plenx=linelength, pleny=0,
                                 plinecolor=linecolor(cellcenter.getassocindirect()))
            parentlinestarty = nvl(parentlinestarty, linestarty)
        else:
            pass
        # fi
        entistartx += CELLWIDTH
        if cellcenter.gettype() == EntityCell.CENTER:
            svgtext += printenti(pcell=cellcenter, pposx=entistartx, pposy=entistarty,precursive=cellcenter.getentirecursive())
            superlinestarty = linestarty
            rolelineendy = linestarty
            childlinestarty = entistarty + ENTIHEIGHT
            parentlineendy = entistarty
        elif cellcenter.gettype() == EntityCell.PARENT:
            svgtext += printrela(pcell=cellcenter, pposx=entistartx, pposy=relastarty)
        elif cellcenter.gettype() == EntityCell.CHILD:
            svgtext += printrela(pcell=cellcenter, pposx=entistartx + CELLWIDTH - ENTIWIDTH + 5, pposy=relastarty)
        else:
            pass
        # fi
        entistartx += CELLWIDTH
        if cellright.gettype() == EntityCell.ROLE:
            svgtext += printenti(pcell=cellright, pposx=entistartx, pposy=entistarty)
            lenx = CELLWIDTH - ENTIWIDTH
            if vkey != 0:
                lenx -= LINESHORTEN
            svgtext += printline(pstartx=entistartx, pstarty=linestarty, plenx=-lenx, pleny=0,
                                 plinecolor=linecolor(cellright.getassocindirect()))
            rolelinestarty = nvl(rolelinestarty, linestarty)
        elif cellcenter.gettype() == EntityCell.CHILD:
            svgtext += printenti(pcell=cellcenter, pposx=entistartx, pposy=entistarty)
            linelength = -ENTIWIDTH
            svgtext += printline(pstartx=entistartx, pstarty=linestarty, plenx=linelength, pleny=0,
                                 plinecolor=linecolor(cellcenter.getassocindirect()))
            childlineendy = linestarty
        else:
            pass
        # fi
        entistarty += CELLHEIGHT
    # for
    # print vertical lines
    if superlineendy is not None and (superlineendy - superlinestarty > 0):
        svgtext += printline(pstartx=CELLWIDTH - LINESHORTEN, pstarty=superlinestarty
                             , plenx=0, pleny=superlineendy - superlinestarty)
    if parentlinestarty is not None and (parentlineendy - parentlinestarty > 0):
        svgtext += printline(pstartx=2 * ENTIWIDTH, pstarty=parentlinestarty
                             , plenx=0, pleny=parentlineendy - parentlinestarty)
    if childlineendy is not None and (childlineendy - childlinestarty > 0):
        svgtext += printline(pstartx=2 * CELLWIDTH - ENTIWIDTH, pstarty=childlinestarty
                             , plenx=0, pleny=childlineendy - childlinestarty)
    if rolelinestarty is not None and (rolelineendy - rolelinestarty > 0):
        svgtext += printline(pstartx=(2 * CELLWIDTH) - (LINESHORTEN / 2), pstarty=rolelinestarty
                             , plenx=0, pleny=rolelineendy - rolelinestarty)

    svgtext += diagramfoot
    return svgtext


"""
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron" modified="2021-07-20T11:52:28.047Z" agent="5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) draw.io/14.6.13 Chrome/89.0.4389.128 Electron/12.0.7 Safari/537.36" etag="NJmVZbbCXh2EGukjSn06" version="14.6.13" type="device">
  <diagram id="-IuDeWdp_pBGzQphX35I" name="Seite-1">
    <mxGraphModel dx="527" dy="475" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="ct_x_fueRCHBXW9Sjaz1-1" value="Kunde" style="rounded=1;whiteSpace=wrap;html=1;" parent="1" vertex="1">
          <mxGeometry x="130" y="200" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="ct_x_fueRCHBXW9Sjaz1-3" value="Produkt" style="rounded=1;whiteSpace=wrap;html=1;" parent="1" vertex="1">
          <mxGeometry x="440" y="110" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="ct_x_fueRCHBXW9Sjaz1-5" value="" style="endArrow=oval;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=0.75;exitY=0;exitDx=0;exitDy=0;startArrow=ERmany;startFill=0;endFill=0;rounded=0;" parent="1" source="ct_x_fueRCHBXW9Sjaz1-1" target="ct_x_fueRCHBXW9Sjaz1-3" edge="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="240" y="220" as="sourcePoint" />
            <mxPoint x="400" y="220" as="targetPoint" />
            <Array as="points">
              <mxPoint x="220" y="140" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="ct_x_fueRCHBXW9Sjaz1-6" value="verkauft an" style="edgeLabel;resizable=0;html=1;align=center;verticalAlign=middle;rotation=0;" parent="ct_x_fueRCHBXW9Sjaz1-5" connectable="0" vertex="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="77" y="-10" as="offset" />
          </mxGeometry>
        </mxCell>
        <mxCell id="ct_x_fueRCHBXW9Sjaz1-7" value="kauft" style="edgeLabel;resizable=0;html=1;align=left;verticalAlign=bottom;rotation=-50;" parent="ct_x_fueRCHBXW9Sjaz1-5" connectable="0" vertex="1">
          <mxGeometry x="-1" relative="1" as="geometry">
            <mxPoint x="30" y="-10" as="offset" />
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""


def generate_drawio_content(penviron: EntityEnvironment):
    diagramhead = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron" modified="{date}T{time}Z" agent="curl/7.1" 
etag="NJmVZbbCXh2EGukjSn06" version="14.6.13" type="device">
  <diagram name="{name}">
    <mxGraphModel dx="{dx}" dy="{dy}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1"
    pageScale="1" pageWidth="{width}" pageHeight="{height}" math="0" shadow="0">
    <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
    """
    diagramfoot = """
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

    if penviron is None:
        print("Penviron is None: ")
        return None
    minvidx, maxvidx = penviron.getminvkey(), penviron.getmaxvkey()

    rectheight = (maxvidx - minvidx + 1) * CELLHEIGHT
    rectwidth = 3 * CELLWIDTH
    centercell = penviron.getcell(pvidx=0, phidx="center")
    drawiotext = diagramhead.format(date=datetime.now().strftime("%Y-%m-%d"),
                                    time=datetime.now().strftime("%H:%M:%S.%s")
                                    , name=centercell.getentiname()
                                    , dx=0, dy=0
                                    , width=rectwidth, height=rectheight)

    entistarty = (CELLHEIGHT - ENTIHEIGHT) / 2
    parentlinestarty, parentlineendy = None, None
    rolelinestarty, rolelineendy = None, None
    childlinestarty, childlineendy = None, None
    superlinestarty, superlineendy = None, None
    for vkey in range(minvidx, maxvidx + 1):
        entistartx = 0
        linestarty = entistarty + (ENTIHEIGHT / 2)
        relastarty = linestarty - 10

        cellleft = penviron.getcell(phidx='left', pvidx=vkey)
        cellcenter = penviron.getcell(phidx='center', pvidx=vkey)
        cellright = penviron.getcell(phidx='right', pvidx=vkey)

        if cellleft.gettype() == EntityCell.SUPER:
            drawiotext += printentidio(pcell=cellleft, pposx=entistartx, pposy=entistarty, unique=f'-s{vkey}')
            lenx = entistartx + CELLWIDTH - ENTIWIDTH
            if vkey != 0:
                lenx -= LINESHORTEN
            drawiotext += printlinedio(pstartx=entistartx + ENTIWIDTH, pstarty=linestarty
                                       , plenx=lenx, pleny=0,
                                 plinecolor=linecolor(cellleft.getassocindirect()))
            superlineendy = linestarty

        elif cellcenter.gettype() == EntityCell.PARENT:
            drawiotext += printentidio(pcell=cellcenter, pposx=entistartx, pposy=entistarty, unique=f'-p{vkey}')
            linelength = ENTIWIDTH
            drawiotext += printlinedio(pstartx=entistartx + ENTIWIDTH, pstarty=linestarty
                                       , plenx=linelength, pleny=0
                                       , prelatext=cellcenter.getassoc(),
                                 plinecolor=linecolor(cellcenter.getassocindirect()))
            parentlinestarty = nvl(parentlinestarty, linestarty)
        else:
            pass
        # fi
        entistartx += CELLWIDTH
        if cellcenter.gettype() == EntityCell.CENTER:
            drawiotext += printentidio(pcell=cellcenter, pposx=entistartx, pposy=entistarty, unique=f'-ce{vkey}')
            superlinestarty = linestarty
            rolelineendy = linestarty
            childlinestarty = entistarty + ENTIHEIGHT
            parentlineendy = entistarty
        else:
            pass
        # fi
        entistartx += CELLWIDTH
        if cellright.gettype() == EntityCell.ROLE:
            drawiotext += printentidio(pcell=cellright, pposx=entistartx, pposy=entistarty, unique=f'-r{vkey}')
            lenx = CELLWIDTH - ENTIWIDTH
            if vkey != 0:
                lenx -= LINESHORTEN
            drawiotext += printlinedio(pstartx=entistartx, pstarty=linestarty,
                                       plenx=-lenx, pleny=0,
                                 plinecolor=linecolor(cellright.getassocindirect()))
            rolelinestarty = nvl(rolelinestarty, linestarty)
        elif cellcenter.gettype() == EntityCell.CHILD:
            drawiotext += printentidio(pcell=cellcenter, pposx=entistartx, pposy=entistarty, unique=f'-c{vkey}')
            linelength = ENTIWIDTH
            drawiotext += printlinedio(pstartx=entistartx - ENTIWIDTH, pstarty=linestarty
                                       , plenx=linelength, pleny=0
                                       , prelatext=cellcenter.getassoc(),
                                 plinecolor=linecolor(cellcenter.getassocindirect()))
            childlineendy = linestarty
        else:
            pass
        # fi
        entistarty += CELLHEIGHT
    # for
    # print vertical lines
    if superlineendy is not None and (superlineendy - superlinestarty > 0):
        drawiotext += printlinedio(pstartx=CELLWIDTH - LINESHORTEN, pstarty=superlinestarty
                                   , plenx=0, pleny=superlineendy - superlinestarty)
    if parentlinestarty is not None and (parentlineendy - parentlinestarty > 0):
        drawiotext += printlinedio(pstartx=2 * ENTIWIDTH, pstarty=parentlinestarty
                                   , plenx=0, pleny=parentlineendy - parentlinestarty)
    if childlineendy is not None and (childlineendy - childlinestarty > 0):
        drawiotext += printlinedio(pstartx=2 * CELLWIDTH - ENTIWIDTH, pstarty=childlinestarty
                                   , plenx=0, pleny=childlineendy - childlinestarty)
    if rolelinestarty is not None and (rolelineendy - rolelinestarty > 0):
        drawiotext += printlinedio(pstartx=(2 * CELLWIDTH) - (LINESHORTEN / 2), pstarty=rolelinestarty
                                   , plenx=0, pleny=rolelineendy - rolelinestarty)

    drawiotext += diagramfoot
    try:
        loaded_dom = etree.fromstring(drawiotext.encode())
    except Exception as e:
        raise Exception(f"Cannot parse {drawiotext}") from e
    verify_dom(loaded_dom)

    return drawiotext


def parse_color(value: str):
    """Convert colors in the rgb(rrr,bbb,ggg) format where r,b,g are in decimals 0-255 into an array (r,g,b,a)"""
    expression = re.compile(r"(rgb|)\(([0-9]+),([0-9]+),([0-9]+)\)")
    match = expression.match(value)
    assert match, f"Value {value} does not match rgb(r,g,b) pattern"
    return 1 / 256 * int(match.group(2)), 1 / 256 * int(match.group(3)), 1 / 256 * int(match.group(4)), 1


def printentidio(pcell: EntityCell, pposx, pposy, unique: str = ''):
    entitydio = \
        """<UserObject label="{name}" {link} id="{id}{unique}">
            <mxCell style="rounded=1;whiteSpace=wrap;html=1;align=left;{style}" parent="1" vertex="1">
              <mxGeometry x="{posx}" y="{posy}" width="{width}" height="{height}" as="geometry" />
            </mxCell>
            </UserObject>
            """
    fill_color = parse_color(pcell.getbgcolor())
    font_color = parse_color(pcell.getfontcolor())

    # fix contrast if colors are dud
    fill_hsv = fill_color
    font_hsv = font_color
    if abs(fill_hsv[2] - font_hsv[2]) < .1:
        font_color = (1, 1, 1, 1) if fill_hsv[2] < .5 else (0, 0, 0, 1)

    style = f'fillColor={colors.to_hex(fill_color)};fontColor={colors.to_hex(font_color)};'
    entibox = entitydio.format(id=pcell.getentiid(), unique=unique, name=translate_and_encode(nvl(pcell.getentiname())[:MAXENTICHARS]),
                               style=style,
                               link="" if pcell.gettype() == EntityCell.CENTER else f'link="ssot:{pcell.getentiid()}"',
                               posx=pposx, posy=pposy, width=ENTIWIDTH, height=ENTIHEIGHT
                               )
    return entibox
