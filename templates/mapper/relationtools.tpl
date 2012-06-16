<%page args="osmid, ref" />
<a href="http://api.openstreetmap.org/api/0.6/relation/${osmid | h}" title="XML">x</a>
<a href="http://ra.osmsurround.org/analyzeRelation?relationId=${osmid | h}" title="OSM Relation Analyzer">a</a>
<a href="http://osmrm.openstreetmap.de/relation.jsp?id=${osmid | h}" title="OSM Route Manager">r</a>
<a href="http://localhost:8111/import?url=http://api.openstreetmap.org/api/0.6/relation/${osmid | h}/full" title="JOSM">j</a>
<a href="http://osm.virtuelle-loipe.de/history/?type=relation&amp;ref=${osmid | h}" title="OSM History Browser">h</a>
<a href="http://www.openstreetmap.org/?relation=${osmid | h}" title="view">v</a>
% if ref != None and ref != "":
<a href="http://www.overpass-api.de/api/sketch-line?ref=${ref | h}&amp;network=VBB&amp;style=wuppertal" title="Sketch Line">s</a>
% endif
<a href="http://osmrm.openstreetmap.de/gpx.jsp?relation=${osmid | h}" title="GPX">g</a>
<a href="http://osm.kesto.de/rnc/?r=${osmid | h}&p=/^(stop:[0-9]+|stop|forward:stop:[0-9]+|backward:stop:[0-9]+|platform:[0-9]+|platform)$$/" title="Relation's Node Connector">n</a>


