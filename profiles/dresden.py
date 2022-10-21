from profiles.base.public_transport import PublicTransportProfile
import validation
import filters

class DresdenProfile(PublicTransportProfile):

  name = 'dresden'

  label = 'Dresden (DVB)'

  overpass_query = """
    <union>
      <query type="relation">
        <has-kv k="type" v="route_master"/>
        <has-kv k="operator" v="DVB"/>
      </query>
      <query type="relation">
        <has-kv k="type" v="route"/>
        <has-kv k="operator" v="DVB"/>
      </query>
      <recurse type="down"/>
    </union>
    <print />
  """
  
  filter_text = 'All route and route_master relations with operator=DVB'

  @staticmethod
  def filter(r):
    return \
        "operator" in r[1] and (r[1]["operator"] == "DVB") and \
        "type" in r[1] and r[1]["type"] in ["route", "route_master"]

  route_validators = [
    validation.relation_route_basics,
    validation.relation_colour,
    validation.relation_stops_in_ways,
    validation.RelationNameRegexp("^(Bus|Tram|alita) "),
  ]

  route_master_validators = [
    validation.relation_route_master_basics,
    validation.RelationNameRegexp("^(Bus|Tram|alita) "),
    validation.relation_colour,
  ]

  stopplan = True

  maps = {
       # 'internal name': ('readable name', filter function)
       'strassenbahn': (u"Straßenbahn", filters.is_tram),
       'bus': ("Bus", filters.is_bus),
  }
