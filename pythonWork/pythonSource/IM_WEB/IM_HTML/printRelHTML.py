import os,re
import sys
sys.path.append(os.getcwd())
from IM_HTML import printHTML,printdiagHTML
from IM_DB import parameters


def nvl(s, default=''):
    return nvl(s, default)

getelement = lambda e:printHTML.getmodel().getbyid(e)

def putrefinsvg(ptext,pintf):
    retval = ptext
    for tabid in pintf["tables+"]:
        tabl = getelement(tabid)
        try:
            odmref = tabl["sourceref"]["ODM"][0]
        except:
            continue

        refid = "{}-{}".format(re.escape(odmref[:8]),re.escape(odmref[-12:]))
        tabsearch = re.search(r'<g.*"translate\((\d+),(\d+)\)".*\n<rect.*width="(\d+)".*\n.*<text id="{}-{}"[\d\D]*?</g>'
                            .format(re.escape(odmref[:8]),re.escape(odmref[-12:])), retval)
        if tabsearch is None:
            continue
        tabstr = tabsearch.group()

        newtabl = tabstr
        #replace id by tabid
        newtabl = re.sub('"{}-{}"'.format(re.escape(odmref[:8]),re.escape(odmref[-12:])), '"{}-{}"'.format(re.escape(pintf["interface-id+"]),re.escape(tabid)), newtabl)
        #add <a href= to table
        newtabl = re.sub('<text id="', '<a href="#{}"><text id="'.format(re.escape(tabid)), newtabl)
        newtabl = re.sub(r'(<text id="[\d\D]+?</text>)', r'\1</a>', newtabl)

        for coluid in tabl["columns+"]:
            coluval = printHTML.getelement(coluid)
            newtabl = re.sub(r'(<text x=".*\n\s*{}\s*\n</text>)'.format(re.escape(coluval["name"])),
                             r'<a href="#{}">\1</a>'.format(re.escape(coluid)), newtabl)
        retval = re.sub(re.escape(tabstr),newtabl,retval)
    #for

    return retval

def interfacediagram(pintf):
    svgtext = printdiagHTML.getsvgfromfile(pname=pintf['name'])
    if svgtext is not None:
        svgtext = putrefinsvg(ptext=svgtext,pintf=pintf)
    return svgtext

