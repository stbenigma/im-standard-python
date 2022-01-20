import re
import shutil
import unittest

import pytest
from lxml import etree
from pathlib import Path

from SSOT_db.IM_JSON import JSModel
from test_xmiexport import IntegrationTestXMIExport
from IM_EA.export.xmiexport import XMIBuilder

from matplotlib.patches import Rectangle

"""

## Simple A-B

Entity A
<element geometry="Left=267;Top=81;Right=357;Bottom=151;" 
    subject="EAID_4EBF0A9D_DCDE_4622_B277_3C3FDC69A7FB" seqno="1" style="DUID=C1CA053B;LWth=0;"/>

Entity B				
<element geometry="Left=82;Top=80;Right=132;Bottom=150;" 
    subject="EAID_F0CF828F_A332_402c_BE09_BFE6FF101B96" seqno="2" style="DUID=9F3C7BA4;HideIcon=0;LWth=2;"/>

Straight line horizontal without waypoints and no labels.
<element geometry="SX=0;SY=0;EX=0;EY=0;EDGE=2;
        $LLB=;
        LLT=;
        LMT=CX=18:CY=14:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;  <- middle label
        LMB=;LRT=;LRB=;IRHS=;ILHS=;
        Path=;" <== No waypoints
    subject="EAID_91DB8A70_5245_46b0_B025_192A288FD2F5" 
    style="Mode=3;
    EOID=C1CA053B;
    SOID=9F3C7BA4;
    Color=-1;LWidth=0;Hidden=0;"/>

## Label
Visual: ./Images/Label.png
Only one label on target (D) which is rotated clockwise

LLB= Label Source Bottom (invisible on IM diagrams)
LLT= Label Source Top -> '+source label' not visible on diagram

LMT = Label Middle Top
LMB = Label Mittle Bottom

LRT= Label Target Top -> '+target label'
LRB= Label Target Bottom (invisible on IM diagrams)


<element geometry="SX=45;SY=29;EX=41;EY=35;
                   SX=45;SY=29 -> source connector position relative to source element (0,0 = default¹)
                               EX=41;EY=35 -> target connector position relative to target element
        EDGE=2; <= 2 = Manual, 3 = Autorouting
        $LLB=CX=122:CY=13:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        LLT=CX=153:CY=14:OX=-8:OY=-22:HDN=1:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0; <- hidden label
        LMT=CX=27:CY=14:OX=15:OY=-28:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        LMB=;
        LRT=CX=61:CY=14:OX=105:OY=10:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=1;
            CX=61 -> label box width
                  CY=14 -> label box height
                        OX=105 -> offset x + 105
                               OY=10 -> offset y + 10
                                     HDN=0 -> Not hidden = Visible
                                                                    ALN=1 -> alignment = Center
                                                                                ROT=1 -> +90° clockwise
        LRB=CX=122:CY=13:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        IRHS=;
        ILHS=;
        Path=231:-165$162:-213$198:-213$;" <== Negative y amount = down
             waypoint 1
                      waypoint 2 (level with WP3)
                               waypoint 3 (level with WP2)
             Waypoints y coordinates * -1 !!!
                               
     subject="EAID_182C295F_C77E_4e60_8565_F3500701C816" 
     style="Mode=3;EOID=952B160A;SOID=BB1AA2D7;Color=-1;LWidth=0;Hidden=0;"/>
            Mode=3 -> 3=custom line, 2=auto, 1=direct line
        
default¹: Connector default position is on the crossing of the line segement 
    to the center of the element with it's bounding box.

Information Modeling Layout:
    <element geometry="SX=0;SY=0;EX=0;EY=0;EDGE=2;
        SCTR=1;SCME=1;SCTR.LEFT=981;SCTR.TOP=-364;SCTR.RIGHT=1012;SCTR.BOTTOM=-349;
        $
        LLB=CX=0:CY=0:OX=0:OY=0:HDN=1:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        LLT=CX=61:CY=27:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        LMT=CX=0:CY=16:OX=0:OY=0:HDN=1:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        LMB=;LRT=CX=56:CY=14:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        LRB=CX=0:CY=0:OX=0:OY=0:HDN=1:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;IRHS=;ILHS=;
        Path=982:-364$1012:-364$1012:-349$982:-349$;" 
    subject="EAID_RELA23933_BC2E_4B90_B227_80E2FE595B32" 
    style="Mode=3;EOID=11FB1052;SOID=11FB1052;Color=-1;LWidth=0;Hidden=0;"/>

"""


class EnhanceXMILine(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = tmp_path

    def test_create_more_waypoints(self):
        src = Path(__file__).parent / 'lines.xmi'
        xmi = etree.parse(str(src))
        element_root = xmi.xpath("//diagram[properties[@name='Label']]")
        self.assertEqual(1, len(element_root))
        lines = element_root[0].xpath("./elements/element[contains(@geometry, 'Path=')]")
        self.assertEqual(1, len(lines))
        connector = lines[0]
        geometry = connector.get('geometry')
        print(f"Geometry='{geometry}'")
        new_geo = geometry.replace('Path=231:-165$162:-213$198:-213$;', 'Path=231:-165$;').replace('ROT=1', 'ROT=0')
        connector.set('geometry', new_geo)

        # persist source and result
        shutil.copy(str(src), self.temp_folder / 'lines.xmi')
        out = self.temp_folder / 'lines-result.xmi'
        xmi.write(str(out), pretty_print=True)
        print(f"Wrote xmi to {out.resolve()}")


class LineCoding(unittest.TestCase):

    def test_extract_waypoints(self):
        pattern = re.compile(r"Path=([^;]+);")
        match = pattern.search(".. ILHS=;Path=234:-112$;\" subject ...")
        self.assertIsNotNone(match)
        self.assertEqual(1, len(match.groups()))
        self.assertEqual("234:-112$", match.group(1))
        elements = match.group(1).split('$')
        self.assertEqual(2, len(elements))
        self.assertEqual('234:-112', elements[0])
        self.assertEqual('', elements[1])

    @staticmethod
    def test_horizontal_relation_one_waypoint():
        segments = [{'x': 120, 'y': 30}, {'x': 140, 'y': 31, }, {'x': 160, 'y': 30}]
        builder = XMIBuilder(JSModel())
        builder.scale = 1.0
        node = builder.create_line(segments,
                                   Rectangle((10, 20), 120, 20),
                                   Rectangle((160, 10), 122, 40))
        print(node.get('geometry'))

    def test_rela_to_ea_path(self):
        eat = IntegrationTestXMIExport()
        eat.setUp()
        json, jsmodel = eat.load_riddle_model()
        relations = list(list(json['diagrams'].values())[0]['relationships'].values())
        self.assertTrue(len(relations) > 0)
        relation = relations[0]
        segments = relation['linesegments']
        self.assertTrue(len(segments) > 2)
        print(f"Processing relation {relation}")
        builder = XMIBuilder(jsmodel)
        builder.scale = 1
        node = builder.create_line(segments, Rectangle((10, 20), 70, 20), Rectangle((105, 15), 75, 25))
        print(node.get('geometry'))
