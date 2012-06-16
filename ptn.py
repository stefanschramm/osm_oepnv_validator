#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ptn.py - list and validate OSM public transport lines
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

import sys
import re
import os
import stat
import datetime
from imposm.parser import OSMParser
from mako.template import Template

# required dependencies:
# sudo apt-get install python-imposm
# sudo apt-get install python-mako

class PublicTransportNetwork:

	# all valid keys for a relation (both, route or route_master)
	valid_keys = ["name", "network", "operator", "ref", "route_master", "route", "type", "from", "to", "via", "by_night", "wheelchair", "bus", "direction", "note", "fixme", "FIXME", "color", "colour", "service_times", "description", "wikipedia"]

	# keys that can't appear on a route_master
	invalid_keys_route_master = ["route", "from", "to", "via"]

	# keys that can't appear on a route
	invalid_keys_route = ["route_master"]

	# valid values for route attribute
	# http://wiki.openstreetmap.org/wiki/Relation:route#Core_values
	valid_route_values = ["bus", "trolleybus", "share_taxi", "train", "monorail", "subway", "tram", "ferry", "light_rail"]

	# valid values for route_master attribute
	valid_route_master_values = valid_route_values

	# pattern for roles of nodes of routes
	# http://wiki.openstreetmap.org/wiki/Relation:route#Members
	route_node_roles_pattern = "^(stop:[0-9]+|stop|forward:stop:[0-9]+|backward:stop:[0-9]+|platform:[0-9]+|platform)$"

	# pattern for roles of ways of routes that need to be connected to each other
	# http://wiki.openstreetmap.org/wiki/Relation:route#Members
	route_way_roles_pattern = "^(|route|forward|backward|platform:[0-9]+|platform)$"


	text_region = ""
	text_filter = ""
	text_datasource = ""

	route_validators = []
	route_master_validators = []

	profile = None
	pbf = ""
	mtime = None
	relation_filter = lambda r: True

	# the interesting objects are stored in these 3 dicts:

	# dict of relations; index: relation id
	# each relation consists of (relation_id, tags, members)
	# where members consists of (member_id, member_type, role)
	relations = {}

	# dict of ways; index: way id
	# each way consists of (way_id, tags, node_ids)
	ways = {}

	# dict of nodes; index: node id
	# each node consists of (node_id, tags, coordinates)
	nodes = {}

	# additionally information about parent-relations is collected:
	# dict of parent relations; index: id of relation to get parent relations for
	parents = {}

	# child classes need to implement:
	# def relation_filter(self, relation)
	# - defines which relations to validate

	def load_network(self, pbf, filterfunction=lambda r: True):

		# read data of public transport network
		# required for validating and displaying

		self.pbf = pbf

		self.relation_filter = filterfunction

		# get modification time of data source
		selfmtime = datetime.datetime.fromtimestamp(os.stat(self.pbf)[stat.ST_MTIME])

		# first pass:
		# collect all interesting relations
		print "Collecting relations..."
		p = OSMParser(concurrency=4, relations_callback=self.relations_cb)
		p.parse(pbf)

		# second pass:
		# collect ways for these relations
		print "Collecting %i ways..." % len(self.ways)
		p = OSMParser(concurrency=4, ways_callback=self.ways_cb)
		p.parse(pbf)

		# collect nodes for collected relations and ways
		print "Collecting %i nodes..." % len(self.nodes)
		p = OSMParser(concurrency=4, nodes_callback=self.nodes_cb)
		p.parse(pbf)

	def relations_cb(self, relations):
		# callback: collect routes to validate
		for relation in relations:
			rid, tags, members = relation
			if self.relation_filter(relation):
				self.relations[rid] = relation
				for member in members:
					mid, typ, role = member
					if typ == "node":
						self.nodes[mid] = None
					if typ == "way":
						self.ways[mid] = None
					if (typ, mid) not in self.parents:
						self.parents[(typ, mid)] = [("relation", rid)]
					else:
						self.parents[(typ, mid)].append(("relation", rid))

	def ways_cb(self, ways):
		# callback: collect interesting ways
		for way in ways:
			wid, tags, nodes = way
			if wid in self.ways and self.ways[wid] == None:
				self.ways[wid] = way
				for nid in nodes:
					self.nodes[nid] = None

	def nodes_cb(self, nodes):
		# callback: collect interesting nodes
		for node in nodes:
			nid, tags, coords = node
			if nid in self.nodes and self.nodes[nid] == None:
				self.nodes[nid] = node


	def create_relation_overview(self, template, output):

		print "Validating relations..."

		# create list that contains all important information for usage in template
		lines_tpl = []
		for relation in sorted(self.relations.values(), key=self.get_sortkey):
			rid, tags, members = relation
			l = {}
			l['osmid'] = rid
			l["fixme"] = ""
			for tag in ['type', 'route', 'route_master', 'color', 'ref', 'name', 'note', 'fixme']:
				l[tag] = tags[tag] if tag in tags else ""
			if "FIXME" in tags:
				l["fixme"] += tags["FIXME"]
			l['errors'] = self.validate(relation)
			l['noroutemaster'] = self.no_route_master(relation)
			members = self.count_member_types(relation)
			l['relations'] = members['relation']
			l['ways'] = members['way']
			l['nodes'] = members['node']
			lines_tpl.append(l)

		# write template
		tpl = Template(filename=template, default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace')
		content = tpl.render(lines=lines_tpl, mtime=self.mtime, region=self.text_region, filter=self.text_filter, datasource=self.text_datasource)
		f = open(output, 'w')
		f.write(content)
		f.close()

		print "Done."

	def create_network_map(self, template, output, filterfunction=lambda r: True):
		lines = []
		for relation in self.relations.values():
			rid, tags, members = relation
			if "type" not in tags or tags["type"] != "route":
				# ignore route_master, only print individual routes
				continue
			if not filterfunction(relation):
				continue
			stations = []
			for member in members:
				mid, typ, role = member
				if typ != "node" or not re.match(self.route_node_roles_pattern, role):
					continue
				if not mid in self.nodes or self.nodes[mid] == None:
					# station hasn't been collected - probably not in pbf
					continue
				stations.append(self.nodes[mid])
			lines.append([rid, tags, stations])

		# write template
		tpl = Template(filename=template, default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace')
		content = tpl.render(lines=lines, mtime=self.mtime, region=self.text_region, filter=self.text_filter, datasource=self.text_datasource)
		f = open(output, 'w')
		f.write(content)
		f.close()

	def create_route_list(self, template, output, filterfunction=lambda m: True):

		# print list of stations of a route
		# within the directions of a route the stations are identified by their name
		# (which will cause problems in routes like M1 having "U Oranienburger Tor" 2 times)

		lines = []

		out = ""
                for relation in sorted(self.relations.values(), key=self.get_sortkey):
			rid, tags, members = relation
			if "type" not in tags or tags["type"] != "route_master" or "ref" not in tags:
				continue
			if not filterfunction(relation):
				continue
			routes = filter(lambda m: m[0] in self.relations and m[1] == "relation", members)
			routes = map(lambda m: self.relations[m[0]], routes)

			pairs = []
			for i in range(0, len(routes)):
				if not "from" in routes[i][1] or not "to" in routes[i][1]:
					continue
				for j in range(i + 1, len(routes)):
					if not "from" in routes[j][1] or not "to" in routes[j][1]:
						continue
					if routes[i][1]['from'] == routes[j][1]['to'] and routes[i][1]['to'] == routes[j][1]['from']:
						pairs.append((routes[i], routes[j]))
			if len(pairs) == 0:
				# only output routes of route_masters that have matching from and to
				continue

			out += (70 * "=") + "\n"
			out += (tags["name"] if "name" in tags else "") + (" (%i)\n" % rid)
			out += "\n"
			
			variations = []

			for pair in pairs:
				rid1, tags1, members1 = pair[0]
				stops1 = filter(lambda m: re.match(self.route_node_roles_pattern, m[2]), members1)
				stops1 = map(lambda s: s[0], stops1)
				rid2, tags2, members2 = pair[1]
				stops2 = filter(lambda m: re.match(self.route_node_roles_pattern, m[2]), members2)
				stops2 = map(lambda s: s[0], stops2)
				stops2.reverse()

				out += "(%i, %i)\n" % (rid1, rid2)
				out += "\n"

				# collect names
				names1 = []
				names2 = []
				changes = {}
				for s in stops1:
					if s in self.nodes and self.nodes[s] != None:
						nid, tags, coords= self.nodes[s]
						if "name" in tags:
							if tags["name"] not in names1:
								names1.append(tags["name"])
							if tags["name"] not in changes:
								changes[tags["name"]] = []
							for p in self.parents[("node", nid)]:
								if p[0] != "relation":
									continue
								# TODO: check if not available?
								r = self.relations[p[1]]
								if "ref" in r[1] and r[1]["ref"] != relation[1]["ref"] and r[1]["ref"] not in changes[tags["name"]]:
									changes[tags["name"]].append(r[1]["ref"])
							
				for s in stops2:
					if s in self.nodes and self.nodes[s] != None:
						nid, tags, coords= self.nodes[s]
						if "name" in tags:
							if tags["name"] not in names2:
								names2.append(tags["name"])
							if tags["name"] not in changes:
								changes[tags["name"]] = []
							for p in self.parents[("node", nid)]:
								if p[0] != "relation":
									continue
								# TODO: check if not available?
								r = self.relations[p[1]]
								if "ref" in r[1] and r[1]["ref"] != relation[1]["ref"] and r[1]["ref"] not in changes[tags["name"]]:
									changes[tags["name"]].append(r[1]["ref"])

				stops = []

				i = 0;
				j = 0;
				while i < len(names1) or j < len(names2):
					# TODO: logic correct??
					if i == len(names1):
						symbol = u"▲"
						name = names2[j]
						j += 1
					elif j == len(names2):
						symbol = u"▼"
						name = names1[i]
						i += 1
					elif names1[i] == names2[j]:
						symbol = u"●"
						name = names1[i]
						i += 1
						j += 1
					elif not names1[i] in names2:
						symbol = u"▼"
						name = names1[i]
						i += 1
					else:
						symbol = u"▲"
						name = names2[j]
						j += 1
					if len(changes[name]) > 0:
						out += "%s %s [%s]\n" % (symbol, name, ", ".join(sorted(changes[name])))
					else:
						out += "%s %s\n" % (symbol, name)
					stops.append((symbol, name, changes[name]))
				out += "\n"
				variations.append({
					"from": pair[0][1]["from"],
					"to": pair[0][1]["to"],
					"ids": (pair[0][0], pair[1][0]),
					"stops": stops
				})
			lines.append({
				'id': rid,
				'name': relation[1]['name'] if "name" in relation[1] else "",
				'ref': relation[1]['ref'] if "ref" in relation[1] else "",
				'variations': variations
			})

		# write template
		tpl = Template(filename=template, default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace')
		content = tpl.render(lines=lines, mtime=self.mtime, region=self.text_region, filter=self.text_filter, datasource=self.text_datasource)
		f = open(output, 'w')
		f.write(content)
		f.close()

	def validate(self, relation):
		# validate passed line

		rid, tags, members = relation
		errors = []

		print "Validating line %s..." % rid

		if self.ignore_relation(relation):
			return [("ignored", "(ignoring this relation)")]

		for key in tags:
			main_key = key.split(":")[0]
			if not main_key in self.valid_keys:
				errors.append(("unknown_key", "unknown key: %s" % key))

		# do validation depending on type of route 

		if "type" not in tags:
			return []

		if tags["type"] == "route_master":
			errors.extend(self.validate_route_master(relation))

		if tags["type"] == "route":
			errors.extend(self.validate_route(relation))

		return set(errors)

	def validate_route_master(self, relation):
		errors = []
		rid, tags, members = relation

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

		# run validators defined in child-class
		for v in self.route_master_validators:
			errors.extend(v(relation))

		return errors

	def validate_route(self, relation):
		errors = []
		rid, tags, members = relation

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
				if typ == "way" and re.match(self.route_way_roles_pattern, role):
					# (ways like platforms will be ignored due to route_way_roles_pattern)
					ways.append(mid)
				if typ == "node":	
					has_node = True
					if not re.match(self.route_node_roles_pattern, role):
						errors.append(("unexpected_role", "route with node-member with a strange role: %s" % ("(empty)" if role == "" else role)))
			if len(ways) <= 0:
				errors.append(("no_ways", "route without ways or type=route instead of type=route_master"))
			else:
				if self.validate_connectivity(ways) == False:
					errors.append(("disconnected_ways", "ways of route are not completely connected (or have strange roles)"))
				# (if validate_connectivity returns None, we can't validate this route because parts of it are outside of our pbf-file)
			if not has_node:
				# TODO: this would be OK, if all stops are modeled as relations
				errors.append(("no_nodes", "route without nodes (stops missing?)"))

		# run validators defined in child-class
		for v in self.route_validators:
			errors.extend(v(relation))

		return errors

	def ignore_relation(self, relation):
		# defines which relations are excluded from validation
		# can be overridden in parent class if required
		return False

	def get_sortkey(self, relation):
		rid, tags, members = relation
		key = ""
		if "route_master" in tags:
			key += tags["route_master"]
		elif "route" in tags:
			key += tags["route"]
		key += "_"
		if "ref" in tags:
			ref = tags["ref"]
			for number in set(re.findall("[0-9]+", ref)):
				# append a lot of leading zeroes to each number
				ref = ref.replace(number, "%010i" % int(number))
			key += ref
		key += "_"
		if "type" in tags and tags["type"] == "route_master":
			# for same refs put route_master at top
			key += "0"
		else:
			key += "1"
		return key

	def count_member_types(self, relation):
		# count how many members of each type the relation has
		rid, tags, members = relation
		types = {'relation': 0, 'node': 0, 'way': 0}
		for member in members:
			mid, typ, role = member
			types[typ] += 1
		return types

	def validate_connectivity(self, ways):
		# check if all passed ways are connected
		edges = {}
		nodes = []
		# build a connectivity (edge) matrix for all nodes in all (non-platform-)ways
		for way in ways:
			node_prev = None
			if way not in self.ways or self.ways[way] == None:
				return None # unable to validate - way not in pbf
			for node in self.ways[way][2]:
				nodes.append(node)
				if node_prev != None:
					if node_prev not in edges:
						edges[node_prev] = [node]
					else:
						edges[node_prev].append(node)
					if node not in edges:
						edges[node] = [node_prev]
					else:
						edges[node].append(node_prev)
				node_prev = node
		nodes = list(set(nodes))
		if len(nodes) == 0:
			# no ways contained
			return True
		if len(nodes) > 900:
			# to many nodes, would raise exception because of recursion
			# TODO: implement better connectivity check
			return None
		# start dfs to check if all nodes are reachable from each other
		reached_nodes = self.dfs(nodes[0], edges, [])
		not_reached = set(nodes).difference(set(reached_nodes))
		return len(not_reached) == 0

	def dfs(self, n, edges, stop):
		# print n
		# depth first search (called recursively), started by validate_connectivity
		if n in stop:
			return []
		reached = [n]
		if n in edges and len(edges[n]) > 0:
			stop.append(n)
			for target in edges[n]:
				reached.extend(self.dfs(target, edges, stop))
		return reached

	def no_route_master(self, relation):
		rid, tags, members = relation
		if not "route" in tags:
			# seems to be route master or something else
			return False
		if not ("relation", rid) in self.parents:
			# route without route_master
			return True
		for p in self.parents[("relation", rid)]:
			if p[0] != "relation":
				continue
			parent_id, parent_tags, parent_members = self.relations[p[1]]
			if "ref" in parent_tags and parent_tags["ref"] == tags["ref"] and "type" in parent_tags and parent_tags["type"] == "route_master":
				# has correct route_master (same ref)
				return False
		# no correct parent: missing route_master
		return True

