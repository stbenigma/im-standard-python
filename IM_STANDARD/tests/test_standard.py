import json
import os
import unittest
import logging
from pathlib import Path

import pytest
from jsonschema import Draft7Validator

from IM_STANDARD import ValidateJsonModel
from IM_STANDARD.jsonvalidation import purevalidate


class MyTestCase(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog, tmp_path, capsys):
        self.caplog = caplog
        caplog.set_level(logging.ERROR)
        self.capsys = capsys
        logging.basicConfig(level=logging.ERROR, force=True)
        return

    def setUp(self) -> None:

        myroot=Path(__file__).parent.parent.parent.parent
        self.basepath =  myroot / "Information-model-standard"
        self.schemadefpath =  self.basepath / "im-standard-json"
        self.examplepath =  self.basepath / "Example models"
        self.schemareferences=self._schemareferences(self.schemadefpath)
        self.testmodelpath = self.schemadefpath / "testmodels"
        self.imdeffilename="InformationModel-schema.json"

        return

    def _schemareferences(self,schemapath):
        retval = {}
        with os.scandir(schemapath) as schemata:
            for schema in schemata:
                if schema.name.endswith("-schema.json"):
                    with open(schema) as infile:
                        injson=json.load(infile)
                    retval[schema.name]=injson
        return retval

    def list_tree(self,path, dotest,level=0):
        for item in sorted(Path(path).iterdir()):
            #print(' ' * level * 4 + item.name)
            if item.is_dir():
                self.list_tree(item, dotest, level + 1)
            elif item.is_file() and item.suffix==".json":
                dotest(file=item,reffile=self.schemadefpath / (item.parts[-3] + "-schema" + item.suffix))

    def test_testmodels(self):
        """ print my testmodels defined in the standard """
        def testonefile(file,reffile):
            with open(file) as infile:
                jsonobj=json.load(infile)
            myfilepath=self.schemadefpath / (file.parts[-3] +"-schema" + file.suffix)
            with open(myfilepath) as schemafile:
                validateschemajson=json.load(schemafile)

            validator = Draft7Validator(validateschemajson,
                                         resolver=ValidateJsonModel.getresolver(basefile=myfilepath,
                                                                     curjson=validateschemajson,
                                                              referencepath=self.schemareferences))
            valid = file.parts[-2] == "valid"
            #TODO domain properties of subdomaintypes are not checked properly see invalid jsonx files
            try:
                validator.validate(jsonobj)
                if not valid:
                    print(f"invalid passed {file.parts[-1]}")
                    self.assertTrue(False,msg=f"invalid passing for valid {file.parts[-1]}")
            except Exception as ex:
                if str(ex).startswith('False is not true'):
                    print(f"{'/'.join(file.parts[-3:])}")
                    #pass on assert from above
                    raise ex
                if valid:
                    print(f"{'/'.join(file.parts[-3:])}")
                    logging.error(ex)
                    self.assertTrue(False)
            return

        print("\ntested:")
        self.list_tree(path=self.testmodelpath,
                       dotest=testonefile)
        return

    def test_testatronomie(self):
        testfilepath=self.examplepath / "Astronomie" / "astronomie-schema.json"
        if not testfilepath.is_file():
            self.skipTest(f"Examplefile not found: {testfilepath}")
        with open(testfilepath) as infile:
            jsonobj=json.load(infile)

        deffilepath=self.schemadefpath / self.imdeffilename
        with open(deffilepath) as schemafile:
            validateschemajson=json.load(schemafile)

        self.assertTrue(purevalidate(tovalidatejs=jsonobj,
                     validattionjs=validateschemajson,
                     resolver=ValidateJsonModel.getresolver(basefile=deffilepath,
                                            curjson=validateschemajson,
                                             referencepath=self.schemareferences )))
        return

    def test_version(self):
        import IM_STANDARD as imstd
        ver=imstd.version()
        self.assertTrue(imstd.__version__["im-standard"]["main"],ver["im-standard"]["main"])

if __name__ == '__main__':
    unittest.main()
