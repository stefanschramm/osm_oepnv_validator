#!/usr/bin/env python
# -*- coding: utf-8 -*-

# hamburg.py - validation rules for public transport in Hamburg

import re

from ptn import PublicTransportNetwork

class PublicTransportNetworkHamburg(PublicTransportNetwork):

	def __init__(self):

		self.valid_route_values = ["bus", "subway", "ferry", "light_rail", "train"]
		self.valid_route_master_values = ["bus", "subway", "ferry", "light_rail", "train"]
		self.route_node_roles_pattern = "^(platform(:.*)?|stop(:.*)?|forward(:.*)?|forward_stop|backward(_stop)?|stop_entry_only|stop_exit_only|platform_exit_only|platform_entry_only|)$"
		self.valid_keys.append("text_color")
		self.route_validators.append(self.check_color)
		self.route_master_validators.append(self.check_color)

		self.text_region = "Hamburg"
		self.text_filter = "All relations of type route or route_master with network=HVV."
		self.text_datasource = "hamburg.osm.pbf from geofabrik.de"


	def relation_filter(self, relation):
		# defines which relations to validate
		osmid, tags, members = relation
		return "network" in tags \
			and tags["network"] == "HVV" \
			and "type" in tags \
			and tags["type"] in ["route", "route_master"]


	def check_color(self, relation):
		osmid, tags, members = relation

		if "type" not in tags or tags["type"] not in ["route", "route_master"]:
			return []
		key = tags["type"]

		if key not in tags:
			return []

		if tags[key] in ["subway", "tram", "light_rail"] and "color" not in tags:
			return ['missing color=#... for %s' % tags[key]]

		if "color" in tags and not re.match("^#[a-fA-F0-9]{6}$", tags["color"]):
			return ['color should be specified as hexadecimal value like #ff0000']

		return []

