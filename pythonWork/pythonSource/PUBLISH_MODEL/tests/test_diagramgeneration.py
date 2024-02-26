import unittest

from PUBLISH_MODEL.diagrams import diagramgeneration
import SSOT_infra.tests.integration as testsrc



class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.testmodel1 = testsrc.ModelHelper(testsrc.TESTMODEL1)

    def test_diagramgenration_parameters(self):
        with self.assertRaises(SystemExit):
            diagramgeneration.main(psysargs=['test_diagramgeneration.py',
                                f'--version'])
        with self.assertRaises(AssertionError):
            diagramgeneration.main(psysargs=['test_diagramgeneration.py',
                                f''])
        with self.assertRaises(AssertionError):
            diagramgeneration.main(psysargs=['test_diagramgeneration.py',
                                f'jsonfile.json'])
        with self.assertRaises(AssertionError):
            diagramgeneration.main(psysargs=['test_diagramgeneration.py',
                                f'--name=diagram'])

    def test_diagramgenration(self):
        diagramgeneration.main(psysargs=['test_diagramgeneration.py',
                                     f'--name=Main-View',
                                     str(self.testmodel1.jsonfile)
                                     ])

        # diagramgeneration.main(psysargs=['test_diagramgeneration.py',
        #                              f'--name=Workshop 8/8',
        #                              '/Users/stb/Documents/Projekte/BayWa/Baywa_miro.json'
        #                              ])


if __name__ == '__main__':
    unittest.main()
