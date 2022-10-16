import profile
import validation
import filters

class BraunschweigProfile(profile.PublicTransportProfile):
  route_validators = [
    validation.relation_route_basics,
    validation.relation_colour,
    validation.relation_stops_in_ways,
    validation.RelationNameRegexp("^(Bus|Tram) "),
  ]
  route_master_validators = [
    validation.relation_route_master_basics,
    validation.RelationNameRegexp("^(Bus|Tram) "),
    validation.relation_colour,
  ]
  stopplan = True

class BraunschweigOepnvProfile(BraunschweigProfile):
  name = 'braunschweig_oepnv'
  label = 'Braunschweiger Verkehrs-GmbH'
  overpass_query = """
    <union>
      <query type="relation">
        <has-kv k="type" v="route_master"/>
        <has-kv k="operator" v="Braunschweiger Verkehrs-GmbH"/>
      </query>
      <query type="relation">
        <has-kv k="type" v="route"/>
        <has-kv k="operator" v="Braunschweiger Verkehrs-GmbH"/>
      </query>
      <recurse type="down"/>
    </union>
    <print />
  """
  filter_text = 'All route and route_master relations with operator=Braunschweiger Verkehrs-GmbH'
  filter = lambda r: "operator" in r[1] \
        and (r[1]["operator"] == "Braunschweiger Verkehrs-GmbH") \
        and "type" in r[1] \
        and r[1]["type"] in ["route", "route_master"]
  maps = {
       # 'internal name': ('readable name', filter function)
       'strassenbahn': (u"Straßenbahn", filters.is_tram),
       'bus': ("Bus", filters.is_bus),
  }

class BraunschweigVrbProfile(BraunschweigProfile):
  name = 'braunschweig_vrb'
  label = 'Braunschweig - VRB'
  overpass_query = """
    <union>
      <query type="relation">
        <has-kv k="type" v="route_master"/>
        <has-kv k="network" v="VRB"/>
      </query>
      <query type="relation">
        <has-kv k="type" v="route"/>
        <has-kv k="network" v="VRB"/>
      </query>
      <recurse type="down"/>
    </union>
    <print />
  """
  filter_text = 'All route and route_master relations with network=VRB'
  filter = lambda r: "network" in r[1] \
        and r[1]["network"] == "VRB" \
        and "type" in r[1] \
        and r[1]["type"] in ["route", "route_master"]
  maps = {
    # 'internal name': ('readable name', filter function)
    'all': (u"all routes", lambda r: True)
  }
