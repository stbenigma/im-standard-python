# Your very first script
import xml.etree.ElementTree as ET
import re
import os
import sys,os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/../IM_db')
from IM_DB import parameters


# vorgesehene Property-Listen je Element
# key = PropertyName   value = default Value
entityDict = {}
tableDict = {}
attrDict = {}
columnDict = {}

def  getPropList(p_udpfilename):
    tree = ET.parse(parameters.odmFilesDirec()+p_udpfilename+'.udposdm')
    root = tree.getroot()
    print(parameters.odmFilesDirec()+p_udpfilename+'.udposdm',root)
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
                        #end for
                    #end if
                #end for
            #end for
        #end if
    #end for
#end getPropList

def neuesProperty(element, name, value):
    """ definiert einen neuen Eintrag als Property in die Map"""
    neuProp = ET.SubElement(element, 'property')
    neuProp.set('name', name)
    neuProp.set('value', value)


def addProperty(element,name,value):
    """Erzeugt einen Property-Eintrag 
    """
    neuProp = ET.SubElement(element, 'property')
    neuProp.set('name', name)
    neuProp.set('value', value)
# END addProperty

def attributePropertyMap(attr):
    """ Parsed eine PropertyMap in einem Attribut und ergaenzt sie um die notwendigen
        Elemente,falls sie fehlen"""
    hatPropMap = 'false'
    for attrEl in attr:
        if attrEl.tag == 'propertyMap':
            print ('   ',attrEl.tag,attrEl.get('name'),attrEl.attrib)
            hatPropMap = 'true'
            curAttrProp = set()
            for prop in attrEl:
#                print '      ', prop.get('name'), prop.get('value')
#                neuesProperty(attrEl, 'NeuProperty', '-')
                curAttrProp.add(prop.get('name'))
            # end for
            for key in attrDict.iterkeys():
                print (key)
                if key not in curAttrProp:
                    addProperty(attrEl, key, attrDict[key])
            #end for
        #end if
    #end for
    if hatPropMap == 'false':
#        print '        No Property Map'
        neuMap = ET.SubElement(attr,'propertyMap')
        for at in attrDict:
            addProperty(neuMap,at,attrDict[at])

#end attributePropertyMap

def createEntityPropertyMap(entity):
    """Erzeugt eine Property-Map fuer die Entitaet mit allen Eintraegen
    """
    neuMap = ET.SubElement(entity, 'propertyMap')
    for ent in entityDict:
        addProperty(neuMap,ent,entityDict[ent])
#END createEntityPropertyMap

def do1Entity(xmlName):
    tree = ET.parse(xmlName+ '.xml')
    root = tree.getroot()
#    print "tag=",root.tag,"attrib=",root.attrib

    print ("Entity:", root.get("name"))
    hatEntityPropMap = 'false'
    for attrs in root.findall('attributes'):
        # Behandle die PropertyMap der Attributes
        attributePropertyMap(attrs)

    child = root.find('propertyMap')
    if child == None:
        # Behandle die PropertyMap der Entitaet
        curEntityProp = set()
        for prop in child:
#                print '  ', prop.get('name'), prop.get('value')
            curEntityProp.add(prop.get('name'))
            #end for
            for key in entityDict.iterkeys():
                print (key)
                if key not in curEntityProp:
                    addProperty(child,key,entityDict[key])
                #end if
        #end loop
    else:
#        hatEntityPropMap == 'false'
        createEntityPropertyMap(root)

    # schreibe die geaenderte definition zurueck als XML
#    tree.write(xmlName + 'New.xml')
    tree.write(xmlName + '.xml')
#END do1Entity

def doEntities(direc):
    for el in os.listdir(direc):
        if re.match('seg_.*', el):
            for file in os.listdir(direc + el):
                fileName = re.sub('.xml','',direc + el + '/' + file)
                do1Entity(fileName)
#END doEntities

# Main Programm
def main(par1,par2):
    parameters.initparam(p_callarg=par1)
    #print(parameters.odmIMDirec(),parameters.odmFilesDirec())
    getPropList(p_udpfilename=par2)
    #print(entityDict)
    doEntities(parameters.odmEntityDirec())


if __name__ == '__main__':
    par1 = sys.argv[1]
    par2 = sys.argv[2]
    main(par1,par2)