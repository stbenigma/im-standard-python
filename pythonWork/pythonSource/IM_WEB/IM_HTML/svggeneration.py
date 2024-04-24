import html
import logging
import math
import os
from pathlib import Path

# used for text label length calculations
import pygame.font

from SSOT_db.IM_JSON import JSModel,arcno
from SSOT_infra import nvl

DEFAULT_LINEWIDTH: int = 1

idnumber=999
def uniqueid():
    global idnumber
    idnumber += 1
    return idnumber

def textmeasure(fontname, size, weight, text):
    """Uses pygame.font.Font for label size calculations"""
    if size is None or text is None:
        return 0, 0
    if fontname is None:
        # foryouandyourcustomers default font
        fontname = "TT Norms Pro"
    wlo = weight.lower() if weight is not None else ''
    italic = 'italic' in wlo
    bold = 'bold' in wlo
    pygame.font.init()
    font_file = resolve_font(fontname, bold, italic)
    pgf = pygame.font.Font(font_file, size)
    pgf.set_bold(bold)
    pgf.set_italic(italic)
    pgf.set_underline('underline' in wlo)
    pgf.set_strikethrough('strikethrough' in wlo)
    return pgf.size(text)


def resolve_font(fontname: str, bold, italic):
    font_file = pygame.font.match_font(fontname, bold=bold, italic=italic)
    if font_file is None:
        fallback = "TT Norms Pro"
        font_file = pygame.font.match_font(fallback, bold=bold, italic=italic)  # fallback
        if font_file is None:
            font_file = Path(Path(__file__).parent, '../../../../res/fonts/TT Norms Pro Regular.otf')
            logging.debug(f"Falling back to font file in {font_file.resolve()}")
            if not font_file.exists():
                logging.error(f"Missing font file {font_file.resolve()}")
                fallback = ["Liberation Sans", "Helvetica", "Tahoma", "Arial" ]  # Any font
                font_file = pygame.font.match_font(fallback, bold=bold, italic=italic)
        logging.debug(f"Falling back from {fontname} to {font_file}")
        assert font_file is not None, f"Cannot use fallback font {font_file}"
        assert font_file.is_file(), f"The path specified is not a valid font file {font_file.resolve()}"
    return font_file


def textwidth(family, size, weight, text):
    return textmeasure(family, size, weight, text)[0]


def textheight(family, size, weight, text):
    return textmeasure(family, size, weight, text)[1]


def hex2rbg(phex):
    assert type(phex) == str and len(phex) == 6
    try:
        r = int(phex[0:2], 16)
        g = int(phex[2:4], 16)
        b = int(phex[4:6], 16)
    except:
        raise Exception(f"illegal hex value '{phex}'")
    return f"({r},{g},{b})"


def rgb2hex(*args) -> str:
    assert len(args) == 3 and args[0] in range(256) \
           and args[2] in range(256) and args[2] in range(256)
    lochex = f'{args[0]:02X}{args[1]:02X}{args[2]:02X}'
    return lochex


def href(diagid=None, elemid=None, subelemid=None,href=None):
    if href is not None:
        retval = f'href="{href}"'.format(href)
    else:
        lochref = """id="{diagelemid}" {href} """
        retval = lochref.format(diagelemid=nvl(diagid,"D"+str(uniqueid())) + "-" + nvl(elemid,str(uniqueid()))+nvl(subelemid),
                                href='' if elemid is None
                                else 'href="#{}"'.format(elemid))
    # fi
    return retval


class SvgRotate:
    def __init__(self, angle, x=0, y=0):
        self.angle = angle
        self.x = x
        self.y = y
        return

    def rotate(self):
        if self.angle == 0:
            retval = ""
        else:
            retval = 'transform="rotate({} {} {})"'.format(self.angle, self.x, self.y)
        return retval


class SvgPos:
    """ Position on plane
        the coordinate system is
        increasing x   left to right  increasing y  top down
            -y
        -x  ...  +x
            +y
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def newpos(self, dx, dy):
        return SvgPos(self.x + dx, self.y + dy)

    def distance(self, pos):
        return round(math.sqrt((pos.y - self.y) ** 2 + (pos.x - self.x) ** 2), 2)

    def angle(self, pos):
        """ angle from self in direction of pos
            NOTE -(delta y) because of coordinate system going top down
        """
        return math.atan2(-(pos.y - self.y), pos.x - self.x)

    def maindirection(self, pos):
        """"         north -y
                       ^
         -x west <--  x,y --> east  +x
                       v
                    south  +y
        """
        PI = math.pi
        return "east" if -PI / 4 < self.angle(pos) <= PI / 4 \
            else "north" if PI / 4 < self.angle(pos) <= PI * 3 / 4 \
            else "south" if -PI * 3 / 4 < self.angle(pos) <= - PI / 4 \
            else "west"


class SvgDiagram:

    # SVGFRAME = """<svg id="{diagid}-SVG" width="{width}" height="{height}" viewBox="0 0 {width} {height}"
    #         xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
    #         version="1.1">
    #         {style}
    #         <defs id="dmw_defs" >
    #         </defs>
    #         {content}
    #     </svg>"""
    SVGFRAME= """<g id="level{minzoom}"  minzoom="{minzoom}" maxzoom="{maxzoom}">
                 {content}
                 </g>
              """


    def __init__(self, **kwargs):
        self._content = None
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.content = nvl(kwargs.get("content"), [])
        self.diagid = kwargs.get("diagid")
        self.title = kwargs.get("title")
        self.minzoomlevel=kwargs.get("minzoomlevel")
        self.maxzoomlevel=kwargs.get("maxzoomlevel")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if type(value) == list:
            self._content = value
        else:
            self._content = [value]

    def maxx(self):
        return max(nvl(c.maxx(), 0) for c in self.content)

    def maxy(self):
        return 0 if len(self.content)==0 else max(nvl(c.maxy(), 0) for c in self.content)

    def addcontent(self, *morecontent):
        self.content.extend(morecontent)

    def _addattributes(self, entijson, svgenti):
        attrs = []
        for attrid in entijson["attributes+"]:
            if attrid not in self._diagattr:
                continue  # not on this diagram
            attrjson = self._model.getbyid(attrid)
            attrs.append([int(attrjson["seq"]),
                          attrjson["descriptive"],
                          attrjson["mandatory"],
                          attrjson["keys+"],
                          attrid,
                          attrjson["name"][self._lang],
                          attrjson["descr"][self._lang]
                          if attrjson["tooltip"][self._lang] == ""
                          else attrjson["tooltip"][self._lang],
                          attrjson["minzoomlevel"],attrjson["maxzoomlevel"]
                          ])
        # for
        attrs.sort(key=lambda x: "0" if x[1] else "1" +
                                                  "0" if len(x[3]) > 0 else "1" +
                                                                            "0" if x[2] else "1" +
                                                                                             str(x[0]).zfill(5)
                   )

        for idx, a in enumerate(attrs, start=1):
            if (idx < SvgAttribute.MAXATTRS) or idx == len(attrs) == SvgAttribute.MAXATTRS:
                svgenti.addattribute(SvgAttribute(name=a[5],
                                                  tooltip=a[6],
                                                  elemid=a[4],
                                                  minzoom=a[7],maxzoom=a[8]
                                                  )
                                     )
            elif idx == SvgAttribute.MAXATTRS:
                attrnamelist = "\n".join(a[5] for a in attrs[idx - 1:])
                svgenti.addattribute(SvgAttribute(name=SvgAttribute.OVERFLOW.format(attrcnt=str(len(attrs) - idx + 1)),
                                                  tooltip=attrnamelist,
                                                  elemid="ATTR-OVL"+str(uniqueid())))
        return

    def _issubentityondiagram(self, entijson):
        superentiid = entijson["supertypeentity"]
        if superentiid is None:
            return False  # I am not a subentity
        # if my superentity is on diagram, I am a subentity on this diagram
        return (superentiid in self._diagentis)

    def _addentity(self, entiid, entijson, entiui, fatherentity=None):
        # mark the absolute position of the entity
        svgenti = SvgEntity(width=entiui["ui"]["width"], height=entiui["ui"]["height"],
                            name=entijson["name"][self._lang],
                            elemid=entiid,
                            elemtooltip=entijson["descr"][self._lang][:200]+"\n\n"+"\n".join(ex[self._lang] for ex in entijson["examples"][:3])
                            if entijson["tooltip"][self._lang] == ""
                            else entijson["tooltip"][self._lang],
                            x=entiui["relpos_x"], y=entiui["relpos_y"],
                            color=entiui["ui"]["color"],
                            fatherentity=fatherentity,
                            minzoom=entijson["minzoomlevel"],
                            maxzoom=entijson["maxzoomlevel"])
        self._addattributes(entijson, svgenti)
        # check for my subentites
        for subentiid in entijson["subtypes+"]:
            if subentiid in self._diagentis:
                subentijson = self._model.getbyid(subentiid)
                if subentijson["supertypeentity"] == entiid:
                    # one of mine subentities found. add it
                    subentiui = self._model.elementui(diagid=self.diagid,
                                                      elemtype="entity",
                                                      elemid=subentiid)
                    # in the jsonfile the subentites are absolutely positioned
                    # here we need them relatively to their superentity
                    subentiui["relpos_x"] = subentiui["pos_x"] - entiui["pos_x"]
                    subentiui["relpos_y"] = subentiui["pos_y"] - entiui["pos_y"]

                    self._addentity(entiid=subentiid, entijson=subentijson,
                                    entiui=subentiui, fatherentity=svgenti)
                # fi
            # fi
        # for
        if fatherentity is None:
            self.addcontent(svgenti)
        return

    def _iscategoryentity(self,entijson):
        """an entity with a name identical to a categroy name, not having any attributs, relationships, sub- oder superentities
           is considered a category-placeholder"""
        catnames=[cat["name"] for cat in self._model.getelements("categories").values()]
        return  entijson["name"][self._lang] in catnames\
                and (len(entijson["supertypes+"]) +len(entijson["roles+"])+len(entijson["subtypes+"])+
                    len(entijson["attributes+"])+len(entijson["relations+"])) == 0

    def _addallentities(self):
        for entiui in self._diagjson["elements"]["entity"]:
            entiid = entiui["element"]
            entijson = self._model.getbyid(entiid)

            if self._iscategoryentity(entijson):
                #skip entities representing categories
                #print (entijson.name[self._lang])
                continue
            # skik subentites,they are added recursively within all entities
            if not self._issubentityondiagram(entijson):
                entiui["relpos_x"] = entiui["pos_x"]
                entiui["relpos_y"] = entiui["pos_y"]
                self._addentity(entiid=entiid, entijson=entijson, entiui=entiui)
        return

    def _arcno(self, arcid, entiid):
        return arcno(enti=self._model.getbyid(entiid),
                     arcid=arcid)

    def _addrelation(self, relajson, relaui):

        svgrelalines = [SvgRelation(pos1=SvgPos(ls["x"], ls["y"]),
                                    dashed=(ls["linetype"]=="DASHED"),
                                    minzoom=relajson["minzoomlevel"],
                                    maxzoom=relajson["maxzoomlevel"]) for ls in relaui["linesegments"]]
        for idx in range(0, len(svgrelalines) - 1):
            svgrelalines[idx].pos2 = svgrelalines[idx + 1].pos1
        svgrelalines.pop()  # remove last point, we have one line less than we have points

        startline = svgrelalines[0]
        startline.text = relajson["from-to"]["assoc"][self._lang]
        startline.manyend = (relaui["start_connector"] == "M")
        startline.arcno = self._arcno(arcid=relajson["from-to"]["arc"],
                                      entiid=relajson["from-to"]["enti"])

        endline = svgrelalines[len(svgrelalines) - 1]
        endline.switchpos()  # the last entry goes into the reverse direction
        endline.text = relajson["to-from"]["assoc"][self._lang]
        endline.manyend = (relaui["end_connector"] == "M")
        endline.arcno = self._arcno(arcid=relajson["to-from"]["arc"],
                                    entiid=relajson["to-from"]["enti"])

        """ if the first line is too short for a proper text, move the text to the second line
            line too short
            there is a text
            there is an intermediate line before the last one
            the intermediate line is long enough 
        """
        secondline = svgrelalines[1]
        if not startline.longenough() \
                and nvl(startline.text) != "" \
                and len(svgrelalines) > 2 \
                and secondline.longenough():
            # move the text to the next line
            secondline.text = startline.text
            startline.text = None
        # fi

        """ if the last line is too short for proper text
            line too short
            there is a text
            there is a line without before the last one
            the usable line is long enough
        """
        beforelastline = svgrelalines[len(svgrelalines) - 2]
        if not endline.longenough() \
                and nvl(endline.text) != "" \
                and nvl(beforelastline.text) == "" \
                and beforelastline.longenough():
            # move the text to the  line before the last
            beforelastline.text = endline.text
            endline.text = None
            # change the direction
            beforelastline.switchpos()
        # fi

        for ls in svgrelalines:
            self.addcontent(ls)
        return

        # idx = 0
        # lineseg = relaui["linesegments"][idx]
        # pos1 = SvgPos(x=lineseg["x"], y=lineseg["y"])
        # pos2 = SvgPos(x=relaui["linesegments"][idx + 1]["x"],
        #               y=relaui["linesegments"][idx + 1]["y"])
        #
        # svgrela = SvgRelation(pos1=pos1, pos2=pos2,
        #                       dashed=(lineseg["linetype"] == "DASHED"),
        #                       text=None if movetext else relajson["from-to"]["assoc"][self._lang],
        #                       manyend=(relaui["start_connector"] == "M"),
        #                       arcno=self._arcno(arcid=relajson["from-to"]["arc"],
        #                                         entiid=relajson["from-to"]["enti"]))
        # self.addcontent(svgrela)
        # idx = 1
        # lineseg = relaui["linesegments"][idx]
        # pos1 = SvgPos(x=lineseg["x"], y=lineseg["y"])
        # pos2 = SvgPos(x=relaui["linesegments"][idx + 1]["x"],
        #               y=relaui["linesegments"][idx + 1]["y"])
        #
        # svgrela = SvgRelation(pos1=pos1, pos2=pos2,
        #                       dashed=(lineseg["linetype"] == "DASHED"),
        #                       text=None if not movetext else relajson["from-to"]["assoc"][self._lang])
        # self.addcontent(svgrela)
        #
        # idx = len(relaui["linesegments"]) - 2
        # lineseg = relaui["linesegments"][idx]
        # # the last is special, we start from the end
        # pos1 = SvgPos(x=lineseg["x"], y=lineseg["y"])
        # pos2 = SvgPos(x=relaui["linesegments"][idx + 1]["x"],
        #               y=relaui["linesegments"][idx + 1]["y"])
        #
        # movetext = pos1.distance(pos2) < SvgRelation.LINEOFFSET + 4 * SvgRelation.LINEENDOFFSET
        #
        # svgrela = SvgRelation(pos1=pos2, pos2=pos1,
        #                       dashed=lineseg["linetype"] == "DASHED",
        #                       text=None if movetext else relajson["from-to"]["assoc"][self._lang],
        #                       manyend=(relaui["end_connector"] == "M"),
        #                       arcno=self._arcno(arcid=relajson["to-from"]["arc"],
        #                                         entiid=relajson["to-from"]["enti"]))
        # self.addcontent(svgrela)
        #
        # idx = len(relaui["linesegments"]) - 3
        # lineseg = relaui["linesegments"][idx]
        # # the last is special, we start from the end
        # pos1 = SvgPos(x=lineseg["x"], y=lineseg["y"])
        # pos2 = SvgPos(x=relaui["linesegments"][idx + 1]["x"],
        #               y=relaui["linesegments"][idx + 1]["y"])
        #
        # svgrela = SvgRelation(pos1=pos2, pos2=pos1,
        #                       dashed=lineseg["linetype"] == "DASHED",
        #                       text=None if movetext is None else relajson["from-to"]["assoc"][self._lang])
        # self.addcontent(svgrela)
        #
        # for idx2 in range(2, len(relaui["linesegments"]) - 2):
        #     lineseg = relaui["linesegments"][idx2]
        #     pos1 = SvgPos(x=lineseg["x"], y=lineseg["y"])
        #     pos2 = SvgPos(x=relaui["linesegments"][idx2 + 1]["x"],
        #                   y=relaui["linesegments"][idx2 + 1]["y"])
        #     svgrela = SvgRelation(pos1=pos1, pos2=pos2,
        #                           dashed=lineseg["linetype"] == "DASHED")
        #     self.addcontent(svgrela)
        # # for
        #
        # return

    def _addallrelations(self):
        for relaid, relaui in self._diagjson["relationships"].items():
            relajson = self._model.getbyid(relaid)
            self._addrelation(relajson=relajson, relaui=relaui)
        return

    def addallelements(self, model, diagjson, lang):
        setattr(self, "_model", model)
        setattr(self, "_diagjson", diagjson)
        setattr(self, "_lang", lang)
        setattr(self, "_diagentis", [enti["element"] for enti in self._diagjson["elements"]["entity"]])
        setattr(self, "_diagattr", [attr["element"] for attr in self._diagjson["elements"]["attribute"]])
        setattr(self, "_diagrelas", [relaid for relaid in self._diagjson["relationships"].keys()])

        self._addallentities()
        self._addallrelations()
        delattr(self, "_model")
        delattr(self, "_diagjson")
        delattr(self, "_lang")
        delattr(self, "_diagentis")
        delattr(self, "_diagattr")
        delattr(self, "_diagrelas")
        return

    def getsvg(self):
        contsvg = ''
        for c in self.content:
            contsvg += '\n' + c.getsvg(self.diagid)
        # svg = SvgDiagram.SVGFRAME.format(diagid=self.diagid, width=self.maxx(), height=self.maxy(),
        #                                  style=SvgText.csstextstyle(),
        #                                  content=contsvg)
        svg=SvgDiagram.SVGFRAME.format(minzoom=self.minzoomlevel,
                                       maxzoom=self.maxzoomlevel,
                                        content=contsvg)
        return svg


class SvgText:
    FWNORMAL = 'normal'
    FWBOLD = 'bold'
    ANCHORSTART = "start"
    ANCHOREND = "end"
    ANCHORMIDDLE = "middle"
    FONTWEITGHTS = [FWNORMAL, FWBOLD]
    TEXTTYPEDEFAULTS = {"entity": (12, FWBOLD, 2),
                        "subentity": (11, FWBOLD, 2),
                        "attribute": (10, FWNORMAL, 1),
                        "subattribute": (9, FWNORMAL, 1),
                        "relation": (8, FWNORMAL, 3),
                        "metainfo": (9, FWNORMAL, 1),
                        "category": (9, FWNORMAL, 1)
                        }
    TEXTTYPES = list(TEXTTYPEDEFAULTS.keys())

    #FONTFAMILY = "Helvetica"
    FONTFAMILY = "TT Norms Pro"
    #FONTFAMILY = "Arial"
    LINEBREAK = 3


    TEXTSVG = """<a {textref} minzoom="{minzoom}" maxzoom="{maxzoom}"><text class="{textclass}" x="{diagposx}" y="{diagposy}" {rotation}
    text-anchor="{anchor}" >
    {content}
    <title>{descr}</title>
    </text></a>"""

    SPANSVG = """<tspan x="{x}" dy="{dy}">{text}</tspan>"""

    def __init__(self, **kwargs):
        # init
        self._size = None
        self._weight = None
        self._multilinetext = []
        self._maxwidth = None
        self._text = None
        self._texttype = None
        self._anchor = None
        self._pos = None
        # params
        self.anchor = nvl(kwargs.get("anchor"), self.ANCHORSTART)
        self.angle = nvl(kwargs.get("angle"), SvgRotate(0))
        self.text = nvl(kwargs.get("text"), "")
        self.texttype = kwargs.get("texttype")
        self.maxwidth = kwargs.get("maxwidth")
        self.elemid = kwargs.get("elemid")
        self.href = kwargs.get("href")
        self.elemtooltip = kwargs.get("elemtooltip")
        self._pos = SvgPos(nvl(kwargs.get("x"), 0), nvl(kwargs.get("y"), 0))
        self.minzoom=nvl(kwargs.get("minzoom"),0)
        self.maxzoom=nvl(kwargs.get("maxzoom"),4)
        return

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, value):
        assert value in (self.ANCHOREND, self.ANCHORSTART, self.ANCHORMIDDLE)
        self._anchor = value
        return

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value if type(value) != str else value.strip()
        self._calcshowname()
        return

    @property
    def x(self):
        return self._pos.x

    @x.setter
    def x(self, value):
        self._pos.x = value
        return

    @property
    def y(self):
        return self._pos.y

    @y.setter
    def y(self, value):
        self._pos.y = value
        return

    @property
    def texttype(self):
        return self._texttype

    @texttype.setter
    def texttype(self, value):
        self._texttype = value
        if value in self.TEXTTYPES:
            self.size, self.weight, self._maxlines = self.TEXTTYPEDEFAULTS[value]
        else:
            self.size, self.weight, self._maxlines = 9, self.FWNORMAL, 1
        self._calcshowname()
        return

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value is not None:
            self._size = value
        self._calcshowname()
        return

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        assert value is None or value in self.FONTWEITGHTS
        if value is not None:
            self._weight = value
        self._calcshowname()
        return

    @property
    def maxwidth(self):
        return self._maxwidth

    @maxwidth.setter
    def maxwidth(self, value):
        assert value is None or (type(value) in (int, float) and value >= 0)
        self._maxwidth = value
        self._calcshowname()
        return

    @classmethod
    def csstextelements(cls):
        retval = ''
        for txttype in cls.TEXTTYPES:
            retval += """text.{texttype} {{
                font-size: {fontsize}px;
                font-weight: {fontweight};
            }}""".format(texttype=txttype,
                         fontsize=cls.TEXTTYPEDEFAULTS[txttype][0],
                         fontweight=cls.TEXTTYPEDEFAULTS[txttype][1]
                         )
        return retval

    @classmethod
    def csstextstyle(cls):
        retval = """<style>
            text{{
                font-family: "{fontfamily}",Helvetica, Arial
            }}
            {elements}
        </style >""".format(fontfamily=cls.FONTFAMILY,elements=cls.csstextelements())
        return retval

    def textwidth(self, text):
        return textwidth(family=self.FONTFAMILY, size=self.size,
                         weight=self.weight, text=text)

    def realwidth(self):
        """real width used up by text: longest multiline or if not present, width of originial"""
        if len(self._multilinetext) == 0:
            retval = self.textwidth(self.text)
        else:
            retval = max(self.textwidth(l) for l in self._multilinetext)
        return retval

    def lineheight(self):
        return textheight(family=self.FONTFAMILY, size=self.size,
                          weight=self.weight, text="y")

    def lineanz(self):
        return len(self._multilinetext)

    def realheight(self):
        rh = self.lineanz() * self.lineheight()
        return rh

    def maxx(self, direction="east"):
        if direction in ("north", "south"):
            dx = self.realwidth() / 2  # vertical line has centered text
        else:
            dx = self.realwidth()
        return self.x + max(5,dx)

    def maxy(self, direction="east"):
        if direction in ("north", "south"):
            dy = self.realheight()
        else:
            dy = self.realheight() / 2  # horizontal lines have centered text
        return self.y + max(5,dy)

    def _shortenstring(self, text, withdots=True):
        if len(text) == 0:
            return '', ''

        contdots = ".." if withdots else ""
        shorttext, reststring = text, ""
        idx = 0
        while len(shorttext) > 4 and self.textwidth(shorttext) > self.maxwidth:
            removechars = 1 + (len(contdots) if shorttext.endswith(contdots) else 0)
            shorttext = shorttext[:-removechars] + contdots
            idx += 1
            reststring = text[-idx:]
        #print(f"'{text}' shortened to '{shorttext}' remaining '{reststring}'")
        return shorttext, reststring

    def _calcshowname(self):
        """ reduce the text to the maxwidth, if possible break it more  new lines
            maxwidth=100
            92 	 Dies ist   ein.Text mit-Umbruch

            maxwith=90
            89 	 Dies ist   ein.Text mit-Umbruc
            4 	 h
         => if there is space on the remaining lines, try to go back to non-character
            ?? 	 Dies ist   ein.Text mit-
            ?? 	 Umbruch


        """
        if self.text is None or self.size is None or self.texttype is None:
            return
        """find max string for available space"""
        # no width-limit given or current textwidth is below the given limit
        # -> we have one line of text
        if self.maxwidth is None or self.textwidth(self.text) <= self.maxwidth:
            self._multilinetext = [self.text]
        else:
            if self._maxlines == 1:
                """create shortened text in exactly one line"""
                shorttext, dummy = self._shortenstring(self.text)
                self._multilinetext = [shorttext]
            else:
                # we have room for several lines

                self._multilinetext = []
                remaininglines = self._maxlines - 1
                shorttext = self.text
                for idx in range(1, self._maxlines + 1):
                    shorttext, reststring = self._shortenstring(shorttext,
                                                                withdots=(idx == self._maxlines))
                    if shorttext == "":
                        break
                    """while text is  at least 3 letters
                            and last character is digit or alpha
                            and reststring contains characters
                            and reststring + one more character fits in combined 
                                    width of resting line
                        move one character to reststring 
                    """
                    savest, savers = shorttext, reststring
                    while (len(shorttext) > 3) \
                            and (shorttext[-1].isdigit() \
                                 or shorttext[-1].isalpha()) \
                            and (len(reststring) > 0) \
                            and (self.textwidth(shorttext[-1] + reststring) \
                                 <= remaininglines * self._maxwidth \
                            ):
                        reststring = shorttext[-1] + reststring
                        shorttext = shorttext[:-1]
                    # while
                    """ if last character is still digit or alpha, there was no break-character
                        return to original break
                    """
                    if (shorttext[-1].isdigit() or shorttext[-1].isalpha()):
                        shorttext, reststring = savest, savers

                    shorttext = shorttext.strip()  # get rid of trailing whitespace
                    # now capture the maximum width of the multilinetext
                    self._multilinetext.append(shorttext)
                    remaininglines -= 1
                    shorttext = reststring.strip()
                # for
        return

    def get1svg(self, text, idx=0):
        svg = self.SPANSVG.format(x=self.x,
                                  dy=(idx if idx == 0 else 1) * (self.lineheight()),
                                  text=html.escape(nvl(text)))
        return svg

    def getsvg(self, diagid=None):
        content = '\n'.join(self.get1svg(l, idx)
                            for idx, l in enumerate(self._multilinetext))

        svg = self.TEXTSVG.format(textref=href(diagid=diagid, elemid=self.elemid, subelemid="NAME",href=self.href),
                                  descr=html.escape(nvl(self.elemtooltip)),
                                  content=content,
                                  diagposx=self.x, diagposy=self.y,
                                  rotation=self.angle.rotate(),
                                  textclass=self.texttype,
                                  anchor=self.anchor,
                                  minzoom=self.minzoom,maxzoom=self.maxzoom)
        return svg


class SvgRelation:
    LINEOFFSET = 13
    LINEENDOFFSET = 5
    SPACELEN = 2
    MAXTEXTWIDTH = 30

    RELATIONSVG = """<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" 
                stroke="black" stroke-width=".7" stroke-dasharray="{dashlen}"/>"""

    ARCRADIUS = 2.2
    ARCDIFF = .6
    ARCSVG = """<circle stroke="black" stroke-width=".3" fill="none" cx="{x}" cy="{y}" r="{r}" />"""

    CFDX = 7
    CFDY = 3.5
    CROWFOOT = """<path {rotate} d="M {x} {y} """ \
               + """l {dx1} {dy1} l {dx2} {dy2}" """.format(dx1=1 * CFDX, dy1=CFDY,
                                                            dx2=-1 * CFDX, dy2=CFDY) \
               + """fill="transparent" stroke="black" stroke-width=".7"/>"""

    DIRECTION = {"east": {"start": [1, 0, 0, 0], "finish": [0, 1, 0, 0],
                          "arcpos": [1, 0], "crowfoot": [1, 0]},
                 "west": {"start": [1, 0, 0, 0], "finish": [-1, 0, 0, 0],
                          "arcpos": [-1, 0], "crowfoot": [1, 180]},
                 "south": {"start": [0, 0, 1, 0], "finish": [0, 0, 0, 1],
                           "arcpos": [0, 1], "crowfoot": [1, 90]},
                 "north": {"start": [0, 0, 0, 1], "finish": [0, 0, -1, 0],
                           "arcpos": [0, -1], "crowfoot": [1, -90]}}

    def __init__(self, pos1: SvgPos, pos2: SvgPos = None,
                 dashed=False, text=None,
                 manyend=False, arcno=None, elemtooltip=None,
                 minzoom=0,maxzoom=4):
        self.pos1 = pos1
        self.pos2 = pos2
        # assert self.pos1.x <= self.pos2.x and self.pos1.y <= self.pos2.y
        self.dashed = dashed
        self.manyend = manyend
        self.arcno = arcno
        self.elemtooltip = elemtooltip
        self.text = text
        self.minzoom = minzoom
        self.maxzoom = maxzoom

        return

    def maxx(self):
        # if there is a text take its endposition
        maxx = 5 if self.text is None else self.text.maxx(direction=self._direction())

        return max(self.pos1.x, self.pos2.x)+ maxx

    def maxy(self):
        # if there is a text take its endposition
        maxy = 0 if self.text is None else self.text.maxy(direction=self._direction())
        return max(self.pos1.y, self.pos2.y, maxy)

    def _direction(self):
        return self.pos1.maindirection(self.pos2)

    def switchpos(self):
        self.pos1, self.pos2 = self.pos2, self.pos1
        return

    def horizontal(self):
        return self._direction() in ("west", "east")

    _mapfields = {"x1": 0, "x2": 1, "y1": 2, "y2": 3}

    def _directionLO(self, field):
        return self.DIRECTION[self._direction()]["finish"][self._mapfields[field]] * self.LINEOFFSET

    def _linelen(self):
        return (self.pos2.x - self.pos1.x) if self.horizontal() \
            else (self.pos2.y - self.pos1.y)

    def _directionCH(self, field):
        factor = self.DIRECTION[self._direction()]["start"][self._mapfields[field]]
        retval = factor * self._linelen()
        return retval

    def _arcpos(self):
        offset = self.LINEOFFSET * 3 / 4
        x, y = self.DIRECTION[self._direction()]["arcpos"]
        return offset * x, offset * y

    def _crowfoot(self):
        x, r = self.DIRECTION[self._direction()]["crowfoot"]
        return (self.CFDX / 2) * x, SvgRotate(r)

    def longenough(self):
        retval = self.pos1.distance(self.pos2) > self.LINEOFFSET + 3 * self.LINEENDOFFSET
        return retval

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if value in (None, ""):
            self._text = None
        elif type(value) == SvgText:
            self._text = value
        else:
            self._text = SvgText(text=value,
                                 texttype="relation",
                                 anchor=SvgText.ANCHORSTART,
                                 elemtooltip=nvl(self.elemtooltip)
                                 )
        return

    def dashlen(self):
        return 3 if self.dashed else 0

    def getsvg(self, diagid=None):
        arcx, arcy = self._arcpos()
        cfstart, cfangle = self._crowfoot()

        if self.text is None:
            content = self.RELATIONSVG.format(x1=0, y1=0,
                                              x2=self.pos2.x - self.pos1.x, y2=self.pos2.y - self.pos1.y,
                                              dashlen=self.dashlen())
        else:
            chevron = SvgText(text=">", texttype="relation")
            if self.horizontal():
                self.text.maxwidth = max(self.LINEOFFSET,
                                         (self.pos1.distance(self.pos2)
                                          - self.LINEOFFSET
                                          - self.LINEENDOFFSET
                                          - chevron.realwidth()
                                          - 2 * self.SPACELEN))
            else:
                self.text.maxwidth = self.MAXTEXTWIDTH

            lineheight = self.text.lineheight()
            realheight = self.text.realheight()

            """
               --part1--  text > --part2----------    (east)
               --part1-------- < text --part2--    (west)
            y positions are constant (swapped with x-positions in case of vertical
            """
            corrmiddle = -2.8
            corrmltext = -lineheight / 2 * (self.text.lineanz() - 1)

            # line from entity to text
            part2x1 = self._directionLO("x1")
            part2x2 = self._directionLO("x2")
            part2y1 = self._directionLO("y1")
            part2y2 = self._directionLO("y2")

            # line from chevron to end
            part1x1 = self._directionCH("x1")
            part1x2 = self._directionCH("x2")
            part1y1 = self._directionCH("y1")
            part1y2 = self._directionCH("y2")

            if self._direction() == "east":
                # add text
                textx = self.LINEOFFSET + self.SPACELEN
                texty = (lineheight / 2) + corrmiddle + corrmltext
                chevron.x = textx + self.text.realwidth() *1.05 + self.SPACELEN
                chevron.y = (chevron.lineheight() / 2) + corrmiddle

                # end with line after text to end
                part1x2 = min(chevron.x + chevron.realwidth() +self.SPACELEN, self._linelen() - self.LINEENDOFFSET)

            elif self._direction() == "west":
                # add  text
                textx = part2x1 - self.text.realwidth() - self.SPACELEN
                texty = (lineheight / 2) + corrmiddle + corrmltext
                chevron.x = textx - chevron.realwidth() - self.SPACELEN
                chevron.y = (chevron.lineheight() / 2) + corrmiddle - 1.0
                chevron.angle = SvgRotate(180, chevron.x + 1, chevron.y - 1.4)

                # end with line after chevron
                part1x2 = chevron.x - self.SPACELEN -2

                cfstart, cfangle = -(self.CFDX / 2), SvgRotate(180, -(self.CFDX / 2), 0)
            elif self._direction() == "south":
                # add  text
                textx = -self._text.realwidth() / 2
                texty = part2y2 + 4 * self.SPACELEN
                chevron.x = -chevron.realwidth() / 2 - 3.9
                chevron.y = texty + realheight
                chevron.angle = SvgRotate(90, chevron.x + chevron.lineheight() / 2, chevron.y)

                # end with line after chevron
                part1y2 = chevron.y + self.SPACELEN

            elif self._direction() == "north":
                # add  text
                textx = -self._text.realwidth() / 2
                # texty = part2y1 - 4 * self.SPACELEN
                texty = part2y1 - self.text.realheight() - corrmltext - self.SPACELEN
                chevron.x = -chevron.realwidth() / 2 + 0.5
                chevron.y = texty - 6 * self.SPACELEN
                chevron.angle = SvgRotate(-90, chevron.x + chevron.lineheight() / 2, chevron.y)

                part1y1 = chevron.y - self.SPACELEN

                cfstart, cfangle = - (self.CFDX / 2), SvgRotate(-90, -self.CFDX / 2, -self.CFDY)

            # fi
            if self.pos1.x !=self.pos2.x and self.pos1.y!=self.pos2.y:
                # line is not vertical or horizontal shift ends of relation
                #print ("===============")
                #print (f"part 1 {part1x1}:{part1y1} - {part1x2}:{part1y2}")
                #print (f"part 2 {part2x1}:{part2y1} - {part2x2}:{part2y2}")
                #print (f"{self.pos1.x}:{self.pos1.y} - {self.pos2.x}:{self.pos2.y}")
                if self._direction() == "east":
                    #y wird geschoben für schräg
                    part1y1 = self.pos2.y -self.pos1.y
                elif self._direction() == "west":
                    part1y1 = self.pos2.y - self.pos1.y
                elif self._direction() == "south":
                    part1x1 = self.pos2.x -self.pos1.x
                elif self._direction() =="north":
                    part1x2 = self.pos2.x -self.pos1.x

            content = self.RELATIONSVG.format(x1=part1x1, y1=part1y1, x2=part1x2, y2=part1y2,
                                              dashlen=self.dashlen())

            self.text.x, self.text.y = textx, texty
            content += "\n" + self.text.getsvg(diagid)
            content += "\n" + chevron.getsvg()
            content += "\n" + self.RELATIONSVG.format(x1=part2x1, y1=part2y1, x2=part2x2, y2=part2y2,
                                                      dashlen=self.dashlen())
        # fi
        if self.manyend:
            crowfoot = self.CROWFOOT.format(rotate=cfangle.rotate(),
                                            x=cfstart - (self.CFDX / 2),
                                            y=-1 * self.CFDY
                                            )
            content += crowfoot
        # fi
        if self.arcno is not None:
            for i in range(self.arcno):
                content += "\n" + self.ARCSVG.format(x=arcx, y=arcy,
                                                     r=max(0, self.ARCRADIUS - (i * self.ARCDIFF)))

        svgline = SvgEntity.GROUPSVG.format(diagposx=self.pos1.x, diagposy=self.pos1.y,
                                        minzoom=self.minzoom, maxzoom=self.maxzoom,
                                       content=content)
        return svgline


class SvgAttribute:
    MAXATTRS = 5
    OVERFLOW = "... +{attrcnt}"

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.tooltip = nvl(kwargs.get("tooltip"), "")
        self.maxwidth = nvl(kwargs.get("maxwidth"))
        self.attrtype = kwargs.get("attrtype")
        self.elemid = kwargs.get("elemid")
        self.minzoom = kwargs.get("minzoom")
        self.maxzoom = kwargs.get("maxzoom")
        return


class SvgEntity:
    GROUPSVG = """<g transform="translate({diagposx},{diagposy})" minzoom="{minzoom}" maxzoom="{maxzoom}">
            {content}
        </g>"""
    ENTISVG = """<a {href} >
            <rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}"
            fill="#{color}" fill-opacity="{opacity}" />
            <title>{descr}</title>
            </a>"""

    TEXTBORDER = 9
    TEXTBREAK = 3

    def __init__(self, **kwargs):
        self.width = kwargs.get("width")
        self.height = kwargs.get("height")
        self.minzoom = nvl(kwargs.get("minzoom"),0)
        self.maxzoom = nvl(kwargs.get("maxzoom"),4)

        self._entipos = SvgPos(nvl(kwargs.get("x", 0)),
                               nvl(kwargs.get("y"), 0))
        self.fatherentity = kwargs.get("fatherentity")
        self.color = nvl(kwargs.get("color"), '000000')
        self.opacity = nvl(kwargs.get("opacity"), 0.2)
        self.radius = nvl(kwargs.get("radius"), 4)
        self.elemid = kwargs.get("elemid")
        self.elemtooltip = kwargs.get("elemtooltip")
        self.namesvg: SvgText = SvgText(text=nvl(kwargs.get("name"), ""),
                                        texttype='subentity' if self.issubentity else 'entity',
                                        maxwidth=self.width - (2 * self.TEXTBORDER),
                                        elemid=self.elemid,
                                        elemtooltip=self.elemtooltip)

        self.attributes = []
        self._subentities = []
        if self.fatherentity is not None:
            self.fatherentity.addsubentity(self)
        return

    def maxx(self):
        return self._entipos.x + self.width

    def maxy(self):
        return self._entipos.y + self.height

    @property
    def issubentity(self):
        return self.fatherentity is not None

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        assert value is not None
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        assert value is not None
        self._height = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        self._opacity = value

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @property
    def namesvg(self):
        return self._namesvg

    @namesvg.setter
    def namesvg(self, value):
        self._namesvg = value

    @property
    def name(self):
        return self._namesvg.text

    @name.setter
    def name(self, value):
        self._namesvg.text = value

    @property
    def x(self):
        return self._entipos.x

    @x.setter
    def x(self, value):
        self._entipos.x = value

    @property
    def y(self):
        return self._entipos.y

    @y.setter
    def y(self, value):
        self._entipos.y = value

    def addattribute(self, *attribute):
        self.attributes.extend(attribute)

    def addsubentity(self, *subentity):
        self._subentities.extend(subentity)

    def setnamepos(self, showname: SvgText):
        """ position the name of the entity
            centralized if there are no attributes or subentities
            top if there are"""

        if len(self.attributes) == 0 and len(self._subentities) == 0:
            # center position for Name but minimal border distance
            startx = max(self.TEXTBORDER,
                         (self.width - showname.realwidth()) / 2)
            showname.x = startx
            starty = max(self.TEXTBORDER + showname.lineheight(),
                         ((self.height - showname.realheight()) / 2) + showname.lineheight())
            showname.y = starty
        else:
            # top position for Name
            showname.x = self.TEXTBORDER
            showname.y = self.TEXTBORDER + showname.lineheight()
        return

    def getsvg(self, diagid=None):
        """get first the main entity, it has no offset in the group, it is the group"""
        myself = self.ENTISVG.format(x=0, y=0,
                                     width=self.width, height=self.height,
                                     radius=self.radius, color=self.color,
                                     opacity=str(self.opacity),
                                     href=href(diagid, self.elemid),
                                     descr=html.escape(nvl(self.elemtooltip))
                                     )
        self.setnamepos(self.namesvg)
        # add myself + my name + all the other content to the group
        groupcontent = myself + self.namesvg.getsvg(diagid)
        endoflasttexty = self.TEXTBORDER + self.namesvg.realheight()
        for attr in self.attributes:
            svgtext = SvgText(text=attr.name,
                              texttype='subattribute' if self.issubentity else 'attribute',
                              maxwidth=self.width - (2 * self.TEXTBORDER),
                              x=self.TEXTBORDER, elemid=attr.elemid,
                              elemtooltip=attr.tooltip,
                              minzoom=attr.minzoom,maxzoom=attr.maxzoom)
            endoflasttexty += self.TEXTBREAK + svgtext.realheight()
            svgtext.y = endoflasttexty
            groupcontent += "\n" + svgtext.getsvg(diagid)
        # for
        for subent in self._subentities:
            groupcontent += subent.getsvg(diagid)

        svg = self.GROUPSVG.format(content=groupcontent,
                                   diagposx=self.x, diagposy=self.y,
                                   minzoom=self.minzoom, maxzoom=self.maxzoom)
        return svg


class SvgCategory:
    CATWIDTH: int = 90
    CATHEIGHT: int = 30
    TEXTWIDTH: int = CATWIDTH - 10

    CATEGORYGROUP = """<g transform="translate({x},{y})" >
                    {content}
                    </g>
                """
    CATSVG = """<rect x="{x}" y="{y}" width="{width}" height="{height}" 
            fill="#{color}" fill-opacity="{opacity}" />"""

    def __init__(self, catname, catcolor, **kwargs):
        self._x = nvl(kwargs.get("x"))
        self._y = nvl(kwargs.get("y"))
        self._catname = catname
        self._catcolor = catcolor
        return

    def maxx(self):
        maxx = self._x + self.CATWIDTH
        return maxx

    def maxy(self):
        maxy = self._y + self.CATHEIGHT
        return maxy

    def setnamepos(self, showname: SvgText):
        """ position the name of the entity centralized """

        # center position for Name but minimal border distance
        startx = max(5,
                     (self.CATWIDTH - showname.realwidth()) / 2)
        showname.x = startx
        starty = max(3 + showname.lineheight(),
                     ((self.CATHEIGHT - showname.realheight()) / 2) + showname.lineheight())
        showname.y = starty
        return

    def getsvg(self, diagid=None):
        content = self.CATSVG.format(x=0, y=0,
                                     width=self.CATWIDTH, height=self.CATHEIGHT,
                                     color=self._catcolor, opacity="0.2"
                                     )
        cattext = SvgText(text=self._catname,
                          x=5, y=5,
                          texttype='category',
                          maxwidth=self.TEXTWIDTH)
        self.setnamepos(cattext)
        content += cattext.getsvg()
        retval = self.CATEGORYGROUP.format(x=self._x, y=self._y, content=content)

        return retval


class SvgMetaInfo:
    PROMPTWIDTH: int = 50
    PROMPTHEIGHT: int = 13
    TEXTWIDTH: int = 160

    METAINFOGROUP = """<g  transform="translate({x},{y})" >
                    {content}
                    </g>
                """

    def __init__(self, **kwargs):
        self._modelname = nvl(kwargs.get("modelname"))
        self._name = nvl(kwargs.get("diagname"))
        self._id = kwargs.get("diagid")
        self._um = nvl(kwargs.get("um"))
        self._dm = nvl(kwargs.get("dm"))
        self._x = nvl(kwargs.get("x"))
        self._y = nvl(kwargs.get("y"))

        self._content = []
        self._addcontent()
        return

    def _addcontent(self):
        x, y = 0, 0
        self._content.append(SvgText(text="Model: ",
                                     x=x, y=y,
                                     maxwidth=self.PROMPTWIDTH - 5,
                                     texttype="metainfo"
                                     )
                             )
        self._content.append(SvgText(text=nvl(self._modelname),
                                     x=x + self.PROMPTWIDTH, y=y,
                                     maxwidth=self.TEXTWIDTH,
                                     texttype="metainfo"
                                     )
                             )
        y = y + self.PROMPTHEIGHT
        self._content.append(SvgText(text="Diagram: ",
                                     x=x, y=y,
                                     maxwidth=self.PROMPTWIDTH - 5,
                                     texttype="metainfo"
                                     )
                             )
        self._content.append(SvgText(text=nvl(self._name),
                                     x=x + self.PROMPTWIDTH, y=y,
                                     maxwidth=self.TEXTWIDTH,
                                     texttype="metainfo"
                                     )
                             )
        y = y + self.PROMPTHEIGHT
        self._content.append(SvgText(text="Modified: ",
                                     x=x, y=y,
                                     maxwidth=self.PROMPTWIDTH - 5,
                                     texttype="metainfo"
                                     )
                             )
        self._content.append(SvgText(text=nvl(self._um) + ',',
                                     x=x + self.PROMPTWIDTH, y=y,
                                     maxwidth=30,
                                     texttype="metainfo"
                                     )
                             )
        self._content.append(SvgText(text=nvl(self._dm),
                                     x=x + self.PROMPTWIDTH + 35, y=y,
                                     maxwidth=self.TEXTWIDTH - 30,
                                     texttype="metainfo"
                                     )
                             )
        return

    def maxx(self):
        maxx = max(nvl(c.maxx(), 0) for c in self._content)
        return self._x + maxx

    def maxy(self):
        maxy = max(nvl(c.maxy(), 0) for c in self._content)
        return self._y + maxy

    def getsvg(self, diagid=None):
        content = "\n".join(c.getsvg() for c in self._content)
        svg = self.METAINFOGROUP.format(x=self._x, y=self._y, content=content)
        return svg


class SvgLegend:
    LEGENDWIDTH = 320

    LEGENDGROUP = """<g transform="translate({x},{y})" >
                    {content}
                    </g>
                """

    def __init__(self, startx, starty):
        self._x = startx
        self._y = starty
        self.addcontent()
        return

    def addcontent(self):
        LEGENTIWIDTH = 85
        LEGENTIHEIGHT = 50
        self._content = []
        self._content.append(SvgText(text="Informationmodel Syntax",
                                     texttype='metainfo', maxwidth=150,
                                     href="http://www.information-modelling.com",
                                     x=0, y=0
                                     )
                             )
        entity = SvgEntity(name="Entity-1",
                           width=LEGENTIWIDTH, height=LEGENTIHEIGHT,
                           x=0, y=10,
                           elemtooltip="Thing of interest in the current environment"
                           )

        entity.addattribute(SvgAttribute(name="Attribute", tooltip="Property of this entity, containing one value"))
        self._content.append(entity)

        self._content.append(SvgEntity(name="Entity-2",
                                       width=LEGENTIWIDTH, height=LEGENTIHEIGHT,
                                       x=self.LEGENDWIDTH - LEGENTIWIDTH, y=10,
                                       elemtooltip="Another thing of interest in the current environment"
                                       )
                             )
        midwayx = LEGENTIWIDTH + (self.LEGENDWIDTH - (2 * LEGENTIWIDTH)) / 2
        midwayy = LEGENTIHEIGHT / 2 + 10
        self._content.append(SvgRelation(pos1=SvgPos(x=LEGENTIWIDTH, y=midwayy),
                                         pos2=SvgPos(x=midwayx, y=midwayy),
                                         text="relation verb",
                                         arcno=1, manyend=True,
                                         elemtooltip="\n".join([
                                             "Relation verb mandatorily (solid line) connecting an instance of Entity-1 with 1 instance " +
                                             "(ending in single line) of Entity-2",
                                             "",
                                             "Several relations comming off an entity which are marked with the same type of circle are exclusive." +
                                             "Meaning, only one of them can be set at any given time."])
                                         )
                             )
        self._content.append(SvgRelation(pos1=SvgPos(x=self.LEGENDWIDTH - LEGENTIWIDTH, y=midwayy),
                                         pos2=SvgPos(x=midwayx, y=midwayy),
                                         text="relation verb2",
                                         dashed=True,
                                         elemtooltip="Relation verb2 optionally (dashed line) connecting an instance of Entity-2 with " +
                                                     "1 or many instances (ending in crowfoot) of Entity-1"
                                         )
                             )

        return

    def maxx(self):
        maxx = max(nvl(c.maxx(), 0) for c in self._content)
        return self._x + maxx

    def maxy(self):
        maxy = max(nvl(c.maxy(), 0) for c in self._content)
        return self._y + maxy

    def getsvg(self, diagid=None):
        content = "\n".join(c.getsvg() for c in self._content)
        svg = self.LEGENDGROUP.format(x=self._x, y=self._y, content=content)
        return svg


def addcategories(model: JSModel, diag, diagjson, startx, starty):
    MAXCATGPERLINE = 4
    """ insert a colored rectangle for every used categroy in the diagram
    """
    diagentis = [enti["element"] for enti in diagjson["elements"]["entity"]]
    allcatgs = model.jsmodel["categories"]
    cntcatgs = {k: 0 for k in allcatgs.keys()}
    for e in diagentis:
        try:
            cntcatgs[model.getbyid(e)["category"]] += 1
        except:
            None #protect from tangling entities
    mycatgs = sorted([[k, c] for k, c in cntcatgs.items() if c > 0], key=lambda x: x[1], reverse=True)
    nextx, nexty, cnt, maxxend = startx, starty, 0, 0
    for c in mycatgs:
        catg = model.getbyid(c[0])

        diag.addcontent(SvgCategory(catname=catg["name"], catcolor=catg["ui"].get("color"),
                                    x=nextx, y=nexty))
        nextx += SvgCategory.CATWIDTH + 5
        maxxend = max(maxxend, nextx)
        cnt += 1
        if cnt == MAXCATGPERLINE:
            cnt = 0
            nextx = startx
            nexty += SvgCategory.CATHEIGHT + 3
        # if
    # for

    return maxxend

def diagramblock(model: JSModel, diagid, minzoomlevel,maxzoomlevel,lang):
    diagjson = model.getbyid(diagid)
    diag = SvgDiagram(width=diagjson["width"], height=diagjson["height"],
                      diagid=diagid, title=diagjson["name"],
                      minzoomlevel=minzoomlevel,maxzoomlevel=maxzoomlevel)

    diag.addallelements(model, diagjson=diagjson, lang=lang)

    footerx = 25
    footery = diag.maxy() + 35
    metainfo = SvgMetaInfo(diagname=diagjson['name'], diagid=diagid, lang=lang,
                           modelname=model.modelname(),
                           um=nvl(diagjson['um'], diagjson['uc']),
                           dm=nvl(diagjson['dm'], diagjson['dc']),
                           x=footerx, y=footery
                           )
    diag.addcontent(metainfo)

    maxcatgx = addcategories(model=model, diag=diag, diagjson=diagjson,
                             startx=footerx + metainfo.maxx(),
                             starty=footery)

    diag.addcontent(SvgLegend(startx=max(diag.maxx() - SvgLegend.LEGENDWIDTH, maxcatgx),
                              starty=footery))

    return diag.getsvg()

def zoomleveldiagrams(diagid):
    zdiags = [(0,4)]
    # TODO andere zoomlevels füllen
    zdiags.sort(key=lambda d:d[0])
    return zdiags

def renderdiagram(model: JSModel, diagid, lang):
    SVGELEMENT = """<svg id="{diagid}-SVG" width="{width}" height="{height}" 
            viewBox="0 0 {width} {height}" 
            xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
            version="1.1"> 
            {style}
            <defs id="dmw_defs" >
            </defs>
            {diagrams}
        </svg>"""

    diagjson = model.getbyid(diagid)
    """ generate  blocks for every diagram-Level found """
    diagrams = "\n".join(diagramblock(model=model,diagid=diagid,
                               minzoomlevel=zdiag[0],maxzoomlevel=zdiag[1],
                                lang=lang)
                         for zdiag in zoomleveldiagrams(diagid=diagid)
                         )

    return SVGELEMENT.format(diagid=diagid,
                             width=diagjson["width"], height=diagjson["height"],
                             style=SvgText.csstextstyle(),
                             diagrams=diagrams)
