import sys,os
from SSOT_infra import parameters
from IM_db.IM_JSON import  JSModel
from xml.etree import ElementTree as ET
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

defaultoutputdirectory = os.path.expanduser('~')+"/Downloads/"
nonodmtables = []
odmtablecnt = 0
nonodmcolumns = []
odmcolumncnt = 0

def getguid (pelem):
    if "sourceref" not in pelem:
        return None
    if "ODM" not in pelem["sourceref"]:
        return None
    return pelem["sourceref"]["ODM"][0]

def doubleguid(pguid1,pguid2):
    return pguid1[0:9]+pguid1[-12:]+pguid2[0:9]+pguid2[-12:]

def docolumnmap(pjson, pelem,pentid, pcolid):
    global nonodmcolumns,odmcolumncnt
    colu = pjson.getbyid(pcolid)
    colguid=getguid(colu)
    if colguid is None:
        print(f"Column {pcolid} is not in model")
        nonodmcolumns.append(colu["colu_name"])
        return

    contmapp = pelem.find("containedMappings")
    attrs = colu["attributesmapped"]
    for attrid in attrs:
        if contmapp is None:
            contmapp =  ET.SubElement(pelem,"containedMappings"
                  ,{"itemClass":"oracle.dbtools.crest.model.xtdmapping.RelMapping"})
        #fi
        attr = pjson.getbyid(attrid)
        attrguid=getguid(attr)
        if attrguid is None:
            print (f"Attribute {attr['techname']} is not in model")
            continue
        if attr["entity"] == pentid:
            odmcolumncnt += 1
            ET.SubElement(contmapp,"Mg"
                          ,{"id":doubleguid(attrguid,colguid), "iT":"3", "lID":attrguid, "rID":colguid})
    #for
    return

def dotablmapenti(pjson,pelem,pentid, ptablguid,pcolumns):
    global nonodmtables,nonodmcolumns,odmtablecnt,odmcolumncnt
    entiguid = getguid(pjson.getbyid(pentid))
    if entiguid is None:
        print (f"Entity {pentid} is not in model")
        return
    tabelem = ET.SubElement(pelem, "CM", {"id": doubleguid(entiguid,ptablguid), "iT": "3", "lID": entiguid, "lT": "0", "rID": ptablguid, "rT": "4"})

    for col in pcolumns:
        docolumnmap(pjson=pjson,pelem=tabelem,pentid=pentid,pcolid=col)

def dotablmaprela(pjson,pelem,prelaid, ptablguid,pcolumns):
    global nonodmtables,nonodmcolumns,odmtablecnt,odmcolumncnt
    rela = pjson.getbyid(prelaid)
    relaguid = getguid(rela)
    if relaguid is None:
        print (f"Entity {prelaid} is not in model")
        return
    srcentiguid=getguid(pjson.getbyid(rela["from-to"]["enti"]))
    dstentiguid = getguid(pjson.getbyid(rela["to-from"]["enti"]))
    ET.SubElement(pelem, "CM", {"id": doubleguid(relaguid,ptablguid), "iT": "3", "lID": relaguid, "lT": "3", "rID": ptablguid, "rT": "4"
                                ,"rSEnt":srcentiguid, "rTEnt":dstentiguid})

def createXML(pjson,pintf):
    global nonodmtables,nonodmcolumns,odmtablecnt,odmcolumncnt
    xml = ET.Element("RMExtendedMap", {"class": "oracle.dbtools.crest.model.xtdmapping.RMExtendedMap"})
    mappings=ET.SubElement(xml,"mappings", {"itemClass": "oracle.dbtools.crest.model.xtdmapping.ContainerMapping"})
    for tab in pintf["tables+"]:
        tabl = pjson.getbyid(tab)
        tablguid = getguid(tabl)
        if tablguid is not None:
            odmtablecnt += 1
            for entiid in tabl["entitiesmapped"]:
                dotablmapenti(pjson=pjson,pelem=mappings,pentid=entiid,ptablguid=tablguid,pcolumns=tabl["columns+"])
            for relaid in tabl["relationsmapped"]:
                dotablmaprela(pjson=pjson,pelem=mappings,prelaid=relaid,ptablguid=tablguid,pcolumns=tabl["columns+"])
        else:
            nonodmtables.append(tabl['name'])
            print(f"Table {tabl['name']} is not in model")

    #print (prettify(xml))
    return prettify(xml)

def export1Map(pimdirec,pintfname):
    global nonodmtables,nonodmcolumns,odmtablecnt,odmcolumncnt
    parameters.initparam(p_callarg=pimdirec)
    jsfilename= parameters.dbDirect() + parameters.modelName() + ".json"
    jsmodel = JSModel.readfromfile(pfilename=jsfilename)
    expintf = None
    for intf in [intf for intf in jsmodel.getelements("systems").values() ]:
        if intf["name"] == pintfname:
            expintf = intf
    if expintf is None:
        print(f"Interface {pintfname} not found in model {parameters.modelName()}")
        return
    intfguid = getguid(expintf)
    if intfguid is None:
        print(f"Interface {pintfname}: is not in model {parameters.modelName()}")
        return
    outputfilename = defaultoutputdirectory + f"ExtendedMap_RM{intfguid}.xml"
    xmltext=createXML(pjson=jsmodel,pintf=expintf)
    outfile = open(outputfilename, "w")
    outfile.write(xmltext)
    outfile.close()



    if len(nonodmtables) > 0:
        print("".join("*" for i in range(1, 20)))
        print (f"Interface {pintfname}: tables not in ODM:")
        for t in nonodmtables: print (t)
    if len(nonodmcolumns) > 0:
        print("".join("*" for i in range(1, 20)))
        print (f"Interface {pintfname}: columns not in ODM:")
        for c in nonodmcolumns: print (f"{c[0]}.{c[1]}")

    print("".join("*" for i in range(1,20)))
    print(f"Interface {pintfname}: mappingxml ({odmtablecnt} tables and {odmcolumncnt} columns) written to {outputfilename}")

if __name__ == '__main__':
    export1Map(pimdirec=None if len(sys.argv) <2  else sys.argv[1],pintfname=None if len(sys.argv) <3 else sys.argv[2])
