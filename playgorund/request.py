from lxml import etree
from typing import List


def create_wfs_getfeature_body(pos_list: List[float], type_name: str) -> str:
    """
    Generates a full WFS GetFeature XML body with an Intersects filter using a gml:Polygon.

    :param pos_list: List of coordinates in [x1, y1, x2, y2, ..., xn, yn] format.
    :param type_name: Feature type name to query.
    :return: XML string of the GetFeature request.
    """
    # Namespaces
    NSMAP = {
        'wfs': "http://www.opengis.net/wfs/2.0",
        'fes': "http://www.opengis.net/fes/2.0",
        'gml': "http://www.opengis.net/gml/3.2",
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'my': "http://www.someserver.com/my"
    }

    # Root element
    root = etree.Element(
        "{http://www.opengis.net/wfs/2.0}GetFeature",
        nsmap=NSMAP,
        service="WFS",
        version="2.0.0",
        attrib={
            "{http://www.w3.org/2001/XMLSchema-instance}schemaLocation":
                "http://www.opengis.net/wfs/2.0 http://schemas.opengis.net/wfs/2.0/wfs.xsd"
        }
    )

    # wfs:Query
    query = etree.SubElement(root, "{http://www.opengis.net/wfs/2.0}Query", typeNames=type_name)

    # fes:Filter
    filter_elem = etree.SubElement(query, "{http://www.opengis.net/fes/2.0}Filter")

    # fes:Intersects
    intersects = etree.SubElement(filter_elem, "{http://www.opengis.net/fes/2.0}Intersects")

    # fes:ValueReference
    value_ref = etree.SubElement(intersects, "{http://www.opengis.net/fes/2.0}ValueReference")
    value_ref.text = "footprint"

    # gml:Polygon
    polygon = etree.SubElement(
        intersects,
        "{http://www.opengis.net/gml/3.2}Polygon",
        srsName="EPSG:4326"
    )
    exterior = etree.SubElement(polygon, "{http://www.opengis.net/gml/3.2}exterior")
    linear_ring = etree.SubElement(exterior, "{http://www.opengis.net/gml/3.2}LinearRing")
    pos_list_elem = etree.SubElement(linear_ring, "{http://www.opengis.net/gml/3.2}posList")

    # Format posList as space-separated string
    pos_list_elem.text = " ".join(f"{x:.14f}" for x in pos_list)

    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode('utf-8')


print(type(
    create_wfs_getfeature_body(type_name="automation_2025_05_07_15_22_58-RasterVectorBest", pos_list=[34.48760376150682
        , 31.530834035809296
        , 34.48819410915064
        , 31.530834035809296
        , 34.48819410915064
        , 31.531043009844296
        , 34.48760376150682
        , 31.531043009844296
        , 34.48760376150682
        , 31.530834035809296]))
)