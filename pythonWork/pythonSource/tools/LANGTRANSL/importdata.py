import os.path
import sys
from copy import deepcopy

from openpyxl import load_workbook, styles
from openpyxl.worksheet.worksheet import Worksheet

from tools.LANGTRANSL.langexceldata import Langexceldata, attrkey2js
from SSOT_db.IM_JSON import JSModel, jsguid2type, printJSON
from SSOT_infra import nvl


def getjsonfile(pmodeldb, pjsonfile):
    return pjsonfile


redfill = styles.PatternFill(patternType='solid',
                             fill_type='solid',
                             fgColor=styles.Color('FB8500'))
greenfill = styles.PatternFill(patternType='solid',
                               fill_type='solid',
                               fgColor=styles.Color('80ED99'))
emptyfill = styles.PatternFill(fill_type=None)


class LangExcelException(Exception):
    pass


def checkkey(pcell, pjson):
    pcell.fill = emptyfill
    try:
        try:
            key, attr, idx = Langexceldata.decodekey(pcell.value)
        except Exception as exp:
            if type(exp) == ValueError:
                raise LangExcelException(f"illegal key in {pcell.value}")
            else:
                raise LangExcelException(f"Error in {pcell.value}, {exp}")
        # try
        # is key in json?
        jselem = pjson.getbyid(key)
        if jselem is None:
            raise LangExcelException(f"key {key} not found")
        else:
            # is the attribute in the keyfield a legal json entry?
            if attr in jselem:
                # if attr is listattr, is idx in json?
                if attr in ("examples", "synonyms") and len(jselem[attr]) < idx:
                    raise LangExcelException(f"index for {attr} does not exist {idx}")
            elif attr not in ("fromto", "tofrom"):
                raise LangExcelException(f"unknown attribute {attr} for this element")
        # fi
    except LangExcelException as lgexp:
        pcell.fill = redfill
        raise lgexp
    return [key, attr, idx]


def checkentries(pws: Worksheet, pexcel: Langexceldata, pjson: JSModel):
    okrows = []
    dupname = {'ENTI': {l: [] for l in pexcel.getlanguages()},
               'ATTR': {l: [] for l in pexcel.getlanguages()}}
    for row in pws.iter_rows(min_row=2):
        try:
            cell = row[pexcel.keyrowidx() - 1]
            key, attr, idx = checkkey(pcell=cell, pjson=pjson)
            # check languages for not null
            for lang in pexcel.getlanguages():
                langidx = pexcel.getheaderidx(lang)
                cell = row[langidx - 1]
                cell.fill = emptyfill
                assert 0 < langidx < 100
                if attr in ('name', "synonyms"):
                    if nvl(cell.value) == '':
                        raise LangExcelException(f"not null columns must not be empty")
                if attr == 'name':
                    elemtyp = jsguid2type(key)
                    if elemtyp in ('ENTI', 'ATTR'):
                        if cell.value in dupname[elemtyp][lang]:
                            raise LangExcelException(f"Nameentry must be unique")
                        else:
                            dupname[elemtyp][lang].append(cell.value)
                    # fi
                # fi
            okrows.append(row)
            comment = ""

        except LangExcelException as exp:
            # key cell has error
            cell.fill = redfill
            comment = str(exp)
        # try
        row[pexcel.getheaderidx('Comments') - 1].value = comment
    # for
    return okrows


def transfer2json(prows, pjson, pexcel):
    resultjson = deepcopy(pjson)
    changes = 0
    for row in prows:
        key, attr, idx = Langexceldata.decodekey(row[pexcel.keyrowidx() - 1].value)
        jsentry = pjson.getbyid(key)
        for lang in pexcel.getlanguages():
            colidx = pexcel.getheaderidx(lang)
            cell=row[colidx - 1]
            xval= cell.value
            entry=jsentry[attrkey2js(attr)]
            if idx is not None:
                #examples or synonyms
                jval = entry[idx-1]
            elif attr in ('fromto','tofrom'):
                #relationshipassocs
                jval = entry['assoc']
            else:
                jval = entry
            if nvl(xval) != nvl(jval[lang]):
                jval[lang]=nvl(xval)
                cell.fill = greenfill
                changes += 1

    return changes, resultjson


def mergeexcel2json(pws: Worksheet, pexcel: Langexceldata, pjson: JSModel):
    okrows = checkentries(pws=pws, pexcel=pexcel, pjson=pjson)
    retval = None
    if len(okrows) == pws.max_row - 1:
        changes, retval = transfer2json(prows=okrows, pjson=pjson, pexcel=pexcel)
    return changes, retval


def importlangexcel(pexcelfile, pmodeldb=None):
    assert os.path.isfile(pexcelfile)

    try:
        wb = load_workbook(filename=pexcelfile)
    except Exception as e:
        print(f"***** Excelfile could not be imported {pexcelfile}")
        print(e)

    ws: Worksheet = wb.active
    excel = Langexceldata()
    a1comment = ws["A1"].comment
    excel.analyzecomment('' if a1comment is None else a1comment.text)
    excel.analyzeheader(ws['1'])
    jsonfile = getjsonfile(pmodeldb, pjsonfile=excel.getmetainfo().getjsonfile())
    mergejson = JSModel.readfromfile(pfilename=jsonfile)

    resultexcel = pexcelfile.replace('.xlsx', '_result.xlsx')
    changes, newjson = mergeexcel2json(pws=ws, pexcel=excel, pjson=mergejson)
    if newjson is None:
        print(f"***** Errors found, see red marks in \n{resultexcel}")
    elif changes == 0:
        print(f"No changes found, nothing was updated")
    else:
        resultjson = jsonfile.replace('.json', '_result.json')
        printJSON(pmodel=newjson.jsmodel, pfilepath=os.path.dirname(resultjson), pfilename=os.path.basename(resultjson))
        print(f"Translations merged, see changed entries in \n{resultexcel}\nand in\n{resultjson}")
    wb.save(resultexcel)

    return


if __name__ == '__main__':
    importlangexcel(pexcelfile=sys.argv[1], pmodeldb=None if len(sys.argv) < 3 else sys.argv[2])
