#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dresden.py - validation rules for public transport in Dresden
#
# Copyright (C) 2012, Stefan Schramm <mail@stefanschramm.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re

from ptn import PublicTransportNetwork

class PublicTransportNetworkDresden(PublicTransportNetwork):

	def __init__(self):

		#self.valid_route_values = ["bus", "subway", "ferry", "light_rail", "train"]
		#self.valid_route_master_values = ["bus", "subway", "ferry", "light_rail", "train"]
		#self.route_node_roles_pattern = "^(platform(:.*)?|stop(:.*)?|forward(:.*)?|forward_stop|backward(_stop)?|stop_entry_only|stop_exit_only|platform_exit_only|platform_entry_only|)$"

		self.text_region = "Dresden"
		self.text_filter = "All relations of type route or route_master with network=VVO."
		self.text_datasource = "sachsen.osm.pbf from geofabrik.de"

	def relation_filter(self, relation):
		# defines which relations to validate
		osmid, tags, members = relation
		return "network" in tags \
			and tags["network"] == "VVO" \
			and "type" in tags \
			and tags["type"] in ["route", "route_master"]

