from . import printdiagHTML, HTMLExport

import re


def putrefinsvg(export: HTMLExport, ptext, pdatm):
    retval = ptext
    retval  = re.sub(r'<svg xmlns="http://www.w3.org/2000/svg"',
                     r'<svg id="{}-SVG" xmlns="http://www.w3.org/2000/svg"'.format(pdatm["datamodel-id+"]), retval)
    for tabid in pdatm["tables+"]:
        tabl = export.getelement(tabid)
        try:
            odmref = tabl["sourceref"]["ODM"][0]
        except:
            continue

        refid = "{}-{}".format(re.escape(odmref[:8]), re.escape(odmref[-12:]))
        tabsearch = re.search(
            r'<g.*"translate\((\d+),(\d+)\)".*\n<rect.*width="(\d+)".*\n.*<text id="{}-{}"[\d\D]*?</g>'
                .format(re.escape(odmref[:8]), re.escape(odmref[-12:])), retval)
        if tabsearch is None:
            continue
        tabstr = tabsearch.group()

        newtabl = tabstr
        # replace id by tabid
        newtabl = re.sub('"{}-{}"'.format(re.escape(odmref[:8]), re.escape(odmref[-12:])),
                         '"{}-{}"'.format(re.escape(pdatm["datamodel-id+"]), re.escape(tabid)), newtabl)
        # add <a href= to table
        newtabl = re.sub('<text id="', '<a href="#{}"><text id="'.format(re.escape(tabid)), newtabl)
        newtabl = re.sub(r'(<text id="[\d\D]+?</text>)', r'\1</a>', newtabl)

        for coluid in tabl["columns+"]:
            coluval = export.getelement(coluid)
            newtabl = re.sub(r'(<text x=".*\n\s*{}\s*\n</text>)'.format(re.escape(coluval["name"])),
                             r'<a href="#{}">\1</a>'.format(re.escape(coluid)), newtabl)
        retval = re.sub(re.escape(tabstr), newtabl, retval)
    # for

    return retval


def datamodeldiagram(export: HTMLExport, pdatm):
    svgtext = printdiagHTML.getsvgfromfile(export=export,pname=pdatm['name'])
    if svgtext is not None:
        svgtext = putrefinsvg(export=export, ptext=svgtext, pdatm=pdatm)
    return svgtext
