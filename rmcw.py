#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mako.template import Template

class RouteMapCreatorByWays():

  def create_network_map(self, template, output, mapkey="", filterfunction=lambda r: True):
    lines = []
    for relation in self.relations.values():
      rid, tags, members = relation
      if "type" not in tags or tags["type"] != "route":
        # ignore route_master, only print individual routes
        continue
      if not filterfunction(relation):
        continue
      ways = []
      # TODO: logic for collecting ways + adopt template
#      for member in members:
#        mid, typ, role = member
#        if typ != "node" or not re.match(self.route_node_roles_pattern, role):
#          continue
#        if not mid in self.nodes or self.nodes[mid] == None:
#          # station hasn't been collected - probably not in pbf
#          continue
#        stations.append(self.nodes[mid])
      lines.append([rid, tags, ways])

    # write template
    tpl = Template(filename=template, default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace', lookup=self.makolookup)
    content = tpl.render(lines=lines, mtime=self.mtime, profile=self.profile, mapkey=mapkey)
    f = open(output, 'w')
    f.write(content)
    f.close()

