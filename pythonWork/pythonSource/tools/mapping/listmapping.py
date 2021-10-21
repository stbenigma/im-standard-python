# -*- coding: latin-1 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../IM_db')
from IM_JSON import JSModel
from IM_OBJECTS import Domain
from mystring import nvl
from openpyxl import Workbook, styles

fileCSV = None
EOL: str = '\n'
CSVSEP: str = ';'


def colnum_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string


# colum_string

def cell_string(n, m):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string + str(m)


# cell_string

def setcell(pws, pcolumn, prow, pvalue
            , phorizontal=None, pvertical=None
            , ptext_rotation=None, pwrap_text=None):
    cell = pws.cell(column=pcolumn, row=prow, value=pvalue)
    if (phorizontal is not None or pvertical is not None \
            or ptext_rotation is not None or pwrap_text is not None):
        cell.alignment = styles.Alignment(horizontal=phorizontal
                                          , vertical=pvertical
                                          , text_rotation=ptext_rotation
                                          , wrap_text=pwrap_text
                                          )
    # if
    """ Alignement horizontal  ?left?, ?centerContinuous?, ?center?, ?distributed?, ?fill?, ?justify?, ?right?, ?general?"""


# setcell

def writesheettabent(pwb: Workbook, pmodel, plang):
    ws = pwb.create_sheet("Table to Entity mapping")
    rowidx, colidx = 1, 1
    ws.cell(column=colidx, row=rowidx, value='Interface')
    colidx += 1
    ws.cell(column=colidx, row=rowidx, value='Table')
    colidx += 1

    cntcolidx, cntrowidx = colidx, rowidx + 1
    xcounts = {}
    setcell(pws=ws, prow=rowidx + 1, pcolumn=colidx, pvalue='Count', phorizontal='right')
    colidx += 1
    for idx, enti in enumerate(pmodel.getelements('entities').values()):
        xcounts[colidx + idx] = 0
        setcell(pws=ws, pcolumn=idx + colidx, prow=rowidx, pvalue=enti['name'][plang]
                , ptext_rotation=90)
    # for
    rowidx += 2
    for sval in pmodel.getelements('systems').values():
        for tkey in sval['tables+']:
            table = pmodel.getbyid(tkey)
            xcount, colidx = 0, 1
            setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=sval['name'])
            colidx += 1
            ws.cell(column=colidx, row=rowidx, value=table['name'])
            colidx += 2  # platz für counter
            for entiid in pmodel.getelements('entities').keys():
                if (entiid in table['entitiesmapped']):
                    setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=table["CRUD"]
                            , phorizontal="center", pvertical="center")
                    xcount += 1
                    xcounts[colidx] += 1
                # fi
                colidx += 1
            # for
            if (xcount > 0):
                setcell(pws=ws, prow=rowidx, pcolumn=cntcolidx
                        , pvalue=xcount, phorizontal='right')
            rowidx += 1
        # for
    # for
    for key, value in xcounts.items():
        if (value > 0):
            setcell(pws=ws, prow=cntrowidx, pcolumn=key, pvalue=value, phorizontal='right')
    rowidx += 1

    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 35
    ws.column_dimensions['C'].width = 7
    for idx in range(4, colidx): ws.column_dimensions[colnum_string(idx)].width = 5


# writesheettabent

def writesheetentitab(pwb: Workbook, pmodel, plang):
    ws = pwb.create_sheet("Entity to Table mapping")

    rowidx, colidx = 1, 1
    ws.cell(column=colidx, row=rowidx, value='Information Model')
    ws.cell(column=colidx, row=rowidx + 1, value='Entity')
    colidx += 1

    cntcolidx, cntrowidx = colidx, rowidx + 2
    setcell(pws=ws, prow=rowidx + 2, pcolumn=colidx, pvalue='Count', phorizontal='right')
    xcounts = {}
    colidx += 1
    for sval in pmodel.getelements("systems").values():
        ws.cell(column=colidx, row=rowidx, value=sval['name'])
        for tkey in sval['tables+']:
            setcell(pws=ws, pcolumn=colidx, prow=rowidx + 1, pvalue=pmodel.getbyid(tkey)['name']
                    , ptext_rotation=90)
            xcounts[colidx] = 0
            colidx += 1
        # for
    # for
    rowidx += 3

    for entiid, enti in pmodel.getelements("entities").items():
        xcount, colidx = 0, 1
        setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=enti['name'][plang])
        colidx += 2  # platz für counter

        for sval in pmodel.getelements("systems").values():
            for tkey in sval['tables+']:
                if (entiid in pmodel.getbyid(tkey)['entitiesmapped']):
                    setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=pmodel.getbyid(tkey)["CRUD"])
                    xcounts[colidx] += 1
                    xcount += 1
                # if
                colidx += 1
            # for
        # for
        if (xcount > 0):
            setcell(pws=ws, prow=rowidx, pcolumn=cntcolidx
                    , pvalue=xcount, phorizontal='right')
        rowidx += 1
    # for
    for key, value in xcounts.items():
        if (value > 0):
            setcell(pws=ws, prow=cntrowidx, pcolumn=key, pvalue=value, phorizontal='right')
    rowidx += 1

    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 7
    for idx in range(3, colidx): ws.column_dimensions[colnum_string(idx)].width = 5


# writesheetentitab

def writesheetcolattr(pwb: Workbook, pmodel, plang):
    ws = pwb.create_sheet("Columns to Attributes mapping")

    rowidx, colidx = 1, 1
    ws.cell(column=colidx + 2, row=rowidx, value='Entity')
    ws.cell(column=colidx, row=rowidx + 1, value='Interface')
    ws.cell(column=colidx + 1, row=rowidx + 1, value='Table')
    ws.cell(column=colidx + 2, row=rowidx + 1, value='Column')
    colidx += 3
    for enti in pmodel.getelements("entities").values():
        ws.cell(column=colidx, row=rowidx, value=enti['name'][plang])
        for attr in enti['attributes']:
            cell = ws.cell(column=colidx, row=rowidx + 1, value=pmodel.getbyid(attr)['name'][plang])
            cell.alignment = Alignment(horizontal='general'
                                       , vertical='bottom'
                                       , text_rotation=90
                                       # ,wrap_text = False
                                       )
            colidx += 1
        # for
    # for
    rowidx += 2

    for skey, sval in pmodel.getelements("systems").items():
        for tkey in sval['tables+']:
            colidx = 1
            tabl = pmodel.getbyid(tkey)
            for ckey in tabl['columns']:
                ws.cell(column=colidx, row=rowidx, value=sval['name'])
                colidx += 1
                ws.cell(column=colidx, row=rowidx, value=tabl['name'])
                colidx += 1
                ws.cell(column=colidx, row=rowidx, value=pmodel.getbyid(ckey)['name'])
                colidx += 1
                for enti in pmodel.getelements("entities").values():
                    for attrid in enti['attributes']:
                        attrcols = pmodel.getbyid(attrid)['columnsmapped']
                        if (skey in attrcols.keys()) and (ckey in attrcols[skey]):
                            ws.cell(column=colidx, row=rowidx, value='X')
                        # if
                        colidx += 1
                    # for
                # for
                rowidx += 1
            # for
        # for
    # for

    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 35
    ws.column_dimensions['C'].width = 35
    for idx in range(4, colidx): ws.column_dimensions[colnum_string(idx)].width = 3


# writesheetcolattr

def valmiteol(pval, padd):
    eoladd = '' if (pval == '') else EOL
    return pval + eoladd + padd


def writesheetattrcol(pwb: Workbook, pmodel, plang):
    ws = pwb.create_sheet("Attributes to Columns mapping")

    rowidx, colidx = 1, 1
    ws.cell(column=colidx, row=rowidx, value='Information Model')
    ws.cell(column=colidx, row=rowidx + 1, value='Entity')
    ws.cell(column=colidx + 1, row=rowidx + 1, value='Attribute')
    colidx += 2
    for skey, sval in pmodel.getelements("systems").items():
        ws.cell(column=colidx, row=rowidx, value=sval['name'])
        setcell(pws=ws, pcolumn=colidx, prow=rowidx + 1, pvalue="Table")
        colidx += 1
        setcell(pws=ws, pcolumn=colidx, prow=rowidx + 1, pvalue="Column")
        colidx += 1
        setcell(pws=ws, pcolumn=colidx, prow=rowidx + 1, pvalue="RW")
        colidx += 1
        setcell(pws=ws, pcolumn=colidx, prow=rowidx + 1, pvalue="Ext-ID")
        colidx += 1
    # for
    rowidx += 2

    attrsort = [[key, pmodel.getbyid(val["entity"])["name"][plang], val['name'][plang]] for key, val in
                pmodel.getelements("attributes").items()]
    attrsort = sorted(attrsort, key=lambda x: x[1] + "-" + x[2])
    for attr in attrsort:
        attrid, entiname, attrname = attr[0], attr[1], attr[2]
        colidx = 1
        setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=entiname
                , pwrap_text=True)
        colidx += 1
        setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=attrname
                , pwrap_text=True)
        colidx += 1
        for sval in pmodel.getelements("systems").values():
            valuecol = ''
            valuetab = ''
            valuerw = ''
            valueid = ''
            for tkey in sval['tables+']:
                tabl = pmodel.getbyid(tkey)
                for ckey in tabl['columns+']:
                    colu = pmodel.getbyid(ckey)
                    if (attrid in colu['attributesmapped']):
                        valuetab = valmiteol(pval=valuetab, padd=tabl['name'])
                        valuecol = valmiteol(pval=valuecol, padd=colu['name'])
                        valuerw = valmiteol(pval=valuerw, padd=nvl(colu['R/W']))
                        valueid = valmiteol(pval=valueid, padd=nvl(colu['interface_col_id']))
                    # if
                # for
                if (valuecol != ''):
                    setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=valuetab
                            , pwrap_text=True)
                    setcell(pws=ws, pcolumn=colidx + 1, prow=rowidx, pvalue=valuecol
                            , pwrap_text=True)
                    setcell(pws=ws, pcolumn=colidx + 2, prow=rowidx, pvalue=valuerw
                            , pwrap_text=True)
                    setcell(pws=ws, pcolumn=colidx + 3, prow=rowidx, pvalue=valueid
                            , pwrap_text=True)
                    headcell = ws.cell(column=colidx, row=3)
                    headcell.alignment = styles.Alignment(text_rotation=0, wrap_text=True)
            # for
            colidx += 4
        # for
        rowidx += 1
    # for

    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 35
    for idx in range(3, colidx):
        colwidth = {0: 35, 1: 5, 2: 15, 3: 35}
        """3 4 .5 6 7   8 .9 10 11"""
        ws.column_dimensions[colnum_string(idx)].width = colwidth[idx % 4]
    # for
    return


def writesheetattrcolold(pwb: Workbook):
    ws = pwb.create_sheet("Attributes to Columns mapping")

    rowidx, colidx = 1, 1
    ws.cell(column=colidx, row=rowidx, value='Information Model')
    ws.cell(column=colidx, row=rowidx + 1, value='Entity')
    colidx += 1
    ws.cell(column=colidx + 1, row=rowidx + 1, value='Attribute')
    colidx += 1
    for intf_name, tabs in schnittstellen.items():
        ws.cell(column=colidx, row=rowidx, value=intf_name)
        for tabkey in tabs.values():
            setcell(pws=ws, pcolumn=colidx, prow=rowidx + 1, pvalue=tabkey[0]
                    , ptext_rotation=90)
            colidx += 1
        # for
    # for
    rowidx += 2

    for enti in entities.values():
        for attrid, attr in enti[2].items():
            colidx = 1
            setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=enti[0]
                    , pwrap_text=True)
            colidx += 1
            setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=attr[0]
                    , pwrap_text=True)
            colidx += 1
            for skey, sval in schnittstellen.items():
                for tkey, tval in sval.items():
                    value = ''
                    for ckey, cval in tval[1].items():
                        if (istincolattrmap(ckey, attrid)):
                            value += '' if (value == '') else EOL
                            value += cval[0]
                        # if
                    # for
                    if (value != ''):
                        setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=value
                                , pwrap_text=True)
                        headcell = ws.cell(column=colidx, row=2)
                        headcell.alignment = Alignment(text_rotation=0, wrap_text=True)
                    colidx += 1
                # for
            # for
            rowidx += 1
        # for
    # for

    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 35
    for idx in range(3, colidx):
        width = 5 if (ws.cell(column=idx, row=2).alignment.text_rotation == 90) else 25
        ws.column_dimensions[colnum_string(idx)].width = width
    # for
    return


def writesheetinterface(pwb, pintfid, pmodel, plang):
    intf = pmodel.getbyid(pintfid)
    ws = pwb.create_sheet(intf["name"])

    rowidx, colidx = 1, 1
    ws.cell(column=colidx, row=rowidx, value=intf['name'])
    ws.cell(column=colidx, row=rowidx + 1, value='tableName')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='tableCRUD')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='columnName')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='columnRW')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='column-ID')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='domain')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='dataType')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='mand.')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='default value')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='descr')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='rules')
    colidx += 1
    ws.cell(column=colidx, row=rowidx, value='Information Model')
    ws.cell(column=colidx, row=rowidx + 1, value='entityName')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='attrName')
    rowidx += 2

    for tabid in intf['tables+']:
        tabl = pmodel.getbyid(tabid)
        firstrowidx = rowidx
        for colid in tabl['columns+']:
            colu = pmodel.getbyid(colid)
            valueenti, valueattr = '', ''
            for attrid in colu['attributesmapped']:
                attr = pmodel.getbyid(attrid)
                enti = pmodel.getbyid(attr['entity'])
                valueenti = valmiteol(pval=valueenti, padd=enti['name'][plang])
                valueattr = valmiteol(pval=valueattr, padd=attr['name'][plang])
            # for
            colidx = 1
            ws.cell(column=colidx, row=rowidx, value=tabl['name'])
            colidx += 1
            ws.cell(column=colidx, row=rowidx, value=tabl['CRUD'])
            colidx += 1
            setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=colu['name'], pwrap_text=True)
            colidx += 1
            setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=colu['R/W'])
            colidx += 1
            ws.cell(column=colidx, row=rowidx, value=colu['interface_col_id'])
            colidx += 1
            doma = pmodel.getbyid(colu['domain'])
            ws.cell(column=colidx, row=rowidx, value=doma['name'][plang] if doma['origin'] == Domain.DOMAIN else None)
            colidx += 1
            ws.cell(column=colidx, row=rowidx, value=colu['datatype'])
            colidx += 1
            # ws.cell(column=colidx, row=rowidx, value=colu['mandatory'])
            colidx += 1
            # ws.cell(column=colidx, row=rowidx, value=colu['default Value'])
            colidx += 1
            setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=colu['descr'], pwrap_text=True)
            colidx += 1
            # setcell(pws=ws,pcolumn=colidx, prow=rowidx, pvalue=colu['rules'],pwrap_text=True)
            colidx += 1
            setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=valueenti, pwrap_text=True)
            colidx += 1
            setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=valueattr, pwrap_text=True)
            rowidx += 1
        # for
        if firstrowidx == rowidx:
            """no columns written write the entity-Mappings if present"""
            valueenti = ''
            for entiid in tabl['entitiesmapped']:
                enti = pmodel.getbyid(entiid)
                valueenti = valmiteol(pval=valueenti, padd=enti['name'][plang])
            # for
            colidx = 1
            ws.cell(column=colidx, row=rowidx, value=tabl['name'])
            colidx += 1
            ws.cell(column=colidx, row=rowidx, value=tabl['CRUD'])
            colidx += 1
            setcell(pws=ws, pcolumn=12, prow=rowidx, pvalue=valueenti, pwrap_text=True)
            rowidx += 1
        # if
    # for
    ch = 'A'
    ws.column_dimensions[ch].width = 35
    ch = chr(ord(ch) + 1)
    ws.column_dimensions[ch].width = 10
    ch = chr(ord(ch) + 1)
    ws.column_dimensions[ch].width = 40
    ch = chr(ord(ch) + 1)
    ws.column_dimensions[ch].width = 10
    ch = chr(ord(ch) + 1)
    ws.column_dimensions[ch].width = 20
    ch = chr(ord(ch) + 1)
    ws.column_dimensions[ch].width = 20
    ch = chr(ord(ch) + 1)
    ws.column_dimensions[ch].width = 20
    ch = chr(ord(ch) + 1)
    ws.column_dimensions[ch].width = 10
    ch = chr(ord(ch) + 1)
    ws.column_dimensions[ch].width = 20
    ch = chr(ord(ch) + 1)
    ws.column_dimensions[ch].width = 35
    ch = chr(ord(ch) + 1)
    ws.column_dimensions[ch].width = 35
    ch = chr(ord(ch) + 1)
    ws.column_dimensions[ch].width = 35
    ch = chr(ord(ch) + 1)
    ws.column_dimensions[ch].width = 35
    return


def writexls(pfilename: str, pmodel, plang):
    wb = Workbook()
    writesheettabent(pwb=wb, pmodel=pmodel, plang=plang)
    writesheetentitab(pwb=wb, pmodel=pmodel, plang=plang)
    writesheetattrcol(pwb=wb, pmodel=pmodel, plang=plang)
    #    writesheetcolattr(pwb=wb)
    wb.remove(wb.worksheets[0])
    wb.save(filename=pfilename)
    return


def writeoverview(pwb, pmodel):
    systems = pmodel.getelements('INTF')
    entis = pmodel.getelements('ENTI')
    relas = pmodel.getelements('RELA')
    attrs = pmodel.getelements('ATTR')
    tabs = pmodel.getelements('TABL')
    cols = pmodel.getelements('COLU')
    ws = pwb.create_sheet("Overview")
    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 15
    rowidx, colidx = 1, 1
    ws.cell(column=colidx, row=rowidx, value='System')
    ws.cell(column=colidx + 1, row=rowidx, value='Tables')
    ws.cell(column=colidx + 2, row=rowidx, value='Enti/Rela mapped')
    ws.cell(column=colidx + 3, row=rowidx, value='Columns')
    ws.cell(column=colidx + 4, row=rowidx, value='Attributes mapped')
    for syskey, sys in systems.items():
        rowidx += 1
        c = ws.cell(column=1, row=2)
        c.alignment = styles.Alignment(horizontal='general'
                                       , vertical='bottom'
                                       , text_rotation=0,
                                       wrap_text=False,
                                       shrink_to_fit=False,
                                       indent=0)
        ws.cell(column=colidx, row=rowidx, value=sys['name'])
        ws.cell(column=colidx + 1, row=rowidx, value=len(sys["tables+"]))
        ws.cell(column=colidx + 2, row=rowidx
                , value=sum([len(t["entitiesmapped"]) + len(t["relationsmapped"]) for t in tabs.values() if
                             t["interface-id"] == syskey]))
        ws.cell(column=colidx + 3, row=rowidx
                , value=len([c["name"] for c in cols.values() if c["interface-id+"] == syskey]))
        ws.cell(column=colidx + 4, row=rowidx
                , value=sum([len(c["attributesmapped"]) for c in cols.values() if c["interface-id+"] == syskey]))
    # for
    rowidx += 2
    ws.cell(column=colidx, row=rowidx, value='Information Model')
    ws.cell(column=colidx + 1, row=rowidx, value='Entities/Relations')
    ws.cell(column=colidx + 2, row=rowidx, value='Tables mapped')
    ws.cell(column=colidx + 3, row=rowidx, value='Attrbutes')
    ws.cell(column=colidx + 4, row=rowidx, value='Columns-Mapped')
    rowidx += 1
    ws.cell(column=colidx + 1, row=rowidx, value=len(entis))
    ws.cell(column=colidx + 2, row=rowidx, value=sum([len(e["tablesmapped+"]) for e in entis.values()])
                                                 + sum([len(e["tablesmapped+"]) for e in relas.values()]))
    ws.cell(column=colidx + 3, row=rowidx, value=len(attrs))
    ws.cell(column=colidx + 4, row=rowidx, value=sum([len(a["columnsmapped+"]) for a in attrs.values()]))

    return


def writeintfxls(pfilename: str, pmodel, plang):
    #    writesheetcolattr(pwb=wb)
    wb = Workbook()
    writeoverview(pwb=wb, pmodel=pmodel)
    writesheettabent(pwb=wb, pmodel=pmodel, plang=plang)
    writesheetentitab(pwb=wb, pmodel=pmodel, plang=plang)
    writesheetattrcol(pwb=wb, pmodel=pmodel, plang=plang)

    for intfid, intf in pmodel.getelements('systems').items():
        writesheetinterface(pwb=wb, pintfid=intfid, pmodel=pmodel, plang=plang)
    wb.remove(wb.worksheets[0])
    wb.save(filename=pfilename)
    return


def istintabentimap(tabid, entiid):
    return (tabid in tabentimap) and (entiid in tabentimap[tabid])


def istincolattrmap(colid, attrid):
    return (colid in colattrmap) and (attrid in colattrmap[colid])


def stripeol(str):
    retval = re.sub("\n+", "\n", str)
    retval = retval.strip(EOL)
    return retval


def createAllMapping(pjsonfile, plang):
    JSONEXTENSION = '.json'
    jsmodel = JSModel.readfromfile(pfilename=pjsonfile)
    lang = plang if plang is not None else jsmodel.jsmodel["model"]["language"]
    filename = pjsonfile[:-len(JSONEXTENSION)] + '_datamodels'
    fileext = '.xlsx'

    #    writexls(pfilename= filename + fileext,pmodel=model,plang=lang)
    writeintfxls(pfilename=filename + fileext, pmodel=jsmodel, plang=lang)
    print("Model {}: \n  => created in file {}"
          .format(jsmodel.jsmodel["model"]["name"]
                  , filename + fileext))
    return


if __name__ == '__main__':
    jsonfile = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv) > 2) else None
    createAllMapping(pjsonfile=jsonfile, plang=lang)
