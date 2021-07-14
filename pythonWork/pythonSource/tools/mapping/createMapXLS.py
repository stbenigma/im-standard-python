import dbDDL
import dbDML
from IM_DB import dbConnect
from IM_JSON import JSModel
from dbDDL import gettablelist
from IM_DB import parameters,logmessages
import sys,os
from openpyxl import Workbook,styles,utils

#utils.get_column_letter(pidx)
val2str = lambda v: '' if v is None else str(v) if type(v) in (int,float) else v
def writesheets(pwb,pjsmodel:JSModel):
    systems = pjsmodel.getelements('INTF')
    ws = pwb.create_sheet("Overview")
    rowidx, colidx = 1, 1
    ws.cell(column=colidx, row=rowidx, value='System')
    ws.cell(column=colidx+1, row=rowidx, value='tablecount')
    for sys in systems.values():
        rowidx += 1
        c = ws.cell(column=1,row=2)
        c.alignment=styles.Alignment(horizontal='general'
                            ,vertical='bottom'
                            ,text_rotation=0,
                            wrap_text=False,
                            shrink_to_fit=False,
                            indent=0)
        ws.cell(column=colidx, row=rowidx, value=sys['name'])
        ws.cell(column=colidx+1, row=rowidx, value=len(sys["tables+"]))
    #for
    for sys in systems.values():
        ws = pwb.create_sheet(sys["name"])
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 50
        tables = [pjsmodel.getbyid(tab) for tab in sys["tables+"]]
        tables = sorted(tables,key=lambda tab:tab["name"])
        rowidx, colidx = 1, 1
        ws.cell(column=colidx, row=rowidx, value='Table')
        ws.cell(column=colidx + 1, row=rowidx, value='Column')
        rowidx += 1
        maxcolidx = 3
        for tab in tables:
            colidx = 1
            ws.cell(column=colidx, row=rowidx, value=tab["name"])
            colidx += 2
            for map in tab['entitiesmapped']:
                ws.cell(column=colidx,row=rowidx,value=pjsmodel.getbyid(map)["name"]["de"])
                colidx += 1
            for map in tab['relationsmapped']:
                ws.cell(column=colidx,row=rowidx,value=pjsmodel.getbyid(map)["name"])
                colidx += 1
            for col in range(maxcolidx,colidx):
                ws.column_dimensions[utils.get_column_letter(col)].width = 30
            maxcolidx= max(maxcolidx,colidx-1)

            rowidx += 1
            columns = [pjsmodel.getbyid(col) for col in tab["columns+"]]
            columns = sorted(columns,key=lambda col:col["name"])
            colidx = 2
            #ws.merge_cells(start_row=2, start_column=1, end_row=4, end_column=4)
            for col in columns:
                ws.cell(column=colidx, row=rowidx, value=col["name"])
                rowidx += 1
            #for
        # for
    # for
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