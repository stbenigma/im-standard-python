import re
import unittest

"""

## Simple A-B
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

LRT= Label Target Top -> '+target label'
LRB= Label Target Bottom (invisible on IM diagrams)

LMT = Label Middle Top
LMB = Label Mittle Bottom

<element geometry="SX=45;SY=29;EX=41;EY=35;EDGE=2;
        $LLB=CX=122:CY=13:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        LLT=CX=153:CY=14:OX=-8:OY=-22:HDN=1:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0; <- hidden label
        LMT=CX=27:CY=14:OX=15:OY=-28:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        LMB=;LRT=CX=61:CY=14:OX=105:OY=10:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=1;
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
                               
     subject="EAID_182C295F_C77E_4e60_8565_F3500701C816" 
     style="Mode=3;EOID=952B160A;SOID=BB1AA2D7;Color=-1;LWidth=0;Hidden=0;"/>
     
"""


class LineCoding(unittest.TestCase):

    def test_extract_waypoints(self):
        pattern = re.compile(r"Path=([^;]+);")
        match = pattern.search(".. ILHS=;Path=234:-112$;\" subject ...")
        self.assertIsNotNone(match)
        self.assertEqual(1, len(match.groups()))
        self.assertEqual("234:-112$", match.group(1))
        elements = match.group(1).split('$')
        self.assertEqual(2, len(elements))
        self.assertEqual('', elements[1])


if __name__ == '__main__':
    unittest.main()
