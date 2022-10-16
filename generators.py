import context
import validator

import re

from profile import PublicTransportProfile
from typing import Type
from network import RouteNetwork

from mako.lookup import TemplateLookup
from mako.template import Template

show_additional_tags = ['ref', 'colour', 'name']

makolookup = TemplateLookup(directories=[context.template_dir])

def generate_index(profiles):
    # write template
    tpl = Template(filename='templates/index.tpl', default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace')
    content = tpl.render(profiles=profiles)
    f = open(context.output_dir + "/index.htm", 'w')
    f.write(content.decode('utf-8'))
    f.close()

def generate_relation_overview(n: Type[RouteNetwork], p: Type[PublicTransportProfile]):
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
      # TODO:
      # l['noroutemaster'] = self.no_route_master(relation)
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

def generate_stop_plan(n: Type[RouteNetwork], p: Type[PublicTransportProfile]):
  # TODO
  # - old rlc.RouteListCreator.create_route_list
  # - filename='templates/routes.tpl'
  # - context.output_file_path(p, '_lines')
  pass

def generate_network_map(n: Type[RouteNetwork], p: Type[PublicTransportProfile], mapkey):
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
