import xml.etree.ElementTree as ET

import requests

# Load the XML data
xml_data = '''
<Capabilities xmlns="http://www.opengis.net/wmts/1.0" xmlns:ows="http://www.opengis.net/ows/1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:gml="http://www.opengis.net/gml" xsi:schemaLocation="http://www.opengis.net/wmts/1.0 http://schemas.opengis.net/wmts/1.0/wmtsGetCapabilities_response.xsd" version="1.0.0">
<ows:ServiceIdentification>
<ows:Title>MapProxy WMS Proxy</ows:Title>
<ows:Abstract>This is a minimal MapProxy example.</ows:Abstract>
<ows:ServiceType>OGC WMTS</ows:ServiceType>
<ows:ServiceTypeVersion>1.0.0</ows:ServiceTypeVersion>
<ows:Fees>none</ows:Fees>
<ows:AccessConstraints>none</ows:AccessConstraints>
</ows:ServiceIdentification>
<Contents>
<Layer>
<ows:Title>Omniscale OSM WMS - osm.omniscale.net</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -85.0511287798066</ows:LowerCorner>
<ows:UpperCorner>180.0 85.0511287798066</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>osm</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>webmercator</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/osm/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>dev-test-transparent-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>dev-test-transparent-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/dev-test-transparent-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>dev-test-transparent2-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>dev-test-transparent2-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/dev-test-transparent2-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>dev-test-transparent3-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>dev-test-transparent3-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/dev-test-transparent3-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>dev-test-OPAQUE-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>dev-test-OPAQUE-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/dev-test-OPAQUE-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>2dev-test-OPAQUE-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2dev-test-OPAQUE-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2dev-test-OPAQUE-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>shay_165-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay_165-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay_165-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>25dev-test-OPAQUE-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>25dev-test-OPAQUE-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/25dev-test-OPAQUE-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>string-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>string-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/string-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay3-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay3-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay3-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay4-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay4-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay4-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay5-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay5-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay5-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>check-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>check-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/check-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay6-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay6-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay6-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay8-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay8-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay8-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay9-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay9-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay9-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay10-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay10-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay10-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay11-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay11-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay11-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay12-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay12-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay12-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay13-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay13-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay13-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay14-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay14-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay14-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay15-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay15-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay15-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay16-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay16-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay16-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay17-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay17-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay17-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay18-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay18-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay18-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay19-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay19-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay19-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay20-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay20-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay20-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay21-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay21-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay21-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay22-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay22-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay22-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2555555dev-test-OPAQUE-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2555555dev-test-OPAQUE-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2555555dev-test-OPAQUE-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>shay23-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay23-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay23-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T08_17_08Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T08_17_08Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T08_17_08Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T08_23_48Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T08_23_48Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T08_23_48Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T08_50_59Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T08_50_59Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T08_50_59Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T09_08_20Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T09_08_20Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T09_08_20Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T09_20_16Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T09_20_16Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T09_20_16Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T09_23_13Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T09_23_13Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T09_23_13Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T09_54_43Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T09_54_43Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T09_54_43Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T10_22_13Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T10_22_13Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T10_22_13Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T10_34_05Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T10_34_05Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T10_34_05Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T11_50_57Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T11_50_57Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T11_50_57Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T12_00_16Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T12_00_16Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T12_00_16Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T12_59_27Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T12_59_27Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T12_59_27Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T13_17_58Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T13_17_58Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T13_17_58Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T13_27_33Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T13_27_33Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T13_27_33Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T13_34_42Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T13_34_42Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T13_34_42Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T13_57_21Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T13_57_21Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T13_57_21Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay26-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay26-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay26-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay27-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay27-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay27-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T18_18_20Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T18_18_20Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T18_18_20Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_17T18_53_22Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_17T18_53_22Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_17T18_53_22Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_18T09_31_34Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_18T09_31_34Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_18T09_31_34Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_18T14_00_44Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_18T14_00_44Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_18T14_00_44Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay28-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay28-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay28-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay29-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay29-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay29-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay30-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay30-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay30-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay31-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay31-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay31-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay32-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay32-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay32-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay33-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay33-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay33-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay34-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay34-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay34-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay35-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay35-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay35-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay36-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay36-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay36-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_19T08_12_56Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_19T08_12_56Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_19T08_12_56Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>ronen_test-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>ronen_test-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/ronen_test-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>2023_01_19T09_30_26Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_19T09_30_26Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_19T09_30_26Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_19T09_39_43Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_19T09_39_43Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_19T09_39_43Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_19T09_43_54Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_19T09_43_54Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_19T09_43_54Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_19T09_47_38Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_19T09_47_38Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_19T09_47_38Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_19T09_56_18Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_19T09_56_18Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_19T09_56_18Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_19T11_40_33Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_19T11_40_33Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_19T11_40_33Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_19T13_41_20Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_19T13_41_20Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_19T13_41_20Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_19T13_45_48Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_19T13_45_48Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_19T13_45_48Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_22T08_14_04Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_22T08_14_04Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_22T08_14_04Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_22T11_28_04Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_22T11_28_04Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_22T11_28_04Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_22T13_41_19Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_22T13_41_19Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_22T13_41_19Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_22T13_45_14Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_22T13_45_14Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_22T13_45_14Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_23T07_24_09Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_23T07_24_09Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_23T07_24_09Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_23T08_03_53Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_23T08_03_53Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_23T08_03_53Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_23T08_35_19Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_23T08_35_19Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_23T08_35_19Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_23T08_51_49Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_23T08_51_49Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_23T08_51_49Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_23T08_56_02Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_23T08_56_02Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_23T08_56_02Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_23T09_09_00Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_23T09_09_00Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_23T09_09_00Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_23T09_42_13Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_23T09_42_13Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_23T09_42_13Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_23T09_51_32Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_23T09_51_32Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_23T09_51_32Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_23T10_24_32Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_23T10_24_32Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_23T10_24_32Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay38-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay38-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay38-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_23T12_06_21Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_23T12_06_21Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_23T12_06_21Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_23T12_54_40Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_23T12_54_40Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_23T12_54_40Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_23T13_57_43Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_23T13_57_43Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_23T13_57_43Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay39-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay39-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay39-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay40-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay40-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay40-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay41-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay41-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay41-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>shay42-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay42-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay42-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>shay43-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay43-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay43-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>shay44-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay44-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay44-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>2023_01_24T12_29_03Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_24T12_29_03Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_24T12_29_03Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_24T12_40_22Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_24T12_40_22Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_24T12_40_22Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_24T12_56_35Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_24T12_56_35Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_24T12_56_35Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_24T13_19_05Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_24T13_19_05Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_24T13_19_05Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay45-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay45-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay45-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>2023_01_24T13_37_39Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_24T13_37_39Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_24T13_37_39Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay47-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay47-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay47-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>shay48-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay48-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay48-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>shay49-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay49-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay49-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>shay50-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay50-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay50-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>shay51-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>shay51-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/shay51-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>2023_01_25T08_43_05Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_25T08_43_05Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_25T08_43_05Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_25T09_34_45Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_25T09_34_45Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_25T09_34_45Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_26T08_24_57Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_26T08_24_57Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_26T08_24_57Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_26T09_06_38Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_26T09_06_38Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_26T09_06_38Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_26T09_45_16Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_26T09_45_16Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_26T09_45_16Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_26T11_48_46Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_26T11_48_46Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_26T11_48_46Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_26T12_17_49Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_26T12_17_49Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_26T12_17_49Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_26T14_39_54Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_26T14_39_54Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_26T14_39_54Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_26T14_43_36Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_26T14_43_36Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_26T14_43_36Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_29T06_41_01Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_29T06_41_01Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_29T06_41_01Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_29T07_29_48Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_29T07_29_48Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_29T07_29_48Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_29T08_56_36Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_29T08_56_36Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_29T08_56_36Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_29T09_34_31Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_29T09_34_31Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_29T09_34_31Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_31T09_43_21Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_31T09_43_21Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_31T09_43_21Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_31T11_20_46Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_31T11_20_46Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_31T11_20_46Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_31T11_31_40Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_31T11_31_40Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_31T11_31_40Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_31T12_06_11Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_31T12_06_11Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_31T12_06_11Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_31T12_20_04Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_31T12_20_04Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_31T12_20_04Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_31T12_24_12Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_31T12_24_12Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_31T12_24_12Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_31T15_07_34Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_31T15_07_34Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_31T15_07_34Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>blue_7-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>blue_7-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/blue_7-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>2023_01_31T20_43_23Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_31T20_43_23Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_31T20_43_23Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_01_31T21_00_56Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_01_31T21_00_56Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_01_31T21_00_56Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T08_18_15Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T08_18_15Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T08_18_15Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>testId1-OrthophotoHistory</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>testId1-OrthophotoHistory</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/testId1-OrthophotoHistory/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>testId2-VectorBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>testId2-VectorBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/testId2-VectorBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T08_45_49Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T08_45_49Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T08_45_49Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T08_58_36Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T08_58_36Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T08_58_36Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T09_04_22Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T09_04_22Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T09_04_22Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T09_17_26Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T09_17_26Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T09_17_26Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T09_23_03Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T09_23_03Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T09_23_03Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T09_29_28Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T09_29_28Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T09_29_28Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T09_40_40Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T09_40_40Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T09_40_40Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T09_59_38Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T09_59_38Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T09_59_38Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T11_20_24Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T11_20_24Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T11_20_24Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T11_31_52Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T11_31_52Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T11_31_52Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T11_40_32Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T11_40_32Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T11_40_32Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T12_01_16Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T12_01_16Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T12_01_16Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T12_11_06Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T12_11_06Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T12_11_06Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T12_23_46Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T12_23_46Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T12_23_46Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T12_32_52Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T12_32_52Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T12_32_52Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T12_48_56Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T12_48_56Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T12_48_56Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T13_11_46Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T13_11_46Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T13_11_46Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T13_42_25Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T13_42_25Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T13_42_25Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T13_51_38Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T13_51_38Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T13_51_38Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T14_06_14Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T14_06_14Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T14_06_14Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T14_18_28Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T14_18_28Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T14_18_28Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T14_27_20Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T14_27_20Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T14_27_20Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_01T14_31_40Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_01T14_31_40Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_01T14_31_40Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_06T11_43_51Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_06T11_43_51Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_06T11_43_51Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_06T11_58_24Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_06T11_58_24Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_06T11_58_24Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_06T12_09_17Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_06T12_09_17Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_06T12_09_17Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_06T12_22_15Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_06T12_22_15Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_06T12_22_15Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_06T13_38_53Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_06T13_38_53Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_06T13_38_53Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_07T07_34_30Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_07T07_34_30Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_07T07_34_30Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_07T08_08_38Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_07T08_08_38Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_07T08_08_38Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_07T09_06_17Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_07T09_06_17Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_07T09_06_17Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_07T12_23_28Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_07T12_23_28Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_07T12_23_28Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_07T14_10_01Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_07T14_10_01Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_07T14_10_01Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_07T14_15_02Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_07T14_15_02Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_07T14_15_02Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_07T14_35_11Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_07T14_35_11Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_07T14_35_11Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_07T14_48_08Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_07T14_48_08Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_07T14_48_08Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_07T15_02_04Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_07T15_02_04Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_07T15_02_04Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_07T15_13_52Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_07T15_13_52Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_07T15_13_52Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T07_59_23Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T07_59_23Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T07_59_23Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T08_13_16Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T08_13_16Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T08_13_16Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T08_17_16Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T08_17_16Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T08_17_16Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T08_26_12Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T08_26_12Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T08_26_12Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T08_37_58Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T08_37_58Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T08_37_58Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T09_01_55Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T09_01_55Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T09_01_55Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T09_04_50Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T09_04_50Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T09_04_50Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T09_37_16Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T09_37_16Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T09_37_16Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T09_47_46Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T09_47_46Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T09_47_46Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T11_00_48Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T11_00_48Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T11_00_48Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T14_02_16Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T14_02_16Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T14_02_16Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T14_35_26Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T14_35_26Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T14_35_26Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_08T14_41_34Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_08T14_41_34Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_08T14_41_34Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_09T07_37_43Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_09T07_37_43Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_09T07_37_43Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>2023_02_09T11_31_29Z_MAS_6_ORT_247557-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>2023_02_09T11_31_29Z_MAS_6_ORT_247557-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/2023_02_09T11_31_29Z_MAS_6_ORT_247557-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>gpkg_test3-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>gpkg_test3-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/gpkg_test3-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>bm_test-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>bm_test-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/png</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/png" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/bm_test-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.png"/>
</Layer>
<Layer>
<ows:Title>sizing4-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>sizing4-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/sizing4-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>sizing-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>sizing-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/sizing-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>sizingX2-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>sizingX2-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/sizingX2-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>Asaf_test_Area_1-Orthophoto</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>Asaf_test_Area_1-Orthophoto</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/Asaf_test_Area_1-Orthophoto/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg1-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg1-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg1-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg2-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg2-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg2-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg3-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg3-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg3-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg4-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg4-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg4-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg5-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg5-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg5-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg6-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg6-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg6-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg7-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg7-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg7-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg8-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg8-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg8-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg9-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg9-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg9-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg10-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg10-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg10-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg11-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg11-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg11-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg12-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg12-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg12-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg13-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg13-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg13-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg14-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg14-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg14-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg15-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg15-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg15-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<Layer>
<ows:Title>basic_gpkg16-OrthophotoBest</ows:Title>
<ows:Abstract/>
<ows:WGS84BoundingBox>
<ows:LowerCorner>-180.0 -90.0</ows:LowerCorner>
<ows:UpperCorner>180.0 90.0</ows:UpperCorner>
</ows:WGS84BoundingBox>
<ows:Identifier>basic_gpkg16-OrthophotoBest</ows:Identifier>
<Style>
<ows:Identifier>default</ows:Identifier>
</Style>
<Format>image/jpeg</Format>
<TileMatrixSetLink>
<TileMatrixSet>newGrids</TileMatrixSet>
</TileMatrixSetLink>
<ResourceURL format="image/jpeg" resourceType="tile" template="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/basic_gpkg16-OrthophotoBest/{TileMatrixSet}/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>
</Layer>
<TileMatrixSet>
<ows:Identifier>webmercator</ows:Identifier>
<ows:SupportedCRS>EPSG:3857</ows:SupportedCRS>
<TileMatrix>
<ows:Identifier>00</ows:Identifier>
<ScaleDenominator>559082264.0287176</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>01</ows:Identifier>
<ScaleDenominator>279541132.0143588</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>2</MatrixWidth>
<MatrixHeight>2</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>02</ows:Identifier>
<ScaleDenominator>139770566.0071794</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>4</MatrixWidth>
<MatrixHeight>4</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>03</ows:Identifier>
<ScaleDenominator>69885283.0035897</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>8</MatrixWidth>
<MatrixHeight>8</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>04</ows:Identifier>
<ScaleDenominator>34942641.50179485</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>16</MatrixWidth>
<MatrixHeight>16</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>05</ows:Identifier>
<ScaleDenominator>17471320.750897426</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>32</MatrixWidth>
<MatrixHeight>32</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>06</ows:Identifier>
<ScaleDenominator>8735660.375448713</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>64</MatrixWidth>
<MatrixHeight>64</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>07</ows:Identifier>
<ScaleDenominator>4367830.187724357</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>128</MatrixWidth>
<MatrixHeight>128</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>08</ows:Identifier>
<ScaleDenominator>2183915.0938621783</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>256</MatrixWidth>
<MatrixHeight>256</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>09</ows:Identifier>
<ScaleDenominator>1091957.5469310891</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>512</MatrixWidth>
<MatrixHeight>512</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>10</ows:Identifier>
<ScaleDenominator>545978.7734655446</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1024</MatrixWidth>
<MatrixHeight>1024</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>11</ows:Identifier>
<ScaleDenominator>272989.3867327723</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>2048</MatrixWidth>
<MatrixHeight>2048</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>12</ows:Identifier>
<ScaleDenominator>136494.69336638614</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>4096</MatrixWidth>
<MatrixHeight>4096</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>13</ows:Identifier>
<ScaleDenominator>68247.34668319307</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>8192</MatrixWidth>
<MatrixHeight>8192</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>14</ows:Identifier>
<ScaleDenominator>34123.673341596535</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>16384</MatrixWidth>
<MatrixHeight>16384</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>15</ows:Identifier>
<ScaleDenominator>17061.836670798268</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>32768</MatrixWidth>
<MatrixHeight>32768</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>16</ows:Identifier>
<ScaleDenominator>8530.918335399134</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>65536</MatrixWidth>
<MatrixHeight>65536</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>17</ows:Identifier>
<ScaleDenominator>4265.459167699567</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>131072</MatrixWidth>
<MatrixHeight>131072</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>18</ows:Identifier>
<ScaleDenominator>2132.7295838497835</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>262144</MatrixWidth>
<MatrixHeight>262144</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>19</ows:Identifier>
<ScaleDenominator>1066.3647919248917</ScaleDenominator>
<TopLeftCorner>-20037508.342789244 20037508.342789244</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>524288</MatrixWidth>
<MatrixHeight>524288</MatrixHeight>
</TileMatrix>
</TileMatrixSet>
<TileMatrixSet>
<ows:Identifier>newGrids</ows:Identifier>
<ows:SupportedCRS>EPSG:4326</ows:SupportedCRS>
<TileMatrix>
<ows:Identifier>00</ows:Identifier>
<ScaleDenominator>279541132.01435894</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>2</MatrixWidth>
<MatrixHeight>1</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>01</ows:Identifier>
<ScaleDenominator>139770566.00717947</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>4</MatrixWidth>
<MatrixHeight>2</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>02</ows:Identifier>
<ScaleDenominator>69885283.00358973</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>8</MatrixWidth>
<MatrixHeight>4</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>03</ows:Identifier>
<ScaleDenominator>34942641.50179487</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>16</MatrixWidth>
<MatrixHeight>8</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>04</ows:Identifier>
<ScaleDenominator>17471320.750897434</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>32</MatrixWidth>
<MatrixHeight>16</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>05</ows:Identifier>
<ScaleDenominator>8735660.375448717</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>64</MatrixWidth>
<MatrixHeight>32</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>06</ows:Identifier>
<ScaleDenominator>4367830.187724358</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>128</MatrixWidth>
<MatrixHeight>64</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>07</ows:Identifier>
<ScaleDenominator>2183915.093862179</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>256</MatrixWidth>
<MatrixHeight>128</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>08</ows:Identifier>
<ScaleDenominator>1091957.5469310896</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>512</MatrixWidth>
<MatrixHeight>256</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>09</ows:Identifier>
<ScaleDenominator>545978.7734655448</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1024</MatrixWidth>
<MatrixHeight>512</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>10</ows:Identifier>
<ScaleDenominator>272989.3867327724</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>2048</MatrixWidth>
<MatrixHeight>1024</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>11</ows:Identifier>
<ScaleDenominator>136494.6933663862</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>4096</MatrixWidth>
<MatrixHeight>2048</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>12</ows:Identifier>
<ScaleDenominator>68247.3466831931</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>8192</MatrixWidth>
<MatrixHeight>4096</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>13</ows:Identifier>
<ScaleDenominator>34123.67334159655</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>16384</MatrixWidth>
<MatrixHeight>8192</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>14</ows:Identifier>
<ScaleDenominator>17061.836670798275</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>32768</MatrixWidth>
<MatrixHeight>16384</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>15</ows:Identifier>
<ScaleDenominator>8530.918335399138</ScaleDenominator>
<TopLeftCorner>90.00000000000001 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>65536</MatrixWidth>
<MatrixHeight>32768</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>16</ows:Identifier>
<ScaleDenominator>4265.459167699569</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>131072</MatrixWidth>
<MatrixHeight>65536</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>17</ows:Identifier>
<ScaleDenominator>2132.7295838497844</ScaleDenominator>
<TopLeftCorner>90.0 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>262144</MatrixWidth>
<MatrixHeight>131072</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>18</ows:Identifier>
<ScaleDenominator>1066.3647919248922</ScaleDenominator>
<TopLeftCorner>89.99999999999999 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>524288</MatrixWidth>
<MatrixHeight>262144</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>19</ows:Identifier>
<ScaleDenominator>533.1823959624461</ScaleDenominator>
<TopLeftCorner>90.00000000000001 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>1048576</MatrixWidth>
<MatrixHeight>524288</MatrixHeight>
</TileMatrix>
<TileMatrix>
<ows:Identifier>20</ows:Identifier>
<ScaleDenominator>266.59119798122305</ScaleDenominator>
<TopLeftCorner>89.99999999999999 -180.0</TopLeftCorner>
<TileWidth>256</TileWidth>
<TileHeight>256</TileHeight>
<MatrixWidth>2097152</MatrixWidth>
<MatrixHeight>1048576</MatrixHeight>
</TileMatrix>
</TileMatrixSet>
</Contents>
<ServiceMetadataURL xlink:href="https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/1.0.0/WMTSCapabilities.xml"/>
</Capabilities>
'''

# Parse the XML data
tree = ET.fromstring(xml_data)

# Extract values from nested XML by parent name
parent_name = "capabilities"
for parent_elem in tree.findall('parent'):
    if parent_elem.get('name') == parent_name:
        child_value = parent_elem.find('child').text
        print("111111111")
        print(child_value)
        print("222222222")

# "https://mapproxy-no-auth-raster-qa.apps.j1lk3njp.eastus.aroapp.io/api/raster/v1/wmts/1.0.0/WMTSCapabilities.xml"


from google.protobuf import json_format
from my_proto_pb2 import MyMessage

# JSON request body
json_data = '''
{
    "field1": "value1",
    "field2": 123,
    "field3": true
}
'''

# Parse JSON and convert to protobuf message
message = MyMessage()
json_format.Parse(json_data, message)

# Access the protobuf message
print(message.field1)
print(message.field2)
print(message.field3)


