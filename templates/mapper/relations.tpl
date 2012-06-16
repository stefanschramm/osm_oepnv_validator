## -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
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

	zebracounter = 1
	zebra_prev_ref = 0
%>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>OSM Relation Overview</title>
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
	$('input.checkbox').each(function(index, checkbox) {
		checkCheckbox(checkbox);
	});
        $('tr').bind('click', function(ev) {
                dbg = ev.target;
                $(ev.target.parentElement).toggleClass('selected');
        });
}

$(document).ready(init);

	</script>
	<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
	<%include file="/header.tpl" args="page='relations'" />
	<p>For relations which contain members outside of the data source no connectivity validation is done and member counts might be wrong.</p>
	<p><strong>Data source:</strong> ${str(profile['datasource']) | h}</p>
	<p><strong>Last update:</strong> ${mtime | h}</p>
	<div><strong>Format:</strong> <input type="submit" value="no-wrap" onclick="$('td').css('white-space', 'nowrap'); return false;" /></div>
	<div><strong>Error classes:</strong>
	% for ec in error_classes:
		<input class="checkbox" type="checkbox" name="${ec | h}" value="1" checked="checked" onchange="return checkCheckbox(this);" />${ec | h} (${error_classes[ec] | h})
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
			<%

			if (zebra_prev_ref != l['ref']):
				zebra_prev_ref = l['ref']
				zebracounter += 1
			next=0
			for e in l['errors']:
				if (e[0] == "ignored"):
					trclass = "zebra_leer"
					next = 1
			if (next == 0):
				if (l['type'] == "route"):
					trclass = "zebra1_route" if zebracounter % 2 == 1 else "zebra2_route"
				else:
					trclass = "zebra1_master" if zebracounter % 2 == 1 else "zebra2_master"

			%>
			<tr class="${trclass}">
				<td class="right"><a href="http://www.openstreetmap.org/browse/relation/${l['osmid'] | h}">${l['osmid'] | h}</a></td>
				<td class="nowrap">
					<%include file="/relationtools.tpl" args="osmid=l['osmid'], ref=l['ref']"/>
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
				<td class="monospace"><span style="background-color: ${color};">&#160;&#160;</span>&#160;${l['color'] | h}</td>
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

