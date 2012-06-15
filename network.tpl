<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>OSM Relation's Node Connector</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
	<script type="text/javascript" src="OpenLayers-2.11/OpenLayers.js"></script>
	<script type="text/javascript">

<%!
    import simplejson as json
    def j(d):
        return json.dumps(d)
%>

var lines = ${j(lines)};

function toLonLat(lon, lat) {
  return new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), new OpenLayers.Projection("EPSG:900913"));
}

function init(){

	map = new OpenLayers.Map('map');
	var mapLayer = new OpenLayers.Layer.OSM("OSM Map");
	mapLayer.setOpacity(0.5);
	var lineLayer = new OpenLayers.Layer.Vector("Line Layer");
	map.addLayers([mapLayer, lineLayer]);
	map.setCenter(toLonLat(13.4, 52.5), 8);

	$(lines).each(function(index, line) {
		var style = { 
			strokeColor: '#999999',
			strokeOpacity: 0.7,
			strokeWidth: 4
		};

		if (line[1]['color'] != undefined) {
			style['strokeColor'] = line[1]['color'];
		}
		var geomPoints = [];
		$(line[2]).each(function(index, station) {
			var lonlat = toLonLat(station[2][0], station[2][1]);
			geomPoints.push(new OpenLayers.Geometry.Point(lonlat.lon, lonlat.lat));
		});
		var geometry = new OpenLayers.Geometry.LineString(geomPoints);
		var feature = new OpenLayers.Feature.Vector(geometry, null, style);
		lineLayer.addFeatures([feature]);
	});

}

$(document).ready(init);
	</script>
	<style type="text/css">
#map {
	width: 600px;
	height: 500px;
}
	</style>
</head>
<body>
<div id="map">
</div>
</body>
</html>

