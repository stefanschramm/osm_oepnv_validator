#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from mako.template import Template

class RouteListCreator():

	def create_route_list(self, template, output, filterfunction=lambda m: True):

		# print list of stations of a route
		# within the directions of a route the stations are identified by their name
		# (which will cause problems in routes like M1 having "U Oranienburger Tor" 2 times)

		lines = []

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

			variations = []

			for pair in pairs:
				# get stops for each direction
				rid1, tags1, members1 = pair[0]
				stops1 = filter(lambda m: re.match(self.route_node_roles_pattern, m[2]), members1)
				stops1 = map(lambda s: s[0], stops1)
				rid2, tags2, members2 = pair[1]
				stops2 = filter(lambda m: re.match(self.route_node_roles_pattern, m[2]), members2)
				stops2 = map(lambda s: s[0], stops2)
				stops2.reverse()

				# collect names and changes for each direction
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
					stops.append((symbol, name, changes[name]))
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
		tpl = Template(filename=template, default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace', lookup=self.makolookup)
		content = tpl.render(lines=lines, mtime=self.mtime, profile=self.profile)
		f = open(output, 'w')
		f.write(content)
		f.close()

