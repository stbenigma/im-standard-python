from lxml import etree
from io import BytesIO
from gettext import gettext
import logging
from matplotlib import colors

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


def create_diagram(diagram_key: str, model: JSModel, translator, base=drawio_diagram_base) -> etree:
    """Create a draw.io diagram from the corresponding node in the jsmodel
    :parameter translator implements gettext() as in the gettext module and tr() to translate SSOT fields
    """
    assert model is not None, f"Expecting a valid model"
    diagram = model.getbyid(diagram_key)
    parser = etree.XMLParser(remove_blank_text=True)
    xml_source = base.format(name=diagram['name'], width=str(diagram['width']), height=str(diagram['height']))
    dom = etree.parse(BytesIO(xml_source.encode('utf-8')), parser)

    xml_node = dom.find('.//root')

    add_entities(diagram, model, translator, xml_node)
    add_relations(diagram, model, translator, xml_node)

    return dom


def sort_by_subtype_level(diagram_entities: [], model: JSModel) -> []:
    return sorted(diagram_entities, key=lambda e: int(model.getbyid(e['element'])['subtypellevel+']))


def to_color(color):
    """Convert color sting in hex to color tuple"""
    if isinstance(color, str):
        return colors.to_rgba('#' + color)
    return color


entity_style = "rounded=1;whiteSpace=wrap;html=1;align=center;verticalAlign=top;"


def prefix_attribute_name():
    """Default generator for attribute prefixes"""
    value = 48
    while True:
        yield f"A{chr(value)}_"
        value += 1


def prefix_none():
    """Default generator for attribute prefixes"""
    while True:
        yield f""


def html_tooltip(entity, translator) -> str:
    """Create a rich text tooltip according to """
    tooltip_text = [f"""<h1>{translator.tr(entity['name'])}</h1>"""]

    description = translator.tr(entity.get('descr'))
    if description is not None and len(description) > 0:
        tooltip_text.append(f"<p>{description}<p>")

    synonyms = entity['synonyms']
    if synonyms is not None and len(synonyms) > 0:
        syn_list = map(lambda s: translator.tr(s), synonyms.values())
        synonym_str = ', '.join(syn_list)
        tooltip_text.append(f"<h2>{translator.tr('Synonyms')}</h2><p>{synonym_str}</p>")

    tt = translator.tr(entity.get('tooltip'))
    if tt is not None and len(tt) > 0:
        tooltip_text.append(f"<h2>{translator.tr('Tooltip')}</h2><p>{tt}</p>")

    return ''.join(tooltip_text)


def add_entities(diagram, model: JSModel, translator, root: etree):
    for element in sort_by_subtype_level(diagram['elements']['entity'], model):

        prefix_generator = prefix_none()

        enti_key = element['element']
        enti = model.getbyid(enti_key)

        # create the container
        uo = etree.Element('UserObject')
        uo.set('id', enti_key)
        uo.set('label', translator.tr(enti['name']))
        uo.set('link', 'ssot:' + enti_key)

        # Add mouseover values: https://drawio.freshdesk.com/support/solutions/articles/16000067813-edit-and-display-shape-metadata
        # Tooltip support embedded html: ... tooltip="&lt;h1&gt;Beschreibung&lt;/h1&gt;"
        # Tooltip (https://www.diagrams.net/doc/faq/tooltips) is an alternative, but does not support Key Value display as do attributes
        uo.set(next(prefix_generator) + gettext("Name"), translator.tr(enti['name']))

        description = translator.tr(enti.get('descr'))
        if description is not None and len(description) > 0:
            uo.set(next(prefix_generator) + gettext("Beschreibung"), description)

        synonyms = enti['synonyms']
        if synonyms is not None and len(synonyms) > 0:
            syn_list = map(lambda s: translator.tr(s), synonyms.values())
            synonym_str = ', '.join(syn_list)
            uo.set(next(prefix_generator) + gettext("Synonyme"), synonym_str)

        tooltip_content = html_tooltip(enti, translator)
        if tooltip_content and len(tooltip_content) > 0:
            # tooltip_content += f"<hr><a href=\"ssot:{enti_key}\">{translator.tr('Details')}</a>"
            uo.set('tooltip', tooltip_content)

        tags = []
        category = enti.get('category')
        if category and len(category) > 0:
            tags.append(category)
        roles = enti.get('roles+')
        if roles and len(roles) > 0:
            tags.extend(roles)
        if len(tags) > 0:
            uo.set('tags', ' '.join(tags))

        style = entity_style
        # stroke_color = '#' + element.get('ui', {}).get('color', "FFFFFF")

        color = to_color(element.get('ui', {}).get('color', 'FFFFFF'))
        nesting_level = int(enti.get('subtypellevel+', 0) + 1)
        hsv_color = colors.rgb_to_hsv(color[0:3])
        adjusted_saturation = hsv_color[1] / nesting_level
        lighter = colors.hsv_to_rgb((hsv_color[0], adjusted_saturation, hsv_color[2]))

        # alpha blend
        # lighter = (*lighter, .23)

        # print(f"Nesting {nesting_level} of entity {translator.tr(enti['name'])} changes saturation from {hsv_color[1]} to {adjusted_saturation} and {lighter}")
        style = ''.join([style, 'fillColor=', colors.to_hex(lighter, keep_alpha=True), ';'])

        cell = etree.Element("mxCell", id=enti_key + '-cell', style=style,
                             parent='1', vertex='1')

        box = etree.Element("mxGeometry", x=str(element['pos_x']), y=str(element['pos_y']),
                            width=str(element['ui']['width']), height=str(element['ui']['height']))
        box.set('as', 'geometry')

        cell.append(box)
        uo.append(cell)
        root.append(uo)


def relation_to_line(segments: [], key: str):
    cell = etree.Element('mxCell', edge="1", parent="1", width="50", height="50")
    cell.set('id', key)

    geo = etree.Element('mxGeometry', width='50', height='50', relative='1')
    geo.set('as', 'geometry')
    start = segments[0]

    source_point = etree.Element('mxPoint', x=str(start['x']), y=str(start['y']))
    source_point.set('as', 'sourcePoint')
    geo.append(source_point)

    end = segments[-1]
    target_point = etree.Element('mxPoint', x=str(end['x']), y=str(end['y']))
    target_point.set('as', 'targetPoint')
    geo.append(target_point)

    logging.debug(f"Line with {len(segments)} segments {start['x']}/{start['y']} to {end['x']}/{end['y']}")

    if len(segments) > 2:
        elbows = etree.Element('Array')
        elbows.set('as', 'points')
        for point in segments[1:-1]:
            elbow = etree.Element('mxPoint', x=str(point['x']), y=str(point['y']))
            elbows.append(elbow)
        geo.append(elbows)

    cell.append(geo)
    return cell



# elbowEdgeStyle
# edgeStyle=orthogonalEdgeStyle;
connector_style = "html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;jumpStyle=none;rounded=0;"


# Lines can consist of multiple styles (linetype = SOLID|DASHED)
# The change from one type to the other requires to break the line in two segments
#
def add_relations(diagram, model: JSModel, translator, parent):
    for key, relation in diagram['relationships'].items():
        segments = relation['linesegments']
        assert len(segments) > 1, f"Expecting at least 2 points"
        start = segments[0]

        elbows = segments[1:-1]

        line_type = segments[0]['linetype']
        if 'DASHED' == line_type:
            start_dashing = '1' #;dashPattern=1 1'
        else:
            start_dashing = '0'

        change_point = -1
        index = 1
        for segment in segments[1:]:
            next_type = segment['linetype']
            if line_type != next_type:
                assert change_point < 0, f"The line style alters multiple times. Last change seen on position {change_point}"
                change_point = index
                if 'DASHED' == next_type:
                    end_dashing = '1' #;dashPattern=1 1;'
                else:
                    end_dashing = '0'
                break
            index += 1

        # Read cardinality
        relation_ssot = model.getbyid(key)
        assert relation_ssot is not None, "Cannot look up relation {key}"
        start_type = map_line_end(relation['start_connector'], relation_ssot['from-to'].get('mandatory'))
        end_type = map_line_end(relation['end_connector'], relation_ssot['to-from'].get('mandatory'))

        if change_point < 1:
            # just one line
            line = relation_to_line(segments, key)
            line.set('style', connector_style + f"dashed={start_dashing};startArrow={start_type};endArrow={end_type};")
            parent.append(line)
        else:
            logging.debug(f"Found line change on position {change_point} in line with {len(elbows)} elbows")
            front = relation_to_line(segments[:change_point+1], key)
            front.set('style', connector_style + f"dashed={start_dashing};startArrow={start_type};endArrow=none")
            parent.append(front)

            back = relation_to_line(segments[change_point:], key + 'tail')
            back.set('style', connector_style + f"dashed={end_dashing};endArrow={end_type};startArrow=none")
            parent.append(back)

        front_label_text = translator.tr(relation_ssot['from-to'].get('assoc'))
        if add_label(relation, 'start', front_label_text, f"{key}-from", parent) is None:
            logging.warning(f"Missing coordinates for label '{front_label_text}' on start of relation {key}")

        tail_label_text = translator.tr(relation_ssot['to-from'].get('assoc'))
        if add_label(relation, 'end', tail_label_text, f"{key}-to", parent) is None:
            logging.warning(f"Missing coordinates for label '{tail_label_text}' on end of relation {key}")


def map_line_end(cardinality: str, mandatory: bool = False) -> str:
    """
    Map cardinalities from JSModel encoding to drawio encoding.
    Mandatory is encoded in the line style (solid = mandatory, dashed=optional) therefore not used here
    """
    if 'M' == cardinality:
        return 'ERmany'
    return 'none'


def add_label(relation, end: str, labeltext: str, key: str, parent) -> etree.Element:
    if labeltext is not None and len(labeltext) > 0:
        if relation.get(f'{end}text_x'):
            start_label = etree.Element('mxCell', value=labeltext, parent="1", vertex="1",
                                        style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;labelBackgroundColor=#F0F0F0;")
            start_label.set('id', key)

            start_label_box = etree.Element('mxGeometry', x=str(int(relation[f'{end}text_x']) + 2),
                                            y=str(int(relation[f'{end}text_y']) + 2),
                                            width=str(int(relation[f'{end}text_width']) - 4),
                                            height=str(int(relation[f'{end}text_height'] - 4)))
            start_label_box.set('as', 'geometry')

            start_label.append(start_label_box)
            parent.append(start_label)

            return start_label
