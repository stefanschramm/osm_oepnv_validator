#!/usr/bin/env python
# -*- coding: utf-8 -*-

# braunschweig.py - validation rules for public transport in Braunschweig

import re

from . import publictransport

class PublicTransportBraunschweig(publictransport.PublicTransport):

	def __init__(self):

		publictransport.PublicTransport.__init__(self)

		self.route_validators.append(self.validate_route_basics)
		self.route_validators.append(self.validate_name)
		self.route_validators.append(self.check_colour)
		self.route_validators.append(self.check_stops_in_ways)
		self.route_master_validators.append(self.validate_route_master_basics)
		self.route_master_validators.append(self.validate_name)
		self.route_master_validators.append(self.check_colour)

	def ignore_relation(self, relation):
		# defines which relations are excluded from validation
		rid, tags, members = relation
		return False # ignore none

	def validate_basics(self, relation):
		rid, tags, members = relation

		for key in tags:
			main_key = key.split(":")[0]
			if not main_key in self.valid_keys:
				errors.append(("unknown_key", "unknown key: %s" % key))

	def validate_route_master_basics(self, relation):
		rid, tags, members = relation
		errors = []

		# invalid keys
		for i in self.invalid_keys_route_master:
			if i in tags:
				errors.append(("unexpected_key", "unexpected key: %s in route_master relation" % i))

		# no members
		if len(members) <= 0:
			errors.append("route_master without members")
		else:
			for member in members:
				mid, typ, role = member
				if typ == "relation":
					if mid not in self.relations:
						errors.append(("unknown_member", "member id %i not found (missing network and/or operator tag?)" % mid))
				else:
					errors.append(("wrong_member", "route_master with non-relation member"))

		# missing tags
		if "name" not in tags:
			errors.append(("missing_tag", "missing name"))
		if "ref" not in tags:
			errors.append(("missing_tag", "missing ref"))
		if "route_master" not in tags:
			errors.append(("missing_tag", "missing route_master=(%s)." % "|".join(self.valid_route_master_values)))
		else:
			if tags["route_master"] not in self.valid_route_master_values:
				errors.append(("unexpected_value", "unexpected value for key route_master. expecting route_master=(%s)." % "|".join(self.valid_route_master_values)))

		return errors

	def validate_route_basics(self, relation):
		rid, tags, members = relation
		errors = []

		# invalid keys
		for i in self.invalid_keys_route:
			if i in tags:
				errors.append(("unexpected_key", "unexpected key: %s in route relation" % i))

		# missing tags
		if "name" not in tags:
			errors.append(("missing_tag", "missing name"))
		if "ref" not in tags:
			errors.append(("missing_tag", "missing ref"))
		if "route" not in tags:
			errors.append(("missing_tag", "missing route=(%s)." % "|".join(self.valid_route_values)))
		else:
			if tags["route"] not in self.valid_route_values:
				errors.append(("unexpected_value", "unexpected value for key route. expecting route=(%s)." % "|".join(self.valid_route_values)))

		# members
		if len(members) <= 0:
			errors.append(("no_members", "route without members"))
		else:
			has_node = False
			ways = []
			for member in members:
				mid, typ, role = member
				if typ == "way" and re.match(self.route_connected_way_roles_pattern, role):
					# (ways like platforms will be ignored due to route_connected_way_roles_pattern)
					ways.append(mid)
				if typ == "node":	
					has_node = True
					if not re.match(self.route_node_roles_pattern, role):
						errors.append(("unexpected_role", "route with node-member with a strange role: %s" % ("(empty)" if role == "" else role)))
			if len(ways) > 0:
				if self.validate_connectivity(ways) == False:
					errors.append(("disconnected_ways", "ways of route are not completely connected (or have strange roles)"))
				# (if validate_connectivity returns None, we can't validate this route because parts of it are outside of our pbf-file)
		return errors


	def validate_name(self, relation):
		rid, tags, members = relation

		if "type" not in tags or tags["type"] not in ["route", "route_master"]:
			return []
		key = tags["type"]

		if key not in tags:
			return []

		if "name" not in tags:
			return []

		if not re.match("^(Bus|Tram) ", tags["name"]):
			return [("wrong_name", u'name does not match convention ("Bus/Tram ...")')]

		return []

	def check_colour(self, relation):
		rid, tags, members = relation

		if "type" not in tags or tags["type"] not in ["route", "route_master"]:
			return []
		key = tags["type"]

		if key not in tags:
			return []

		if "type" in tags and tags["type"] == "router_master" and tags[key] in ["subway", "tram", "light_rail"] and "colour" not in tags:
			return [("no_colour", 'missing colour=#... for %s' % tags[key])]

		if "colour" in tags and not re.match("^#[a-fA-F0-9]{6}$", tags["colour"]):
			return [("wrong_colour", 'colour should be specified as hexadecimal value like #ff0000')]

		return []

	def check_stops_in_ways(self, relation):
		rid, tags, members = relation
		errors = []
		nodes_in_ways = []
		for m in members:
			mid, typ, role = m
			if typ == "way":
				if not mid in self.ways or self.ways[mid] == None:
					return [] # not in pbf - unable to check
				nodes_in_ways.extend(self.ways[mid][2])
		for m in members:
			mid, typ, role = m
			if typ == "node" and role == "stop" and mid not in nodes_in_ways:
				errors.append(('stop_outside_way', 'node-member %i has role \'stop\' but is not part of a contained way (might rather be a platform instead)' % mid, mid))
		return set(errors)

def is_normal_bus(r):
	return (("route" in r[1] and r[1]["route"] == "bus") or \
			("route_master" in r[1] and r[1]["route_master"] == "bus")) and \
			("ref" in r[1] and re.match("^[0-9]+$", r[1]["ref"]))

def is_metro_bus(r):
	return (("route" in r[1] and r[1]["route"] == "bus") or \
			("route_master" in r[1] and r[1]["route_master"] == "bus")) and \
			("ref" in r[1] and re.match("^M[0-9]+$", r[1]["ref"]))

def is_express_bus(r):
	return (("route" in r[1] and r[1]["route"] == "bus") or \
			("route_master" in r[1] and r[1]["route_master"] == "bus")) and \
			("ref" in r[1] and (re.match("^X[0-9]+$", r[1]["ref"]) or r[1]["ref"] == "TXL"))

def is_normal_tram(r):
	return (("route" in r[1] and r[1]["route"] == "tram") or \
			("route_master" in r[1] and r[1]["route_master"] == "tram")) and \
			("ref" in r[1] and re.match("^[0-9]+$", r[1]["ref"]))

def is_metro_tram(r):
	return (("route" in r[1] and r[1]["route"] == "tram") or \
			("route_master" in r[1] and r[1]["route_master"] == "tram")) and \
			("ref" in r[1] and re.match("^M[0-9]+$", r[1]["ref"]))

def is_ubahn(r):
	return (("route" in r[1] and r[1]["route"] == "subway") or \
			("route_master" in r[1] and r[1]["route_master"] == "subway")) and \
			("ref" in r[1] and re.match("^U[0-9]+$", r[1]["ref"]))

def is_sbahn(r):
	return (("route" in r[1] and r[1]["route"] == "light_rail") or \
			("route_master" in r[1] and r[1]["route_master"] == "light_rail")) and \
			("ref" in r[1] and re.match("^S[0-9]+$", r[1]["ref"]))

def is_s_or_u_bahn(r):
	return is_sbahn(r) or is_ubahn(r)

