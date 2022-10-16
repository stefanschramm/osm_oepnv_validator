import profile
import validation
import filters

class HalleProfile(profile.PublicTransportProfile):
  name = 'halle'
  label = 'Halle (HAVAG)'
  overpass_query = """
    <union>
      <query type="relation">
        <has-kv k="type" v="route_master"/>
        <has-kv k="operator" v="HAVAG"/>
      </query>
      <query type="relation">
        <has-kv k="type" v="route"/>
        <has-kv k="operator" v="HAVAG"/>
      </query>
      <recurse type="down"/>
    </union>
    <print />
  """
  filter_text = 'All route and route_master relations with operator=HAVAG'
  filter = lambda r: "operator" in r[1] \
        and (r[1]["operator"] == "HAVAG") \
        and "type" in r[1] \
        and r[1]["type"] in ["route", "route_master"]
  def ignore_relation(relation):
      rid, tags, members = relation
      # don't try to validate "Straßenbahnnetz Halle" relation
      return rid in [8659225]
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
  maps = {
       # 'internal name': ('readable name', filter function)
       'strassenbahn': (u"Straßenbahn", filters.is_tram),
       'bus': ("Bus", filters.is_bus),
  }


