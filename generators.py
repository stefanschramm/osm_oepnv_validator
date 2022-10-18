import context
import validator

import re

from profiles.base.public_transport import PublicTransportProfile
from network import RouteNetwork

from mako.lookup import TemplateLookup
from mako.template import Template

show_additional_tags = ['ref', 'colour', 'name']

makolookup = TemplateLookup(directories=[context.get_template_dir()])

def generate_index(profiles):
    # write template
    tpl = Template(filename='templates/index.tpl', default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace')
    content = tpl.render(profiles=profiles)
    f = open(context.custom_output_file_path('index.htm'), 'w')
    f.write(content.decode('utf-8'))
    f.close()

def generate_relation_overview(n: RouteNetwork, p: PublicTransportProfile):
    v = validator.Validator(n, p)

    lines_tpl = []
    for relation in sorted(n.relations.values(), key=get_sortkey):
      rid, tags, members = relation
      l = {}
      l['osmid'] = rid
      l["fixme"] = ""
      for tag in ['type', 'route', 'route_master', 'note', 'fixme']:
        l[tag] = tags[tag] if tag in tags else ""
      for tag in show_additional_tags:
        l[tag] = tags[tag] if tag in tags else ""
      if "FIXME" in tags:
        l["fixme"] += tags["FIXME"]
      l['errors'] = v.validate_relation(relation)
      members = count_member_types(relation)
      l['relations'] = members['relation']
      l['ways'] = members['way']
      l['nodes'] = members['node']
      lines_tpl.append(l)

    # write template
    tpl = Template(filename='templates/relations.tpl', default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace', lookup=makolookup)
    content = tpl.render(lines=lines_tpl, mtime=n.mtime, profile=p, additional_tags=show_additional_tags)
    f = open(context.output_file_path(p), 'w')
    f.write(content.decode('utf-8'))
    f.close()

def generate_stop_plan(n: RouteNetwork, p: PublicTransportProfile):
  # print list of stations of a route
  # within the directions of a route the stations are identified by their name
  # (which will cause problems in routes like M1 having "U Oranienburger Tor" 2 times)

  lines = []

  for relation in sorted(n.relations.values(), key=get_sortkey):
    rid, tags, members = relation
    if "type" not in tags or tags["type"] != "route_master" or "ref" not in tags:
      continue
    if not p.filter(relation):
      continue
    routes = filter(lambda m: m[0] in n.relations and m[1] == "relation", members)
    routes = list(map(lambda m: n.relations[m[0]], routes))

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
      stops1 = filter(lambda m: re.match(p.route_node_roles_pattern, m[2]), members1)
      stops1 = list(map(lambda s: s[0], stops1))
      rid2, tags2, members2 = pair[1]
      stops2 = filter(lambda m: re.match(p.route_node_roles_pattern, m[2]), members2)
      stops2 = list(map(lambda s: s[0], stops2))
      stops2.reverse()

      # collect names and changes for each direction
      names1 = []
      names2 = []
      changes = {}
      for s in stops1:
        if s in n.nodes and n.nodes[s] != None:
          nid, tags, coords= n.nodes[s]
          if "name" in tags:
            if tags["name"] not in names1:
              names1.append(tags["name"])
            if tags["name"] not in changes:
              changes[tags["name"]] = []
            for parent in n.parents[("node", nid)]:
              if parent[0] != "relation":
                continue
              # TODO: check if not available?
              r = n.relations[parent[1]]
              if "ref" in r[1] and r[1]["ref"] != relation[1]["ref"] and r[1]["ref"] not in changes[tags["name"]]:
                changes[tags["name"]].append(r[1]["ref"])
      for s in stops2:
        if s in n.nodes and n.nodes[s] != None:
          nid, tags, coords= n.nodes[s]
          if "name" in tags:
            if tags["name"] not in names2:
              names2.append(tags["name"])
            if tags["name"] not in changes:
              changes[tags["name"]] = []
            for parent in n.parents[("node", nid)]:
              if parent[0] != "relation":
                continue
              # TODO: check if not available?
              r = n.relations[parent[1]]
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
  tpl = Template(filename='templates/routes.tpl', default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace', lookup=makolookup)
  content = tpl.render(lines=lines, mtime=n.mtime, profile=p)
  f = open(context.output_file_path(p, '_lines'), 'w')
  f.write(content.decode('utf-8'))
  f.close()

def generate_network_map(n: RouteNetwork, p: PublicTransportProfile, mapkey):
  lines = []
  for relation in n.relations.values():
    rid, tags, members = relation
    if "type" not in tags or tags["type"] != "route":
      # ignore route_master, only print individual routes
      continue
    if not p.maps[mapkey][1](relation):
      continue
    stations = []
    for member in members:
      mid, typ, role = member
      if typ != "node" or not re.match(p.route_node_roles_pattern, role):
        continue
      if not mid in n.nodes or n.nodes[mid] == None:
        # station hasn't been collected - probably not in pbf
        continue
      stations.append(n.nodes[mid])
    lines.append([rid, tags, stations])

  # write template
  tpl = Template(filename='templates/map.tpl', default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace', lookup=makolookup)
  content = tpl.render(lines=lines, mtime=n.mtime, profile=p, mapkey=mapkey)
  f = open(context.output_file_path(p, '_map_' + mapkey), 'w')
  f.write(content.decode('utf-8'))
  f.close()

def count_member_types(relation):
  # count how many members of each type the relation has
  rid, tags, members = relation
  types = {'relation': 0, 'node': 0, 'way': 0}
  for member in members:
    mid, typ, role = member
    types[typ] += 1
  return types

def get_sortkey(relation):
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
