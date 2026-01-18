import json

from openpyxl import Workbook
from openpyxl.utils import get_column_letter

from IM_STANDARD import nvl, JsonElement, ElementId
from .standardexcel import StandardExcel


class CreateDataExcel:
    def __init__(self, standardjson):
        if type(standardjson) == dict:
            self.standardjson = standardjson
        else:
            with open(standardjson) as infile:
                self.standardjson = json.load(infile)
        return

    def writeemptyexcel(self, outfilepath, withexamples: bool):
        wb = Workbook()
        wb.remove(wb.active)
        desired_width = 25
        for dataobj in self.standardjson.get("DataObjects", []):
            ws = wb.create_sheet(dataobj.get("name", "???"))
            row = []
            row2 = []
            rowlen = 0
            for dataattr in self.standardjson.get("DataAttributes", []):
                if dataattr.get("dataobjectid") == dataobj.get("elementid"):
                    rowlen += 1
                    row.append(nvl(dataattr.get("technicalname"), dataattr.get("name")))
                    examples = dataattr.get("examples")
                    if type(examples) == list:
                        example = nvl(examples, [None])[0]
                    else:
                        example = examples
                    row2.append(example)
            ws.append(row)
            if withexamples:
                ws.append(row2)

            # Loop through columns 1 to 10 (A through J)
            for i in range(1, rowlen + 1):
                ws.column_dimensions[get_column_letter(i)].width = desired_width
            wb.save(outfilepath)
        return


class StandardDataExcel(StandardExcel):
    def __init__(self, filespec=None):
        super().__init__(filespec=filespec)
        self.readExcel()
        return

    def analyzeExcel(self, headerline=1):
        if self.myexcel is None:
            raise Exception("No excel loaded")

        self.dataobjects = []
        self.dataattributes = []
        for sheet in self.myexcel.worksheets:
            dataobjectname = sheet.title
            datoid = ElementId.nextid("DATO")
            additionalProps = dict()
            for rownum, row in enumerate(sheet.iter_rows(values_only=False), start=1):
                if rownum >= headerline:
                    break
                for cell in row:
                    if cell is not None and cell.value is not None:
                        additionalProps[dataobjectname + ":" + cell.coordinate] = cell.value
            additionalProps["EXCELSOURCE"] = f"{dataobjectname}"

            dataobject = JsonElement().dataobjectjson(elementid=datoid,
                                                      name=dataobjectname,
                                                      additionalProps=additionalProps)

            self.dataobjects.append(dataobject)
            # read headers als attributes
            for row in sheet.iter_rows(values_only=False, min_row=headerline, max_row=headerline):
                for cell in row:
                    if cell is not None and cell.value is not None:
                        # get example row below header row
                        valuecell = sheet[cell.column_letter + str(cell.row + 1)]
                        try:
                            isdate = valuecell.is_date
                        except:
                            isdate = False

                    self.dataattributes.append(JsonElement().dataattributejson(elementid=ElementId.nextid("DATA"),
                                                                               name=cell.value,
                                                                               mandatory=None,
                                                                               dataobjectid=datoid,
                                                                               technicaldatatype=valuecell.data_type,
                                                                               basedatatype=StandardExcel.excel2standarddatatypes(valuecell.data_type),
                                                                               examples=[valuecell.value],
                                                                               additionalProps={"EXCELSOURCE":f"{dataobjectname}:{cell.coordinate}"}
                                                                               )
                                               )

        self.model.jsonschemamodel.setdefault("DataObjects", self.dataobjects)
        self.model.jsonschemamodel.setdefault("DataAttributes", self.dataattributes)

        return
        return
