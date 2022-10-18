import validation
import re

from network import RouteNetwork
from profiles.base.public_transport import PublicTransportProfile

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

def validate_name(p: PublicTransportProfile, n: RouteNetwork, relation):
  rid, tags, members = relation

  if "type" not in tags or tags["type"] not in ["route", "route_master"]:
    return []
  key = tags["type"]

  if key not in tags:
    return []

  if "name" not in tags:
    return []

  if tags[key] == "bus" and not re.match("^Bus ", tags["name"]):
      return [("wrong_name", u'name does not match convention ("Bus ...")')]
  if tags[key] == "ferry" and not re.match(u"^Fähre ", tags["name"]):
      return [("wrong_name", u'name does not match convention ("Fähre ...")')]
  if tags[key] == "tram" and not re.match(u"^Tram ", tags["name"]):
      return [("wrong_name", u'name does not match convention ("Tram ...")')]
  if tags[key] == "subway" and not re.match(u"^U[0-9]+: ", tags["name"]):
      return [("wrong_name", u'name does not match convention ("Un: ...")')]
  if tags[key] == "light_rail" and not re.match(u"^S-Bahnlinie ", tags["name"]):
      return [("wrong_name", u'name does not match convention ("U-Bahnlinie ...")')]

  return []

def validate_colour(p: PublicTransportProfile, n: RouteNetwork, relation):
  rid, tags, members = relation

  if "type" not in tags or tags["type"] not in ["route", "route_master"]:
    return []
  key = tags["type"]

  if key not in tags:
    return []

  if tags[key] in ["subway", "tram", "light_rail"] and "colour" not in tags:
    return [("no_colour", 'missing colour=#... for %s' % tags[key])]

  if "colour" in tags and not re.match("^#[a-fA-F0-9]{6}$", tags["colour"]):
    return [("wrong_colour", 'colour should be specified as hexadecimal value like #ff0000')]

  return []

class BerlinOepnvProfile(PublicTransportProfile):

  name = 'berlin_oepnv'

  label = 'Berlin: ÖPNV (only BVG and S-Bahn Berlin GmbH)'
  
  overpass_query = """
    <union>
      <query type="relation">
        <has-kv k="type" v="route_master"/>
        <has-kv k="network" regv="VBB|Verkehrsverbund Berlin-Brandenburg"/>
      </query>
      <query type="relation">
        <has-kv k="type" v="route"/>
        <has-kv k="network" regv="VBB|Verkehrsverbund Berlin-Brandenburg"/>
      </query>
      <recurse type="down"/>
    </union>
    <print />
  """

  filter_text = 'All route and route_master relations with network=VBB and (operator=BVG or operator=S-Bahn Berlin GmbH)'

  @staticmethod
  def filter(r):
    return "network" in r[1] \
        and (r[1]["network"] in ["Verkehrsverbund Berlin-Brandenburg", "VBB"]) \
        and "operator" in r[1] \
        and (r[1]["operator"] in ["BVG", "S-Bahn Berlin GmbH", "Berliner Verkehrsbetriebe"]) \
        and "type" in r[1] \
        and r[1]["type"] in ["route", "route_master"]

  @staticmethod
  def ignore_relation(relation):
      rid, tags, members = relation
      # don't try to validate "...linien in Berlin"-relations
      return rid in [18812, 174283, 53181, 174255, 18813]

  route_validators = [
    validation.relation_route_basics,
    validation.relation_stops_in_ways,
    validate_colour,
    validate_name,
  ]

  route_master_validators = [
    validation.relation_route_master_basics,
    validate_name,
    validate_colour,
  ]

  stopplan = True

  maps = {
      # 'internal name': ('readable name', filter function)
      'sunetz': ("S+U-Bahn", is_s_or_u_bahn),
      'strassenbahn': (u"Straßenbahn (no MetroTram)", is_normal_tram),
      'metrotram': ("MetroTram", is_metro_tram),
      'bus': ("Bus (no Metro- or ExpressBus)", is_normal_bus),
      'metrobus': ("MetroBus", is_metro_bus),
      'expressbus': ("ExpressBus", is_express_bus)
    }


# TODO: uses same dataset as berlin
# 'berlinbrandenburg_vbb': {
#   'shortname': 'berlinbrandenburg_vbb',
#   'name': u"Berlin/Brandenburg: VBB (excluding BVG and S-Bahn Berlin GmbH)",
#   'rules': rulesets.publictransport.PublicTransport,
#   'filter': lambda r: \
#       "network" in r[1] \
#       and (r[1]["network"] == "Verkehrsverbund Berlin-Brandenburg" or r[1]["network"] == "VBB") \
#       and "type" in r[1] \
#       and r[1]["type"] in ["route", "route_master"]
#       and (not "operator" in r[1] or r[1]["operator"] not in ["BVG", "S-Bahn Berlin GmbH"]),
#   'datasource': 'vbb.overpass.xml',
#   'stopplan': True,
#   'maps': {
#     'all': ("alle Linien", lambda r: True)
#   }
# },