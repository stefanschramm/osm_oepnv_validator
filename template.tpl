## -*- coding: utf-8 -*-
<%!
	import re
	def good_color(color):
		return re.match("#[0-9A-Fa-f]{6}", color)
%>
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>OSM Berlin Transportation Overview</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
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
.right {
	text-align: right;
}
.monospace {
	font-family: monospace;
}
.nowrap {
	white-space: nowrap;
}
	</style>
</head>
<body>
	<h1>OSM Berlin Transportation Overview</h1>
	<p>All relations with (type=route or type=route_master) and network=VBB and (operator=BVG or operator=S-Bahn Berlin GmbH).</p>
	<p>For relations that cross the border of Berlin no connectivity validation is done and member counts might be wrong.</p>
	<p>Last update: ${mtime}</p>
	<table>
		<thead>
			<tr>
				<th class="right">id</th>
				<th>tools</th>
				<th>type=</th>
				<th><abbr title="route_master=">r_m=</abbr></th>
				<th class="right"><abbr title="number of members of type 'relation'">#R</abbr></th>
				<th>route=</th>
				<th class="right"><abbr title="number of members of type 'way'">#W</abbr></th>
				<th class="right"><abbr title="number of members of type 'node'">#N</abbr></th>
				<th>ref=</th>
				<th>color=</th>
				<th>name=</th>
				<th>validation errors</th>
				<th>fixme+FIXME=</th>
				<th>note=</th>
			</tr>
		</thead>
		<tbody>
		% for l in lines:
			<tr>
				<td class="right"><a href="http://www.openstreetmap.org/browse/relation/${l['osmid']}">${l['osmid']}</a></td>
				<td class="nowrap">
<a href="http://api.openstreetmap.org/api/0.6/relation/${l['osmid']}" title="XML">x</a>
<a href="http://ra.osmsurround.org/analyzeRelation?relationId=${l['osmid']}" title="OSM Relation Analyzer">a</a>
<a href="http://osmrm.openstreetmap.de/relation.jsp?id=${l['osmid']}" title="OSM Route Manager">r</a>
<a href="http://localhost:8111/import?url=http://api.openstreetmap.org/api/0.6/relation/${l['osmid']}/full" title="JOSM">j</a>
<a href="http://osm.virtuelle-loipe.de/history/?type=relation&ref=${l['osmid']}" title="OSM History Browser">h</a>
<a href="http://www.openstreetmap.org/?relation=${l['osmid']}" title="view">v</a>
<a href="http://www.overpass-api.de/api/sketch-line?ref=${l['ref']}&network=VBB&style=wuppertal" title="Sketch Line">s</a>
<a href="http://osmrm.openstreetmap.de/gpx.jsp?relation=${l['osmid']}&network=VBB&style=wuppertal" title="GPX">g</a>
				</td>
				<td>${l['type']}</td>
				<td>${l['route_master']}</td>
				<td class="right">${l['relations']}</td>
				<td>${l['route']}</td>
				<td class="right">${l['ways']}</td>
				<td class="right">${l['nodes']}</td>
				<td>${l['ref']}</td>
				<%
					color = l['color'] if good_color(l['color']) else "#ffffff"
				%>
				<td class="monospace"><span style="background-color: ${color};">&nbsp;&nbsp;</span>&nbsp;${l['color']}</td>
				<td>${l['name']}</td>
				<td>
				% if len(l['errors']) > 0:
					<ul>
					% for e in l['errors']:
						<li>${e}</li>
					% endfor
					</ul>
				% endif
				</td>
				<td>${l['fixme']}</td>
				<td>${l['note']}</td>
			</tr>
		% endfor
		</tbody>
	</table>
	<p>Map data © <a href="http://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC BY-SA</a></p>
	<p>Source code of validation script is available at <a href="https://github.com/stefanschramm/osm_oepnv_validator">https://github.com/stefanschramm/osm_oepnv_validator</a></p>
</body>
</html>

