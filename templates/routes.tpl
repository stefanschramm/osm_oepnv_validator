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
	<title>OSM Route Utilities</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
	<%include file="/header.tpl" args="page='routes'" />
	<p><strong>Lines:</strong>
	% for l in lines:
		<a href="#relation-${l['id'] | h}">${l['ref'] | h}</a>
	% endfor
	</p>
	% for l in lines:
		<div>
			<h2 id="relation-${l['id'] | h}">${l['name'] | h}, ref=${l['ref'] | h} (<a href="http://www.openstreetmap.org/browse/relation/${l['id'] | h}">${l['id'] | h}</a> <small><%include file="/relationtools.tpl" args="osmid=l['id'], ref=l['ref']"/> <a href="${profile['shortname'] | h}.htm#relation-${l['id'] | h}" title="Relation List">rl</a></small>)</h2>
			% for v in l['variations']:
				<div>
				<h3>${v['from'] | h} &lt;=&gt; ${v['to'] | h}
					(<a href="http://www.openstreetmap.org/browse/relation/${v['ids'][0] | h}">${v['ids'][0] | h}</a> <small><%include file="/relationtools.tpl" args="osmid=v['ids'][0], ref=l['ref']"/> <a href="${profile['shortname'] | h}.htm#relation-${v['ids'][0] | h}" title="Relation List">rl</a></small>, <a href="http://www.openstreetmap.org/browse/relation/${v['ids'][1] | h}">${v['ids'][1] | h}</a> <small><%include file="/relationtools.tpl" args="osmid=v['ids'][1], ref=l['ref']"/> <a href="${profile['shortname'] | h}.htm#relation-${v['ids'][1] | h}" title="Relation List">rl</a></small>)</h3>
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
	<%include file="/footer.tpl" />
</body>
</html>

