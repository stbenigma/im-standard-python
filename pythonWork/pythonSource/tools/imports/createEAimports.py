import sys
from openpyxl import Workbook, styles
from IM_JSON import JSModel

# utils.get_column_letter(pidx)
val2str = lambda v: '' if v is None else str(v) if type(v) in (int, float) else v


def genentities(pwb, pjsmodel):
    entis = pjsmodel.getelements("ENTI")
    ws = pwb.create_sheet("entities")
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['C'].width = 5
    ws.column_dimensions['D'].width = 60
    ws.column_dimensions['D'].width = 5
    ws.column_dimensions['D'].width = 5
    ws.column_dimensions['D'].width = 5
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['D'].width = 20
    rowidx, colidx = 1, 1
    """Name	Type	Notes	Stereotype	Author	Is Leaf	Is Root	Created Date"""
    ws.cell(column=colidx, row=rowidx, value='Name')
    ws.cell(column=colidx + 1, row=rowidx, value='Type')
    ws.cell(column=colidx + 2, row=rowidx, value='Notes')
    ws.cell(column=colidx + 3, row=rowidx, value='Stereotype')
    ws.cell(column=colidx + 4, row=rowidx, value='Is Leaf')
    ws.cell(column=colidx + 5, row=rowidx, value='Is Root')
    ws.cell(column=colidx + 6, row=rowidx, value='Author')
    ws.cell(column=colidx + 7, row=rowidx, value='Created Date')
    for enti in entis.values():
        rowidx += 1
        colidx = 1
        ws.cell(column=colidx, row=rowidx, value=enti["name"]["de"])
        colidx += 1
        ws.cell(column=colidx , row=rowidx, value="Class")
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=enti["descr"]["de"])
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value="Entitiy")
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=1 if len(enti["subtypes+"])+len(enti["roles+"])==0 else 0)
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=1 if len(enti["supertypes+"])==0 else 0)
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=enti["uc"])
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=enti["dc"])
    # for
    return
def genattributes(pwb, pjsmodel):
    attrs = pjsmodel.getelements("ATTR")
    ws = pwb.create_sheet("attributes")
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['C'].width = 5
    ws.column_dimensions['D'].width = 60
    ws.column_dimensions['D'].width = 5
    ws.column_dimensions['D'].width = 5
    ws.column_dimensions['D'].width = 5
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['D'].width = 20
    rowidx, colidx = 1, 1
    """Name	Type	Notes	Stereotype	Author	Is Leaf	Is Root	Created Date"""
    ws.cell(column=colidx, row=rowidx, value='Name')
    ws.cell(column=colidx + 1, row=rowidx, value='Type')
    ws.cell(column=colidx + 2, row=rowidx, value='Notes')
    ws.cell(column=colidx + 3, row=rowidx, value='Stereotype')
    ws.cell(column=colidx + 4, row=rowidx, value='Is Leaf')
    ws.cell(column=colidx + 5, row=rowidx, value='Is Root')
    ws.cell(column=colidx + 6, row=rowidx, value='Author')
    ws.cell(column=colidx + 7, row=rowidx, value='Created Date')
    for attr in attrs.values():
        rowidx += 1
        colidx = 1
        ws.cell(column=colidx, row=rowidx, value=attr["name"]["de"])
        colidx += 1
        ws.cell(column=colidx , row=rowidx, value="Class???")
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=attr["descr"]["de"])
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value="Attribute???")
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=0)
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=0)
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=attr["uc"])
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=attr["dc"])
    # for
    return
def genrelations(pwb, pjsmodel):
    relas = pjsmodel.getelements("RELA")
    ws = pwb.create_sheet("relations")
    ws.column_dimensions['A'].width = 20
    ws.column_dimensions['C'].width = 5
    ws.column_dimensions['D'].width = 60
    ws.column_dimensions['D'].width = 5
    ws.column_dimensions['D'].width = 5
    ws.column_dimensions['D'].width = 5
    ws.column_dimensions['D'].width = 10
    ws.column_dimensions['D'].width = 20
    rowidx, colidx = 1, 1
    """Name	Type	Notes	Stereotype	Author	Is Leaf	Is Root	Created Date"""
    ws.cell(column=colidx, row=rowidx, value='Name');colidx += 1
    ws.cell(column=colidx , row=rowidx, value='Type');colidx += 1
    ws.cell(column=colidx , row=rowidx, value='Stereotype');colidx += 1
    ws.cell(column=colidx , row=rowidx, value='fromto entity');colidx += 1
    ws.cell(column=colidx , row=rowidx, value='fromto type');colidx += 1
    ws.cell(column=colidx , row=rowidx, value='fromto text');colidx += 1
    ws.cell(column=colidx , row=rowidx, value='tofrom entity');colidx += 1
    ws.cell(column=colidx , row=rowidx, value='tofrom type');colidx += 1
    ws.cell(column=colidx , row=rowidx, value='tofrom text');colidx += 1
    ws.cell(column=colidx , row=rowidx, value='Author');colidx += 1
    ws.cell(column=colidx , row=rowidx, value='Created Date');colidx += 1
    for rela in relas.values():
        rowidx += 1
        colidx = 1
        ws.cell(column=colidx, row=rowidx, value=rela["name"])
        colidx += 1
        ws.cell(column=colidx , row=rowidx, value="Connection")
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value="Relationship")
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=pjsmodel.getbyid(rela["from-to"]["enti"])["name"]["de"])
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=rela["from-to"]["cardstr+"])
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=rela["from-to"]["assoc"]["de"])
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=pjsmodel.getbyid(rela["to-from"]["enti"])["name"]["de"])
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=rela["to-from"]["cardstr+"])
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=rela["to-from"]["assoc"]["de"])
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=rela["uc"])
        colidx += 1
        ws.cell(column=colidx, row=rowidx, value=rela["dc"])
    # for
    return
def writesheets(pwb, pjsmodel: JSModel):
    genentities(pwb=pwb,pjsmodel=pjsmodel)
    genattributes(pwb=pwb,pjsmodel=pjsmodel)
    genrelations(pwb=pwb,pjsmodel=pjsmodel)
    return


def createExcel(pfilename: str, pjsmodel):
    wb = Workbook()
    writesheets(pwb=wb, pjsmodel=pjsmodel)
    wb.remove(wb.worksheets[0])
    wb.save(filename=pfilename)
    return


def createMapExcel(pjsonfile):
    JSONEXTENSION = '.json'
    jsmodel = JSModel.readfromfile(pfilename=pjsonfile)
    filename = pjsonfile[:-len(JSONEXTENSION)] + 'EAimport'
    fileext = '.xlsx'
    createExcel(pfilename=filename + fileext, pjsmodel=jsmodel)
    print("Excel {} created".format(filename + fileext))


if __name__ == '__main__':
    createMapExcel(pjsonfile=None if len(sys.argv) == 1 else sys.argv[1])
