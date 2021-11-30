# Your very first script
import xml.etree.ElementTree as ET
import re
import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../IM_db')
from SSOT_infra import parameters

entityDict = {}
tableDict = {}
attrDict = {}
relationDict = {}
columnDict = {}

def  getPropList(p_udpfilename):
    tree = ET.parse(parameters.odmFilesDirec() + p_udpfilename + '.udposdm')
    root = tree.getroot()
    #print(parameters.odmFilesDirec()+p_udpfilename+'.udposdm',root)
    for child in root:
        if child.tag == 'properties':
            for props in child:
                name = props.get('name')
                defValue = props.get('default_value')
                for obj in props:
                    if obj.tag == 'list_of_values':
                        for lov in obj:
                            if lov.get('default') == 'true':
                                defValue = lov.get('value')
                #                print name,defValue
                for obj in props:
                    if obj.tag == 'objects':
                        for entry in obj:
                            if re.search('Entity$', entry.get('class')) != None:
                                entityDict[name] = defValue
                            if re.search('Table$', entry.get('class')) != None:
                                tableDict[name] = defValue
                            if re.search('Attribute$', entry.get('class')) != None:
                                attrDict[name] = defValue
                            if re.search('Column$', entry.get('class')) != None:
                                columnDict[name] = defValue
                            if re.search('Relation$', entry.get('class')) != None:
                                relationDict[name] = defValue
                        #end for
                    #end if
                #end for
            #end for
        #end if
    #end for
#end getPropList

def addProperty(element,name,value):
    """Erzeugt einen Property-Eintrag 
    """
    neuProp = ET.SubElement(element, 'property')
    neuProp.set('name', name)
    neuProp.set('value', value)
# END addProperty

def createpropertymap(p_obj,p_dict):
    """Erzeugt eine Property-Map fuer das Objekt mit allen Eintraegen aus dict
    """
    neuMap = ET.SubElement(p_obj, 'propertyMap')
    for ele in p_dict:
        addProperty(neuMap,ele,p_dict[ele])
#END createpropertymap

def dopropmap(p_obj,p_dict):
    """ Parsed eine PropertyMap in einem objekt und ergaenzt sie um die notwendigen
        Elemente,falls sie fehlen"""
    propMap = p_obj.find('propertyMap')
    if (propMap is not None):
        # Behandle die PropertyMap des Attributes
        curattrprop = {prop.get('name') for prop in propMap}
        for key in p_dict:
            if key not in curattrprop:
                addProperty(propMap,key,p_dict[key])
            #end if
        #end for
    else:
        createpropertymap(p_obj=p_obj, p_dict=p_dict)
    #fi
#dopropmap


def do1file(p_xmlname,p_dict,p_attr):
    tree = ET.parse(p_xmlname + '.xml')
    root = tree.getroot()
#    print "tag=",root.tag,"attrib=",root.attrib

    #print ("Entity:", root.get("name"))

    dopropmap(p_obj=root,p_dict=p_dict)

    if p_attr:
        for attrs in root.findall('attributes'):
            # Behandle die PropertyMap der Attributes
            for attr in attrs:
                dopropmap(p_obj=attr,p_dict=attrDict)
            #endfor
        #endfor
    #fi

    # schreibe die geaenderte definition zurueck als XML
    tree.write(p_xmlname + '.xml')
#do1file

def dofiles(p_direc,p_dict,p_attr=False):
    for el in os.listdir(p_direc):
        if re.match('seg_.*', el):
            for file in os.listdir(p_direc + el):
                fileName = re.sub('.xml','', p_direc + el + '/' + file)
                #print (fileName)
                do1file(p_xmlname=fileName,p_dict=p_dict,p_attr=p_attr)
#dofiles

# Main Programm
def main(par1,par2):
    parameters.initparam(p_callarg=par1)
    #print(parameters.odmIMDirec(),parameters.odmFilesDirec())
    getPropList(p_udpfilename=par2)
    #print(entityDict,attrDict,relationDict)
    dofiles(p_direc=parameters.odmEntityDirec(), p_dict=entityDict, p_attr=True)
    dofiles(p_direc=parameters.odmRelationDirec(), p_dict=relationDict)


if __name__ == '__main__':
    par1 = sys.argv[1]
    par2 = sys.argv[2]
    main(par1,par2)