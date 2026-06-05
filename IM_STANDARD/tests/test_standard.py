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
        self.schemadefpath =  self.basepath / "Model"/ "im-standard-schema"
        self.schemajsonpath =  self.basepath / "Model"/ "im-standard-json"
        self.examplepath =  self.basepath / "Example models"
        self.schemareferences=self._schemareferences(self.schemadefpath)
        self.testmodelpath = self.schemajsonpath / "testmodels"
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
        return

    def test_testmodels(self):
        """ print my testmodels defined in the standard """

        def testonefile(file,reffile):
            with open(file) as infile:
                try:
                    jsonobj=json.load(infile)
                except Exception as ex:
                    logging.error(f"File {str(file)}")
                    logging.error(ex)
                    return
            myfilepath=self.schemadefpath / file.parts[-4] / (file.parts[-3] +"-schema" + file.suffix)
            if not myfilepath.is_file():
                myfilepath = self.schemadefpath / (file.parts[-3] + "-schema" + file.suffix)
            with open(myfilepath) as schemafile:
                validateschemajson=json.load(schemafile)

            # Validate
            validator = Draft7Validator(validateschemajson)
            errors = list(validator.iter_errors(jsonobj))

            if not errors:
                logging.info(f"OK: {json_file.name} is valid")
                return True
            else:
                for error in errors:
                    logging.error(
                        f"Validation error at {' -> '.join(str(p) for p in error.absolute_path)}: {error.message}")
                return False

            validator = Draft7Validator(validateschemajson,
                                         resolver=ValidateJsonModel.getresolver(basefile=myfilepath,
                                                                     curjson=validateschemajson,
                                                              referencepath=self.schemareferences))
            valid = file.parts[-2] == "valid"
            #TODO domain properties of subdomaintypes are not checked properly see invalid jsonx files
            try:
                validator.validate(jsonobj)
                if not valid:
                    logging.error (f"******* invalid passed {file.parts[-1]}")
                    self._errors+=1
            except Exception as ex:

                if str(ex).startswith('False is not true'):
                    print(f"{'/'.join(file.parts[-4:])}")
                    #pass on assert from above
                    raise ex
                if valid:
                    print(f"{'/'.join(file.parts[-3:])}")
                    logging.error(ex)
                    self._errors += 1
            return
        self._errors=0
        print("\ntested:")
        self.list_tree(path=self.testmodelpath,
                       dotest=testonefile)
        print("\n".join(self.caplog.messages))
        self.assertEqual(0,self._errors,"errors detected")

        return

    def test_examples(self):
        def _test1expl(testfilepath):
            if not testfilepath.is_file():
                logging.warning(f"Examplefile not found: {testfilepath}")
                return
            with open(testfilepath) as infile:
                jsonobj = json.load(infile)
            print(f"tested {str(testfilepath)}")
            deffilepath = self.schemadefpath / "InformationModel" / self.imdeffilename
            with open(deffilepath) as schemafile:
                validateschemajson = json.load(schemafile)

            purevalidate(tovalidatejs=jsonobj,
                                         validattionjs=validateschemajson,
                                         resolver=ValidateJsonModel.getresolver(basefile=deffilepath,
                                                                                curjson=validateschemajson,
                                                                                referencepath=self.schemareferences))
            return

        logging.getLogger().setLevel(logging.WARNING)
        _test1expl(testfilepath=self.examplepath / "Astronomie" / "astronomie-schema.json")
        #_test1expl(testfilepath=self.examplepath / "Astronomie" / "astronomie-schema.json")
        print()
        print ("\n".join(self.caplog.messages))
        self.assertEqual(0,len(self.caplog.messages))
        return

    def test_version(self):
        import IM_STANDARD as imstd
        ver=imstd.version()

        self.assertTrue(imstd.__version__["im-standard"]["main"],ver["im-standard"]["main"])

if __name__ == '__main__':
    unittest.main()
