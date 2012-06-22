<%page args="osmid, ref" />
<a rel="nofollow" href="http://api.openstreetmap.org/api/0.6/relation/${osmid | h}" title="XML">x</a>
<a rel="nofollow" href="http://ra.osmsurround.org/analyzeRelation?relationId=${osmid | h}" title="OSM Relation Analyzer">a</a>
<a rel="nofollow" href="http://osmrm.openstreetmap.de/relation.jsp?id=${osmid | h}" title="OSM Route Manager">r</a>
<a rel="nofollow" href="http://localhost:8111/import?url=http://api.openstreetmap.org/api/0.6/relation/${osmid | h}/full" title="JOSM">j</a>
<a rel="nofollow" href="http://osm.virtuelle-loipe.de/history/?type=relation&amp;ref=${osmid | h}" title="OSM History Browser">h</a>
<a rel="nofollow" href="http://www.openstreetmap.org/?relation=${osmid | h}" title="view">v</a>
% if ref != None and ref != "":
<a rel="nofollow" href="http://www.overpass-api.de/api/sketch-line?ref=${ref | h}&amp;network=VBB&amp;style=wuppertal" title="Sketch Line">s</a>
% endif
<a rel="nofollow" href="http://osmrm.openstreetmap.de/gpx.jsp?relation=${osmid | h}" title="GPX">g</a>
<a rel="nofollow" href="http://osm.kesto.de/rnc/?r=${osmid | h}&p=${'/^(stop:[0-9]+|stop|forward:stop:[0-9]+|backward:stop:[0-9]+|platform:[0-9]+|platform)$$/' | u}" title="Relation's Node Connector">n</a>
