#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from mako.template import Template

class RelationValidationOverviewCreator():

	show_additional_tags = ['ref', 'colour', 'name']

	def __init__(self):
		self.route_validators = []
		self.route_master_validators = []

	def create_relation_overview(self, template, output):

		print("Validating relations...")

		# create list that contains all important information for usage in template
		lines_tpl = []
		for relation in sorted(self.relations.values(), key=self.get_sortkey):
			rid, tags, members = relation
			l = {}
			l['osmid'] = rid
			l["fixme"] = ""
			for tag in ['type', 'route', 'route_master', 'note', 'fixme']:
				l[tag] = tags[tag] if tag in tags else ""
			for tag in self.show_additional_tags:
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
		tpl = Template(filename=template, default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace', lookup=self.makolookup)
		content = tpl.render(lines=lines_tpl, mtime=self.mtime, profile=self.profile, additional_tags=self.show_additional_tags)
		f = open(output, 'w')
		f.write(content.decode('utf-8'))
		f.close()

	def validate(self, relation):
		# validate passed route/route_master

		rid, tags, members = relation
		errors = []

		print("Validating %s..." % rid)

		if self.ignore_relation(relation):
			return [("ignored", "(ignoring this relation)")]

		# do validation depending on type of route 
		if "type" not in tags:
			return [("missing_type", "missing type=(route_master|route)")]
		if tags["type"] == "route_master":
			errors.extend(self.validate_route_master(relation))
		if tags["type"] == "route":
			errors.extend(self.validate_route(relation))

		return set(errors)

	def validate_route_master(self, relation):
		errors = []
		# run validators defined by child-class
		for v in self.route_master_validators:
			errors.extend(v(relation))
		return errors

	def validate_route(self, relation):
		errors = []
		# run validators defined by child-class
		for v in self.route_validators:
			errors.extend(v(relation))
		return errors

	def ignore_relation(self, relation):
		# defines which relations are excluded from validation
		# can be overridden in child class if required
		return False

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
			# TODO: implement better connectivity check based on node-id-intersection of ways
			return None
		# start dfs to check if all nodes are reachable from each other
		reached_nodes = self.dfs(nodes[0], edges, [])
		not_reached = set(nodes).difference(set(reached_nodes))
		return len(not_reached) == 0

	def dfs(self, n, edges, stop):
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
		if not "ref" in tags:
			# missing ref for comparing route with route_master
			return False
		if not ("relation", rid) in self.parents:
			# route without parent => without route_master
			return True
		for p in self.parents[("relation", rid)]:
			if p[0] != "relation":
				continue
			parent_id, parent_tags, parent_members = self.relations[p[1]]
			if "ref" in parent_tags and parent_tags["ref"] == tags["ref"] and "type" in parent_tags and parent_tags["type"] == "route_master":
				# has correct route_master (parent with type=route_master and same ref)
				return False
		# no correct parent: missing route_master
		return True

