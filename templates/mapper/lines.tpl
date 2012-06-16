## -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<%
	import re

	def good_color(color):
		return re.match("#[0-9A-Fa-f]{6}", color)

%>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>OSM ${region | h} Transportation Overview</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
	<script type="text/javascript">

function init() {
}

$(document).ready(init);

	</script>
	<style type="text/css">
body,td {
	font-family: sans-serif;
	font-size: 8pt;
	vertical-align: top;
}
table {
	border-collapse: collapse
}
th {
	background-color: #eee;
	text-align: left;
}
th,td {
	border: 1px solid #ccc;
	padding: 1px;
}
ul {
	list-style-position: outside;
	padding: 0;
	margin: 0 0 0 14px;
}
a {
	text-decoration: none;
}
input {
	display: none;
}
.right {
	text-align: right;
}
.center {
	text-align: center;
}
.monospace {
	font-family: monospace;
}
.nowrap {
	white-space: nowrap;
}
.selected {
	background-color: #ddd;
}
	</style>
</head>
<body>
	<h1>OSM ${region | h} Transportation Overview</h1>
<%
#<td class="right"><a href="http://www.openstreetmap.org/browse/relation/${l['osmid'] | h}">${l['osmid'] | h}</a></td>
#<a href="http://api.openstreetmap.org/api/0.6/relation/${l['osmid'] | h}" title="XML">x</a>
#<a href="http://ra.osmsurround.org/analyzeRelation?relationId=${l['osmid'] | h}" title="OSM Relation Analyzer">a</a>
#<a href="http://osmrm.openstreetmap.de/relation.jsp?id=${l['osmid'] | h}" title="OSM Route Manager">r</a>
#<a href="http://localhost:8111/import?url=http://api.openstreetmap.org/api/0.6/relation/${l['osmid'] | h}/full" title="JOSM">j</a>
#<a href="http://osm.virtuelle-loipe.de/history/?type=relation&amp;ref=${l['osmid'] | h}" title="OSM History Browser">h</a>
#<a href="http://www.openstreetmap.org/?relation=${l['osmid'] | h}" title="view">v</a>
#<a href="http://www.overpass-api.de/api/sketch-line?ref=${l['ref'] | h}&amp;network=VBB&amp;style=wuppertal" title="Sketch Line">s</a>
#<a href="http://osmrm.openstreetmap.de/gpx.jsp?relation=${l['osmid'] | h}" title="GPX">g</a>
#<a href="http://osm.kesto.de/rnc/?r=${l['osmid'] | h}&p=/^(stop:[0-9]+|stop|forward:stop:[0-9]+|backward:stop:[0-9]+|platform:[0-9]+|platform)$$/" title="Relation's Node Connector">n</a>
%>

	% for l in lines:
		<div>
			<h2>${l['name'] | h} ${l['ref'] | h} (${l['id'] | h})</h2>
			% for v in l['variations']:
				<div>
				<h3>${v['from'] | h} &lt;=&gt; ${v['to'] | h} (${v['ids'][0]}, ${v['ids'][1]})</h3>
				<table>
				% for s in v['stops']:
					<tr>
						<td>${s[0] | h}</td>
						<td>${s[1] | h}</td>
						<td>${",".join(s[2]) | h}</td>
					</tr>
				% endfor
				</table>
				</div>
			% endfor
		</div>
	% endfor

	<p>Map data © <a href="http://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC BY-SA</a></p>
	<p>Source code of validation script is available at <a href="https://github.com/stefanschramm/osm_oepnv_validator">https://github.com/stefanschramm/osm_oepnv_validator</a>.</p>
</body>
</html>

