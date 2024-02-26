import argparse
import logging
import os
import re
from pathlib import Path

import openpyxl.workbook.workbook
from openpyxl import load_workbook

from LOAD_MODELS.LOAD_INFRA import mergedbs
from SSOT_db.IM_JSON import JSModel
from SSOT_infra import nvl
from tools.excel.datamapping import mappingexceldata as mapxls

SOURCEREF = "MAPIMPORT"


def findrow(pws, psearch: dict):
    for row in pws.rows:
        for col, val in psearch.items():
            if row[col - 1].value == val:
                return row
    return None


def findcol(pws, psearch: dict):
    for col in pws.columns:
        for row, val in psearch.items():
            if col[row - 1].value == val:
                return col
    return None


def getjsonfile(pws):
    if pws is None:
        return None
    row = findrow(pws, {1: "JSON file"})
    # JSON file     \abd\asdf\...
    return None if row is None else row[2 - 1].value


def getlang(pws):
    if pws is None:
        return None
    row = findrow(pws, {1: "Language"})
    # Language     en...
    return None if row is None else row[2 - 1].value


def getmultilines(pvalue: str, pidx: int = None) -> list:
    """
       "Entität1
        Entität2 (Subentität)"
       returned into
       [["Entität1",""], ["Entität2","Subentität"]]
       all leading and trailing blanks, tabs are removed
       if pidx is not None:
            missing indices are filled with Nones
            no subelements in () are handled
       """
    names = [name.strip("\t ") for name in nvl(pvalue).splitlines()]
    if pidx is None:
        # entities, they could have subentites in parentheses
        retval = []
        for name in names:
            entis = re.match(r"^([^(]*)\(?([^)]*)\)?\s*$", name)
            if entis is not None and entis[1].strip("\t ") != "":
                retval.append([entis[1].strip("\t "), entis[2].strip("\t ")])
    else:
        # simple names
        retval = names
        if len(retval) < pidx:
            retval.extend(["" for i in range(pidx - len(retval))])
    return retval


def checkandaddcolmap(pcolid: str, pcol: dict, pattrinfo: tuple):
    """ check if mapping to current column already exists
        if not, add it
                 "attributesmapped": [
            [
               "ATTR182",
               null
            ]
        parameter pattrinfo (attrid,subentiid,attrname,entiname,subentiname)

    """
    changes = 0
    if pattrinfo[0] not in [attrmap[0] for attrmap in pcol["attributesmapped"] if attrmap[1] == pattrinfo[1]]:
        pcol["attributesmapped"].append([pattrinfo[0], pattrinfo[1]])
        changes += 1
        ses = lambda s: "" if s == "" else f" ({s})"
        logging.info(f"{pcol['datamodel-name+']} - {pcol['table-name+']}" +
                     f" - {pcol['name']}: attribute added {pattrinfo[3]} {ses(pattrinfo[4])}- {pattrinfo[2]} ({pattrinfo[0]})")
    return changes


def checkandaddentimap(ptabid: str, ptab: dict, pentiid: str, pentiname: str):
    """ check if mapping to current table already exists
        if not, add it
    """
    changes = 0
    if pentiid not in ptab["entitiesmapped"]:
        ptab["entitiesmapped"].append(pentiid)
        changes += 1
        logging.info(f"{ptab['datamodel-name+']} -  {ptab['name']}:" +
                     f" entity added '{pentiname}' ({pentiid})")
    return changes


def removenoncheckedattributes(pmodel: JSModel, pdatmname, pchechedcolattr: dict) -> int:
    """ remove all col-attr-mappings which were not touched """
    changes = 0
    return changes


def removenoncheckedentities(pmodel: JSModel, pdatmname, pchechedtabenti: dict) -> int:
    return 0
    """ remove all tab-enti-mappings which were not touched """
    changes = 0
    tables = pmodel.getelements("tables")
    for tabid, tab in filter (lambda t : t[1]["datamodel-name+"] == pdatmname,
                              tables.items()):
        #replaced by filter if tab["datamodel-name+"] != pdatmname: continue  ##only for one datamodel!!
        entismapped = tab["entitiesmapped"]
        tokeep = {e for e in pchechedtabenti.values()}
        toremove = set(entismapped).difference(tokeep)
        for e in toremove:
            entismapped.remove(e)
            changes += 1
            logging.info(f"{pdatmname} - '{tab['name']}'" +
                         f" entity removed {pmodel.getlangtext(pelem=pmodel.getbyid(e)['name'], plang=pmodel.modellanguage())}")

    return changes


def import1row(pdatmname, pmodel, plang, prowidx,
               ptabname, pcolname,
               pentinames, pattrnames,
               pcheckedtabenti: dict, pcheckedcolattr: dict):
    changes = 0
    # find the table in the json structure
    tables = pmodel.getelements("tables")
    tabs = [(key, val) for key, val in tables.items() if
            (val["name"] == ptabname and val["datamodel-name+"] == pdatmname)]
    if len(tabs) != 1:
        logging.warning(f"Datamodel {pdatmname} - {ptabname} not found or redundant")
        return changes

    tabid, tab = tabs[0][0], tabs[0][1]

    # find the column in the json structure
    columns = pmodel.getelements("columns")
    cols = [(key, val) for key, val in columns.items() if (val["datamodel-name+"] == pdatmname and
                                                           val["table-name+"] == ptabname and
                                                           val["name"] == pcolname)]
    if len(cols) != 1 and nvl(pcolname) != '':
        logging.warning(f"Datamodel '{pdatmname}': table '{ptabname}', column '{pcolname}' not found or redundant")
        return changes
    colid, col = (None, None) if len(cols) == 0 else (cols[0][0], cols[0][1])
    # hurra column was found
    # find the attribute(s) in the json structure
    # find the entity in the json structure
    mainentis, subentis = [], []
    for entiname in pentinames:
        enti = pmodel.getbyfield(ptype="entities", pvalue=entiname[0], plang=plang)
        if len(enti) != 1:
            logging.warning(f"Entity '{entiname[0]}': not found or redundant")
            return changes
        mainentis.append(None if len(enti) == 0 else enti[0])
        enti = pmodel.getbyfield(ptype="entities", pvalue=entiname[1], plang=plang)
        if len(enti) != 1 and nvl(entiname[1]) != '':
            logging.warning(f"Entity '{entiname[1]}': not found or redundant")
            return changes
        subentis.append(None if len(enti) == 0 else enti[0])

    # find attributes
    attributes = pmodel.getelements("attributes")
    attrs = []
    for idx, enti in enumerate(mainentis):
        entiname = enti[1]['name'][plang]
        subentiname = "" if subentis[idx] is None else subentis[idx][1]['name'][plang]
        attr = [(key, val) for key, val in attributes.items() if (val["entity"] == enti[0] and
                                                                  val["name"][plang] == pattrnames[idx])]
        if len(attr) != 1 and nvl(pattrnames[idx]) != '':
            logging.warning(
                f"Attribute '{pattrnames[idx]}' of entity '{entiname}': not found or redundant")
            return changes
        # [(attrid,subentiid,attrname,entiname,subentiname)]
        attrs.append(None if len(attr) == 0 else (attr[0][0],
                                                  None if subentis[idx] is None else subentis[idx][0],
                                                  attr[0][1]['name'][plang],
                                                  entiname,
                                                  subentiname
                                                  )
                     )

    assert (tabid is not None and (len(mainentis) == len(subentis) == len(attrs))), \
        f"invalid value-combination for row {prowidx}"

    """ tabid,tab contain current table"""
    for enti in mainentis + subentis:
        if enti is not None:
            pcheckedtabenti[tabid] = enti[0] #mark as checked
            changes += checkandaddentimap(ptabid=tabid, ptab=tab,
                                          pentiid=enti[0], pentiname=enti[1]["name"][plang])

    if col is not None:
        for attr in attrs:
            if attr is not None:
                pcheckedcolattr[colid] = attr[0]
                changes += checkandaddcolmap(pcolid=colid, pcol=col,
                                             pattrinfo=attr
                                             )

    if pdatmname == "TestMapping":
        logging.debug(changes, ptabname, pcolname,
                      pentinames, pattrnames, attrs)
    return changes


def colidx(s):
    return mapxls.attrkey2idx(s)


def do1row(pdatmname, pws, pmodel, plang, prowidx,
           pcheckedtabenti: dict, pcheckedcolattr: dict) -> int:
    changes = 0
    tabname = pws.cell(prowidx, colidx("tableName")).value
    if tabname is None:
        logging.warning(f"****Datamodel '{pdatmname}' row {str(prowidx)} does not contain tablenName ")
        return changes
    colname = pws.cell(prowidx, colidx("columnName")).value
    # the following can be multiple lines entities with a subentity in parentheses
    """
       "Entität1
        Entität2 (Subentität)"
       returned into
       [["Entität1",None], ["Entität2","Subentität"]]
       all leading and trailing blanks, tabs or lf are removed
       """
    entinames = getmultilines(pvalue=pws.cell(prowidx, colidx("entityName")).value)
    """
        missing indices are filled with blanks,
        no parentheses will be handled 
    """
    attrnames = getmultilines(pvalue=pws.cell(prowidx, colidx("attrName")).value, pidx=len(entinames))
    assert len(entinames) == len(attrnames), \
        f"number of entitynamen {str(len(entinames))} and attribute-names {str(len(attrnames))} in row {str(prowidx)} must match"

    #####currently we do only mapping############
    # optional columns
    # colrw = None if "colrws" not in pcoldict else pcoldict["colrws"][pidx].value
    # colid = None if "colids" not in pcoldict else pcoldict["colids"][pidx].value

    # all values for one column filled.
    # check with json
    changes += import1row(pdatmname=pdatmname, pmodel=pmodel, plang=plang, prowidx=prowidx,
                          ptabname=tabname, pcolname=colname,
                          pentinames=entinames, pattrnames=attrnames,
                          pcheckedtabenti=pcheckedtabenti, pcheckedcolattr=pcheckedcolattr)
    return changes


def import1datamodel(pws, pwsname, pmodel, plang) -> int:
    myexception: Exception

    """ imports one sheet = 1 datamodel
        columns with header in row 2   mapxls.COLMAPHEADERS
        followed by entity columns   mapxls.IMHEAD
        """
    changes = 0

    # check structure of worksheet to import
    if not (pws.cell(1, 1).value == pwsname):
        logging.warning(f"Datamodelname in ws '{pwsname}'.cell(A,1) '{pws.cell(1, 1).value}' does not match sheetname")
        logging.warning(f"Datamodel '{pwsname}' skipped")
        return changes
    if not (pws.cell(1, len(mapxls.COLHEADERS) + 1).value == mapxls.IMHEAD):
        logging.warning(
            f"column title '{pws.cell(1, len(mapxls.COLHEADERS) + 1).value}' for IM-columns does not match '{mapxls.IMHEAD}'")
        logging.warning(f"Datamodel '{pwsname}' skipped")
        return changes

    for idx, title in enumerate(mapxls.COLHEADERS + mapxls.IMHEADERS, start=1):
        if not (pws.cell(2, idx).value == title):
            logging.warning(
                f"titlecolumn '{pws.cell(2, idx).value}' at index {str(idx)} does not match expected value '{title}'")
            logging.warning(f"Datamodel '{pwsname}' skipped")
            return changes

    checkedtabenti = {}  # {tableid:[entiid]}
    checkedcolattr = {}  # {coluid:[attrid]}
    for idx in range(3, len(list(pws.rows)) + 1):
        changes += do1row(pdatmname=pwsname, pws=pws, pmodel=pmodel,
                          plang=plang, prowidx=idx,
                          pcheckedtabenti=checkedtabenti,
                          pcheckedcolattr=checkedcolattr)

    changes += removenoncheckedentities(pmodel=pmodel, pdatmname=pwsname, pchechedtabenti=checkedtabenti)
    changes += removenoncheckedattributes(pmodel=pmodel, pdatmname=pwsname, pchechedcolattr=checkedcolattr)

    return changes


def importdatamodels(pwb: openpyxl.workbook.workbook.Workbook, pmodel: JSModel,
                     plang) -> int:
    changes = 0
    for wsname in filter(lambda w : w not in mapxls.WS_OVERVIEWSHEETS,
                         pwb.sheetnames):
        #replaced by filter if wsname in mapxls.WS_OVERVIEWSHEETS: continue
        ws = pwb.get_sheet_by_name(wsname)
        changes += import1datamodel(pws=ws, pwsname=wsname, pmodel=pmodel, plang=plang)
    return changes


def importmapexcel(pexcelfile, pjsonfile=None, pdbfile=None, pdryrun=False):
    """
    imports an excelfile (format as generated from listmapping) into the database
    reads for every datamodel the column-list and its mapping to the information model.
    Only this is written back into the json-file
    NO Table or columns, nor entites or attributes are inserted or deleted
    mark updates in sourceref of changed column and tables resp.
     sourcref-name is MAPIMPORT

    Improvements:
    1. if the json file was created after the excel-file, refuse merging resp. require overwrite parameter
    2. if in jsonfile there are source-updates after the creation of the excel file, check for conflicts

    params:pexcelfile file to import
        jsonfile filespec of existing file to update
                None -> take filespec from excelfile (JSON file) in Overview-tab

    """
    logging.basicConfig(level=logging.INFO)
    assert (pexcelfile is not None) and os.path.exists(pexcelfile), f"Excel not found: {pexcelfile}"
    wb = load_workbook(pexcelfile)
    ws = wb.get_sheet_by_name(mapxls.WS_OVERVIEW) if mapxls.WS_OVERVIEW in wb.sheetnames else None

    jsonfile = pjsonfile if pjsonfile is not None else getjsonfile(ws)
    assert jsonfile is not None and os.path.exists(jsonfile), f"json-file '{jsonfile}' not found"
    jsmodel = JSModel.readfromfile(jsonfile)

    dbfile = pdbfile
    if dbfile is None:
        dbfile = jsmodel.jsmodel["_imprint_"]["database"]
    assert pdryrun or os.path.exists(dbfile), f"db-file '{dbfile}' not found"

    lang = getlang(ws)
    assert lang in jsmodel.getelements("languages").keys(), \
        f"Language '{lang}' in excelfile '{pexcelfile}' not found in modellanguages in\njsonfile '{jsonfile}' "

    changes = importdatamodels(pwb=wb, pmodel=jsmodel, plang=lang)
    if changes > 0:
        # print (mirojsmodel.mirojsmodel["tables"]["TABL387"]["entitiesmapped"])
        # wb.save("/Users/stb/Downloads/testexcel2.xlsx")
        # mirojsmodel.write_json("/Users/stb/Downloads/testjson2.json")
        # wb.save(pexcelfile)
        # mirojsmodel.write_json(mirojsmodel.jsxfile)
        newjson = mergedbs.mergejs2db(pdbfile=dbfile, pdryrun=pdryrun,
                                      pmodel=jsmodel, psrcname=SOURCEREF)
        # generate new jsonfile
        newjson.write_json(destination=jsonfile)

    # fi
    logging.info(f"File '{pexcelfile}'\n\tloaded. {str(changes)} changes applied.")
    return changes


def main():
    """
    parses sysargs, reads json file and create excel mapping file out of it

    :param argv:

    :return:
    """
    parser = argparse.ArgumentParser(description='Create IM-DM mappingexcel.')
    parser.add_argument('excelfilepath', nargs=1,
                        help=f"Path of the excelfile to load.")
    parser.add_argument('--jsonfile', '-j', dest="jsonfile",
                        help=f"Filepath of jsonfile to load into. Default: JSON file found in excel Overview")
    parser.add_argument('--dbfile', '-d', dest="dbfile",
                        help=f"Filepath of database file. Default: database name found in jsonfile")
    parser.add_argument('--dryrun', '-dry', action='store_true',
                        help=f"Do not change database.")
    argparse.Namespace()
    arguments = parser.parse_args()

    # logging_level = logging.DEBUG if arguments.verbose else logging.INFO

    excelfile = Path(arguments.excelfilepath[0])

    importmapexcel(pexcelfile=excelfile,
                   pjsonfile=arguments.jsonfile,
                   pdbfile=arguments.dbfile,
                   pdryrun=arguments.dryrun)


if __name__ == '__main__':
    main()
