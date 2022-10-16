import re

from typing import Type
from network import RouteNetwork
from profile import PublicTransportProfile

def relation_colour(p: Type[PublicTransportProfile], n: Type[RouteNetwork], relation):
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

class RelationNameRegexp():
  def __init__(self, regexp):
    self.regexp = regexp
  def __call__(self, p: Type[PublicTransportProfile], n: Type[RouteNetwork], relation):
    rid, tags, members = relation

    if "type" not in tags or tags["type"] not in ["route", "route_master"]:
      return []
    key = tags["type"]

    if key not in tags:
      return []

    if "name" not in tags:
      return []

    if not re.match(self.regexp, tags["name"]):
      return [("wrong_name", u'name does not match regular expression: %s' % self.regexp)]

    return []

def relation_stops_in_ways(p: Type[PublicTransportProfile], n: Type[RouteNetwork], relation):
  rid, tags, members = relation
  errors = []
  nodes_in_ways = []
  for m in members:
    mid, typ, role = m
    if typ == "way":
      if not mid in n.ways or n.ways[mid] == None:
        return [] # not in pbf - unable to check
      nodes_in_ways.extend(n.ways[mid][2])
  for m in members:
    mid, typ, role = m
    if typ == "node" and role == "stop" and mid not in nodes_in_ways:
      errors.append(('stop_outside_way', 'node-member %i has role \'stop\' but is not part of a contained way (might rather be a platform instead)' % mid, mid))
  return set(errors)

def relation_route_basics(p: Type[PublicTransportProfile], n: Type[RouteNetwork], relation):
  rid, tags, members = relation
  errors = []

  # invalid keys
  for i in p.invalid_keys_route:
    if i in tags:
      errors.append(("unexpected_key", "unexpected key: %s in route relation" % i))

  # missing tags
  if "name" not in tags:
    errors.append(("missing_tag", "missing name"))
  if "ref" not in tags:
    errors.append(("missing_tag", "missing ref"))
  if "route" not in tags:
    errors.append(("missing_tag", "missing route=(%s)." % "|".join(p.valid_route_values)))
  else:
    if tags["route"] not in p.valid_route_values:
      errors.append(("unexpected_value", "unexpected value for key route. expecting route=(%s)." % "|".join(p.valid_route_values)))

  # members
  if len(members) <= 0:
    errors.append(("no_members", "route without members"))
  else:
    has_node = False
    ways = []
    for member in members:
      mid, typ, role = member
      if typ == "way" and re.match(p.route_connected_way_roles_pattern, role):
        # (ways like platforms will be ignored due to route_connected_way_roles_pattern)
        ways.append(mid)
      if typ == "node":  
        has_node = True
        if not re.match(p.route_node_roles_pattern, role):
          errors.append(("unexpected_role", "route with node-member with a strange role: %s" % ("(empty)" if role == "" else role)))
    if len(ways) > 0:
      if connectivity(n, ways) == False:
        errors.append(("disconnected_ways", "ways of route are not completely connected (or have strange roles)"))
      # (if validate_connectivity returns None, we can't validate this route because parts of it are outside of our pbf-file)

    if no_route_master(p, n, relation):
      errors.append(("no_route_master", "route relation without corresponding route_master as parent"))

  return errors

def relation_route_master_basics(p: Type[PublicTransportProfile], n: Type[RouteNetwork], relation):
  rid, tags, members = relation
  errors = []

  # invalid keys
  for i in p.invalid_keys_route_master:
    if i in tags:
      errors.append(("unexpected_key", "unexpected key: %s in route_master relation" % i))

  # no members
  if len(members) <= 0:
    errors.append("route_master without members")
  else:
    for member in members:
      mid, typ, role = member
      if typ == "relation":
        if mid not in n.relations:
          errors.append(("unknown_member", "member id %i not found (missing network and/or operator tag?)" % mid))
      else:
        errors.append(("wrong_member", "route_master with non-relation member"))

  # missing tags
  if "name" not in tags:
    errors.append(("missing_tag", "missing name"))
  if "ref" not in tags:
    errors.append(("missing_tag", "missing ref"))
  if "route_master" not in tags:
    errors.append(("missing_tag", "missing route_master=(%s)." % "|".join(p.valid_route_master_values)))
  else:
    if tags["route_master"] not in p.valid_route_master_values:
      errors.append(("unexpected_value", "unexpected value for key route_master. expecting route_master=(%s)." % "|".join(p.valid_route_master_values)))

  return errors

def no_route_master(p: Type[PublicTransportProfile], n: Type[RouteNetwork], relation):
  rid, tags, members = relation
  if not "route" in tags:
    # seems to be route master or something else
    return False
  if not "ref" in tags:
    # missing ref for comparing route with route_master
    return False
  if not ("relation", rid) in n.parents:
    # route without parent => without route_master
    return True
  for p in n.parents[("relation", rid)]:
    if p[0] != "relation":
      continue
    parent_id, parent_tags, parent_members = n.relations[p[1]]
    if "ref" in parent_tags and parent_tags["ref"] == tags["ref"] and "type" in parent_tags and parent_tags["type"] == "route_master":
      # has correct route_master (parent with type=route_master and same ref)
      return False
  # no correct parent: missing route_master
  return True

def connectivity(n: Type[RouteNetwork], ways):
  # check if all passed ways are connected
  edges = {}
  nodes = []
  # build a connectivity (edge) matrix for all nodes in all (non-platform-)ways
  for way in ways:
    node_prev = None
    if way not in n.ways or n.ways[way] == None:
      return None # unable to validate - way not in pbf
    for node in n.ways[way][2]:
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
  reached_nodes = dfs(nodes[0], edges, [])
  not_reached = set(nodes).difference(set(reached_nodes))
  return len(not_reached) == 0

def dfs(n, edges, stop):
  # depth first search (called recursively), started by validate_connectivity
  if n in stop:
    return []
  reached = [n]
  if n in edges and len(edges[n]) > 0:
    stop.append(n)
    for target in edges[n]:
      reached.extend(dfs(target, edges, stop))
  return reached