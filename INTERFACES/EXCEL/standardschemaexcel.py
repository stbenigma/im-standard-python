from IM_STANDARD import JsonElement, ElementId
from .standardexcel import StandardExcel


class StandardSchemaExcel(StandardExcel):
    HEADERS = ["Name", "TechnicalName", "DataType", "Description",
               "Mandatory", "Cardinality", "Examples", "Synonyms",
               "Restriction"]

    def __init__(self, filespec=None):
        super().__init__(filespec=filespec)
        self._headers = dict()
        self.readExcel()

        return

    @property
    def reverseheaders(self):
        return {val: key for key, val in self._headers.items()}

    def do1sheet(self, sheet, headerline: int):
        dataobjectname = sheet.title
        datoid = ElementId.nextid("DATO")
        dataobject = JsonElement().dataobjectjson(elementid=datoid,
                                                  name=dataobjectname)

        additionalProperties = dict()
        for rownum, row in enumerate(sheet.iter_rows(values_only=False), start=1):
            if rownum == headerline:
                break  # take only rows before the headerline
            for cell in row:
                if cell is not None and cell.value is not None:
                    additionalProperties[dataobjectname + ":" + cell.coordinate] = cell.value
        additionalProperties["SOURCE-ID"]= f"{dataobjectname}"
        if len(additionalProperties) > 0:
            dataobject.setproperty(propname="additionalProps",
                                   val=additionalProperties)

        headers = {self.reverseheaders[cell.value]: cell.column for cell in sheet[headerline] if
                   cell.value in self.reverseheaders}
        self.dataattributes.extend(self.doattributes(dataobjectid=datoid,
                                                     sheet=sheet,
                                                     headers=headers,
                                                     headerline=headerline)
                              )
        return dataobject

    def getrowvalue(self,row,index):
        #index is 1..n, rows are 0..n-1
        return None if index is None else row[index-1].value

    def doattributes(self, dataobjectid, sheet, headers: dict, headerline: int):
        attributes = []
        additionalprops=dict()
        for row in sheet.iter_rows(values_only=False, min_row=headerline + 1):
            dataid=ElementId.nextid("DATA")
            for cell in row:
                if cell.column == headers.get("Restriction"):
                    if cell.value is not None:
                        self.businessrules.append(JsonElement().
                                              businessrulejson(elementid=ElementId.nextid("BURU"),
                                                               restrictedelems=[dataid],
                                                               description=None,
                                                               rule=cell.value,
                                                               additionalprops={
                                                                   "SOURCE-ID": f"{sheet.title}:{cell.coordinate}"}
                                                               ))
                elif cell.column not in headers.values():
                    name=sheet.cell(row=headerline,column=cell.column).value
                    additionalprops[name]=cell.value
                additionalprops["SOURCE-ID"]= f"{sheet.title}:{cell.coordinate}"
            attributes.append(JsonElement().dataattributejson(elementid=dataid,
                                                              name=self.getrowvalue(row,headers.get("Name")),
                                                              mandatory=
                                                                  "0" not in str(self.getrowvalue(row,headers.get("Cardinality"))),
                                                              description=self.getrowvalue(row,headers.get("Description")),
                                                              dataobjectid=dataobjectid,
                                                              technicalname=self.getrowvalue(row,headers.get("TechnicalName")),
                                                              technicaldatatype=self.getrowvalue(row,headers.get("DataType")),
                                                              examples=self.makelistofmultiline(self.getrowvalue(row,headers.get("Examples"))),
                                                              additionalprops=additionalprops
                                                              )
                              )


        return attributes

    def analyzeExcel(self, headerline=1, **kwargs):
        if self.myexcel is None:
            raise Exception("No excel loaded")

        self._headers = {h: kwargs.get(h, h) for h in self.HEADERS}

        self.dataobjects = []
        self.dataattributes = []
        self.domains = []
        self.businessrules = []
        additionalprops = dict()


        for sheet in self.myexcel.worksheets:
            self.dataobjects.append(self.do1sheet(sheet=sheet, headerline=headerline))

        self.model.jsonschemamodel.setdefault("DataObjects", self.dataobjects)
        self.model.jsonschemamodel.setdefault("DataAttributes", self.dataattributes)
        if len(self.businessrules) > 0:
            self.model.jsonschemamodel["BusinessRules"] = self.businessrules
        if len(self.domains) > 0:
            self.model.jsonschemamodel["Domains"] = self.domains
        if len(additionalprops) > 0:
            self.model.jsonschemamodel["additionalProps"] = additionalprops

        return
