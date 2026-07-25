from pathlib import Path

from openpyxl import load_workbook

from IM_STANDARD import JsonElement, JsonSchema


class StandardExcel:
    """
    reads an excel and prepares a JsonSchemna model to fill in the analyzed information
    has to be extended by an use with a special analyzefunction
    """
    def __init__(self, filespec=None):
        self._filespec = filespec
        self.model=None
        self.myexcel = None
        self.readExcel()
        return

    @staticmethod
    def excel2standarddatatypes(exceldt):
        translatedt = {"s": "Text",
                       "n": "Number",
                       "d": "Date",
                       "b": "Boolean"
                       }

        """f FormulaEine 
           e Error #N/A, #VALUE!, oder #DIV/0!.
           mInline String
        """

        return translatedt.get(exceldt, None)

    def readExcel(self, filespec=None):
        """
        loads an excel and sets up a empty JsonSchema model
        :param filespec:
        :return: member objects myescel and model set
        """
        if filespec is not None:
            self._filespec = filespec
        self.myexcel = load_workbook(self._filespec)
        self.model = JsonSchema(model={"ModelInfo": JsonElement().modelinfojson(modelname=Path(self._filespec).stem,
                                                                                modeltype="Data model",
                                                                                origintool="EXCEL",
                                                                                originref=str(self._filespec),
                                                                                targetEnvironment="Test"
                                                                                )}
                                )
        return

    def analyzeExcel(self, *args, **kwargs):
        """
        analyze an excel and fill all found elements into the model of this class
        :param args:
        :param kwargs:
        :return:
        """
        raise Exception("Function not implemented in basetype")

    def makelistofmultiline(self, val):
        """
            if val is of type str:
                return list of values of a string separated with \n
            else:
                return val
        :param val: value containing list of strings
        """
        if type(val) == str:
            return val.split("\n")
        else:
            return val
