import os.path
import sys

from openpyxl import load_workbook,styles
from openpyxl.worksheet.worksheet import Worksheet

from LANGTRANSL.langexceldata import Langexceldata
from SSOT_db.IM_JSON import JSModel

def getjsonfile (pmodeldb,pjsonfile):
    return pjsonfile


redfill = styles.PatternFill(patternType='solid',
                                            fill_type='solid',
                                            fgColor=styles.Color('FB8500'))
greenfill = styles.PatternFill(patternType='solid',
                                            fill_type='solid',
                                            fgColor=styles.Color('80ED99'))
emptyfill = styles.PatternFill(fill_type=None)

def checkentries(pws:Worksheet, pexcel:Langexceldata, pjson:JSModel, pkeyidx:int):
    okrows = []
    for row in pws.iter_rows(min_row=2):
        cell = row[pkeyidx-1]
        cell.fill = emptyfill
        comment=""
        try:
            key,attr,idx = Langexceldata.decodekey(cell.value)
        except Exception as exp:
            if type(exp) == ValueError:
                comment = f"illegal key in {cell.value}"
            else:
                comment = f"Error in {cell.value}, {exp}"
        if comment == "":
            # is key in json?
            jselem = pjson.getbyid(key)
            if jselem is None:
                comment = f"key {key} not found"
            else:
                #is the attribute in the keyfield a legal json entry?
                if attr in jselem:
                    #if attr is listattr, is idx in json?
                    if attr in ("examples","synonyms") and len(jselem[attr])<idx:
                        comment=f"index for {attr} does not exist {idx}"
                elif attr not in ("fromto","tofrom"):
                    comment = f"unknown attribute {attr} for this element"
            #fi
        #fi
        if comment != "":
            #key cell has error
            cell.fill = redfill
        else:
            #check languages for not null
            pass

        if comment != "":
            row[pexcel.getheaderidx('Comments') - 1].value = comment
        else:
            okrows.append(row)
    #for

        #handle okrows
    return okrows

def mergeexcel2json(pws:Worksheet,pexcel:Langexceldata,pjson:JSModel):
    keyidx=pexcel.keyrowidx()
    checkentries(pws=pws, pexcel=pexcel, pjson=pjson, pkeyidx=keyidx)
    return


def importlangexcel(pexcelfile, pmodeldb=None):
    assert os.path.isfile(pexcelfile)

    try:
        wb = load_workbook(filename=pexcelfile)
    except Exception as e:
        print(f"***** Excelfile could not be imported {pexcelfile}")
        print(e)

    ws:Worksheet = wb.active
    excel = Langexceldata()
    a1comment = ws["A1"].comment
    excel.analyzecomment('' if a1comment is None else a1comment.text)
    excel.analyzeheader(ws['1'])
    jsonfile = getjsonfile (pmodeldb,pjsonfile=excel.getmetainfo().getjsonfile())
    mergejson = JSModel.readfromfile(pfilename=jsonfile)

    mergeexcel2json(pws=ws,pexcel=excel,pjson=mergejson)
    wb.save(pexcelfile)

    return


if __name__ == '__main__':
    importlangexcel(pexcelfile=sys.argv[1], pmodeldb=None if len(sys.argv) < 3 else sys.argv[2])
