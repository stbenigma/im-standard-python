import os.path
import sys

from openpyxl import load_workbook

from LANGTRANSL.langexceldata import Langexceldata


def importlangexcel(pexcelfile, pmodeldb=None):
    assert os.path.isfile(pexcelfile)

    try:
        wb = load_workbook(filename=pexcelfile)
    except Exception as e:
        print(f"***** Excelfile could not be imported {pexcelfile}")
        print(e)

    ws = wb.active
    excel = Langexceldata()
    a1comment = ws["A2"].comment
    excel.analyzecomment('' if a1comment is None else a1comment.text)
    # jsonfile = getjsonfile (pmodeldb,pjsonfile=metainfo[])
    # mergejson = JSModel.readfromfile(pfilename=None)

    return


if __name__ == '__main__':
    importlangexcel(pexcelfile=sys.argv[1], pmodeldb=None if len(sys.argv) < 3 else sys.argv[2])
