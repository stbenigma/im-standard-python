from lxml import etree
from uuid import uuid4
from dateutil import parser as dateparser

from IM_db.IM_JSON import  JSModel
from IM_db.IM_OBJECTS import  Modelelemtype

ROOT_FRAME = """<?xml version="1.0" encoding="windows-1252"?>
<xmi:XMI xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.1"
        xmlns:xmi="http://schema.omg.org/spec/XMI/2.1"
        xmlns:thecustomprofile="http://www.sparxsystems.com/profiles/thecustomprofile/1.0"
        xmlns:Informationmodel="http://www.sparxsystems.com/profiles/Informationmodel/3.4">
    <xmi:Documentation exporter="Enterprise Architect" exporterVersion="6.5" exporterID="1559"/>
    <uml:Model xmi:type="uml:Model" name="EA_Model" visibility="public">
    </uml:Model>
</xmi:XMI>"""

EA_PACKAGE_TEMPLATE = """
<element xmi:idref="{ea_package_id}" xmi:type="uml:Package" name="{package_name}" scope="public">
    <model package2="{ea_package2}" package="{ea_package}" tpos="0" ea_localid="3" ea_eleType="package"/>
    <properties isSpecification="false" sType="Package" nType="0" scope="public"/>
    <project author="generator" version="1.0" phase="1.0" created="2021-06-29 17:32:29" modified="2021-06-29 17:32:29"
        complexity="1" status="Proposed"/>
    <code gentype="Informationmodel"/>
    <style appearance="BackColor=-1;BorderColor=-1;BorderWidth=-1;FontColor=-1;VSwimLanes=1;HSwimLanes=1;BorderStyle=0;"
    />
    <tags/>
    <xrefs/>
    <extendedProperties tagged="0" package_name="Model"/>
    <packageproperties version="1.0"/>
    <paths/>
    <times created="2021-06-29 17:32:29" modified="2021-06-29 17:32:29"/>
    <flags iscontrolled="FALSE" isprotected="FALSE" usedtd="FALSE" logxml="FALSE" packageFlags="isModel=1;VICON=3;"/>
</element>
"""


class IdentityMap(object):

    def __init__(self, prefix: str):
        self.map = dict()
        self.prefix = prefix

    def create(self, identity: str, mark: str = None) -> str:
        new_identity = uuid4()
        key = self.prefix + str(new_identity).upper().replace('-', '_')
        if mark is not None:
            key = key[0:4] + '_' + mark + key[(4 + len(mark)):]
        self.map[identity] = key
        return key

    def get(self, identity: str) -> str:
        return self.map[identity]


class XMIBuilder(object):

    def __init__(self, language: str = 'en'):
        self.language = language

        self.parser = etree.XMLParser(remove_blank_text=True, recover=True, ns_clean=True)
        self.root = etree.fromstring(ROOT_FRAME.encode('UTF-8'), parser=self.parser)

        # namespace for XMI's
        self.xmi_ns = '{' + self.root.nsmap['xmi'] + '}'
        self.im_namespace = self.root.nsmap['Informationmodel']

        self.model_node = self.root.find('uml:Model', self.root.nsmap)
        self.package_node = None

        self.package_map = IdentityMap('EAPK_')
        self.class_map = IdentityMap('EAID_')
        self.relation_map = IdentityMap('EAID_')
        self.diagram_map = IdentityMap('EAPK_')

        self.package_key = None
        self.ea_local_id = 0

    def model_to_basic_xmi(self, model: JSModel, package_name: str = 'initial') -> etree.Element:
        """Convert the jsmodel"""
        assert self.model_node is not None

        self.package_node = self.create_package(package_name)
        self.model_node.append(self.package_node)

        for key, entity in model.getelements(pelemtype=Modelelemtype.ENTI, pfiltered=False).items():
            self.add_entity(key, entity)

        for key, relation in model.getelements(pelemtype=Modelelemtype.RELA, pfiltered=False).items():
            self.add_relation(key, relation)

        # Stereotype needs to be in the end
        for ea_entity_key in self.class_map.map.values():
            class_extension = etree.Element(etree.QName(self.im_namespace, 'Entity'))
            class_extension.set('base_Class', ea_entity_key)
            self.model_node.append(class_extension)

        for relation_parent_key in self.relation_map.map.values():
            relation_extension = etree.Element(etree.QName(self.im_namespace, 'Relation'), nsmap=self.root.nsmap)
            relation_extension.set('base_Association', relation_parent_key)
            self.model_node.append(relation_extension)

        return self.root

    def model_to_ea_extension(self, model: JSModel):
        ea_extension = self.create_ea_extension_frame()

        elements_root = self.create_ea_elements(self.package_node.get('name'))
        ea_extension.append(elements_root)

        for key, entity in model.getelements(pelemtype=Modelelemtype.ENTI, pfiltered=False).items():
            element_node = self.create_ea_entity(key, entity)
            elements_root.append(element_node)

        diagrams_root = etree.Element('diagrams')
        ea_extension.append(diagrams_root)
        for key, diagram in model.getelements(pelemtype=Modelelemtype.DIAG, pfiltered=False).items():
            diag = self.create_diagram(key, diagram)
            diagrams_root.append(diag)

        self.root.append(ea_extension)
        return ea_extension

    def create_package(self, name: str) -> etree.Element:
        self.package_key = self.package_map.create(name)
        package_node = etree.Element('packagedElement')
        package_node.set(self.xmi_ns + 'type', 'uml:Package')
        package_node.set(self.xmi_ns + 'id', self.package_key)
        package_node.set('name', name)
        package_node.set('visibility', 'public')
        return package_node

    def add_entity(self, entity_key: str, entity: dict) -> etree.Element:
        ea_entity_key = self.class_map.create(entity_key, entity_key)
        class_node = etree.Element('packagedElement')
        self.package_node.append(class_node)

        class_node.set(self.xmi_ns + 'type', 'uml:Class')
        class_node.set(self.xmi_ns + 'id', ea_entity_key)
        class_node.set('name', self.translate(entity['name']))
        class_node.set('visibility', 'public')

    def add_relation(self, key: str, relation: dict):
        relation_parent_key = self.relation_map.create(key, key)
        relation_parent_node = etree.Element('packagedElement')
        self.package_node.append(relation_parent_node)

        relation_parent_node.set(self.xmi_ns + 'type', 'uml:Association')
        relation_parent_node.set(self.xmi_ns + 'id', relation_parent_key)
        relation_parent_node.set('visibility', 'public')

        # memberEnd dst (order as in original)
        relation_dst_key = relation_parent_key[0:4] + '_dst' + relation_parent_key[7:]
        relation_dst_ref = etree.Element('memberEnd')
        relation_dst_ref.set(self.xmi_ns + 'idref', relation_dst_key)
        relation_parent_node.append(relation_dst_ref)

        # memberEnd src
        # relation_src_key = self.relation_map.create(key + 'src', 'src')
        relation_src_key = relation_parent_key[0:4] + '_src' + relation_parent_key[7:]
        relation_src_ref = etree.Element('memberEnd')
        relation_src_ref.set(self.xmi_ns + 'idref', relation_src_key)
        relation_parent_node.append(relation_src_ref)

        # ownedEnd src
        relation_src = etree.Element('ownedEnd')
        relation_src.set(self.xmi_ns + 'type', 'uml:Property')
        relation_src.set(self.xmi_ns + 'id', relation_src_key)
        relation_src.set('visiblity', 'public')
        relation_src.set('association', relation_parent_key)
        relation_src.set('name', self.safe_translate(relation['from-to'].get('assoc')))
        relation_src.set('isStatic', "false")
        relation_src.set('isReadOnly', "false")
        relation_src.set('isDerived', "false")
        relation_src.set('isOrdered', "false")
        relation_src.set('isUnique', "true")
        relation_src.set('isDerivedUnion', "false")
        relation_src.set('aggregation', "none")

        relation_parent_node.append(relation_src)

        # ownedEnd src
        relation_dst = etree.Element('ownedEnd')
        relation_dst.set(self.xmi_ns + 'type', 'uml:Property')
        relation_dst.set(self.xmi_ns + 'id', relation_dst_key)
        relation_dst.set('visiblity', 'public')
        relation_dst.set('association', relation_parent_key)
        relation_dst.set('name', self.safe_translate(relation['to-from'].get('assoc')))
        relation_dst.set('isStatic', "false")
        relation_dst.set('isReadOnly', "false")
        relation_dst.set('isDerived', "false")
        relation_dst.set('isOrdered', "false")
        relation_dst.set('isUnique', "true")
        relation_dst.set('isDerivedUnion', "false")
        relation_dst.set('aggregation', "none")
        relation_parent_node.append(relation_dst)

        # reference source / from
        from_key = relation['from-to']['enti']
        assert from_key is not None and len(from_key) > 3
        from_entity_key = self.class_map.get(from_key)
        src_class_ref = etree.Element('type')
        src_class_ref.set(self.xmi_ns + 'idref', from_entity_key)
        relation_src.append(src_class_ref)

        # reference to / destination
        to_key = relation['to-from']['enti']
        assert to_key is not None and len(to_key) > 3
        to_entity_key = self.class_map.get(to_key)
        dst_class_ref = etree.Element('type')
        dst_class_ref.set(self.xmi_ns + 'idref', to_entity_key)
        relation_dst.append(dst_class_ref)

        # add cardinalities
        self.set_cardinality(relation_dst, relation['to-from']['maptype'], relation['to-from']['mandatory'])
        self.set_cardinality(relation_src, relation['from-to']['maptype'], relation['from-to']['mandatory'])

        # hint
        debug_string = f"{key}: {relation['from-to']['enti']} <=> {relation['to-from']['enti']}"
        relation_parent_node.set('documentation', debug_string)
        relation_parent_node.set('doc', debug_string)
        relation_parent_node.set('note', debug_string)
        relation_parent_node.set('hint', debug_string)

        return relation_parent_node

    def set_cardinality(self, end: etree.Element, cardinality: str, mandatory: bool):
        """"<lowerValue xmi:type="uml:LiteralInteger" xmi:id="EAID_LI000001_C29B_4f9a_8B72_FFE959450E46" value="1"/>
        <upperValue xmi:type="uml:LiteralInteger" xmi:id="EAID_LI000002_C29B_4f9a_8B72_FFE959450E46" value="1"/>"""
        if cardinality == 'M':
            upper_value = '-1'
        else:
            upper_value = '1'
            if mandatory:
                return

        lower_value = '1' if mandatory else '0'

        lower_value_node = etree.Element('lowerValue')
        lower_value_node.set(self.xmi_ns + 'type', 'uml:LiteralUnlimitedNatural')
        lower_value_node.set(self.xmi_ns + 'id', str(uuid4()))  # random GUID
        lower_value_node.set('value', lower_value)
        end.append(lower_value_node)

        upper_value_node = etree.Element('upperValue')
        upper_value_node.set(self.xmi_ns + 'type', 'uml:LiteralUnlimitedNatural')
        upper_value_node.set(self.xmi_ns + 'id', str(uuid4()))  # random GUID
        upper_value_node.set('value', upper_value)
        end.append(upper_value_node)

    def create_ea_extension_frame(self):
        # <xmi:Extension extender="Enterprise Architect" extenderID="6.5">
        ea_extension = etree.Element(etree.QName(self.root.nsmap['xmi'], 'Extension'))
        ea_extension.set('extender', 'Enterprise Architect')
        ea_extension.set('extenderID', '6.5')
        return ea_extension

    def create_ea_elements(self, package_name: str):
        """Elements node + package"""
        ea_elements = etree.Element('elements')
        ea_package_id = self.package_map.get(package_name)
        ea_package_node = etree.fromstring(EA_PACKAGE_TEMPLATE.format(
            ea_package_id=ea_package_id,
            package_name=package_name,
            ea_package=str(uuid4()),
            ea_package2=str(uuid4()),
        ).encode('UTF-8'), parser=self.parser)
        ea_elements.append(ea_package_node)

        return ea_elements

    def create_ea_entity(self, key: str, entity: dict):
        entity_ea_id = self.class_map.get(key)
        entity_node = etree.Element('element')
        entity_node.set(self.xmi_ns + 'idref', entity_ea_id)
        entity_node.set(self.xmi_ns + 'type', 'uml:Class')
        entity_node.set('name', self.safe_translate(entity.get('name')))
        entity_node.set('scope', 'public')

        # <model package="EAPK_68389B05_EBA4_4e57_954C_DFBC51443B65" tpos="0" ea_localid="31" ea_eleType="element"/>
        model = etree.Element('model')
        entity_node.append(model)
        model.set('package', list(self.package_map.map.values())[0])
        model.set('tpos', '0')
        self.ea_local_id += 1
        model.set('ea_localid', str(self.ea_local_id))
        model.set('ea_eleType', 'element')

        # <project author="bue" version="1.0" phase="1.0" created="2021-12-02 15:27:31" modified="2021-12-02 15:29:41"
        # complexity="1" status="Proposed"/>
        project = etree.Element('project')
        entity_node.append(project)
        project.set('author', entity['uc'])
        create_date = dateparser.parse(entity['dc'])
        project.set('created', create_date.strftime("%Y-%m-%d %H:%M:%S"))

        # <code product_name="Java" gentype="Java"/>
        code = etree.Element('code')
        entity_node.append(code)
        code.set('product_name', 'Informationmodel')
        code.set('gentype', 'IM')

        modified_date = entity.get('dm')
        if modified_date is not None:
            modify_date = dateparser.parse(modified_date)
            project.set('modified', modify_date.strftime("%Y-%m-%d %H:%M:%S"))

        status = 'Proposed'
        devstatus = entity.get('devstatus')
        if devstatus is not None:
            if devstatus.upper() == 'DEV':
                status = 'Implemented'
        project.set('status', status)

        props = etree.Element('properties')
        entity_node.append(props)
        props.set('documentation', self.safe_translate(entity.get('descr')))
        props.set('isSpecification', 'false')
        props.set('sType', 'Class')
        props.set('nType', '0')
        props.set('scope', 'public')
        props.set('stereotype', 'Entity')
        props.set('isRoot', 'false')
        props.set('isLeaf', 'false')
        props.set('isAbstract', 'false')
        props.set('isActive', 'false')

        # <xrefs value="$XREFPROP=$XID={D6EE24F7-15C0-4e44-A539-E92CCD471AAB}$XID;$NAM=Stereotypes$NAM;
        # $TYP=element property$TYP;
        # $VIS=Public$VIS;$PAR=0$PAR;$DES=@STEREO;Name=Entity;FQName=Informationmodel::Entity;@ENDSTEREO;
        # $DES;$CLT={1FDCDC17-0587-4f38-AFB1-3ED0159DA4A7}$CLT;$SUP=&lt;none&gt;$SUP;$ENDXREF;
        # $XREFPROP=$XID={8C41D7F4-7474-4307-AF8E-193A7F3E4B7C}$XID;$NAM=CustomProperties$NAM;$TYP=element property$TYP;
        # $VIS=Public$VIS;$PAR=0$PAR;$DES=@PROP=@NAME=_HideUmlLinks@ENDNAME;
        # @TYPE=string@ENDTYPE;@VALU=True@ENDVALU;@PRMT=@ENDPRMT;@ENDPROP;$DES;
        # $CLT={1FDCDC17-0587-4f38-AFB1-3ED0159DA4A7}$CLT;$SUP=&lt;none&gt;$SUP;$ENDXREF;"/>
        xrefs = etree.Element('xrefs')
        entity_node.append(xrefs)
        cltid = str(uuid4())
        xrefs.set('value', f"""$XREFPROP=$XID={{{str(uuid4())}}}$XID;\
$NAM=Stereotypes$NAM;$TYP=element property$TYP;$VIS=Public$VIS;$PAR=0$PAR;$DES=@STEREO;\
Name=Entity;FQName=Informationmodel::Entity;@ENDSTEREO;$DES;$CLT={{{cltid}}}$CLT;$SUP=<none>$SUP;$ENDXREF;\
$XREFPROP=$XID={{{uuid4()}}}$XID;$NAM=CustomProperties$NAM;$TYP=element property$TYP;$VIS=Public$VIS;$PAR=0$PAR;\
$DES=@PROP=@NAME=_HideUmlLinks@ENDNAME;@TYPE=string@ENDTYPE;@VALU=True@ENDVALU;@PRMT=@ENDPRMT;@ENDPROP;\
$DES;$CLT={{{cltid}}}$CLT;$SUP=<none>$SUP;$ENDXREF;""")

        return entity_node

    def create_diagram(self, key: str, diagram: dict):
        diagram_key = self.diagram_map.create(key, key)
        ea_diagram = etree.Element('diagram')
        ea_diagram.set(self.xmi_ns + 'id', diagram_key)

        properties = etree.Element('properties')
        ea_diagram.append(properties)
        properties.set('name', diagram['name'])
        properties.set('type', 'Logical')

        model = etree.Element('model')
        ea_diagram.append(model)
        model.set('package', self.package_key)
        self.ea_local_id += 1
        model.set('localID', str(self.ea_local_id))
        model.set('owner', self.package_key)

        elements = etree.Element('elements')
        ea_diagram.append(elements)

        sequence = 1
        for entity in diagram['elements']['entity']:
            element = etree.Element('element')
            scale = .8
            x = entity['pos_x'] * scale
            y = entity['pos_y'] * scale
            element.set('geometry', "Left={x};Top={y};Right={right};Bottom={bottom};".format(
                x=x, y=y,
                right=x + (entity['ui']['width'] * scale),
                bottom=y + (entity['ui']['height'] * scale)
            ))
            element.set('subject', self.class_map.get(entity['element']))
            element.set('seqno', str(sequence))
            sequence += 1

            elements.append(element)

        return ea_diagram

    def translate(self, element: dict) -> str:
        if element is None or len(element) < 1:
            assert False, f"Element {element} cannot be translated"
        return element.get(self.language, element.get('en', list(element.values())[0]))

    def safe_translate(self, element: dict) -> str:
        result = self.translate(element)
        if result is None:
            result = ''
        return result
