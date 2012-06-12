#!/usr/bin/env python
# -*- coding: utf-8 -*-

# validate_oepnv.py - List and validate OEPNV in Berlin from OSM.
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

class OEPNVNetwork:

	lines = []
	collected_relations = {}
	interesting_ways = []
	collected_ways = {}
	interesting_nodes = []
	parents = {}

	def relation_filter(self, relation):
		# defines which relations to validate
		osmid, tags, members = relation
		return "network" in tags \
			and tags["network"] == "VBB" \
			and "operator" in tags \
			and (tags["operator"] == "BVG" or tags["operator"] == "S-Bahn Berlin GmbH") \
			and "type" in tags \
			and tags["type"] in ["route", "route_master"]

	def relation_ignore(self, relation):
		# defines which relations are excluded from validation
		osmid, tags, members = relation
		# don't try to validate "...linien in Berlin"-relations
		return osmid in [18812, 174283, 53181]

	def relations(self, relations):
		# callback: collect routes to validate
		for relation in relations:
			osmid, tags, members = relation
			# fast DEBUGGING with line 100:
			#if osmid not in [17697, 1900690, 1900691]:
			#	continue
			if self.relation_filter(relation):
				self.lines.append(relation)
				osmid, tags, members = relation
				self.collected_relations[osmid] = relation
				for member in members:
					osmid_member, typ, role = member
					if typ == "way":
						self.interesting_ways.append(osmid_member)
					if typ == "relation":
						if osmid_member not in self.parents:
							self.parents[osmid_member] = [osmid]
						else:
							self.parents[osmid_member].append(osmid)

	def ways(self, ways):
		# callback: collect interesting ways
		for way in ways:
			osmid, tags, nodes = way
			if osmid in self.interesting_ways:
				self.collected_ways[osmid] = nodes
				self.interesting_nodes.extend(nodes)

	def get_sortkey(self, line):
		osmid, tags, members = line
		if "name" in tags:
			return tags["name"]
		else:
			return ""

	def count_member_types(self, relation):
		# count how many members of each type the relation has
		osmid, tags, members = relation
		types = {'relation': 0, 'node': 0, 'way': 0}
		for member in members:
			osmid_member, typ, role = member
			types[typ] += 1
		return types

	def dfs(self, n, edges, stop):
		# depth first search (called recursively)
		if n in stop:
			return []
		reached = [n]
		if n in edges and len(edges[n]) > 0:
			stop.append(n)
			for target in edges[n]:
				reached.extend(self.dfs(target, edges, stop))
		return reached

	def validate_connectivity(self, ways):
		# check if all passed ways are connected
		edges = {}
		nodes = []
		# build a connectivity (edge) matrix for all nodes in all ways
		for way in ways:
			node_prev = None
			if way not in self.collected_ways:
				return None # unable to validate - way not in pbf
			for node in self.collected_ways[way]:
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
		# start dfs to check if all nodes are reachable from each other
		reached_nodes = self.dfs(nodes[0], edges, [])
		not_reached = set(nodes).difference(set(reached_nodes))
		return len(not_reached) == 0

	def validate(self, line):
		# validate passed line

		osmid, tags, members = line
		errors = []

		print "Validating line %s..." % osmid

		if self.relation_ignore(line):
			return ["(ignoring this relation)"]

		if tags["type"] == "route_master":
			unexpected_tags = ["route", "from", "to"]
			for u in unexpected_tags:
				if u in tags:
					errors.append("unexpedted key: %s in route_master relation" % u)
			if len(members) <= 0:
				errors.append("route_master without members")
			else:
				for member in members:
					osmid_member, typ, role = member
					if typ == "relation":
						if osmid_member not in self.collected_relations:
							errors.append("member id %i not found (missing network and/or operator tag?)" % osmid_member)
					else:
						errors.append("route_master with non-relation member")
			if "name" not in tags:
				errors.append("missing name")
			if "ref" not in tags:
				errors.append("missing ref")
			if "route_master" not in tags:
				errors.append("missing key route_master=(bus|tram|subway|ferry|light_rail)")
			else:
				if tags["route_master"] not in ["bus", "tram", "subway", "ferry", "light_rail"]:
					errors.append("unexpected value for key route_master. expecting route_master=(bus|tram|subway|ferry|light_rail).")
				if "name" in tags:
					if tags["route_master"] == "bus":
						if not re.match("^Buslinie ", tags["name"]):
							errors.append(u'name does not match convention ("Buslinie ...")')
					if tags["route_master"] == "ferry":
						if not re.match(u"^Fähre ", tags["name"]):
							errors.append(u'name does not match convention ("Fähre ...")')
					if tags["route_master"] == "tram":
						if not re.match(u"^Straßenbahnlinie ", tags["name"]):
							errors.append(u'name does not match convention ("Straßenbahnlinie ...")')
					if tags["route_master"] == "subway":
						if not re.match(u"^U-Bahnlinie ", tags["name"]):
							errors.append(u'name does not match convention ("U-Bahnlinie ...")')

		if tags["type"] == "route":
			if "route_master" in tags:
				errors.append("unexpedted key: route_master in route relation")
			if "name" not in tags:
				errors.append("missing name")
			if "ref" not in tags:
				errors.append("missing ref")
			if "route" not in tags:
				errors.append("missing key route=(bus|tram|subway|ferry|light_rail)")
			else:
				if tags["route"] not in ["bus", "tram", "subway", "ferry", "light_rail"]:
					errors.append("unexpected value for key route. expecting route=(bus|tram|subway|ferry|light_rail).")
				if "name" in tags:
					if tags["route"] == "bus":
						if not re.match("^Buslinie ", tags["name"]):
							errors.append(u'name does not match convention ("Buslinie ...")')
					if tags["route"] == "ferry":
						if not re.match(u"^Fähre ", tags["name"]):
							errors.append(u'name does not match convention ("Fähre ...")')
					if tags["route"] == "tram":
						if not re.match(u"^Straßenbahnlinie ", tags["name"]):
							errors.append(u'name does not match convention ("Straßenbahnlinie ...")')
					if tags["route"] == "subway":
						if not re.match(u"^U-Bahnlinie ", tags["name"]):
							errors.append(u'name does not match convention ("U-Bahnlinie ...")')
				if tags["route"] == "subway" and "color" not in tags:
					errors.append(u'missing color=#... for subway line')
				if tags["route"] == "tram" and "color" not in tags:
					errors.append(u'missing color=#... for tram line')
			if len(members) <= 0:
				errors.append("route without members")
			else:
				has_node = False
				ways = []
				for member in members:
					osmid_member, typ, role = member
					if typ == "way" and role == "":
						# only collect ways without role - others might be (not-connected) platforms
						ways.append(osmid_member)
					if typ == "node":	
						has_node = True
						if not re.match("^(platform(:.*)?|stop(:.*)?|forward(:.*)?|backward|)$", role):
							errors.append("route with node-member with a strange role: %s" % role)
				if len(ways) <= 0:
					errors.append("route without ways or type=route instead of type=route_master")
				else:
					if self.validate_connectivity(ways) == False:
						errors.append("ways of route are not completely connected (or have strange roles)")
					# (if validate_connectivity returns None, we can't validate this route because parts of it are outside of our pbf-file)
				if not has_node:
					errors.append("route without nodes (stops missing?)")

		return set(errors)

	def create_report(self, pbf="berlin.osm.pbf", template="template.tpl", output="lines.htm"):

		# collect all relations that should be validated
		print "Collecting relations..."
		p = OSMParser(concurrency=4, relations_callback=self.relations)
		p.parse(pbf)

		# collect ways for these relations for performing a connectivity check
		# (doing 2 parses because this tooks less time+space than collecting all ways in a single parse)
		self.interesting_ways = list(set(self.interesting_ways))
		print "Collecting %i interesting ways..." % len(self.interesting_ways)
		p = OSMParser(concurrency=4, ways_callback=self.ways)
		p.parse(pbf)

		print "Validating relations..."

		# create list that contains all important information for usage in template
		lines_tpl = []
		for line in sorted(self.lines, key=self.get_sortkey):
			osmid, tags, members = line
			l = {}
			l['osmid'] = osmid
			l["fixme"] = ""
			for tag in ['type', 'route', 'route_master', 'color', 'ref', 'name', 'note', 'fixme']:
				l[tag] = tags[tag] if tag in tags else ""
			if "FIXME" in tags:
				l["fixme"] += tags["FIXME"]
			l['errors'] = self.validate(line)
			members = self.count_member_types(line)
			l['relations'] = members['relation']
			l['ways'] = members['way']
			l['nodes'] = members['node']
			lines_tpl.append(l)


		mtime = datetime.datetime.fromtimestamp(os.stat(pbf)[stat.ST_MTIME])

		# write template
		tpl = Template(filename=template, default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace')
		# TODO: escape html - in template?
		content = tpl.render(lines=lines_tpl, mtime=mtime)
		f = open(output, 'w')
		f.write(content)
		f.close()

		print "Done."

def main():
	if len(sys.argv) < 4:
		print "Please speficy pbf file, template file and output file."
	else:
		net = OEPNVNetwork()
		net.create_report(pbf=sys.argv[1], template=sys.argv[2], output=sys.argv[3])

if __name__ == '__main__':
	main()

