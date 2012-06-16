#!/usr/bin/env python
# -*- coding: utf-8 -*-

# leipzig.py - validation rules for public transport in Leipzig

import re

from ptn import PublicTransportNetwork

class PublicTransportNetworkLeipzig(PublicTransportNetwork):

	def __init__(self):

		#self.valid_route_values = ["bus", "subway", "ferry", "light_rail", "train"]
		#self.valid_route_master_values = ["bus", "subway", "ferry", "light_rail", "train"]
		#self.route_node_roles_pattern = "^(platform(:.*)?|stop(:.*)?|forward(:.*)?|forward_stop|backward(_stop)?|stop_entry_only|stop_exit_only|platform_exit_only|platform_entry_only|)$"

		self.text_region = "Leipzig"
		self.text_filter = "All relations of type route or route_master with network=MDV."
		self.text_datasource = "sachsen.osm.pbf from geofabrik.de"

	def relation_filter(self, relation):
		# defines which relations to validate
		osmid, tags, members = relation
		return "network" in tags \
			and tags["network"] == "MDV" \
			and "type" in tags \
			and tags["type"] in ["route", "route_master"]

