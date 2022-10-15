#!/usr/bin/env python
# -*- coding: utf-8 -*-

# rn.py - load network of routes from OSM
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
import os
import stat
import datetime

from mako.lookup import TemplateLookup

import xml.etree.cElementTree as ET

class RouteNetwork(object):

  # dummy profile
  profile = {
    'name': '',
    'shortname': '',
    'filter_text': '',
    'datasource': '',
    'stopplan': False,
    'maps': {}
  }

  pbf = ""
  mtime = None
  relation_filter = lambda r: True
  makolookup = TemplateLookup(directories=[os.path.dirname(__file__) + '/templates'])

  def __init__(self):
    # the interesting objects will be stored in these 3 dicts:

    # dict of relations; index: relation id
    # each relation consists of (relation_id, tags, members)
    # where members consists of (member_id, member_type, role)
    self.relations = {}

    # dict of ways; index: way id
    # each way consists of (way_id, tags, node_ids)
    self.ways = {}

    # dict of nodes; index: node id
    # each node consists of (node_id, tags, coordinates)
    self.nodes = {}

    # additionally information about parent-relations is collected:
    # dict of parent relations; index: id of relation to get parent relations for
    self.parents = {}

  def load_network(self, xml, filterfunction=lambda r: True):

    # read data of public transport network
    # required for validating and displaying

    self.relation_filter = filterfunction

    # get modification time of data source
    # TODO: how to determine time when reading from multiple sources?
    self.mtime = datetime.datetime.fromtimestamp(os.stat(xml)[stat.ST_MTIME])

    root = ET.parse(xml).getroot()

    self.relations_cb(self.iter_relations(root))
    self.ways_cb(self.iter_ways(root))
    self.nodes_cb(self.iter_nodes(root))

  def iter_relations(self, root):
    for e in root:
      if e.tag != "relation":
        continue
      members = []
      for m in e:
        if m.tag != "member":
          continue
        members.append((int(m.attrib["ref"]), m.attrib["type"], m.attrib["role"]))
      yield (int(e.attrib["id"]), self.get_kvs(e), members)

  def iter_nodes(self, root):
    for e in root:
      if e.tag != "node":
        continue
      yield (int(e.attrib["id"]), self.get_kvs(e), (float(e.attrib["lon"]), float(e.attrib["lat"])))

  def iter_ways(self, root):
    for e in root:
      if e.tag != "way":
        continue
      nodes = []
      for n in e:
        if n.tag != "nd":
          continue
        nodes.append(int(n.attrib["ref"]))
      yield (int(e.attrib["id"]), self.get_kvs(e), nodes)

  @staticmethod
  def get_kvs(element):
    kvs = {}
    for kv in element:
      if kv.tag != "tag":
        continue
      kvs[kv.attrib["k"]] = kv.attrib["v"]
    return kvs

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

