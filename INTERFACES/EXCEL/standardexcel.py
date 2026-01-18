from pathlib import Path

from openpyxl import load_workbook

from IM_STANDARD import JsonElement, JsonSchema


class StandardExcel:
    def __init__(self, filespec=None):
        self._filespec = filespec
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
        if filespec is not None:
            self._filespec = filespec
        self.myexcel = load_workbook(self._filespec)
        self.model = JsonSchema(model={"ModelInfo": JsonElement().modelinfojson(modelname=Path(self._filespec).stem,
                                                                                modeltype="Data model",
                                                                                origintool="EXCEL",
                                                                                originref=str(self._filespec),
                                                                                targetenvironment="Test"
                                                                                )}
                                )
        return

    def analyzeExcel(self, *args, **kwargs):
        raise Exception("Function not implemented in basetype")

    def makelistofmultiline(self, val):
        """ make a list of values of a string separated with \n """
        if type(val) == str:
            return val.split("\n")
        else:
            return val
