from config.config import config_obj

QUERY_TEMPLATE = lambda query: f"""
<?xml version="1.0" encoding="UTF-8"?>
<csw:GetRecords xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" service="CSW" maxRecords="{config_obj["pycsw"].PYCSW_RETURN_NUMBER_PROPERTY}"  startPosition="1"
outputSchema="http://schema.mapcolonies.com/raster" version="2.0.2" xmlns:mc="mc:MCRasterRecord" >
  <csw:Query typeNames="[SUB-SYSTEM-TYPENAME]">
   <csw:ElementSetName>full</csw:ElementSetName>
    <csw:Constraint version="1.1.0">
      <Filter xmlns="http://www.opengis.net/ogc">
        <PropertyIsLike wildCard="%" singleChar="_" escapeChar="\\">
          <PropertyName>{query["name"]}</PropertyName>
          <Literal>{query["value"]}</Literal>
        </PropertyIsLike>
      </Filter>
    </csw:Constraint>
  </csw:Query>
</csw:GetRecords>


"""
