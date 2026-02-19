import json
import logging

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

from IM_STANDARD import JsonSchema, nvl


class CreateSchemaExcel:
    def __init__(self, standardjson, lang=None, nid=None):
        if type(standardjson) == dict:
            self._infilepath = None
            self._standardjson = JsonSchema(model=standardjson)
        else:
            self._infilepath = standardjson
            with open(standardjson) as infile:
                self._standardjson = JsonSchema(model=json.load(infile))
        self._standardjson.curlang = lang if lang is not None else self._standardjson.mainlang
        self._nid = nid
        self._usedgroupdomains = []
        return

    _header = {"Name": 35,
               "Technical name (camelCase)": 35,
               "Definition": 45,
               "ValeDataType": 15,
               "Cardinality": 10,
               "Mand./Opt.": 10,
               "Example": 35,
               "Comment/Rule": 30,
               "Dataspot": 10,
               "Dataspot Link to Datapoint/attribute": 60
               }
    _wrapped = ["C", "H"]

    def _mlvalue(self, struct, name):
        return self._standardjson.mlvalue(struct.get(name))

    @staticmethod
    def _addprop(struct, name):
        return struct.get("additionalProps").get(name)

    @staticmethod
    def _domavalues(doma):
        return [v.get("value") for v in doma.get("values", [])]

    @staticmethod
    def _xsd_type(doma):
        if doma.get("domaintype") == "LOVDomain":
            return "<xsd:Enumeration>"
        elif doma.get("domaintype") == "BooleanDomain":
            return "<xsd:boolean>"
        elif doma.get("domaintype") in ("DatetimeDomain"):
            if doma.get("granularity") in ("HOUR", "MINUTE",
                                           "SECOND", "MILISECOND"):
                return "<xsd:datetime>"
            else:
                return "<xsd:date>"
        elif doma.get("domaintype") in ("NumericDomain"):
            if doma.get("fractdigits", 0) == 0:
                return "<xsd:integer>"
            else:
                return "<xsd:float>"
        elif doma.get("domaintype") == "TextDomain":
            return "<xsd:string>"
        return ""

    def _groupmembers(self, doma):
        attrs = [attr for attr in self._standardjson.getelementinstances("Attributes")
                 if attr.get("parentid") == doma.get("elementid")]
        attrs.sort(key=lambda x: x.get("displayseq", 999))
        return [self._mlvalue(attr, "name") for attr in attrs]

    def _comments(self, domain):
        domatype = None if domain is None else domain.get("domaintype")
        if domatype == "LOVDomain":
            retval = '\n'.join(self._domavalues(domain))
        elif domatype == "GroupDomain":
            retval = '\n'.join(self._groupmembers(domain))
        elif domatype in ["TextDomain"]:
            retval = domain.get("syntaxrule")
        elif domatype == "NumericDomain":
            int2str = lambda x: "" if x is None else str(x)
            locstr=[]
            if domain.get("totaldigits", 0) != 0:
                if domain.get("fractdigits") is None:
                    locstr.append(f'Digits: {str(domain.get("totaldigits"))}')
                else:
                    locstr.append(f'Format: {str(domain.get("totaldigits"))}:{str(domain.get("fractdigits"))}')

            if domain.get("minvalue") is not None or domain.get("maxvalue") is not None:
                locstr.append(f'Range: {int2str(domain.get("minvalue"))} - {int2str(domain.get("maxvalue"))}')
            retval= '\n'.join(locstr)
        elif domatype == "DatetimeDomain":
            if domain.get("granularity") != "DAY":
                retval = f'Granularity: {domain.get("granularity")}'
            else:
                retval = ""
        else:
            retval = ""
        return retval

    def _getbyid(self, elemtype, elemid):
        retval = [elem for elem in self._standardjson.getelementinstances(elementname=elemtype)
                  if elem.get("elementid") == elemid]

        return retval[0] if len(retval) == 1 else None

    def _createentitysheet(self, ws, elem):

        ws.append(list(self._header.keys()))

        for attr in self._standardjson.getelementinstances("Attributes"):
            if attr.get("parentid") == elem.get("elementid"):
                domain = self._getbyid("Domains", attr.get("domainid"))
                if domain is None:
                    domatype = None
                    domaname = ""
                else:
                    domatype = domain.get("domaintype")
                    doma_tecname = self._addprop(domain, "TechnicalName")
                    doma_datatype = self._addprop(domain, "SOURCE-DATATYPE")
                    if domatype == "GroupDomain":
                        self._usedgroupdomains.append(domain)  # to be created later
                        domaname = f'[{self._mlvalue(domain, "name")}]'
                    else:
                        domaname = self._xsd_type(domain)  # if
                        # else doma_tecname if doma_tecname is not None
                        # else doma_datatype if doma_datatype is not None
                        # else self._mlvalue(domain, "name")
                link = nvl(self._addprop(attr, "SOURCE-HREF")).replace("/rest/", "/web/")
                row = [self._mlvalue(attr, "name"),
                       self._addprop(attr, "TechnicalName"),
                       self._mlvalue(attr, "description"),
                       domaname,
                       "N" if attr.get("repeated") else "1",
                       "mandatory" if attr.get("mandatory") else "optional",
                       "" if len(attr.get("examples", [])) == 0 else attr.get("examples")[0],
                       self._comments(domain),
                       1,
                       link
                       ]
                ws.append(row)
        return

    def _writesheet(self, ws, elem):

        self._createentitysheet(ws=ws, elem=elem)
        linkcolumn = 10
        for i, headsize in enumerate(self._header.values(), start=1):

            ws.column_dimensions[get_column_letter(i)].width = headsize
            ws[get_column_letter(i) + "1"].font = Font(bold=True)

            wrap_alignment = Alignment(wrapText=True, vertical='top')
            for cell in ws[get_column_letter(i)]:
                cell.alignment = wrap_alignment

        # color links
        for i, cell in enumerate(ws[get_column_letter(linkcolumn)], start=1):
            if i == 1: continue
            if cell.value not in ("", None):
                cell.hyperlink = cell.value
                cell.font = Font(color="0000FF", underline="single")

        return

    def writeexcel(self, outfilepath):
        wb = Workbook()
        wb.remove(wb.active)

        for enti in self._standardjson.getelementinstances(elementname="Entities"):
            self._writesheet(ws=wb.create_sheet(self._mlvalue(enti, "name")),
                             elem=enti)

        # fill group domains
        donegroupdomains = []
        while len(self._usedgroupdomains) > 0:
            doma = self._usedgroupdomains.pop(0)
            if doma.get("elementid") in donegroupdomains:
                continue

            self._writesheet(ws=wb.create_sheet(self._mlvalue(doma, "name")),
                             elem=doma)
            donegroupdomains.append(doma.get("elementid"))  # mark as done

        wb.save(outfilepath)
        print(f"Schema excel written: {str(outfilepath)}")

        return


def createexcel(jsonfilepath=None,
                jsonstruct=None,
                nid=None,
                outfilepath=None
                ):
    if jsonstruct is not None:
        jsstruct = jsonstruct
    elif jsonfilepath is not None:
        with open(jsonfilepath) as infile:
            jsstruct = json.load(infile)
    else:
        logging.error("No input given")
        return None
    CreateSchemaExcel(standardjson=jsstruct,
                      nid=nid).writeexcel(outfilepath=outfilepath)
    return
