#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import rulesets.berlin

script_path = os.path.dirname(__file__)

output_dir = script_path + "/output"
data_dir = script_path + "/data"
template_dir = script_path + "/templates"

profiles = {
	'berlin': {
		'shortname': 'berlin',
		'name': "Berlin (BVG + S-Bahn Berlin GmbH)",
		'rules': rulesets.berlin.PublicTransportNetworkBerlin,
		'filter': lambda r: "network" in r[1] \
				and r[1]["network"] == "VBB" \
				and "operator" in r[1] \
				and (r[1]["operator"] == "BVG" or r[1]["operator"] == "S-Bahn Berlin GmbH") \
				and "type" in r[1] \
				and r[1]["type"] in ["route", "route_master"],
		'filter_text': 'All route and route_master relations with network=VBB and (operator=BVG or operator=S-Bahn Berlin GmbH)',
		'datasource': 'berlin.osm.pbf',
		'maps': {
			# 'internal name': ('readable name', filter function)
			'sunetz': ("S+U-Bahn Netz", rulesets.berlin.is_s_or_u_bahn),
			'strassenbahn': (u"Straßenbahn Netz", rulesets.berlin.is_normal_tram),
			'metrotram': ("MetroTram Netz", rulesets.berlin.is_metro_tram),
			'bus': ("Bus Netz", rulesets.berlin.is_normal_bus),
			'metrobus': ("MetroBus Netz", rulesets.berlin.is_metro_bus),
			'expressbus': ("ExpressBus Netz", rulesets.berlin.is_express_bus)
		}
	},
	'vbb': {
		'shortname': 'vbb',
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
		'datasource': ['berlin.osm.pbf'], # TODO: test germany.osm.pbf
		'maps': {
			'all': ("alle Linien", lambda r: True)
		}
	},
	'no_vbb': {
		'shortname': 'no_vbb',
		'rules': rulesets.berlin.PublicTransportNetworkBerlin,
		'filter': lambda r: ("network" not in r[1] \
				or r[1]["network"] != "VBB") \
				and "type" in r[1] \
				and r[1]["type"] in ["route", "route_master"],
		'datasource': ['berlin.osm.pbf'], # TODO: test germany.osm.pbf
		'maps': {
			'all': ("alle Linien", lambda r: True)
		}
	}
}

