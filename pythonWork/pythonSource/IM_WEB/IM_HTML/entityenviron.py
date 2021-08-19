from IM_JSON import JSModel
from . import hex2rbg
from datetime import datetime
from uuid import uuid4
from matplotlib import colors

nvl = lambda value, default='': value if value is not None else default


def parse_color(color):
    if isinstance(color, str):
        if color.startswith('rgb('):
            return [int(component) / 255 for component in color[4:-1].split(',')]
        elif color.startswith('#'):
            return colors.to_rgba(color)
    return None

class EntityCell():
    """defines the classes and functions to implement an entity-environment representation"""
    CENTER = 'center'
    ROLE = 'role'
    SUPER = 'super'
    PARENT = 'parent'
    CHILD = 'child'

    def __init__(self,ptype=None,pentiid=None,pentiname=None,passoc=None,pbgcolor=None,pfontcolor=None):
        self.setentiid(pentiid)
        self.setentiname(pentiname)
        self.setassoc(passoc)
        self.settype(nvl(ptype))
        self.setbgcolor(nvl(parse_color(pbgcolor), (1,1,1,1)))
        self.setfontcolor(nvl(parse_color(pfontcolor), (0,0,0,1)))

    def getentiid(self):
        return self._entiid

    def setentiid(self,pentiid):
        self._entiid = pentiid

    def getbgcolor(self):
        return self._bgcolor

    def setbgcolor(self,pbgcolor):
        self._bgcolor = pbgcolor

    def getfontcolor(self):
        return self._fontcolor

    def setfontcolor(self,pfontcolor):
        self._fontcolor = pfontcolor

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
    def __init__(self,pentiid,pentiname,pbgcolor):
        self._grid = dict()
        self.fillcell (pvidx=0,phidx='center',pcell=EntityCell(ptype=EntityCell.CENTER,pentiid=pentiid,pentiname=pentiname,pbgcolor=pbgcolor))
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

def hexcolor(pcolor):
    return hex2rbg(nvl(pcolor,"000000"))

def related(pentiid,prelated,pjson,pcardinality,pmodellang,pentities):
    retval = []
    for relaid in prelated:
        rela = pjson.getelements(pelemtype=Modelelemtype.RELA,pfiltered=False)[relaid]
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
                             ,pentiid=parentid, pentiname=pentities[parentid]['name'][pmodellang],passoc=assoc
                                 ,pbgcolor=hexcolor(pjson.getentitycolor(pentiid=parentid,pcolortype="color"))))
    #for
    return retval

def createentienvironment(pentiid,pjson:JSModel,pmodellang):

    """creates an EntityEnvironment for the given entity found in the json-structure"""
    entities:dict = pjson.getelements(pelemtype=Modelelemtype.ENTI,pfiltered=False)

    if not pentiid in entities.keys(): return None #non existing entity is Nothing

    entienvir = EntityEnvironment(pentiid=pentiid,pentiname=entities[pentiid]['name'][pmodellang]
                         ,pbgcolor=hexcolor(pjson.getentitycolor(pentiid=pentiid,pcolortype="color")))
    enties = [EntityCell(ptype=EntityCell.ROLE,pentiid=entiid, pentiname=entities[entiid]['name'][pmodellang]
                         ,pbgcolor=hexcolor(pjson.getentitycolor(pentiid=entiid,pcolortype="color"))
                         ) for entiid in entities[pentiid]['roles+'] + entities[pentiid]['subtypes+']]
    entienvir.togrid(pcells=enties, ptype=EntityCell.ROLE)

    enties = [EntityCell(ptype=EntityCell.SUPER,pentiid=entiid, pentiname=entities[entiid]['name'][pmodellang]
                         ,pbgcolor=hexcolor(pjson.getentitycolor(pentiid=entiid,pcolortype="color"))
                         ) for entiid in entities[pentiid]['supertypes+']]
    entienvir.togrid(pcells=enties, ptype=EntityCell.SUPER)

    """handle Parents (I am ONE, parent is MANY)"""
    parents = related(pentiid=pentiid,prelated=entities[pentiid]['relations+'], pjson=pjson, pcardinality=Relation.ONE, pmodellang=pmodellang
                      ,pentities=entities)
    entienvir.togrid(pcells=parents, ptype=EntityCell.PARENT)

    """handle children (I am MANY, Child is ONE or MANY)"""
    children = related(pentiid=pentiid,prelated=entities[pentiid]['relations+'], pjson=pjson, pcardinality=Relation.MANY, pmodellang=pmodellang
                      ,pentities=entities)
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

ENTIWIDTH = 240
ENTIHEIGHT = 20
FONTSIZE = 9
CELLHEIGHT = 30
CELLWIDTH = ENTIWIDTH * 5/4
LINESHORTEN = 20
MAXRELACHARS = 16
MAXENTICHARS = 21

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


def printentidio(pcell: EntityCell, pposx, pposy, unique: str = ''):
    entitydio = \
        """<UserObject label="{name}" {link} id="{id}{unique}">
            <mxCell style="rounded=1;whiteSpace=wrap;html=1;align=left;{style}" parent="1" vertex="1">
              <mxGeometry x="{posx}" y="{posy}" width="{width}" height="{height}" as="geometry" />
            </mxCell>
            </UserObject>
            """
    fill_color = pcell.getbgcolor()
    font_color = pcell.getfontcolor()

    # fix contrast if colors are dud
    fill_hsv = colors.rgb_to_hsv(fill_color)
    font_hsv = colors.rgb_to_hsv(fill_color)
    if abs(fill_hsv[2] - font_hsv[2]) < .1:
        font_color = (1,1,1,1) if fill_hsv[2] < .5 else (0,0,0,1)

    style = f'fillColor={colors.to_hex(fill_color)};fontColor={colors.to_hex(font_color)};'
    entibox = entitydio.format(id=pcell.getentiid(), unique=unique, name=nvl(pcell.getentiname())[:MAXENTICHARS],
                               style=style,
                               link="" if pcell.gettype() == EntityCell.CENTER else f'link="ssot:{pcell.getentiid()}"',
                               posx=pposx, posy=pposy, width=ENTIWIDTH, height=ENTIHEIGHT
                               )
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

def printlinedio (pstartx,pstarty,plenx,pleny,psrcid=None,prelatext=None):
    uuid=uuid4()
    line = """<mxCell id="{id}" value="" style="endArrow=none;html=1;rounded=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" 
                edge="1" parent="1" >
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="{startx}" y="{starty}" as="sourcePoint" />
            <mxPoint x="{endx}" y="{endy}" as="targetPoint" />
            <Array as="points" />
          </mxGeometry>
        </mxCell>
            """.format(id=uuid,startx=pstartx,starty=pstarty
                       ,endx=pstartx+plenx,endy=pstarty+pleny)
    #source="{srcid}"
    if prelatext is not None:
        relatext = """<mxCell id="{id}" value="{assoc}" style="edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];" vertex="1" connectable="0" 
        parent="{uuid}">
          <mxGeometry x="-0.5672" relative="1" as="geometry">
            <mxPoint x="14" y="-10" as="offset" />
          </mxGeometry>
        </mxCell>""".format(id=str(uuid)+"xx",assoc=prelatext[:MAXRELACHARS],uuid=uuid)
        line += relatext
    #fi
    return line

def entienviro2svg(pentiid,penviron):
    return '<div id="{}-container">\n{}\n</div>'.format(pentiid, generate_svg_content(penviron))

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

    if penviron is None:
        print ("Penviron is None: ")
        return None
    minvidx,maxvidx = penviron.getminvkey(), penviron.getmaxvkey()

    rectheight = (maxvidx - minvidx + 1) * CELLHEIGHT
    rectwidth = 3 * CELLWIDTH
    svgtext = diagramhead.format(width=rectwidth, height=rectheight)

    entistarty = (CELLHEIGHT - ENTIHEIGHT) / 2
    parentlinestarty,parentlineendy = None,None
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
def generate_drawio_content(penviron:EntityEnvironment):

    diagramhead ="""<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron" modified="{date}T{time}Z" agent="curl/7.1" 
etag="NJmVZbbCXh2EGukjSn06" version="14.6.13" type="device">
  <diagram id="{id}" name="{name}">
    <mxGraphModel dx="{dx}" dy="{dy}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1"
    pageScale="1" pageWidth="{width}" pageHeight="{height}" math="0" shadow="0">
    <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
    """
    diagramfoot ="""
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
"""

    if penviron is None:
        print ("Penviron is None: ")
        return None
    minvidx,maxvidx = penviron.getminvkey(), penviron.getmaxvkey()

    rectheight = (maxvidx - minvidx + 1) * CELLHEIGHT
    rectwidth = 3 * CELLWIDTH
    centercell = penviron.getcell(pvidx=0,phidx="center")
    drawiotext = diagramhead.format(date=datetime.now().strftime("%Y-%m-%d"),time=datetime.now().strftime("%H:%M:%S.%s")
                                    ,id=centercell.getentiid(),name=centercell.getentiname()
                                    ,dx=0,dy=0
                                    ,width=rectwidth, height=rectheight)

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
            drawiotext += printentidio(pcell=cellleft,pposx=entistartx,pposy=entistarty, unique=f'-s{vkey}')
            lenx = entistartx+CELLWIDTH-ENTIWIDTH
            if vkey != 0:
                lenx -= LINESHORTEN
            drawiotext += printlinedio(psrcid=cellleft.getentiid(),pstartx=entistartx+ENTIWIDTH, pstarty=linestarty
                                       , plenx=lenx, pleny=0)
            superlineendy = linestarty

        elif cellcenter.gettype() == EntityCell.PARENT:
            drawiotext += printentidio(pcell=cellcenter,pposx=entistartx,pposy=entistarty, unique=f'-p{vkey}')
            linelength = ENTIWIDTH
            drawiotext += printlinedio(psrcid=cellcenter.getentiid(),pstartx=entistartx+ENTIWIDTH, pstarty=linestarty
                                       , plenx=linelength, pleny=0
                                       ,prelatext=cellcenter.getassoc())
            parentlinestarty = nvl(parentlinestarty,linestarty)
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
            lenx = CELLWIDTH-ENTIWIDTH
            if vkey != 0:
                lenx -= LINESHORTEN
            drawiotext += printlinedio(psrcid=cellright.getentiid(),pstartx=entistartx, pstarty=linestarty, plenx=-lenx, pleny=0)
            rolelinestarty = nvl(rolelinestarty,linestarty)
        elif cellcenter.gettype() == EntityCell.CHILD:
            drawiotext += printentidio(pcell=cellcenter, pposx=entistartx, pposy=entistarty, unique=f'-c{vkey}')
            linelength = ENTIWIDTH
            drawiotext += printlinedio(psrcid=cellcenter.getentiid(),pstartx=entistartx - ENTIWIDTH , pstarty=linestarty
                                       , plenx=linelength, pleny=0
                                       ,prelatext=cellcenter.getassoc())
            childlineendy = linestarty
        else:
            pass
        # fi
        entistarty += CELLHEIGHT
    #for
    # print vertical lines
    if superlineendy is not None and (superlineendy-superlinestarty > 0):
        drawiotext += printlinedio(psrcid="",pstartx=CELLWIDTH - LINESHORTEN, pstarty=superlinestarty
                                   , plenx=0, pleny=superlineendy-superlinestarty)
    if parentlinestarty is not None and (parentlineendy - parentlinestarty > 0):
        drawiotext += printlinedio(psrcid="",pstartx=2 * ENTIWIDTH, pstarty=parentlinestarty
                                   , plenx=0, pleny=parentlineendy - parentlinestarty)
    if childlineendy is not None and (childlineendy - childlinestarty > 0):
        drawiotext += printlinedio(psrcid="",pstartx=2 * CELLWIDTH - ENTIWIDTH, pstarty=childlinestarty
                                   , plenx=0, pleny=childlineendy - childlinestarty)
    if rolelinestarty is not None and (rolelineendy - rolelinestarty > 0):
        drawiotext += printlinedio(psrcid="",pstartx=(2 * CELLWIDTH) - (LINESHORTEN / 2), pstarty=rolelinestarty
                                   , plenx=0, pleny= rolelineendy - rolelinestarty)

    drawiotext += diagramfoot
    return drawiotext

from IM_OBJECTS import Modelelemtype,Relation





