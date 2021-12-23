import re
import unittest

"""

Straight line horizontal without waypoints:
<element geometry="SX=0;SY=0;EX=0;EY=0;EDGE=2;$LLB=;LLT=;
        LMT=CX=18:CY=14:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;  <- Label position
        LMB=;LRT=;LRB=;IRHS=;ILHS=;
        Path=;" 
    subject="EAID_91DB8A70_5245_46b0_B025_192A288FD2F5" 
    style="Mode=3;
    EOID=C1CA053B;
    SOID=9F3C7BA4;
    Color=-1;LWidth=0;Hidden=0;"/>

E ⏋
  E
Right angle C to D with one waypoint:
<element geometry="SX=0;SY=0;EX=0;EY=0;EDGE=2;$LLB=;LLT=;
        LMT=CX=27:CY=14:OX=-30:OY=-51:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=1:DIR=0:ROT=0;
        LMB=;LRT=;LRB=;IRHS=;ILHS=;
        Path=234:-112$;" <- Waypoint?
    subject="EAID_182C295F_C77E_4e60_8565_F3500701C816" 
    style="Mode=3;EOID=F3E45154;SOID=B5035F09;Color=-1;LWidth=0;Hidden=0;"/>
    
Bounding box around the line
<element geometry="Left=119;Top=113;Right=235;Bottom=209;" subject="EAID_DC5E74C2_4524_474b_8A7D_65847FB8020F" seqno="3" style="DUID=8E27E1DC;"/>
"""


class LineCoding(unittest.TestCase):

    def test_extract_waypoints(self):
        pattern = re.compile(r"Path=([^$]+)\$")
        match = pattern.search("ILHS=;Path=234:-112$;\"")
        self.assertIsNotNone(match)
        self.assertEqual(1, len(match.groups()))
        self.assertEqual("234:-112", match.group(1))


if __name__ == '__main__':
    unittest.main()
