import os.path
import sys
from copy import deepcopy

from openpyxl import load_workbook, styles
from openpyxl.worksheet.worksheet import Worksheet

from SSOT_db.IM_JSON import JSModel, jsguid2type, printJSON
from SSOT_infra import nvl
from tools.LANGTRANSL.langexceldata import Langexceldata, attrkey2js

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


def formukvalue(pelemtype, pkey, pvalue):
    if (pelemtype == 'ATTR' or pelemtype == 'SYNO'):
        # attributes-names and synonyms are unique within entity
        return pkey + '-' + pvalue
    else:
        return pvalue


def check1langentry(pcell, plang, pkey, pattr, pdupnames):
    """checks cell for not null and uniquteness
    """
    pcell.fill = emptyfill

    if pattr in ('name', 'synonyms'):
        if nvl(pcell.value) == '':
            pcell.fill = redfill
            raise LangExcelException(f"not null columns must not be empty")
        elemtyp = jsguid2type(pkey)
        if elemtyp in ('ENTI', 'ATTR', 'DOMA'):
            if elemtyp == 'ENTI' and pattr == 'synonyms':
                elemtyp = 'SYNO'
            ukvalue = formukvalue(pelemtype=elemtyp, pkey=pkey, pvalue=pcell.value)
            if ukvalue in pdupnames[elemtyp][plang]:
                pcell.fill = redfill
                raise LangExcelException(f"Nameentry must be unique")
            else:
                pdupnames[elemtyp][plang].append(ukvalue)
            # fi
        # fi
    # fi
    return


def checkentries(pws: Worksheet, pexcel: Langexceldata, pjson: JSModel):
    okrows = []
    dupnames = {'ENTI': {l: [] for l in pexcel.getlanguages()},
                'ATTR': {l: [] for l in pexcel.getlanguages()},
                'DOMA': {l: [] for l in pexcel.getlanguages()},
                'SYNO': {l: [] for l in pexcel.getlanguages()}}
    for row in pws.iter_rows(min_row=2):
        try:
            comment = ''
            key, attr, idx = checkkey(pcell=row[pexcel.keyrowidx() - 1], pjson=pjson)
            try:
                # check languages for not null
                for lang in pexcel.getlanguages():
                    # returns erroneus cell in exception or nothing if ok
                    langidx = pexcel.getheaderidx(lang)
                    assert 0 < langidx < 100
                    check1langentry(pkey=key, pattr=attr, plang=lang, pcell=row[langidx - 1], pdupnames=dupnames)
                # row is ok (no exception) add to rows to be handled later
                okrows.append(row)

            except LangExcelException as lgexp:
                # cell has error
                comment = str(lgexp)

        except LangExcelException as lgexp:
            comment = str(lgexp)
        finally:
            row[pexcel.getheaderidx('Comments') - 1].value = comment
    # for row in
    return okrows


def transfer2json(prows, pjson, pexcel):
    resultjson = deepcopy(pjson)
    changes = 0
    for row in prows:
        key, attr, idx = Langexceldata.decodekey(row[pexcel.keyrowidx() - 1].value)
        jsentry = resultjson.getbyid(key)
        for lang in pexcel.getlanguages():
            colidx = pexcel.getheaderidx(lang)
            cell = row[colidx - 1]
            xval = cell.value
            entry = jsentry[attrkey2js(attr)]
            if idx is not None:
                # examples or synonyms
                jval = entry[idx - 1]
            elif attr in ('fromto', 'tofrom'):
                # relationshipassocs
                jval = entry['assoc']
            else:
                jval = entry
            if nvl(xval) != nvl(jval[lang]):
                jval[lang] = nvl(xval)
                cell.fill = greenfill
                changes += 1

    return changes, resultjson


def mergeexcel2json(pws: Worksheet, pexcel: Langexceldata, pjson: JSModel):
    okrows = checkentries(pws=pws, pexcel=pexcel, pjson=pjson)
    changes, resultjson = None, None
    if len(okrows) == pws.max_row - 1:
        changes, resultjson = transfer2json(prows=okrows, pjson=pjson, pexcel=pexcel)
    return changes, resultjson


def importlangexcel(pexcelfile):
    assert os.path.isfile(pexcelfile)

    try:
        wb = load_workbook(filename=pexcelfile)
    except Exception as e:
        print(e)
        raise Exception(f"***** Excelfile could not be imported {pexcelfile}")

    ws: Worksheet = wb.active
    excel = Langexceldata()
    a1comment = ws["A1"].comment
    excel.analyzecomment('' if a1comment is None else a1comment.text)
    excel.analyzeheader(ws['1'])
    jsonfile = excel.getmetainfo().getjsonfile()
    mergejson = JSModel.readfromfile(pfilename=jsonfile)

    resultexcel = pexcelfile.replace('.xlsx', '_result.xlsx')
    changes, newjson = mergeexcel2json(pws=ws, pexcel=excel, pjson=mergejson)
    resultjson = jsonfile.replace('.json', '_result.json')
    if os.path.exists(resultjson):
        os.remove(resultjons)
    if newjson is None:
        print(f"***** Errors found, see red marks in \n{resultexcel}")
        wb.save(resultexcel)
    elif changes == 0:
        print(f"No changes found, nothing was updated")
    else:
        printJSON(pmodel=newjson.jsmodel, pfilepath=os.path.dirname(resultjson), pfilename=os.path.basename(resultjson))
        print(f"Translations merged, see changed entries in \n{resultexcel}\nand in\n{resultjson}")
        wb.save(resultexcel)
    return changes

if __name__ == '__main__':
    args = sys.argv
    importlangexcel(pexcelfile=args[1], pmodeldb=None if len(args) < 3 else args[2])
