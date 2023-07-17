from config.config import config_obj

# Constants for XML post requests - with data

# POLYGON_XML = rf"""<?xml version="1.0" encoding="UTF-8"?>
#
# <csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" service="CSW" maxRecords="1" startPosition="1" \
# outputSchema="http://schema.mapcolonies.com/raster" version="2.0.2" xmlns:mc="http://schema.mapcolonies.com/raster" >
#
# <csw:Query typeNames="mc:MCRasterRecord">
#
# <csw:ElementSetName>brief</csw:ElementSetName>
#
# <csw:Constraint version="1.1.0">
#
# <Filter xmlns="http://www.opengis.net/ogc">
#
# <PropertyIsLike wildCard="%" singleChar="_" escapeChar="\\">
#
# <PropertyName>{config_obj['pycsw'].PYCSW_POLYGON_PROPERTY}</PropertyName>
#
# <Literal>{config_obj['pycsw'].PYCSW_POLYGON_VALUE}</Literal>
#
# </PropertyIsLike>
#
# </Filter>
#
# </csw:Constraint>
#
# </csw:Query>
#
# </csw:GetRecords>
# """
#
# ID_RECORD_XML = rf"""<?xml version="1.0" encoding="UTF-8"?>
#
# <csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" service="CSW" maxRecords="1" startPosition="1" \
# outputSchema="http://schema.mapcolonies.com/raster" version="2.0.2" xmlns:mc="http://schema.mapcolonies.com/raster" >
#
# <csw:Query typeNames="mc:MCRasterRecord">
#
# <csw:ElementSetName>brief</csw:ElementSetName>
#
# <csw:Constraint version="1.1.0">
#
# <Filter xmlns="http://www.opengis.net/ogc">
#
# <PropertyIsLike wildCard="%" singleChar="_" escapeChar="\\">
#
# <PropertyName>{config_obj['pycsw'].PYCSW_ID_PROPERTY}</PropertyName>
#
# <Literal>{config_obj['pycsw'].PYCSW_ID_VALUE}</Literal>
#
# </PropertyIsLike>
#
# </Filter>
#
# </csw:Constraint>
#
# </csw:Query>
#
# </csw:GetRecords>
# """
#
# REGION_RECORD_XML = rf"""<?xml version="1.0" encoding="UTF-8"?>
#
# <csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" service="CSW" maxRecords="1" startPosition="1" \
# outputSchema="http://schema.mapcolonies.com/raster" version="2.0.2" xmlns:mc="http://schema.mapcolonies.com/raster" >
#
# <csw:Query typeNames="mc:MCRasterRecord">
#
# <csw:ElementSetName>brief</csw:ElementSetName>
#
# <csw:Constraint version="1.1.0">
#
# <Filter xmlns="http://www.opengis.net/ogc">
#
# <PropertyIsLike wildCard="%" singleChar="_" escapeChar="\\">
#
# <PropertyName>{config_obj['pycsw'].PYCSW_REGION_PROPERTY}</PropertyName>
#
# <Literal>{config_obj['pycsw'].PYCSW_REGION_VALUE}</Literal>
#
# </PropertyIsLike>
#
# </Filter>
#
# </csw:Constraint>
#
# </csw:Query>
#
# </csw:GetRecords>
# """


def QUERY_TEMPLATE(query):
    return f"\n<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<csw:GetRecords xmlns:csw=\"http://www.opengis.net/cat/csw/2.0.2\" service=\"CSW\" maxRecords=\"{config_obj['pycsw'].PYCSW_RETURN_NUMBER_PROPERTY}\"  startPosition=\"1\"\noutputSchema=\"http://schema.mapcolonies.com/raster\" version=\"2.0.2\" xmlns:mc=\"mc:MCRasterRecord\" >\n  <csw:Query typeNames=\"[SUB-SYSTEM-TYPENAME]\">\n   <csw:ElementSetName>full</csw:ElementSetName>\n    <csw:Constraint version=\"1.1.0\">\n      <Filter xmlns=\"http://www.opengis.net/ogc\">\n        <PropertyIsLike wildCard=\"%\" singleChar=\"_\" escapeChar=\"\\\">\n          <PropertyName>{query['name']}</PropertyName>\n          <Literal>{query['value']}</Literal>\n        </PropertyIsLike>\n      </Filter>\n    </csw:Constraint>\n  </csw:Query>\n</csw:GetRecords>\n\n\n"
