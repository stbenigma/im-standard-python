import os.path
import sys

from openpyxl import load_workbook

from SSOT_db.IM_JSON.jsmodel import JSModel
from .langexceldata import Langexceldata


def importlangexcel(pexcelfile, pmodeldb=None):
    assert os.path.isfile(pexcelfile)

    try:
        wb = load_workbook(filename=pexcelfile)
    except Exception as e:
        print(f"***** Excelfile could not be imported {pexcelfile}")
        print(e)

    excel = Langexceldata()
    ws = wb.active
    metainfo = Langexceldata.analyzecomment(ws["A1"].comment.text)
    jsonfile = getjsonfile (pmodeldb,pjsonfile=metainfo[])
    mergejson = JSModel.readfromfile(pfilename=)

    return


if __name__ == '__main__':
    importlangexcel(pexcelfile=sys.argv[1], pmodeldb=None if len(sys.argv) < 3 else sys.argv[2])
