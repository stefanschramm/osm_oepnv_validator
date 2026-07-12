from profiles.base.public_transport import PublicTransportProfile
import validation
import filters
import re

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

class HamburgProfile(PublicTransportProfile):

  name = 'hamburg'

  label = 'Hamburg (HVV)'

  overpass_query = """
    <union>
      <query type="relation">
        <has-kv k="type" v="route_master"/>
        <has-kv k="network" v="Hamburger Verkehrsverbund"/>
      </query>
      <query type="relation">
        <has-kv k="type" v="route"/>
        <has-kv k="network" v="Hamburger Verkehrsverbund"/>
      </query>
      <recurse type="down"/>
    </union>
    <print />
  """
  
  filter_text = 'All route and route_master relations with network=Hamburger Verkehrsverbund'

  @staticmethod
  def filter(r):
    return \
        "network" in r[1] and (r[1]["network"] == "Hamburger Verkehrsverbund") and \
        "type" in r[1] and r[1]["type"] in ["route", "route_master"]

  name_regexp = "^(S[0-9]:|U[0-9]:|A[13]:|Fähre [0-9]+:|XpressBus X[0-9]+:|MetroBus [0-9]:|Bus [0-9]+:|) "

  route_validators = [
    validation.relation_route_basics,
    # colour is currently mix of named colors and hexadecimal values
    # validation.relation_colour,
    validation.relation_stops_in_ways,
    validation.RelationNameRegexp(name_regexp),
  ]

  route_master_validators = [
    validation.relation_route_master_basics,
    validation.RelationNameRegexp(name_regexp),
    # colour is currently mix of named colors and hexadecimal values
    # validation.relation_colour,
  ]

  stopplan = True

  maps = {
        # 'internal name': ('readable name', filter function)
        'sunetz': ("S+U-Bahn", is_s_or_u_bahn),
        'bus': ("Bus", filters.is_bus),
        'faehre': ("Fähre", filters.is_ferry),
  }
