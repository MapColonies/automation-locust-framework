import xml.etree.ElementTree as ET


def build_filter_xml(type_name, filters, wfs_version="2.0.0", ogc_ns="http://www.opengis.net/ogc"):
    """
    Build a WFS GetFeature POST XML body with multiple filters.

    :param type_name: The name of the feature type (layer name).
    :param filters: A dictionary of property_name: value pairs to filter on.
    :param wfs_version: The WFS version to use (default: "2.0.0").
    :param ogc_ns: The OGC namespace (adjust based on version).
    :return: XML string of the GetFeature request.
    """
    ns_wfs = "http://www.opengis.net/wfs/2.0"
    ns_gml = "http://www.opengis.net/gml/3.2"
    ns_xsi = "http://www.w3.org/2001/XMLSchema-instance"
    ns_fes = "http://www.opengis.net/fes/2.0" if wfs_version == "2.0.0" else ogc_ns

    ET.register_namespace("wfs", ns_wfs)
    ET.register_namespace("gml", ns_gml)
    ET.register_namespace("xsi", ns_xsi)
    ET.register_namespace("fes", ns_fes)

    # Root element: GetFeature
    get_feature = ET.Element(f"{{{ns_wfs}}}GetFeature", {
        "service": "WFS",
        "version": wfs_version
    })

    # Query element
    query = ET.SubElement(get_feature, f"{{{ns_wfs}}}Query", {"typeNames": type_name})

    # Filter element
    filter_elem = ET.SubElement(query, f"{{{ns_fes}}}Filter")

    if len(filters) > 1:
        and_elem = ET.SubElement(filter_elem, f"{{{ns_fes}}}And")
    else:
        and_elem = filter_elem

    for prop, val in filters.items():
        equals = ET.SubElement(and_elem, f"{{{ns_fes}}}PropertyIsEqualTo")
        prop_name = ET.SubElement(equals, f"{{{ns_fes}}}ValueReference")
        prop_name.text = prop
        literal = ET.SubElement(equals, f"{{{ns_fes}}}Literal")
        literal.text = str(val)

    return ET.tostring(get_feature, encoding="unicode")

filters = {
    "country": "Germany",
    "population": "83000000"
}
type_name = "vector:buildings"

xml_body = build_filter_xml(type_name, filters)
print(xml_body)
