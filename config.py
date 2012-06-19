#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import rulesets.berlin
import rulesets.hiking

script_path = os.path.dirname(__file__)

output_dir = script_path + "/output"
data_dir = script_path + "/data"
template_dir = script_path + "/templates"

profiles = {
	'berlin_oepnv': {
		'shortname': 'berlin_oepnv',
		'name': u"Berlin ÖPNV (BVG + S-Bahn Berlin GmbH)",
		'rules': rulesets.berlin.PublicTransportNetworkBerlin,
		'filter': lambda r: "network" in r[1] \
				and r[1]["network"] == "VBB" \
				and "operator" in r[1] \
				and (r[1]["operator"] == "BVG" or r[1]["operator"] == "S-Bahn Berlin GmbH") \
				and "type" in r[1] \
				and r[1]["type"] in ["route", "route_master"],
		'filter_text': 'All route and route_master relations with network=VBB and (operator=BVG or operator=S-Bahn Berlin GmbH)',
		'datasource': 'berlin.osm.pbf',
		'stopplan': True,
		'maps': {
			# 'internal name': ('readable name', filter function)
			'sunetz': ("S+U-Bahn", rulesets.berlin.is_s_or_u_bahn),
			'strassenbahn': (u"Straßenbahn (ohne MetroTram)", rulesets.berlin.is_normal_tram),
			'metrotram': ("MetroTram", rulesets.berlin.is_metro_tram),
			'bus': ("Bus (ohne Metro- und ExpressBus)", rulesets.berlin.is_normal_bus),
			'metrobus': ("MetroBus", rulesets.berlin.is_metro_bus),
			'expressbus': ("ExpressBus", rulesets.berlin.is_express_bus)
		}
	},
	'vbb': {
		'shortname': 'vbb',
		'name': u"VBB (ohne BVG und S-Bahn Berlin GmbH)",
		'rules': rulesets.berlin.PublicTransportNetworkBerlin,
#		'filter': lambda r: "network" in r[1] \
#				and r[1]["network"] == "VBB" \
#				and "type" in r[1] \
#				and r[1]["type"] in ["route", "route_master"],
		'filter': lambda r: "network" in r[1] \
				and r[1]["network"] == "VBB" \
				and "type" in r[1] \
				and r[1]["type"] in ["route", "route_master"]
				and (not "operator" in r[1] or r[1]["operator"] not in ["BVG", "S-Bahn Berlin GmbH"]),
		'datasource': 'berlin.osm.pbf',
		'stopplan': True,
		'maps': {
			'all': ("alle Linien", lambda r: True)
		}
	},
	'no_vbb': {
		'shortname': 'no_vbb',
		'name': 'nicht-VBB',
		'rules': rulesets.berlin.PublicTransportNetworkBerlin,
		'filter': lambda r: ("network" not in r[1] \
				or r[1]["network"] != "VBB") \
				and "type" in r[1] \
				and r[1]["type"] in ["route", "route_master"],
		'datasource': 'berlin.osm.pbf',
		'stopplan': False,
		'maps': {
			# 'all': ("alle Linien", lambda r: True)
		}
	},
	'berlin_hiking': {
		'shortname': 'berlin_hiking',
		'name': 'Berlin Wanderwege',
		'rules': rulesets.hiking.Hiking,
		'filter': lambda r: "type" in r[1] \
				and r[1]["type"] in ["route", "route_master"] \
				and (("route" in r[1] and r[1]["route"] == "hiking") \
				or ("route_master" in r[1] and r[1]["route_master"] == "hiking")),
		'datasource': 'berlin.osm.pbf',
		'stopplan': False,
		'maps': {
			# 'all': ("alle Linien", lambda r: True)
		}
	}
}

