import dbDDL
import dbDML
from IM_DB import dbConnect
from IM_JSON import JSModel
from dbDDL import gettablelist
from IM_DB import parameters,logmessages
import sys,os
from openpyxl import Workbook

val2str = lambda v: '' if v is None else str(v) if type(v) in (int,float) else v
def writesheets(pwb,pjsmodel:JSModel):
    systems = pjsmodel.getelements('INTF')
    ws = pwb.create_sheet("Overview")
    rowidx, colidx = 1, 1
    ws.cell(column=colidx, row=rowidx, value='System')
    ws.cell(column=colidx+1, row=rowidx, value='tablecount')
    for sys in systems.values():
        rowidx += 1
        ws.cell(column=colidx, row=rowidx, value=sys['name'])
        ws.cell(column=colidx+1, row=rowidx, value=len(sys["tables+"]))
    #for
    for sys in systems.values():
        ws = pwb.create_sheet(sys["name"])
        tables = [pjsmodel.getbyid(tab) for tab in sys["tables+"]]
        tables = sorted(tables,key=lambda tab:tab["name"])
        rowidx, colidx = 1, 1
        for tab in tables:
            ws.cell(column=colidx, row=rowidx, value=tab["name"])
            rowidx += 1
        #for
    return

def createExcel(pfilename: str,pjsmodel):
    wb = Workbook()
    writesheets(pwb=wb,pjsmodel=pjsmodel)
    wb.remove(wb.worksheets[0])
    wb.save(filename=pfilename)
    return

def main(param1):
    JSONEXTENSION = '.json'
    jsmodel = JSModel.readfromfile(pfilename=param1)
    filename = param1[:-len(JSONEXTENSION)]+'_MAP'
    fileext = '.xlsx'
    createExcel(pfilename=filename+fileext,pjsmodel=jsmodel)
    print ("Excel {} created".format (filename+fileext))

if __name__ == '__main__':
    main(param1=None if len(sys.argv) == 1 else sys.argv[1])