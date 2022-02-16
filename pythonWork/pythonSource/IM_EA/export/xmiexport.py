from typing import Set

from lxml import etree
from uuid import uuid4
from dateutil import parser as dateparser

from SSOT_db.IM_JSON import JSModel
from SSOT_db.IM_OBJECTS import Modelelemtype
from matplotlib.patches import Rectangle

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

# This tag is used in various places to enable tracing back to SSOT elements
SSOT_ID_TAG = 'ssotid'


class IdentityMap(object):

    def __init__(self, prefix: str):
        self.map = dict()
        self.prefix = prefix

    def create(self, identity: str, mark: str = None) -> str:
        new_identity = uuid4()
        key = self.prefix + str(new_identity).upper().replace('-', '_')
        if mark is not None:
            key = key[0:4] + '_' + mark + '_' + key[(4 + len(mark)):]
        self.map[identity] = key
        return key

    def get(self, identity: str) -> str:
        return self.map[identity]


class XMIBuilder(object):

    def __init__(self, model: JSModel, language: str = 'en'):
        assert model is not None
        self.model = model
        self.language = language

        self.parser = etree.XMLParser(remove_blank_text=True, recover=True, ns_clean=True)
        self.root = etree.fromstring(ROOT_FRAME.encode('UTF-8'), parser=self.parser)

        # namespace for XMI's
        self.xmi_ns = '{' + self.root.nsmap['xmi'] + '}'
        self.im_namespace = self.root.nsmap['Informationmodel']

        self.model_node = self.root.find('uml:Model', self.root.nsmap)
        self.package_node = None

        # Could be simplified since export currently contains exactly 1 package
        self.package_map = IdentityMap('EAPK_')

        # key: SSOT key (ENTInnn, ARCSnnn)
        # value: EA identity (prefixed uuid)
        self.class_map = IdentityMap('EAID_')

        self.attribute_map = IdentityMap('EAID_')
        self.relation_map = IdentityMap('EAID_')
        self.diagram_map = IdentityMap('EAPK_')

        self.package_key = None
        self.ea_local_id = 0
        self.scale = 1.2

    def model_to_basic_xmi(self, package_name: str = 'initial') -> etree.Element:
        """Convert the jsmodel"""
        assert self.model_node is not None

        self.package_node = self.create_package(package_name)
        self.model_node.append(self.package_node)

        for key, entity in self.model.getelements(pelemtype=Modelelemtype.ENTI, pfiltered=False).items():
            self.add_entity(key, entity)

        for key, arc in self.model.getelements(pelemtype=Modelelemtype.ARCS, pfiltered=False).items():
            self.add_arc(key, arc)

        for key, relation in self.model.getelements(pelemtype=Modelelemtype.RELA, pfiltered=False).items():
            self.add_relation(key, relation)

        # Stereotype refining elements follow the declarations
        for key, ea_entity_key in self.class_map.map.items():
            # sort out Entities and Arcs
            if key.startswith(Modelelemtype.ARCS):
                class_extension = etree.Element(etree.QName(self.im_namespace, 'Arc'))
                class_extension.set('base_Constraint', ea_entity_key)
            else:
                class_extension = etree.Element(etree.QName(self.im_namespace, 'Entity'))
                class_extension.set('base_Class', ea_entity_key)
            self.model_node.append(class_extension)

        for key, relation_parent_key in self.relation_map.map.items():
            relation = self.model.getbyid(key)
            # The link between an Entity and it's Arcs has no element in the SSOT
            if relation is None:
                relation_extension = etree.Element(etree.QName(self.im_namespace, 'ArcParent'), nsmap=self.root.nsmap)
            else:
                relation_extension = etree.Element(etree.QName(self.im_namespace, 'Relation'), nsmap=self.root.nsmap)
            relation_extension.set('base_Association', relation_parent_key)
            self.model_node.append(relation_extension)

        for attribute_parent_key in self.attribute_map.map.values():
            attribute_extension = etree.Element(etree.QName(self.im_namespace, 'Attribute'), nsmap=self.root.nsmap)
            attribute_extension.set('base_Property', attribute_parent_key)
            self.model_node.append(attribute_extension)

        return self.root

    def model_to_ea_extension(self):
        ea_extension = self.create_ea_extension_frame()

        elements_root = self.create_ea_elements(self.package_node.get('name'))
        ea_extension.append(elements_root)

        for key, entity in self.model.getelements(pelemtype=Modelelemtype.ENTI, pfiltered=False).items():
            element_node = self.create_ea_entity(key, entity)
            elements_root.append(element_node)

        for key, arc in self.model.getelements(pelemtype=Modelelemtype.ARCS, pfiltered=False).items():
            arc_node = self.create_ea_arc(key, arc)
            elements_root.append(arc_node)

        # Refine connectors
        connectors_root = etree.Element('connectors')
        ea_extension.append(connectors_root)
        self.add_connectors_ea(connectors_root)

        diagrams_root = etree.Element('diagrams')
        ea_extension.append(diagrams_root)
        for key, diagram in self.model.getelements(pelemtype=Modelelemtype.DIAG, pfiltered=False).items():
            diag = self.create_diagram(key, diagram)
            diagrams_root.append(diag)

        self.root.append(ea_extension)
        return ea_extension

    def add_connectors_ea(self, connectors_root):
        for key, relation_key in self.relation_map.map.items():
            relation = self.model.getbyid(key)
            connector = etree.Element('connector')
            connector.set(self.xmi_ns + 'idref', relation_key)

            doc = etree.Element('documentation')
            connector.append(doc)
            props = etree.Element('properties')
            connector.append(props)

            if relation is not None:
                connector.set('name', f"{relation['from-to']['enti']} - {relation['to-from']['enti']}")
                arc_source = relation['from-to'].get('arc')
                doc_string = f"{self.entity_name(relation['from-to']['enti'])} {('- (' + arc_source + ')') if arc_source is not None else ''} - {self.entity_name(relation['to-from']['enti'])}"
                doc.set('value', doc_string if len(doc_string) > 0 else connector.get('name'))
                props.set('stereotype', 'Relation')
            else:
                connector.set('name', f"Entity - Arc")
                props.set('stereotype', 'ArcParent')
                labels = etree.Element('labels')
                labels.set('mb', "«ArcParent»")
                labels.set('mt', "ArcParentRelation")
                connector.append(labels)

                # "$XREFPROP=$XID={5B843D40-A7AE-42b4-A852-20D9379A0A07}$XID;$NAM=Stereotypes$NAM;
                # $TYP=connector property$TYP;$VIS=Public$VIS;$PAR=0$PAR;
                # $DES=@STEREO;Name=ArcParent;FQName=Informationmodel::ArcParent;@ENDSTEREO;
                # $DES;$CLT={592E355E-E238-4bab-AC81-2B4C1EB1878F}$CLT;$SUP=&lt;none&gt;$SUP;$ENDXREF;"/>
                xrefs = etree.Element('xrefs')
                xrefs.set('value', f""""$XREFPROP=$XID={{{str(uuid4())}}}$XID;$NAM=Stereotypes$NAM;
$TYP=connector property$TYP;$VIS=Public$VIS;$PAR=0$PAR;
$DES=@STEREO;Name=ArcParent;FQName=Informationmodel::ArcParent;@ENDSTEREO;
$DES;$CLT={{{str(uuid4())}}}$CLT;$SUP=&lt;none&gt;$SUP;$ENDXREF;""")
                connector.append(xrefs)

            props.set('ea_type', 'Association')
            props.set('direction', 'Unspecified')

            # self.add_tag(connector, relation_key, SSOT_ID_TAG, key)
            connectors_root.append(connector)

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

        for attr_key in entity['attributes+']:
            attribute = self.model.getbyid(attr_key)
            attr_node = self.create_entity_attribute(attr_key, attribute)
            class_node.append(attr_node)

    def create_entity_attribute(self, attribute_key: str, attribute: dict) -> etree.Element:
        """
        <ownedAttribute xmi:type="uml:Property" xmi:id="EAID_CB0F96CF_C29B_4f9a_8B72_FFE959450E46" name="IATA Code"
            visibility="public" isStatic="false" isReadOnly="false" isDerived="false"
            isOrdered="false" isUnique="true" isDerivedUnion="false">
        <type xmi:idref="EAID_7320D192_A2DF_463e_9FF6_A1E3A7987E33"/>
        <lowerValue xmi:type="uml:LiteralInteger" xmi:id="EAID_LI000001_C29B_4f9a_8B72_FFE959450E46" value="1"/>
        <upperValue xmi:type="uml:LiteralInteger" xmi:id="EAID_LI000002_C29B_4f9a_8B72_FFE959450E46" value="1"/>
        </ownedAttribute>
        :param attribute_key:
        :param attribute:
        :return:
        """
        assert len(attribute_key) > 3
        assert attribute is not None

        node = etree.Element('ownedAttribute')
        node.set(self.xmi_ns + 'type', 'uml:Property')
        attr_ea_id = self.attribute_map.create(attribute_key, attribute_key)
        node.set(self.xmi_ns + 'id', attr_ea_id)
        node.set('name', self.translate(attribute['name']))
        node.set('isStatic', 'false')
        node.set('isReadOnly', 'false')
        node.set('isDerived', 'false')
        node.set('isOrdered', 'false')
        node.set('isUnique', 'true')
        node.set('isDerivedUnion', 'false')

        lower_value = etree.Element('lowerValue')
        lower_value.set(self.xmi_ns + 'type', 'uml:LiteralInteger')
        lower_value.set(self.xmi_ns + 'id', attr_ea_id + '_1')
        lower_value.set('value', '1')
        node.append(lower_value)

        upper_value = etree.Element('upperValue')
        upper_value.set(self.xmi_ns + 'type', 'uml:LiteralInteger')
        upper_value.set(self.xmi_ns + 'id', attr_ea_id + '_2')
        upper_value.set('value', '1')
        node.append(upper_value)

        return node

    def add_arc(self, arc_key: str, arc: dict) -> etree.Element:
        ea_arc_key = self.class_map.create(arc_key, arc_key)
        class_node = etree.Element('packagedElement')
        self.package_node.append(class_node)

        class_node.set(self.xmi_ns + 'type', 'uml:Constraint')
        class_node.set(self.xmi_ns + 'id', ea_arc_key)
        class_node.set('name', arc['name'])
        class_node.set('visibility', 'public')

        # The relation between Entity and it's arc has no representation
        # in the SSOT. Create it on the fly
        self.add_relation(arc_key + '-' + arc['entity'], {
            'type': 'E:A',
            'from-to': {'enti': arc['entity'], },
            'to-from': {'enti': arc_key, },
        })

    def add_relation(self, key: str, relation: dict):
        relation_parent_key = self.relation_map.create(key, key)
        relation_parent_node = etree.Element('packagedElement')
        self.package_node.append(relation_parent_node)

        relation_parent_node.set(self.xmi_ns + 'type', 'uml:Association')
        relation_parent_node.set(self.xmi_ns + 'id', relation_parent_key)
        relation_parent_node.set('visibility', 'public')

        # Add a name hint
        relation_parent_node.set('name', f"{relation['from-to']['enti']} - {relation['to-from']['enti']}")

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

        arc_src = relation['from-to'].get('arc')
        if arc_src is not None:
            from_key = arc_src
        else:
            # regular entity-entity relation
            from_key = relation['from-to']['enti']

        # reference source / from
        assert from_key is not None and len(from_key) > 3
        from_entity_key = self.class_map.get(from_key)
        src_class_ref = etree.Element('type')
        src_class_ref.set(self.xmi_ns + 'idref', from_entity_key)
        relation_src.append(src_class_ref)

        arc_target = relation['to-from'].get('arc')
        if arc_target is not None:
            to_key = arc_target
        else:
            to_key = relation['to-from']['enti']

        # reference to / destination
        assert to_key is not None and len(to_key) > 3
        to_entity_key = self.class_map.get(to_key)
        dst_class_ref = etree.Element('type')
        dst_class_ref.set(self.xmi_ns + 'idref', to_entity_key)
        relation_dst.append(dst_class_ref)

        if not 'E:A' in relation.get('type'):  # required only for regular relations
            self.set_cardinality(relation_src, relation['from-to']['maptype'], relation['from-to']['mandatory'],
                                 arc_src is not None)
            self.set_cardinality(relation_dst, relation['to-from']['maptype'], relation['to-from']['mandatory'])

        # hint
        debug_string = f"{key}: {relation['from-to']['enti']} <=> {relation['to-from']['enti']} {relation.get('type')}"
        relation_parent_node.set('documentation', debug_string)
        relation_parent_node.set('doc', debug_string)
        relation_parent_node.set('note', debug_string)
        relation_parent_node.set('hint', debug_string)

        return relation_parent_node

    def set_cardinality(self, end: etree.Element, cardinality: str, mandatory: bool, arc: bool = False):
        """"<lowerValue xmi:type="uml:LiteralInteger" xmi:id="EAID_LI000001_C29B_4f9a_8B72_FFE959450E46" value="1"/>
        <upperValue xmi:type="uml:LiteralInteger" xmi:id="EAID_LI000002_C29B_4f9a_8B72_FFE959450E46" value="1"/>"""
        if cardinality == 'M':
            upper_value = '-1'
        else:
            upper_value = '1'
            if mandatory:
                return

        lower_value = '1' if mandatory else '0'

        # Omit values to paint single line without any cardinality marker
        if not ((mandatory and cardinality == '1') or arc):
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

        dm = entity.get('dm')
        if dm is not None:
            modify_date = dateparser.parse(dm)
            project.set('modified', modify_date.strftime("%Y-%m-%d %H:%M:%S"))
        project.set('keywords', key)

        status = 'Proposed'
        publstatus = entity.get('publstatus')
        if publstatus is not None:
            if publstatus.upper() == 'DRAFT':
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

        # self.add_tag(entity_node, entity_ea_id, SSOT_ID_TAG, key)
        attributes_node = etree.Element('attributes')
        for attribute_key in entity['attributes+']:
            attributes_node.append(self.create_entity_attribute_ea(attribute_key))
        entity_node.append(attributes_node)

        return entity_node

    def create_entity_attribute_ea(self, attribute_key: str) -> etree.Element:
        """
        <attribute xmi:idref="EAID_CB0F96CF_C29B_4f9a_8B72_FFE959450E46" name="IATA Code" scope="Public">
						<initial/>
						<documentation/>
						<model ea_localid="8" ea_guid="{CB0F96CF-C29B-4f9a-8B72-FFE959450E46}"/>
						<properties type="Airport Codes" derived="0" collection="false" length="0" static="0" duplicates="0" changeability="changeable"/>
						<coords ordered="0"/>
						<containment containment="Not Specified" position="0"/>
						<stereotype stereotype="Attribute"/>
						<bounds lower="1" upper="1"/>
						<options/>
						<style/>
						<styleex value="volatile=0;union=0;"/>
						<tags/>
						<xrefs value="$XREFPROP=$XID={5B7359BB-3AF5-4f17-A2DB-224CF3A7E96A}$XID;$NAM=Stereotypes$NAM;$TYP=attribute property$TYP;$VIS=Public$VIS;$PAR=0$PAR;$DES=@STEREO;Name=Attribute;FQName=Informationmodel::Attribute;@ENDSTEREO;$DES;$CLT={CB0F96CF-C29B-4f9a-8B72-FFE959450E46}$CLT;$SUP=&lt;none&gt;$SUP;$ENDXREF;"/>
					</attribute>
        :param attribute_key:
        :return:
        """
        attribute = self.model.getbyid(attribute_key)
        assert attribute is not None

        node = etree.Element('attribute')
        ea_attr_id = self.attribute_map.get(attribute_key)
        node.set(self.xmi_ns + 'idref', ea_attr_id)
        node.set('name', self.translate(attribute['name']))

        # properties = etree.Element('properties')
        # properties.set('type', ) for LoV
        return node

    def create_ea_arc(self, key: str, arc: dict):
        entity_ea_id = self.class_map.get(key)
        entity_node = etree.Element('element')
        entity_node.set(self.xmi_ns + 'idref', entity_ea_id)
        entity_node.set(self.xmi_ns + 'type', 'uml:Constraint')
        # entity_node.set('name', self.safe_translate(entity.get('name')))
        entity_node.set('name', arc.get('name'))
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
        project.set('author', arc['uc'])
        create_date = dateparser.parse(arc['dc'])
        project.set('created', create_date.strftime("%Y-%m-%d %H:%M:%S"))
        dm = arc.get('dm')
        if dm is not None:
            modify_date = dateparser.parse(dm)
            project.set('modified', modify_date.strftime("%Y-%m-%d %H:%M:%S"))
        project.set('keywords', key)

        # <code product_name="Java" gentype="Java"/>
        code = etree.Element('code')
        entity_node.append(code)
        code.set('product_name', 'Informationmodel')
        code.set('gentype', 'IM')

        modified_date = arc.get('dm')
        if modified_date is not None:
            modify_date = dateparser.parse(modified_date)
            project.set('modified', modify_date.strftime("%Y-%m-%d %H:%M:%S"))

        # <properties isSpecification="false" sType="Constraint" nType="0" scope="public" stereotype="Arc"/>
        props = etree.Element('properties')
        entity_node.append(props)
        # props.set('documentation', f"Arc {key} from {arc.get('entity')} -> [{'|'.join(arc.get('relations'))}")
        props.set('isSpecification', 'false')
        props.set('sType', 'Constraint')
        props.set('nType', '0')
        props.set('scope', 'public')
        props.set('stereotype', 'Arc')

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

        # value="$XREFPROP=$XID={3DAF398E-F7D0-402a-B652-665590E1DBA1}$XID;
        # $NAM=Stereotypes$NAM;$TYP=element property$TYP;$VIS=Public$VIS;$PAR=0$PAR;$DES=@STEREO;
        # Name=Arc;FQName=Informationmodel::Arc;@ENDSTEREO;$DES;$CLT={FEAE01B6-71E0-4663-B202-EB07FF57D2D5}$CLT;$SUP=&lt;none&gt;$SUP;$ENDXREF;
        # $XREFPROP=$XID={67679D06-95BD-42cc-8BAC-E9CD38A9AFAE}$XID;$NAM=CustomProperties$NAM;$TYP=element property$TYP;$VIS=Public$VIS;$PAR=0$PAR;
        # $DES=@PROP=@NAME=_HideUmlLinks@ENDNAME;@TYPE=string@ENDTYPE;@VALU=True@ENDVALU;@PRMT=@ENDPRMT;@ENDPROP;
        # $DES;$CLT={FEAE01B6-71E0-4663-B202-EB07FF57D2D5}$CLT;$SUP=&lt;none&gt;$SUP;$ENDXREF;"

        xrefs.set('value', f"""$XREFPROP=$XID={{{str(uuid4())}}}$XID;\
$NAM=Stereotypes$NAM;$TYP=element property$TYP;$VIS=Public$VIS;$PAR=0$PAR;$DES=@STEREO;\
Name=Arc;FQName=Informationmodel::Arc;@ENDSTEREO;$DES;$CLT={{{cltid}}}$CLT;$SUP=<none>$SUP;$ENDXREF;\
$XREFPROP=$XID={{{uuid4()}}}$XID;$NAM=CustomProperties$NAM;$TYP=element property$TYP;$VIS=Public$VIS;$PAR=0$PAR;\
$DES=@PROP=@NAME=_HideUmlLinks@ENDNAME;@TYPE=string@ENDTYPE;@VALU=True@ENDVALU;@PRMT=@ENDPRMT;@ENDPROP;\
$DES;$CLT={{{cltid}}}$CLT;$SUP=<none>$SUP;$ENDXREF;""")

        # $XREFPROP=$XID={F1ED4092-6F2D-462f-9876-286322A1F40D}$XID;
        # $NAM=Stereotypes$NAM;$TYP=element property$TYP;$VIS=Public$VIS;$PAR=0$PAR;$DES=@STEREO;
        # Name=Arc;FQName=Informationmodel::Arc;@ENDSTEREO;@STEREO;Name=Arc ARCS110;FQName=Informationmodel::Arc;@ENDSTEREO;$DES;$CLT={ARC6E5F0A-A689-48F5-89BF-D569F3D83B00}$CLT;$SUP=&lt;none&gt;$SUP;$ENDXREF;$XREFPROP=$XID={4D659F6B-2545-48f5-8A96-865ED069EB0C}$XID;$NAM=CustomProperties$NAM;$TYP=element property$TYP;$VIS=Public$VIS;$PAR=0$PAR;$DES=@PROP=@NAME=_HideUmlLinks@ENDNAME;@TYPE=string@ENDTYPE;@VALU=True@ENDVALU;@PRMT=@ENDPRMT;@ENDPROP;$DES;$CLT={ARC6E5F0A-A689-48F5-89BF-D569F3D83B00}$CLT;$SUP=&lt;none&gt;$SUP;$ENDXREF;"/>

        # self.add_tag(entity_node, entity_ea_id, SSOT_ID_TAG, key)

        return entity_node

    def add_tag(self, parent: etree.Element, parent_key: str, key: str, value: str) -> etree.Element:
        """
        Add a custom tag
        ```
        <tags>
          <tag xmi:id="EAID_A5E86956_4364_4106_A61A_3D328E69C62A" name="SSOTID" value="ENTI174" modelElement="EAID_ENTI174B1_C174_418E_A1CB_158CEDB361B4"/>
        </tags>
        ```
        """
        tags = parent.find('tags')
        if tags is None or len(tags) < 1:
            tags = etree.Element('tags')
            parent.append(tags)
        else:
            tags = tags[0]
        tag = etree.Element('tag')
        tags.append(tag)

        tag.set(self.xmi_ns + 'id', str(uuid4()).replace('-', '_'))
        tag.set('name', key)
        tag.set('value', value)
        tag.set('modelElement', parent_key)

        return tag

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

        style1 = etree.Element('style1')
        ea_diagram.append(style1)
        style1.set('value',
                   "ShowPrivate=1;ShowProtected=1;ShowPublic=1;HideRelationships=0;Locked=0;Border=1;HighlightForeign=1;PackageContents=1;SequenceNotes=0;ScalePrintImage=0;PPgs.cx=0;PPgs.cy=0;DocSize.cx=783;DocSize.cy=1126;ShowDetails=0;Orientation=P;Zoom=100;ShowTags=0;OpParams=1;VisibleAttributeDetail=0;ShowOpRetType=1;ShowIcons=1;CollabNums=0;HideProps=0;ShowReqs=0;ShowCons=0;PaperSize=9;HideParents=0;UseAlias=0;HideAtts=0;HideOps=0;HideStereo=0;HideElemStereo=1;ShowTests=0;ShowMaint=0;ConnectorNotation=Information Engineering;ExplicitNavigability=0;ShowShape=1;AllDockable=0;AdvancedElementProps=1;AdvancedFeatureProps=1;AdvancedConnectorProps=1;m_bElementClassifier=0;SPT=1;ShowNotes=0;SuppressBrackets=0;SuppConnectorLabels=0;PrintPageHeadFoot=0;ShowAsList=0;")

        style2 = etree.Element('style2')
        ea_diagram.append(style2)
        # ConnectorNotation= Information Engineering -> Crow foot notation
        style2.set('value',
                   "ExcludeRTF=0;DocAll=0;HideQuals=0;AttPkg=1;ShowTests=0;ShowMaint=0;SuppressFOC=1;MatrixActive=0;SwimlanesActive=0;KanbanActive=0;MatrixLineWidth=1;MatrixLineClr=0;MatrixLocked=0;TConnectorNotation=Information Engineering;TExplicitNavigability=0;AdvancedElementProps=1;AdvancedFeatureProps=1;AdvancedConnectorProps=1;m_bElementClassifier=0;SPT=1;MDGDgm=;STBLDgm=;ShowNotes=0;VisibleAttributeDetail=0;ShowOpRetType=1;SuppressBrackets=0;SuppConnectorLabels=0;PrintPageHeadFoot=0;ShowAsList=0;SuppressedCompartments=,;Theme=:119;SaveTag=BB1CB51E;")

        elements = etree.Element('elements')
        ea_diagram.append(elements)

        # sequence number 1 = topmost element. painting starts with highest number
        sequence = 1

        # need entity coordinates later to place lines
        elment_position = {}

        # stack up elements in subtype-level order
        levels = list(map(lambda entity: int(entity['subtypellevel+']),
                          self.model.getelements(Modelelemtype.ENTI, pfiltered=False).values()))
        deepest_subtype_level = max(levels)
        # inverse order: process subtypes first to assign them small sequence numbers
        for subtypelevel in range(deepest_subtype_level, -1, -1):
            for entity in diagram['elements']['entity']:
                if int(self.model.getbyid(entity['element'])['subtypellevel+']) == subtypelevel:
                    element = etree.Element('element')
                    box = Rectangle((entity['pos_x'], entity['pos_y']), entity['ui']['width'], entity['ui']['height'])
                    element.set('geometry', "Left={x};Top={y};Right={right};Bottom={bottom};".format(
                        x=self.ea_coord(box.get_x()), y=self.ea_coord(box.get_y()),
                        right=self.ea_coord(box.get_x() + box.get_width()),
                        bottom=self.ea_coord(box.get_y() + box.get_height())
                    ))
                    elment_position[entity['element']] = box
                    element.set('subject', self.class_map.get(entity['element']))
                    element.set('seqno', str(sequence))
                    sequence += 1
                    elements.append(element)

        for key, arc in diagram['arcs'].items():
            element = etree.Element('element')

            # fake arc coordinates around circles
            x_coordinates = list(map(lambda e: e[0], arc['circles']))
            y_coordinates = list(map(lambda e: e[1], arc['circles']))
            width = max(x_coordinates) - min(x_coordinates)
            height = max(y_coordinates) - min(y_coordinates)
            horizontal_minimum = 20 if width < height else 150
            vertical_minimum = 20 if width >= height else 150
            box = Rectangle((min(x_coordinates), min(y_coordinates)),
                            max(width, horizontal_minimum),
                            max(height, vertical_minimum))
            # write bounding box to model
            arc['box'] = {'x': box.get_x(), 'y': box.get_y(), 'width': box.get_width(), 'height': box.get_height()}
            element.set('geometry', "Left={x};Top={y};Right={right};Bottom={bottom};".format(
                x=self.ea_coord(box.get_x()), y=self.ea_coord(box.get_y()),
                right=self.ea_coord(box.get_x() + box.get_width()),
                bottom=self.ea_coord(box.get_y() + box.get_height())
            ))
            elment_position[key] = box
            element.set('subject', self.class_map.get(key))
            element.set('seqno', str(sequence))
            element.set(SSOT_ID_TAG, key)
            sequence += 1
            elements.append(element)

        # <element geometry="SX=0;SY=0;EX=0;EY=0;EDGE=2;
        #       $LLB=CX=122:CY=13:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        #       LLT=CX=69:CY=40:OX=131:OY=-100:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        #       LMT=CX=27:CY=14:OX=7:OY=-1:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        #       LMB=;LRT=CX=61:CY=14:OX=94:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        #       LRB=CX=122:CY=13:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;
        #       IRHS=;
        #       ILHS=;
        #       Path=344:-160$436:-185$;"
        #   subject="EAID_182C295F_C77E_4e60_8565_F3500701C816"
        #   style="Mode=3;EOID=8224EF41;SOID=85BBD632;Color=-1;LWidth=0;Hidden=0;"/>
        for key, rel in diagram['relationships'].items():
            segments = rel['linesegments']
            relation = self.model.getbyid(key)
            source_entity = elment_position[relation['from-to']['enti']]
            target_entity = elment_position[relation['to-from']['enti']]

            arc_key = relation['from-to'].get('arc')
            if arc_key is not None:
                arc = diagram['arcs'][arc_key]
                # reposition end-points for arc source
                box = arc['box']
                segments[0]['x'] = box['x'] + (box['width'] / 2) + int(key[-1] * 5)
                segments[0]['y'] = box['y'] + (box['height'] / 2)
                source_entity = Rectangle((box['x'], box['y']),
                                          box['width'], box['height'])
            element = self.create_line(segments, source_entity, target_entity)
            element.set('subject', self.relation_map.get(key))
            element.set('style', "Mode=3;EOID=8224EF41;SOID=85BBD632;Color=-1;LWidth=0;Hidden=0;")
            element.set(SSOT_ID_TAG, key)
            elements.append(element)

        # Hide invisible relationships (Supertype <- Subtype)
        all_relations = self.find_invisible_relations(set(elment_position.keys()))
        invisible_relations = all_relations - set(diagram['relationships'].keys())
        self.hide_invisible_relations(elements, invisible_relations)

        return ea_diagram

    def find_invisible_relations(self, visible_elements: Set[str]) -> Set[str]:
        """Find all relations connected to two elements on the diagram
        @:parameter visible_elements Entities, Arcs
        """
        all_relevant_relations = set()
        for element_key in visible_elements:
            for relation_key, relation in self.model.getelements(Modelelemtype.RELA, pfiltered=False).items():
                if relation['from-to']['enti'] == element_key or relation['to-from']['enti'] == element_key:
                    all_relevant_relations.add(relation_key)

        return all_relevant_relations

    def hide_invisible_relations(self, parent: etree.Element, invisible_relations: []):
        for relation_key in invisible_relations:
            element = etree.Element('element')
            parent.append(element)
            element.set('geometry', 'SX=0:SY=0:EX=0:EY=0:EDGE=2;$LLB=;LLT=;LMT=;LMB=;LRT=;IRHS=;ILHS=;Path=;')
            element.set('subject', self.relation_map.get(relation_key))
            element.set('style', 'Mode=3;EOID=8224EF41;SOID=85BBD632;Color=-1;LWidth=0;Hidden=1;')
            element.set(SSOT_ID_TAG, relation_key)

    def create_line(self, segments: [], source_box: Rectangle, target_box: Rectangle) -> etree.Element:
        """Add relations to diagram"""
        assert len(segments) > 1
        assert source_box is not None
        assert target_box is not None

        element = etree.Element('element')
        sx, sy = self.relative_to(source_box, segments[0])
        ex, ey = self.relative_to(target_box, segments[-1])
        geo = f"SX={self.ea_coord(sx)};SY={self.ea_coord(sy * -1)};EX={self.ea_coord(ex)};EY={self.ea_coord(ey * -1)};"
        geo += "EDGE=2;$"
        geo += self.label('LLB', True)  # LEFT BOTTOM - Hide source cardinality label
        geo += self.label('LLT', False)  # LEFT TOP - Show source name
        geo += self.label('LMT', True)  # MIDDLE TOP - Hide relation name
        geo += self.label('LMB', True)  # MIDDLE BOTTOM - Hide relation stereotype
        geo += self.label('LRT', False)  # RIGHT TOP - Show target name
        geo += self.label('LRB', True)  # RIGHT BOTTOM - Hide target cardinality label
        geo += 'IRHS=;ILHS=;Path='
        for waypoint in segments[1:-1]:
            geo += f"{self.ea_coord(waypoint['x'])}:{self.ea_coord(waypoint['y'] * -1)}$"
        geo += ';'
        element.set('geometry', geo)
        return element

    def label(self, id: str, hidden: bool):
        """CX=17:CY=14:OX=0:OY=0:HDN=0:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;"""
        return f"{id}=CX=0:CY=0:OX=0:OY=0:HDN={'1' if hidden else '0'}:BLD=0:ITA=0:UND=0:CLR=-1:ALN=0:DIR=0:ROT=0;"

    def relative_to(self, box: Rectangle, segment: dict) -> (int, int):
        box_center_x = box.get_x() + (box.get_width() / 2)
        box_center_y = box.get_y() + (box.get_height() / 2)
        return segment['x'] - box_center_x, segment['y'] - box_center_y

    def translate(self, element: dict) -> str:
        if element is None or len(element) < 1:
            assert False, f"Element {element} cannot be translated"
        return element.get(self.language, element.get('en', list(element.values())[0]))

    def safe_translate(self, element: dict) -> str:
        if element is None:
            return ''
        result = self.translate(element)
        if result is None:
            result = ''
        return result

    def entity_name(self, key: str) -> str:
        enti = self.model.getbyid(key)
        assert enti is not None
        return self.safe_translate(enti['name'])

    def ea_coord(self, point: float) -> int:
        return int(round(point * self.scale))
