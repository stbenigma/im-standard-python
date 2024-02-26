import shutil
import unittest

import pytest

import SSOT_infra.tests.integration as testsrc
from IM_WEB.IM_HTML.svggeneration import *


class TestSVGGeneration(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init(self, tmp_path):
        self.temp_folder = Path(tmp_path)
        self.debugpath = Path.home() / 'Downloadsx'
        if not self.debugpath.is_dir():
            self.debugpath = self.temp_folder / 'debug'
            self.debugpath.mkdir(exist_ok=True)

    def setUp(self) -> None:
        self.testmodel2 = testsrc.ModelHelper(testsrc.TESTMODEL2).initDB()
        self.crm = testsrc.ModelHelper(testsrc.CRMTEST).initDB()



    def test_text_measure(self):
        width, height = textmeasure("Arial", 12, None, "Hello World!")
        print(f"Arial: Box width:{width} x height:{height}")
        width, height = textmeasure("TT Norms Pro", 12, None, "Hello World!")
        print(f"TT Norms Pro: Box width:{width} x height:{height}")
        width, height = textmeasure("Helvetica", 12, None, "Hello World!")
        print(f"Helvetica: Box width:{width} x height:{height}")
        self.assertTrue(64 <= width <= 68)
        self.assertTrue(10 <= height <= 15)

    def test_svgpos(self):
        pos = SvgPos(0, 0)
        self.assertEqual(0, pos.angle(pos.newpos(5, 0)))
        self.assertEqual(math.pi, pos.angle(pos.newpos(-5, 0)))
        self.assertEqual(math.pi / 2, pos.angle(pos.newpos(0, -5)))
        self.assertEqual(-math.pi / 2, pos.angle(pos.newpos(0, 5)))

        pos = SvgPos(50, 40)
        self.assertTrue(pos.angle(pos.newpos(5, 5)) < 0)
        self.assertTrue(pos.angle(pos.newpos(5, -5)) > 0)
        self.assertEqual(0, pos.angle(pos.newpos(5, 0)))
        self.assertEqual(math.pi, pos.angle(pos.newpos(-5, 0)))
        self.assertEqual(math.pi / 2, pos.angle(pos.newpos(0, -5)))
        self.assertEqual(-math.pi / 2, pos.angle(pos.newpos(0, 5)))

        self.assertEqual("east", pos.maindirection(pos.newpos(5, -5)))
        self.assertEqual("east", pos.maindirection(pos.newpos(5, 0)))
        self.assertEqual("east", pos.maindirection(pos.newpos(5, 4)))
        self.assertEqual("south", pos.maindirection(pos.newpos(5, 5)))
        self.assertEqual("south", pos.maindirection(pos.newpos(0, 5)))
        self.assertEqual("south", pos.maindirection(pos.newpos(-5, 6)))
        self.assertEqual("west", pos.maindirection(pos.newpos(-5, 5)))
        self.assertEqual("west", pos.maindirection(pos.newpos(-5, 1)))
        self.assertEqual("west", pos.maindirection(pos.newpos(-5, 0)))
        self.assertEqual("west", pos.maindirection(pos.newpos(-5, -2)))
        self.assertEqual("west", pos.maindirection(pos.newpos(-5, -4)))
        self.assertEqual("north", pos.maindirection(pos.newpos(-5, -5)))
        self.assertEqual("north", pos.maindirection(pos.newpos(0, -1)))
        self.assertEqual("north", pos.maindirection(pos.newpos(5, -6)))

    def test_hex2rgb(self):
        with self.assertRaises(Exception):
            self.assertEqual("(0,0,0)", hex2rbg("00000000"))
        with self.assertRaises(Exception):
            self.assertEqual("(0,0,0)", hex2rbg("0000"))
        with self.assertRaises(Exception):
            self.assertEqual("(0,0,0)", hex2rbg("0000GX"))
        self.assertEqual("(0,0,0)", hex2rbg("000000"))
        self.assertEqual("(255,255,255)", hex2rbg("FFFFFF"))
        self.assertEqual("(4,8,10)", hex2rbg("04080a"))
        self.assertEqual("(4,8,10)", hex2rbg("04080A"))

        with self.assertRaises(Exception):
            self.assertEqual("000000", rgb2hex(0, 0, 1000))
        with self.assertRaises(Exception):
            self.assertEqual("000000", rgb2hex(0, 0))
        with self.assertRaises(Exception):
            self.assertEqual("000000", rgb2hex(0, 0, 1, 1))
        with self.assertRaises(Exception):
            self.assertEqual("000000", rgb2hex(0, 0, -1))
        with self.assertRaises(Exception):
            self.assertEqual("000000", rgb2hex(0, 0, 256))
        self.assertEqual("000000", rgb2hex(0, 0, 0))
        self.assertEqual("FFFFFF", rgb2hex(255, 255, 255))
        self.assertEqual("04080A", rgb2hex(4, 8, 10))

        return

    def test_generateelements(self):
        entity = SvgEntity(width=200, height=120)
        self.assertEqual("", entity.name)
        self.assertEqual("", entity.name)

        entity.name = 'My name is nobody'
        self.assertEqual(200, entity.width)
        self.assertEqual(0.2, entity.opacity)

        diag = SvgDiagram(width=460, height=500, diagid="DIAG0001")
        diag.addcontent(entity)

        diag.addcontent(SvgRelation(SvgPos(x=200, y=30), SvgPos(x=350, y=30),
                                    text="ein langer beziehungstext [LT]",
                                    arcno=1, manyend=True))
        diag.addcontent(SvgRelation(SvgPos(x=200, y=60), SvgPos(x=290, y=60),
                                    text="ein langer beziehungstext [LT]",
                                    arcno=None, manyend=False))
        diag.addcontent(SvgRelation(SvgPos(x=200, y=90), SvgPos(x=250, y=90),
                                    text="ein langer beziehungstext [LT]",
                                    arcno=1, dashed=True))

        diag.addcontent(SvgRelation(SvgPos(x=180, y=170), SvgPos(x=280, y=170),
                                    text="hat gekauft von", manyend=True))
        diag.addcontent(SvgRelation(SvgPos(x=280, y=225), SvgPos(x=280, y=170),
                                    text="hat verkauft an", dashed=True, manyend=True))

        diag.addcontent(SvgRelation(SvgPos(x=310, y=225), SvgPos(x=310, y=170),
                                    text="hat verkauft an aber sehr lange für 3 Zeilen", dashed=True, manyend=True))
        diag.addcontent(SvgRelation(SvgPos(x=330, y=230), SvgPos(x=330, y=170),
                                    text="hat", dashed=True, manyend=True))
        diag.addcontent(SvgRelation(SvgPos(x=350, y=225), SvgPos(x=355, y=280),
                                    text="ist",
                                    dashed=False, manyend=True,
                                    arcno=3))
        diag.addcontent(SvgRelation(SvgPos(x=360, y=340), SvgPos(x=355, y=280),
                                    text="ist auch",
                                    dashed=True, manyend=True))

        diag.addcontent(SvgRelation(SvgPos(x=380, y=225), SvgPos(x=380, y=290),
                                    text="ist zweizeilig",
                                    dashed=False, manyend=True,
                                    arcno=3))



        diag.addcontent(SvgRelation(SvgPos(x=250, y=245), SvgPos(x=130, y=245),
                                    text="ist",
                                    dashed=True, manyend=True))
        diag.addcontent(SvgRelation(SvgPos(x=130, y=235), SvgPos(x=250, y=235),
                                    text="ist länger als erlaubt auf einer",
                                    dashed=True, manyend=True))
        diag.addcontent(SvgRelation(SvgPos(x=190, y=275), SvgPos(x=130, y=275),
                                    text=None, arcno=2,
                                    dashed=False, manyend=True))
        diag.addcontent(SvgRelation(SvgPos(x=130, y=270), SvgPos(x=130, y=245),
                                    dashed=True, manyend=True))

        diag.addcontent(SvgRelation(SvgPos(x=120, y=245), SvgPos(x=120, y=270),
                                    dashed=False, manyend=True, arcno=2))
        diag.addcontent(SvgRelation(SvgPos(x=100, y=245), SvgPos(x=100, y=290),
                                    text="ist auch eine Verb in einer Beziehung die lang ist",
                                    dashed=False, manyend=True,
                                    arcno=3))

        diag.addcontent(SvgRelation(SvgPos(x=70, y=235), SvgPos(x=70, y=290),
                                    text="ist auch eine Verb in einer Beziehung die lang ist",
                                    dashed=False, manyend=True,
                                    arcno=3))

        diag.addcontent(SvgRelation(SvgPos(x=200, y=260), SvgPos(x=220, y=260),
                                    dashed=False, manyend=True))
        diag.addcontent(SvgRelation(SvgPos(x=230, y=255), SvgPos(x=220, y=255),
                                    dashed=False, manyend=True))
        diag.addcontent(SvgRelation(SvgPos(x=230, y=270), SvgPos(x=220, y=270),
                                    dashed=False, manyend=False, arcno=2))

        diag.addcontent(SvgEntity(width=80, height=90, name="And now Anybody"
                                  , x=5, y=125))
        entity4 = SvgEntity(width=80, height=90, name="And no wadays "
                            , x=100, y=125, elemid="ENTI0001")
        entity4.addattribute(SvgAttribute(name="Attr1", elemid="ATTR0001"),
                             SvgAttribute(name="ein langes Attribut", elemid="ATTR0002"),
                             SvgAttribute(name="das zu lang ist", elemid="ATTR0004"))
        diag.addcontent(entity4)

        diag.addcontent(SvgEntity(width=50, height=40, name="Shortentity"
                                  , x=5, y=125 + 100))
        entity5 = SvgEntity(width=50, height=40, name="Short"
                            , x=250, y=125 + 100)
        entity5.addattribute(SvgAttribute(name="1"))
        diag.addcontent(entity5)

        entity6 = SvgEntity(width=200, height=120, name="with subentities"
                            , x=5, y=300)
        diag.addcontent(entity6)
        SvgEntity(width=120, height=30, name="subentity 1"
                  , x=5, y=40, fatherentity=entity6)

        entity8 = SvgEntity(width=190, height=40, name="subentity 2"
                            , x=5, y=75, fatherentity=entity6)
        entity8.addattribute(SvgAttribute(name="Attr 1"))
        SvgEntity(width=45, height=25, name="SE 4"
                  , x=130, y=10, fatherentity=entity8)

        diag.addcontent(SvgRelation(SvgPos(x=205, y=310), SvgPos(x=260, y=330),
                                    text="schräg",
                                    dashed=False, manyend=False))
        diag.addcontent(SvgRelation(SvgPos(x=320, y=350), SvgPos(x= 260, y=330),
                                    text="zurück 1",
                                    dashed=True, manyend=True))


        diag.addcontent(SvgRelation(SvgPos(x=205, y=360), SvgPos(x=250, y=360),
                                    text="nachher scrhäg",
                                    dashed=True, manyend=False))
        diag.addcontent(SvgRelation(SvgPos(x=250, y=360), SvgPos(x=270, y=390),
                                    dashed=True))
        diag.addcontent(SvgRelation(SvgPos(x=320, y=390), SvgPos(x=270, y=390),
                                    text="zurück",
                                    dashed=False, manyend=True))


        svgfile = self.temp_folder / 'testsvg.svg'
        f = open(svgfile, "w")
        f.write(diag.getsvg())
        f.close()

        if self.debugpath.is_dir():
            debugfile = self.debugpath / 'testsvg.svg'
            shutil.copyfile(svgfile, debugfile)

            print()
            print(f"DEBUG: copied svg to {debugfile}")



        return

    def test_generate_diagram(self):

        jsonmodel = JSModel.readfromfile(pfilename=self.testmodel2.jsonfile)
        diags = jsonmodel.getelements('diagrams')
        diagid = list(diags.keys())[0]

        svgfile = self.temp_folder / 'testsvgdiag.svg'
        f = open(svgfile, "w")
        f.write(renderdiagram(model=jsonmodel, diagid=diagid,
                              lang=jsonmodel.getdefaultlang()))
        f.close()

        if self.debugpath.is_dir():
            debugfile = self.debugpath / 'testsvgdiag.svg'
            shutil.copyfile(svgfile, debugfile)

            print()
            print(f"DEBUG: copied svg to {debugfile}")

        jsonmodel = JSModel.readfromfile(pfilename=self.crm.jsonfile)
        diags = jsonmodel.getelements('diagrams')
        diagid = list(diags.keys())[1]

        svgfilecrm = self.temp_folder / 'testsvgcrm.svg'
        f = open(svgfilecrm, "w")
        f.write(renderdiagram(model=jsonmodel, diagid=diagid,
                              lang=jsonmodel.getdefaultlang()))
        f.close()

        if self.debugpath.is_dir():
            debugfile = self.debugpath / 'testsvgcrm.svg'
            shutil.copyfile(svgfilecrm, debugfile)

            print()
            print(f"DEBUG: copied svg to {debugfile}")

            testsvg = self.debugpath / 'testsvg.html'
            f = open(testsvg, "w")
            testhtml = """<!DOCTYPE html>
<html lang="en">
<style>
	body {
	  font-family: Helvetica;
	}
</style>

<head>
    <h2>Test SVG</h2>
    <meta charset="utf-8">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>

<body>
	<div> <img alt="testsvg.svg" src="./testsvg.svg">
	</div>
	<div> <img alt="testsvgdiag.svg" src="./testsvgdiag.svg">
	</div>
	<div> <img alt="testsvgcrm.svg" src="./testsvgcrm.svg">
	</div>
</body>"""
            f.write(testhtml)
            f.close()


        return

    def test_calcshortname(self):
        textstr = "Dies ist\tein.Text mit-Umbruch"

        def onetext(diffw, texttype="relation"):
            text = SvgText(text=textstr,
                           texttype=texttype
                           )
            maxw = text.realwidth() + diffw
            text.maxwidth = max(10, maxw)
            print("\nmaxwidth={}    realwith={}   text={}".format(maxw, text.realwidth(), text.text))
            for t in text._multilinetext:
                print(text.textwidth(t), "\t", t)
            return text

        print("\nAttribute\n=========")
        text = onetext(1, "attribute")
        self.assertEqual(text.textwidth(text.text), text.realwidth())
        text = onetext(-1, "attribute")
        self.assertTrue(text.maxwidth >= text.realwidth())
        self.assertEqual("..", text._multilinetext[0][-2:])
        print("\nRelation\n========")
        text = onetext(2)
        self.assertEqual(text.textwidth(text.text), text.realwidth())
        text = onetext(-3)
        self.assertTrue(text.maxwidth >= text.realwidth() < text.textwidth(text.text))
        text = onetext(-23)
        self.assertTrue(text.maxwidth >= text.realwidth() < text.textwidth(text.text))
        self.assertEqual(2, len(text._multilinetext))
        text = onetext(-33)
        self.assertTrue(text.maxwidth >= text.realwidth() < text.textwidth(text.text))
        self.assertEqual(2, len(text._multilinetext))
        text = onetext(-42)
        self.assertTrue(text.maxwidth >= text.realwidth() < text.textwidth(text.text))
        self.assertEqual(2, len(text._multilinetext))
        text = onetext(-75)
        self.assertTrue(text.maxwidth >= text.realwidth() < text.textwidth(text.text))
        self.assertEqual(3, len(text._multilinetext))
        self.assertEqual("..", text._multilinetext[2][-2:], f"Ganzer text: {text._multilinetext}")
        textstr = "DiesisteinTextmitUmbruchderaberzulangist"
        text = onetext(-50)
        self.assertTrue(text.maxwidth >= text.realwidth() < text.textwidth(text.text))
        self.assertEqual(2, len(text._multilinetext))
        textstr = "D iesisteinTextmitUmbruchderaber zulangist"
        text = onetext(-50)
        self.assertTrue(text.maxwidth >= text.realwidth() < text.textwidth(text.text))
        self.assertEqual(2, len(text._multilinetext))
        textstr = "D iesist"
        text = onetext(-10)
        self.assertTrue(text.maxwidth >= text.realwidth() < text.textwidth(text.text))
        self.assertEqual(2, len(text._multilinetext))

        return


if __name__ == '__main__':
    unittest.main()
