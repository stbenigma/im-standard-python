from lxml import etree
from io import BytesIO
from gettext import gettext

from IM_db.IM_JSON import JSModel

drawio_diagram_base = """<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="Electron" modified="2021-07-20T12:02:15.557Z" agent="curl/7.1" etag="25mQkM6mx7LJW4tu3GDx" version="14.6.13" type="device">
  <diagram id="-IuDeWdp_pBGzQphX35I" name="{name}">
    <mxGraphModel dx="{width}" dy="{height}" pageWidth="{width}" pageHeight="{height}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""


def create_diagram(diagram_key: str, model: JSModel, language, base=drawio_diagram_base) -> etree:
    """Create a draw.io diagram from the corresponding node in the jsmodel"""
    assert model is not None, f"Expecting a valid model"
    diagram = model.getbyid(diagram_key)
    parser = etree.XMLParser(remove_blank_text=True)
    xml_source = base.format(name=diagram['name'], width=str(diagram['width']), height=str(diagram['height']))
    dom = etree.parse(BytesIO(xml_source.encode('utf-8')), parser)

    xml_node = dom.find('.//root')

    add_entities(diagram, model, language, xml_node)
    add_relations(diagram, model, language, xml_node)

    return dom


def sort_by_subtype_level(diagram_entities: [], model: JSModel) -> []:
    return sorted(diagram_entities, key=lambda e: int(model.getbyid(e['element'])['subtypellevel+']))


entity_style = "rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=top;"


def add_entities(diagram, model: JSModel, language, root: etree):
    for element in sort_by_subtype_level(diagram['elements']['entity'], model):
        enti_key = element['element']
        enti = model.getbyid(enti_key)

        # create the container
        uo = etree.Element('UserObject')
        uo.set('id', enti_key)
        uo.set('label', enti['name'][language])
        uo.set('link', 'ssot:' + enti_key)
        description = enti.get('descr', {}).get(language)
        if description is not None and len(description) > 0:
            uo.set(gettext("Beschreibung"), description)

        synonyms = enti['synonyms']
        if synonyms is not None and len(synonyms) > 0:
            syn_list = map(lambda s: s.get(language), synonyms.values())
            synonym_str = ', '.join(syn_list)
            uo.set(gettext("Synonyme"), synonym_str)

        fillcolor = '#' + element.get('ui', {}).get('color', "FFFFFF")
        # fill = spectra.html('#' + fillcolor)

        # supertypes = enti.get('supertypes+', [])
        # if len(supertypes) > 0 and len(visible.intersection(supertypes)) > 0:
        #    # print(f"Brightening up {enti_key}")
        #    fill = fill.brighten(amount=5)

        cell = etree.Element("mxCell", id=enti_key + '-cell', style=entity_style + f"fillColor={fillcolor};",
                             parent='1', vertex='1')

        box = etree.Element("mxGeometry", x=str(element['pos_x']), y=str(element['pos_y']),
                            width=str(element['ui']['width']), height=str(element['ui']['height']))
        box.set('as', 'geometry')

        cell.append(box)
        uo.append(cell)
        root.append(uo)


# orthogonalEdgeStyle
# elbowEdgeStyle
connector_style = "html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;jumpStyle=none;edgeStyle=orthogonalEdgeStyle;"


def add_relations(diagram, model: JSModel, lang, parent):
    for key, relation in diagram['relationships'].items():
        linekeys = relation['linesegments'].keys()
        segments_sorted = sorted(linekeys, key=lambda e: int(e))
        assert len(segments_sorted) > 2, f"Expecting at least 2 points"
        start = relation['linesegments'][segments_sorted[0]]
        end = relation['linesegments'][segments_sorted[-1]]
        elbows = segments_sorted[1:-1]

        connector = etree.Element('mxCell', edge="1", parent="1", width="50", height="50")
        connector.set('id', key)
        geo = etree.Element('mxGeometry', width='50', height='50', relative='1')
        geo.set('as', 'geometry')

        start_node = etree.Element('mxPoint', x=str(start['x']), y=str(start['y']))
        start_node.set('as', 'sourcePoint')
        geo.append(start_node)

        end_node = etree.Element('mxPoint', x=str(end['x']), y=str(end['y']))
        end_node.set('as', 'targetPoint')
        geo.append(end_node)

        if len(elbows) > 0:
            elbows = etree.Element('Array')
            elbows.set('as', 'points')
            for linesegment in elbows:
                segment = relation['linesegments'][linesegment]
                elbow = etree.Element('mxPoint', x=str(segment['x']), y=str(segment('y')))
                elbows.append(elbow)

            geo.append(elbows)

        # Set end's
        relation_ssot = model.getbyid(key)
        start_type = map_line_end(relation['start_connector'], relation_ssot['from-to'].get('mandatory'))
        end_type = map_line_end(relation['end_connector'])
        connector.set('style', connector_style + f'startArrow={start_type};endArrow={end_type};')

        connector.append(geo)
        parent.append(connector)

        labeltext = relation_ssot['from-to'].get('assoc').get(lang)
        add_label(relation, 'start', labeltext, f"{key}-from", parent)

        labeltext = relation_ssot['to-from'].get('assoc').get(lang)
        add_label(relation, 'end', labeltext, f"{key}-to", parent)


def map_line_end(cardinality: str, mandatory: bool = False) -> str:
    """Map cardinalities from JSModel encoding to drawio encoding"""
    if 'M' == cardinality:
        return 'ERoneToMany' if mandatory else 'ERmany'
    elif '1' == cardinality:
        return 'ERzeroToOne' if mandatory else 'ERone'
    return 'none'


def add_label(relation, end: str, labeltext: str, key: str, parent):
    if labeltext is not None and len(labeltext) > 0:
        start_label = etree.Element('mxCell', value=labeltext, parent="1", vertex="1",
                                    style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;labelBackgroundColor=#FFFFFF;")
        start_label.set('id', key)

        start_label_box = etree.Element('mxGeometry', x=str(int(relation[f'{end}text_x']) + 2),
                                        y=str(int(relation[f'{end}text_y']) + 2),
                                        width=str(int(relation[f'{end}text_width']) - 4),
                                        height=str(int(relation[f'{end}text_height'] - 4)))
        start_label_box.set('as', 'geometry')

        start_label.append(start_label_box)
        parent.append(start_label)
