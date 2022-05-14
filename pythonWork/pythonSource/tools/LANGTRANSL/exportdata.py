import sys
import os.path
from LANGTRANSL.langexceldata import Langexceldata
from SSOT_db.IM_JSON import JSModel
from openpyxl import Workbook, styles
from openpyxl.utils import get_column_letter
from openpyxl.comments import Comment


class Exportdata:
    def __init__(self, pmodel: JSModel, pjsonfile):
        self._model: JSModel = pmodel
        self._deflang = self._model.jsmodel['model']['language']
        self._languages = self._model.jsmodel['languages'].keys()
        self.gatherdata()
        self.setmetainfo(pjsonfile)

    def fulldata(self, ptext: dict, pdesc: str, pcomment: str) -> dict:
        retval = ptext
        retval['descr'] = pdesc
        retval['comment'] = pcomment
        return retval

    @staticmethod
    def xlskey(pid: str, pattr: str, pidx: int = None):
        retval = pid + '-' + pattr
        if pidx is not None:
            retval += '-' + str(pidx)
        return retval

    def setmetainfo(self, pjsonfile):
        self._gitrevision = self._model.jsmodel["_imprint_"]["git-revision"]
        self._dbmodelversion = self._model.jsmodel["_imprint_"]["Modelversion"]
        dm = self._model.jsmodel["model"]["dm"]
        if dm is None:
            dm = self._model.jsmodel["model"]["dc"]
        self._lastupdate = dm
        self._jsonfile = pjsonfile
        self._modellang = self._model.jsmodel["model"]["language"]
        self._modelname = self._model.jsmodel["model"]["name"]

    def getjsongitrevision(self):
        return self._gitrevision

    def getjsondbmodelversion(self):
        return self._dbmodelversion

    def getjsonlastupdate(self):
        return self._lastupdate

    def getjsonmodelname(self):
        return self._modelname

    def getjsonmodellang(self):
        return self._modellang

    def getjsonfile(self):
        return self._jsonfile

    def getdata(self, ptype=None):
        if ptype is None:
            return self._data
        else:
            return self._data[ptype]

    def _getdeflangstr(self, pelem):
        return pelem[self._deflang]

    def getlanguages(self):
        return self._languages

    def _getdefname(self, pelem):
        return self._getdeflangstr(pelem['name'])

    def _getelement(self, pelemid):
        return self._model.getbyid(pelemid)

    def _readentidata(self):
        elements = self._model.getelements('entities')
        for key, elem in elements.items():
            self._data[self.xlskey(key, 'name')] = self.fulldata(elem['name'], self._getdefname(elem) + '  Entity-Name',
                                                                 '')
            self._data[self.xlskey(key, 'descr')] = self.fulldata(elem['descr'],
                                                                  self._getdefname(elem) + '  Entity--Description', '')
            self._data[self.xlskey(key, 'tooltip')] = self.fulldata(elem['tooltip'],
                                                                    self._getdefname(elem) + '  Entity--Tooltip', '')
            for idx, syno in enumerate(elem['synonyms'], start=1):
                self._data[self.xlskey(key, 'synonym', idx)] = self.fulldata(syno, self._getdefname(
                    elem) + '->' + self._getdeflangstr(syno) + '  - Synonym-' + str(idx), '')
            for idx, expl in enumerate(elem['examples'], start=1):
                self._data[self.xlskey(key, 'example', idx)] = self.fulldata(expl, self._getdefname(
                    elem) + '  - Example-' + str(idx), '')

    def _readburudata(self):
        elements = self._model.getelements('businessrules')
        for key, elem in elements.items():
            refname = self._getdefname(elem)
            self._data[self.xlskey(key, 'name')] = self.fulldata(elem['name'], refname + '  Businessrule-Name', '')
            self._data[self.xlskey(key, 'descr')] = self.fulldata(elem['descr'], refname + '  Businessrule-Description',
                                                                  '')
            self._data[self.xlskey(key, 'errormsg')] = self.fulldata(elem['errormsg'],
                                                                     refname + '  Businessrule-Errormessage', '')

    def _readattrdata(self):
        elements = self._model.getelements('attributes')
        for key, elem in elements.items():
            refname = self._getdefname(self._getelement(elem['entity'])) + '->' + self._getdefname(elem)
            self._data[self.xlskey(key, 'name')] = self.fulldata(elem['name'], refname + '  Attribute-Name', '')
            self._data[self.xlskey(key, 'descr')] = self.fulldata(elem['descr'], refname + '  Attribute-Description',
                                                                  '')
            self._data[self.xlskey(key, 'tooltip')] = self.fulldata(elem['tooltip'], refname + '  Attribute-Tooltip',
                                                                    '')
            for idx, expl in enumerate(elem['examples'], start=1):
                self._data[self.xlskey(key, 'example', idx)] = self.fulldata(expl, self._getdefname(
                    elem) + '  - Example-' + str(idx), '')

    def _readdomadata(self):
        elements = self._model.getelements('domains')
        for key, elem in elements.items():
            refname = self._getdefname(elem)
            self._data[self.xlskey(key, 'name')] = self.fulldata(elem['name'], refname + '  Domain-Name', '')
            self._data[self.xlskey(key, 'descr')] = self.fulldata(elem['descr'], refname + '  Domain-Description', '')
        return

    def _readreladata(self):
        elements = self._model.getelements('relations')
        for key, elem in elements.items():
            fromentiname = self._getdefname(self._getelement(elem['from-to']['enti']))
            toentiname = self._getdefname(self._getelement(elem['to-from']['enti']))
            self._data[self.xlskey(key, 'fromto')] = self.fulldata(elem['from-to']['assoc'],
                                                                   'Relation -' + fromentiname + ' => ' + toentiname,
                                                                   '')
            self._data[self.xlskey(key, 'tofrom')] = self.fulldata(elem['to-from']['assoc'],
                                                                   'Relation -' + toentiname + ' => ' + fromentiname,
                                                                   '')

    def gatherdata(self):
        self._data = {}
        self._readentidata()
        self._readattrdata()
        self._readdomadata()
        self._readreladata()
        self._readburudata()


# Exportdata

def writesheets(pwb, pdata: Exportdata):
    ws = pwb.active
    ws.protection.sheet = True

    excel = Langexceldata()
    langs = pdata.getlanguages()
    excel.setheader(plangs=langs)

    excel.setheaderwidth(pdimensions=[20] + [50] * len(langs) + [45, 40])

    ws.append(excel.getheaderlist())
    comment = '\n'.join(s for s in [f"model={pdata.getjsonmodelname()}",
                                    f"lastmodified={pdata.getjsonlastupdate()}",
                                    f"modellanguage={pdata.getjsonmodellang()}",
                                    f"git-revision={pdata.getjsongitrevision()}",
                                    f"jsonfile={pdata.getjsonfile()}"
                                    ])
    ws["A1"].comment = Comment(text=comment,
                               author="SPOD-Generator", height=100, width=400)

    for idx, d in enumerate(excel.getheaderwidth(), start=1):
        ws.column_dimensions[get_column_letter(idx)].width = d

    for key, data in pdata.getdata().items():
        row = [key]
        for l in langs:
            row.append(data[l])
        row.append(data['descr'])
        row.append(data['comment'])
        ws.append(row)

    # unlock all cells but head and first
    for row in ws.rows:
        for cell in row:
            if cell.row > 1:
                if cell.column > 1:
                    cell.protection = styles.Protection(locked=False)
                cell.alignment = styles.Alignment(wrapText=True, vertical='top')

    return


def createexcel(pdestfile, pjsonfile):
    jsmodel = JSModel.readfromfile(pfilename=pjsonfile)
    data = Exportdata(jsmodel, pjsonfile)
    # getdata = {key: {lang:str,} 'desc':desc,'comment':comment}
    wb = Workbook()
    writesheets(pwb=wb, pdata=data)
    wb.save(filename=pdestfile)
    print(f"""Translation excel generated: {pdestfile} """)
    return


def createlangexcel(pjsonfile, pdest=None):
    assert os.path.isfile(pjsonfile)
    destdir = os.path.dirname(pjsonfile)
    destfilename = os.path.basename(pjsonfile)[:-5] + '.xlsx'
    if pdest is None:
        destfile = os.path.join(destdir, destfilename)
    elif os.path.isdir(pdest):
        destfile = os.path.join(pdest, destfilename)
    else:
        # assume it is a full file spec
        destfile = pdest
    createexcel(pdestfile=destfile, pjsonfile=pjsonfile)
    return


if __name__ == '__main__':
    createlangexcel(pjsonfile=sys.argv[1], pdest=None if len(sys.argv) < 3 else sys.argv[2])
