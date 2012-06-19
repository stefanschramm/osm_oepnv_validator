## -*- coding: utf-8 -*-
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>OSM Route Utilities</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
	<h1>OSM Route Tools - Index</h1>
	<ul>
	% for profile in sorted(profiles.values(), key=lambda p: p['name']):
		<li><a href="${profile['shortname'] | h}.htm">${profile['name'] | h}</a></li>
	% endfor
	</ul>
</body>
</html>

