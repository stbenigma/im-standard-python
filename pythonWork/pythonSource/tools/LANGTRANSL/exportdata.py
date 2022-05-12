import os.path
from .langexceldata import Langexceldata
from SSOT_db.IM_JSON import JSModel
from openpyxl import Workbook

class Exportdata:
    def __init__(self, pmodel:JSModel):
        self._model:JSModel = pmodel
        self._deflang= self._model.jsmodel['model']['language']
        self.gatherdata()

    def fulldata(self, ptext: dict, pdesc: str, pcomment: str) -> dict:
        retval = ptext
        retval['descr'] = pdesc
        retval['comment'] = pcomment
        return retval

    @staticmethod
    def xlskey(pid: str, pattr: str):
        return pid + '-' + pattr

    def getdata(self, ptype=None):
        if ptype is None:
            return self._data
        else:
            return self._data[ptype]

    def _getdeflangstr(self, pelem):
        return pelem[self._deflang]

    def _getdefname(self, pelem):
        return self._getdeflangstr(pelem['name'])

    def _getelement(self,pelemid):
        return self._model.getbyid(pelemid)

    def _readentidata(self):
        elements = self._model.getelements('entities')
        for key,elem in elements.items():
            self._data[self.xlskey(key, 'name')] = self.fulldata(elem['name'], self._getdefname(elem) + '  - Name', '')
            self._data[self.xlskey(key,  'descr')] = self.fulldata(elem['descr'], self._getdefname(elem) + '  - Description', '')
            self._data[self.xlskey(key, 'tooltip')] = self.fulldata(elem['tooltip'], self._getdefname(elem) + '  - Tooltip', '')
            for idx,syno in enumerate(elem['synonyms'],start=1):
                self._data[self.xlskey(key+'-'+str(idx), 'synonym')] = self.fulldata(syno,self._getdefname(elem)+'->'+ self._getdeflangstr(syno)+'  - Synonym', '')
            #for idx,expl in enumerate(elem['examples'],start=1):
            #    self._data[self.xlskey(key+'-'+str(idx),'example')] = self.fulldata(expl.expl_value_l, elem.enti_name + '  - Example', '')

    def _readburudata(self):
        elements = self._model.getelements('businessrules')
        for key,elem in elements.items():
            refname=self._getdefname(elem)
            self._data[self.xlskey(key, 'name')] = self.fulldata(elem['name'], refname+ '  - Name', '')
            self._data[self.xlskey(key, 'descr')] = self.fulldata(elem['descr'], refname + '  - Description', '')
            self._data[self.xlskey(key, 'errormsg')] = self.fulldata(elem['errormsg'], refname + '  - Errormessage', '')

    def _readattrdata(self):
        elements = self._model.getelements('attributes')
        for key,elem in elements.items():
            refname=self._getdefname(self._getelement(elem['entity'])) +'->'+ self._getdefname(elem)
            self._data[self.xlskey(key, 'name')] = self.fulldata(elem['name'], refname+ '  - Name', '')
            self._data[self.xlskey(key, 'descr')] = self.fulldata(elem['descr'], refname + '  - Description', '')
            self._data[self.xlskey(key, 'tooltip')] = self.fulldata(elem['tooltip'], refname + '  - Tooltip', '')
            #for expl in elem.getexamples():
            #    self._data[self.xlskey(self.EXPL, expl.expl_id, 'examples')] = self.fulldata(expl.expl_value_l, elem.attr_tech_name + '  - Example', '')

    def _readdomadata(self):
        elements = self._model.getelements('domains')
        for key,elem in elements.items():
            refname=self._getdefname(elem)
            self._data[self.xlskey(key, 'name')] = self.fulldata(elem['name'], refname+ '  - Name', '')
            self._data[self.xlskey(key, 'descr')] = self.fulldata(elem['descr'], refname + '  - Description', '')
        return

    def _readreladata(self):
        elements = self._model.getelements('relations')
        for key,elem in elements.items():
            fromentiname = self._getdefname(self._getelement(elem['from-to']['enti']))
            toentiname = self._getdefname(self._getelement(elem['to-from']['enti']))
            self._data[self.xlskey(key, 'fromto')] = self.fulldata(elem['from-to']['assoc'], fromentiname + ' => ' + toentiname, '')
            self._data[self.xlskey(key, 'tofrom')] = self.fulldata(elem['to-from']['assoc'], toentiname + ' => ' + fromentiname, '')

    def gatherdata(self):
        self._data = {}
        self._readentidata()
        self._readattrdata()
        self._readdomadata()
        self._readreladata()
        self._readburudata()
#Exportdata

def createexcel(pdestfile, pmodel):
    data = Exportdata(pmodel).getdata()
    wb = Workbook()
    #writesheets(pwb=wb,pdata=data)
    wb.save(filename=pdestfile)
    print (f"""Translation excel generated: {pdestfile} """)
    return


def createlangexcel(pjsonfile,pdest=None):
    assert os.path.isfile(pjsonfile)
    destdir=os.path.dirname(pjsonfile)
    destfilename= os.path.basename(pjsonfile)[:-5]+'.xlsx'
    if pdest is None:
        destfile = os.path.join(destdir,destfilename)
    elif os.path.isfile(pdest):
        destfile = pdest
    else:
        destfile = os.path.join(destdir,destfilename)
    jsmodel = JSModel.readfromfile(pfilename=pjsonfile)
    createexcel(pdestfile=destfile,pmodel=jsmodel)
    return

if __name__ == '__main__':
    createlangexcel(pjsonfile=sys.argv[1],pdest=None if len(sys.argv)<3 else sys.argv[2])
