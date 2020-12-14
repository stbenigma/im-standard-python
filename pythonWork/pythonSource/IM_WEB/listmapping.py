# -*- coding: latin-1 -*-
import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../IM_db')
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from IM_DB import *
from IM_OBJECTS import *
from mystring import nvl
from openpyxl import Workbook
from openpyxl.styles import Alignment
import listWebdoku

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
        cell.alignment = Alignment(horizontal=phorizontal
                                   , vertical=pvertical
                                   , text_rotation=ptext_rotation
                                   , wrap_text=pwrap_text
                                   )
    # if
    """ Alignement horizontal  ?left?, ?centerContinuous?, ?center?, ?distributed?, ?fill?, ?justify?, ?right?, ?general?"""

# setcell

def writesheettabent(pwb: Workbook,pmodel,plang):
    ws = pwb.create_sheet("Table to Entity mapping")
    rowidx, colidx = 1, 1
    ws.cell(column=colidx, row=rowidx, value='Interface')
    colidx += 1
    ws.cell(column=colidx, row=rowidx, value='Table')
    colidx += 1

    cntcolidx,cntrowidx = colidx,rowidx+1
    xcounts = {}
    setcell(pws=ws,prow=rowidx+1,pcolumn=colidx,pvalue='Count',phorizontal='right')
    colidx += 1
    for idx, enti in enumerate(pmodel['entities'].values()):
        xcounts[colidx+idx] = 0
        setcell(pws=ws, pcolumn=idx + colidx, prow=rowidx, pvalue=enti['name'][plang]
                , ptext_rotation=90)
    # for
    rowidx += 2
    for sval in pmodel['systems'].values():
        for tkey in sval['tables']:
            table = pmodel['tables'][tkey]
            xcount,colidx = 0,1
            setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=sval['name'])
            colidx += 1
            ws.cell(column=colidx, row=rowidx, value=table['name'])
            colidx += 2 #platz für counter
            for entiid in pmodel['entities'].keys():
                if (entiid in table['entitiesmapped']):
                    setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue='X'
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
    for key,value in xcounts.items():
        if (value > 0):
            setcell(pws=ws, prow=cntrowidx, pcolumn=key, pvalue=value, phorizontal='right')
    rowidx += 1

    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 35
    ws.column_dimensions['C'].width = 7
    for idx in range(4, colidx): ws.column_dimensions[colnum_string(idx)].width = 3


# writesheettabent

def writesheetentitab(pwb: Workbook,pmodel,plang):
    ws = pwb.create_sheet("Entity to Table mapping")

    rowidx, colidx = 1, 1
    ws.cell(column=colidx, row=rowidx, value='Information Model')
    ws.cell(column=colidx, row=rowidx + 1, value='Entity')
    colidx += 1

    cntcolidx,cntrowidx = colidx,rowidx + 2
    setcell(pws=ws,prow=rowidx + 2,pcolumn=colidx,pvalue='Count',phorizontal='right')
    xcounts = {}
    colidx += 1
    for sval in pmodel['systems'].values():
        ws.cell(column=colidx, row=rowidx, value=sval['name'])
        for tkey in sval['tables']:
            setcell(pws=ws, pcolumn=colidx, prow=rowidx + 1, pvalue=pmodel['tables'][tkey]['name']
                    , ptext_rotation=90)
            xcounts[colidx] = 0
            colidx += 1
        # for
    # for
    rowidx += 3

    for entiid,enti in pmodel['entities'].items():
        xcount,colidx = 0,1
        setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=enti['name'][plang])
        colidx += 2 #platz für counter

        for sval in pmodel['systems'].values():
            for tkey in sval['tables']:
                if (entiid in pmodel['tables'][tkey]['entitiesmapped']):
                    setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue='X')
                    xcounts[colidx] += 1
                    xcount +=1
                # if
                colidx += 1
            # for
        # for
        if (xcount > 0):
            setcell(pws=ws, prow=rowidx, pcolumn=cntcolidx
                    , pvalue=xcount, phorizontal='right')
        rowidx += 1
    # for
    for key,value in xcounts.items():
        if (value > 0):
            setcell(pws=ws, prow=cntrowidx, pcolumn=key, pvalue=value, phorizontal='right')
    rowidx += 1

    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 7
    for idx in range(3, colidx): ws.column_dimensions[colnum_string(idx)].width = 3
# writesheetentitab

def writesheetcolattr(pwb: Workbook,pmodel,plang):
    ws = pwb.create_sheet("Columns to Attributes mapping")

    rowidx, colidx = 1, 1
    ws.cell(column=colidx + 2, row=rowidx, value='Entity')
    ws.cell(column=colidx, row=rowidx + 1, value='Interface')
    ws.cell(column=colidx + 1, row=rowidx + 1, value='Table')
    ws.cell(column=colidx + 2, row=rowidx + 1, value='Column')
    colidx += 3
    for enti in pmodel['entities'].values():
        ws.cell(column=colidx, row=rowidx, value=enti['name'][plang])
        for attr in enti['attributes']:
            cell = ws.cell(column=colidx, row=rowidx + 1, value=pmodel['attributes'][attr]['name'][plang])
            cell.alignment = Alignment(horizontal='general'
                                       , vertical='bottom'
                                       , text_rotation=90
                                       # ,wrap_text = False
                                       )
            colidx += 1
        # for
    # for
    rowidx += 2

    for skey,sval in pmodel['systems'].items():
        for tkey in sval['tables']:
            colidx = 1
            tabl = pmodel['tables'][tkey]
            for ckey in tabl['columns']:
                ws.cell(column=colidx, row=rowidx, value=sval['name'])
                colidx += 1
                ws.cell(column=colidx, row=rowidx, value=tabl['name'])
                colidx += 1
                ws.cell(column=colidx, row=rowidx, value=pmodel['columns'][ckey]['name'])
                colidx += 1
                for enti in pmodel['entities'].values():
                    for attrid in enti['attributes']:
                        attrcols = pmodel['attributes'][attrid]['columnsmapped']
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

def valmiteol(pval,padd):
    eoladd = '' if (pval == '') else EOL
    return pval + eoladd + padd


def writesheetattrcol(pwb: Workbook,pmodel,plang):
    ws = pwb.create_sheet("Attributes to Columns mapping")

    rowidx, colidx = 1, 1
    ws.cell(column=colidx, row=rowidx, value='Information Model')
    ws.cell(column=colidx, row=rowidx + 1, value='Entity')
    ws.cell(column=colidx + 1, row=rowidx + 1, value='Attribute')
    colidx += 2
    for skey,sval in pmodel['systems'].items():
        ws.cell(column=colidx, row=rowidx, value=sval['name'])
        setcell(pws=ws, pcolumn=colidx, prow=rowidx + 1, pvalue="Table")
        colidx += 1
        setcell(pws=ws, pcolumn=colidx, prow=rowidx + 1, pvalue="Column")
        colidx += 1
        setcell(pws=ws, pcolumn=colidx, prow=rowidx + 1, pvalue="Ext-ID")
        colidx += 1
    # for
    rowidx += 2

    for entiid, enti in pmodel['entities'].items():
        colidx = 1

        """Entity Table Mapping """
        setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=enti['name'][plang])
        colidx += 2  # Attribute überspringen

        for sval in pmodel['systems'].values():
            valuetab = ''
            for tabkey in sval['tables']:
                if (tabkey in enti['tablesmapped']):
                    valuetab = valmiteol(valuetab ,pmodel['tables'][tqabkey]['name'])
                # if
            # for
            if valuetab != '':
                setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=valuetab
                                , pwrap_text=True)
            colidx += 3  # skip column and ID col
        # for
        rowidx += 1

        for attrid in enti['attributes']:
            colidx = 1
            attr = pmodel['attributes'][attrid]
            setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=enti['name'][plang]
                    , pwrap_text=True)
            colidx += 1
            setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=attr['name'][plang]
                    , pwrap_text=True)
            colidx += 1
            for sval in pmodel['systems'].values():
                valuecol = ''
                valuetab = ''
                valueid = ''
                for tkey in sval['tables']:
                    tabl = pmodel['tables'][tkey]
                    for ckey in tabl['columns']:
                        colu = pmodel['columns'][ckey]
                        if (attrid in colu['attributes-mapped']):
                            valuetab = valmiteol(pval=valuetab,padd=tabl['name'])
                            valuecol = valmiteol(pval=valuecol,padd=colu['name'])
                            valueid = valmiteol(pval=valueid,padd=nvl(colu['interface_col_id']))
                        # if
                    # for
                    if (valuecol != ''):
                        setcell(pws=ws, pcolumn=colidx, prow=rowidx, pvalue=valuetab
                                , pwrap_text=True)
                        setcell(pws=ws, pcolumn=colidx+1, prow=rowidx, pvalue=valuecol
                                , pwrap_text=True)
                        setcell(pws=ws, pcolumn=colidx+2, prow=rowidx, pvalue=valueid
                                , pwrap_text=True)
                        headcell = ws.cell(column=colidx, row=2)
                        headcell.alignment = Alignment(text_rotation=0, wrap_text=True)
                # for
                colidx += 3
            # for
            rowidx += 1
        # for
    # for

    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 35
    for idx in range(3, colidx):
        width = 35
        ws.column_dimensions[colnum_string(idx)].width = width
    # for
# writesheetattrcol

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
# writesheetattrcolold

def writesheetinterface(pwb, pintfid, pmodel, plang):
    intf = pmodel['systems'][pintfid]
    ws = pwb.active

    rowidx, colidx = 1, 1
    ws.cell(column=colidx, row=rowidx, value=intf['name'])
    ws.cell(column=colidx, row=rowidx + 1, value='tableName')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='columnName')
    colidx += 1
    ws.cell(column=colidx, row=rowidx + 1, value='attr-ID')
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

    for tabid in intf['tables']:
        tabl = pmodel['tables'][tabid]
        firstrowidx = rowidx
        for colid in tabl['columns']:
            colu = pmodel['columns'][colid]
            valueenti,valueattr = '',''
            for attrid in colu['attributes-mapped']:
                attr = pmodel['attributes'][attrid]
                enti = pmodel['entities'][attr['entity']]
                valueenti = valmiteol(pval=valueenti, padd=enti['name'][plang])
                valueattr = valmiteol(pval=valueattr, padd=attr['name'][plang])
            # for
            colidx = 1
            ws.cell(column=colidx, row=rowidx, value=tabl['name'])
            colidx += 1
            setcell(pws=ws,pcolumn=colidx, prow=rowidx, pvalue=colu['name'],pwrap_text=True)
            colidx += 1
            ws.cell(column=colidx, row=rowidx, value=colu['interface_col_id'])
            colidx +=1
            doma = pmodel['domains'][colu['domain']]
            ws.cell(column=colidx, row=rowidx, value=doma['name'][plang] if doma['origin']== Domain.DOMAIN else None)
            colidx +=1
            ws.cell(column=colidx, row=rowidx, value=colu['datatype'])
            colidx +=1
            #ws.cell(column=colidx, row=rowidx, value=colu['mandatory'])
            colidx +=1
            #ws.cell(column=colidx, row=rowidx, value=colu['default Value'])
            colidx +=1
            setcell(pws=ws,pcolumn=colidx, prow=rowidx, pvalue=colu['descr'],pwrap_text=True)
            colidx +=1
            #setcell(pws=ws,pcolumn=colidx, prow=rowidx, pvalue=colu['rules'],pwrap_text=True)
            colidx +=1
            setcell(pws=ws,pcolumn=colidx, prow=rowidx, pvalue=valueenti,pwrap_text=True)
            colidx +=1
            setcell(pws=ws,pcolumn=colidx, prow=rowidx, pvalue=valueattr,pwrap_text=True)
            rowidx += 1
        # for
        if firstrowidx == rowidx:
            """no columns written write the entity-Mappings if present"""
            valueenti = ''
            for entiid in tabl['entitiesmapped']:
                enti = pmodel['entities'][entiid]
                valueenti = valmiteol(pval=valueenti, padd=enti['name'][plang])
            #for
            ws.cell(column=1, row=rowidx, value=tabl['name'])
            setcell(pws=ws,pcolumn=10 , prow=rowidx, pvalue=valueenti,pwrap_text=True)
            rowidx += 1
        #if
    #for
    ch = 'A'
    ws.column_dimensions[ch].width = 35
    ch = chr(ord(ch)+1)
    ws.column_dimensions[ch].width = 40
    ch = chr(ord(ch)+1)
    ws.column_dimensions[ch].width = 20
    ch = chr(ord(ch)+1)
    ws.column_dimensions[ch].width = 20
    ch = chr(ord(ch)+1)
    ws.column_dimensions[ch].width = 20
    ch = chr(ord(ch)+1)
    ws.column_dimensions[ch].width = 10
    ch = chr(ord(ch)+1)
    ws.column_dimensions[ch].width = 20
    ch = chr(ord(ch)+1)
    ws.column_dimensions[ch].width = 35
    ch = chr(ord(ch)+1)
    ws.column_dimensions[ch].width = 35
    ch = chr(ord(ch)+1)
    ws.column_dimensions[ch].width = 35
    ch = chr(ord(ch)+1)
    ws.column_dimensions[ch].width = 35

# writesheetinterface

def writexls(pfilename: str,pmodel,plang):
    wb = Workbook()

    writesheettabent(pwb=wb,pmodel=pmodel,plang=plang)
    writesheetentitab(pwb=wb,pmodel=pmodel,plang=plang)
    writesheetattrcol(pwb=wb,pmodel=pmodel,plang=plang)
    #    writesheetcolattr(pwb=wb)
    wb.remove(wb.worksheets[0])
    wb.save(filename=pfilename)
# writexls

# def createFile(pfilename):
#     global fileCSV
#     csvfile = parameters.webDirec() + pfilename
#     if os.path.exists(csvfile):
#         os.remove(csvfile)
#     fileCSV = open(csvfile, 'w')
#
#
# # createFile

# def closefile():
#     global fileCSV
#     fileCSV.close()
#
#
# # closefile

# def write(*args, **kwargs):
#     global fileCSV
#     sep = kwargs['sep'] if 'sep' in kwargs else ''
#     str = sep.join(arg for arg in args)
#     fileCSV.write(str)
#
#
# def writeln(*args, **kwargs):
#     write(*args, **kwargs)
#     write(EOL)


# def listtabenti():
#     global entities
#     global attributes
#     global tables
#     global schnittstellen
#     global tabentimap
#
#     createFile(pfilename=parameters.odmModelName() + '_tabenti.csv')
#     write('\ufeff')
#     topheader = 'Interface' + CSVSEP + 'Table' + CSVSEP + CSVSEP.join(e[0] for e in entities.values())
#     writeln(topheader)
#     for skey, sval in schnittstellen.items():
#         for tkey, tval in sval.items():
#             writeln(skey, tval[0], CSVSEP.join(tables[tkey][3]), sep=CSVSEP)
#     print("Erstellt: {}".format(fileCSV.name))
#     closefile()
#
#
# # listtabenti


# def listcolattr():
#     createFile(pfilename=parameters.odmModelName() + '_colattr.csv')
#     write('\ufeff')
#     topheader = CSVSEP + CSVSEP + 'Entity' + CSVSEP
#     subheader = 'Interface' + CSVSEP + 'Table' + CSVSEP + 'Column' + CSVSEP
#     for enti in entities.values():
#         attrs = enti[2]
#         topheader += enti[0] + CSVSEP + CSVSEP.join('' for at in attrs)[:-1]
#         subheader += CSVSEP + CSVSEP.join(at[0] for at in attrs.values())
#     writeln(topheader)
#     writeln(subheader)
#     for skey, sval in schnittstellen.items():
#         for tkey, tval in sval.items():
#             for ckey, cval in tval[1].items():
#                 writeln(skey, tval[0], cval[0], CSVSEP.join(columns[ckey][3]), sep=CSVSEP)
#     print("Erstellt: {}".format(fileCSV.name))
#     closefile()
#
#
# # listcolattr


def writeintfxls(pfilepath: str,pmodel,plang):

    #    writesheetcolattr(pwb=wb)
    for intfid,intf in pmodel['systems'].items():
        wb = Workbook()
        writesheetinterface(pwb=wb, pintfid=intfid, pmodel=pmodel, plang=plang)
        wb.save(filename=pfilepath+ intf['name']  + '.xlsx')
# writexls

def istintabentimap(tabid, entiid):
    return (tabid in tabentimap) and (entiid in tabentimap[tabid])


# istintabentimap

def istincolattrmap(colid, attrid):
    return (colid in colattrmap) and (attrid in colattrmap[colid])


# istincolattrmap

def stripeol(str):
    retval = re.sub("\n+", "\n", str)
    retval = retval.strip(EOL)
    return retval
# stripeol



# def filllists(plang):
#     entities = {enti.enti_id: [enti.enti_name
#         , {tem[0]: [t for t in tem[1].keys()]
#            for tem in TablEntiMap.tablelist(pentiid=enti.enti_id)}
#         , {attr.attr_id: [attr.attr_displ_name, attr.attr_tech_name]
#            for attr in enti.getattributes()}
#                                ]
#                 for enti in Entity.select()}
#     attributes = {attr.attr_id: [attr.attr_displ_name, attr.attr_tech_name, attr.attr_enti_id, attr.attr_rela_id] for attr
#                   in Attribute.select()}
#     tables = {tabl.tabl_id: [tabl.tabl_name
#         , Interface().getbyid(tabl.tabl_intf_id).getname()
#         , {c.colu_id: c.colu_column_name for c in tabl.getcolumns()}
#                              ]
#               for tabl in Table.select()}
#
#     columns = {scha.colu_id: [scha.colu_column_name, scha.colu_tabl_id, scha.colu_ext_system_id]
#                for scha in Column.select()}
#     schnittstellen = {schn.intf_name:
#                           {tabl.tabl_id: [tabl.tabl_name
#                                         , {c.colu_id: [c.colu_column_name, c.colu_ext_system_id]
#                                             for c in tabl.getcolumns()
#                                            }
#                                         ] for tabl in Table.selectbyschnid(schn.intf_id)
#                            }
#                       for schn in Interface.select()}
#     tabentimap = TablEntiMap.extendedtabentimap()
#     for tkey, tval in tables.items():
#         matentry = lambda tabid, entiid: 'X' if (tabid in tabentimap) and (entiid in tabentimap[tabid]) else ''
#         maps = [matentry(tkey, e) for e in entities.keys()]
#         tval.append(maps)
#     # for
#     for ekey, eval in entities.items():
#         matentry = lambda tabid, entiid: 'X' if (tabid in tabentimap) and (entiid in tabentimap[tabid]) else ''
#         maps = [matentry(tkey, ekey) for tkey in tables.keys()]
#         eval.append(maps)
#     # for
#     colattrmap = AttrTransf.colattrmap()
#     for colid, cval in columns.items():
#         matentry = lambda colid, attrid: 'X' if (istincolattrmap(colid, attrid)) else ''
#         maps = [matentry(colid, attrid) for attrid in attributes.keys()]
#         cval.append(maps)
#     # for
#
#
# #    print (len(entities),entities)
# #    print(len(attributes),attributes)
# #    print (len(tables),tables)
# #    print (len(schnittstellen),schnittstellen)
# #    print (len(mapping),mapping)
# #    print(len(colattrmap),colattrmap)
# # filllists

def main(pdirec, plang):
    parameters.initparam(p_callarg=pdirec)
    logmessages.initlog('createMapping')

    print("listmapping", parameters.odmBaseDirec(), parameters.odmModelName())

    if plang is not None:
        Languagetext.reportLang(plang.lower())
    else:
        Languagetext.reportLang(parameters.dbDefaultLang())

    dbConnect.openDB(p_filepath=parameters.dbFilePath());
    #filllists(plang=Languagetext.reportLang())
    model = listWebdoku.createJSON.sql2json()
    dbConnect.myDbConn.close()
    writexls(pfilename=parameters.webDirec() + 'Mappingtables_' + parameters.odmModelName() + '.xlsx',pmodel=model,plang=Languagetext.reportLang())
    writeintfxls(pfilepath=parameters.webDirec(),pmodel=model,plang=Languagetext.reportLang())
    logmessages.showmessages("Model {}: mappinglist form database {}\n  => created in file {}"
                             .format(parameters.odmModelName(), parameters.dbFilePath()
                               , parameters.webDirec() + 'Mappingtables_' + parameters.odmModelName() + '.xlsx'))


# main

if __name__ == '__main__':
    direc = sys.argv[1]
    lang = sys.argv[2] if (len(sys.argv) > 2) else None
    main(pdirec=direc, plang=lang)
