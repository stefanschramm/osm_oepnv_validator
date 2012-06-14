## -*- coding: utf-8 -*-
<%
	import re

	def good_color(color):
		return re.match("#[0-9A-Fa-f]{6}", color)

	error_classes = {}
	for l in lines:
		for e in l["errors"]:
			if e[0] not in error_classes:
				error_classes[e[0]] = 1
			else:
				error_classes[e[0]] += 1

%>
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>OSM ${region | h} Transportation Overview</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
	<script type="text/javascript">

function checkCheckbox(checkbox) {
	var errors = $('.' + checkbox.getAttribute("name"));
	if (checkbox.checked) {
		errors.show()
	}
	else {
		errors.hide()
	}
}
function init() {
	$('input').show();
	$('input').each(function(index, checkbox) {
		checkCheckbox(checkbox);
	});
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
input {
	display: none;
}
	</style>
</head>
<body>
	<h1>OSM ${region | h} Transportation Overview</h1>
	<p>${filter | h}</p>
	<p>For relations which contain members outside of the data source no connectivity validation is done and member counts might be wrong.</p>
	<p><strong>Data source:</strong> ${datasource | h}</p>
	<p><strong>Last update:</strong> ${mtime | h}</p>
	<div>
	% for ec in error_classes:
		<input type="checkbox" name="${ec | h}" value="1" checked="checked" onchange="return checkCheckbox(this);" />${ec | h} (${error_classes[ec] | h})
	% endfor
	</div>
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
				<th>no <abbr title="route_master">r_m</abbr></th>
				<th>fixme+FIXME=</th>
				<th>note=</th>
			</tr>
		</thead>
		<tbody>
		% for l in lines:
			<tr>
				<td class="right"><a href="http://www.openstreetmap.org/browse/relation/${l['osmid'] | h}">${l['osmid'] | h}</a></td>
				<td class="nowrap">
<a href="http://api.openstreetmap.org/api/0.6/relation/${l['osmid'] | h}" title="XML">x</a>
<a href="http://ra.osmsurround.org/analyzeRelation?relationId=${l['osmid'] | h}" title="OSM Relation Analyzer">a</a>
<a href="http://osmrm.openstreetmap.de/relation.jsp?id=${l['osmid'] | h}" title="OSM Route Manager">r</a>
<a href="http://localhost:8111/import?url=http://api.openstreetmap.org/api/0.6/relation/${l['osmid'] | h}/full" title="JOSM">j</a>
<a href="http://osm.virtuelle-loipe.de/history/?type=relation&ref=${l['osmid'] | h}" title="OSM History Browser">h</a>
<a href="http://www.openstreetmap.org/?relation=${l['osmid'] | h}" title="view">v</a>
<a href="http://www.overpass-api.de/api/sketch-line?ref=${l['ref'] | h}&network=VBB&style=wuppertal" title="Sketch Line">s</a>
<a href="http://osmrm.openstreetmap.de/gpx.jsp?relation=${l['osmid'] | h}" title="GPX">g</a>
				</td>
				<td>${l['type'] | h}</td>
				<td>${l['route_master'] | h}</td>
				<td class="right">${l['relations'] | h}</td>
				<td>${l['route'] | h}</td>
				<td class="right">${l['ways'] | h}</td>
				<td class="right">${l['nodes'] | h}</td>
				<td>${l['ref'] | h}</td>
				<%
					color = l['color'] if good_color(l['color']) else "#ffffff"
				%>
				<td class="monospace"><span style="background-color: ${color};">&nbsp;&nbsp;</span>&nbsp;${l['color'] | h}</td>
				<td>${l['name'] | h}</td>
				<td>
				% if len(l['errors']) > 0:
					<ul>
					% for e in l['errors']:
						<li class="${e[0] | h}">${e[1] | h}</li>
					% endfor
					</ul>
				% endif
				</td>
				% if l['noroutemaster']:
				<td class="center">x</td>
				% else:
				<td class="center"></td>
				% endif
				<td>${l['fixme'] | h}</td>
				<td>${l['note'] | h}</td>
			</tr>
		% endfor
		</tbody>
	</table>
	<p>Map data © <a href="http://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC BY-SA</a></p>
	<p>Source code of validation script is available at <a href="https://github.com/stefanschramm/osm_oepnv_validator">https://github.com/stefanschramm/osm_oepnv_validator</a>.</p>
</body>
</html>

