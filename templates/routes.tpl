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
	<title>OSM Transportation Overview</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<script type="text/javascript" src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
	<script type="text/javascript">

function init() {
}

$(document).ready(init);

	</script>
	<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
	<%include file="/header.tpl" args="page='routes'" />
	% for l in lines:
		<div>
			<h2>${l['name'] | h} ${l['ref'] | h} (<a href="http://www.openstreetmap.org/browse/relation/${l['id'] | h}">${l['id'] | h}</a> <small><%include file="/relationtools.tpl" args="osmid=l['id'], ref=l['ref']"/></small>)</h2>
			% for v in l['variations']:
				<div>
				<h3>${v['from'] | h} &lt;=&gt; ${v['to'] | h}
					(<a href="http://www.openstreetmap.org/browse/relation/${v['ids'][0] | h}">${v['ids'][0] | h}</a> <small><%include file="/relationtools.tpl" args="osmid=v['ids'][0], ref=l['ref']"/></small>,
					<a href="http://www.openstreetmap.org/browse/relation/${v['ids'][1] | h}">${v['ids'][1] | h}</a> <small><%include file="/relationtools.tpl" args="osmid=v['ids'][1], ref=l['ref']"/></small>)</h3>
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

