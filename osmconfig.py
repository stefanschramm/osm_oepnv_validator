#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import rulesets.publictransport
import rulesets.berlin
import rulesets.braunschweig
import rulesets.hiking
import rulesets.bicycle
import rulesets.power
import rulesets.other

script_path = os.path.dirname(__file__)

output_dir = script_path + "/output"
#output_dir = "/var/www/user1/htdocs/osm.kesto.de/routes"
data_dir = script_path + "/data"
template_dir = script_path + "/templates"

profiles = {
  'braunschweig_oepnv': {
    'shortname': 'braunschweig_oepnv',
    'name': u"Braunschweiger Verkehrs-GmbH",
    'rules': rulesets.braunschweig.PublicTransportBraunschweig,
    'filter': lambda r: "operator" in r[1] \
        and (r[1]["operator"] == "Braunschweiger Verkehrs-GmbH") \
        and "type" in r[1] \
        and r[1]["type"] in ["route", "route_master"],
    'filter_text': 'All route and route_master relations with operator=Braunschweiger Verkehrs-GmbH',
    'datasource': 'braunschweig.overpass.xml',
    'stopplan': True,
    'maps': {
      # 'internal name': ('readable name', filter function)
      'strassenbahn': (u"Straßenbahn", rulesets.publictransport.is_tram),
      'bus': ("Bus", rulesets.publictransport.is_bus)
    }
  },
  'braunschweig_vrb': {
    'shortname': 'braunschweig_vrb',
    'name': u"Braunschweig - VRB",
    'rules': rulesets.braunschweig.PublicTransportBraunschweig,
    'filter': lambda r: "network" in r[1] \
        and r[1]["network"] == "VRB" \
        and "type" in r[1] \
        and r[1]["type"] in ["route", "route_master"],
    'filter_text': 'All route and route_master relations with network=VRB',
    'datasource': 'vrb.overpass.xml',
    'stopplan': True,
    'maps': {
      # 'internal name': ('readable name', filter function)
      'all': (u"all routes", lambda r: True)
    }
  },
  'berlin_oepnv': {
    'shortname': 'berlin_oepnv',
    'name': u"Berlin: ÖPNV (only BVG and S-Bahn Berlin GmbH)",
    'rules': rulesets.berlin.PublicTransportBerlin,
    'filter': lambda r: "network" in r[1] \
        and (r[1]["network"] in ["Verkehrsverbund Berlin-Brandenburg", "VBB"]) \
        and "operator" in r[1] \
        and (r[1]["operator"] in ["BVG", "S-Bahn Berlin GmbH", "Berliner Verkehrsbetriebe"]) \
        and "type" in r[1] \
        and r[1]["type"] in ["route", "route_master"],
    'filter_text': 'All route and route_master relations with network=VBB and (operator=BVG or operator=S-Bahn Berlin GmbH)',
    'datasource': 'vbb.overpass.xml',
    'stopplan': True,
    'maps': {
      # 'internal name': ('readable name', filter function)
      'sunetz': ("S+U-Bahn", rulesets.berlin.is_s_or_u_bahn),
      'strassenbahn': (u"Straßenbahn (no MetroTram)", rulesets.berlin.is_normal_tram),
      'metrotram': ("MetroTram", rulesets.berlin.is_metro_tram),
      'bus': ("Bus (no Metro- or ExpressBus)", rulesets.berlin.is_normal_bus),
      'metrobus': ("MetroBus", rulesets.berlin.is_metro_bus),
      'expressbus': ("ExpressBus", rulesets.berlin.is_express_bus)
    }
  },
  'berlinbrandenburg_vbb': {
    'shortname': 'berlinbrandenburg_vbb',
    'name': u"Berlin/Brandenburg: VBB (excluding BVG and S-Bahn Berlin GmbH)",
    'rules': rulesets.publictransport.PublicTransport,
    'filter': lambda r: \
        "network" in r[1] \
        and (r[1]["network"] == "Verkehrsverbund Berlin-Brandenburg" or r[1]["network"] == "VBB") \
        and "type" in r[1] \
        and r[1]["type"] in ["route", "route_master"]
        and (not "operator" in r[1] or r[1]["operator"] not in ["BVG", "S-Bahn Berlin GmbH"]),
    'datasource': 'vbb.overpass.xml',
    'stopplan': True,
    'maps': {
      'all': ("alle Linien", lambda r: True)
    }
  },
#  'berlin_bicycle': {
#    'shortname': 'berlin_bicycle',
#    'name': 'Berlin: Bicycle Routes',
#    'rules': rulesets.bicycle.Bicycle,
#    'filter': lambda r: "type" in r[1] \
#        and r[1]["type"] in ["route", "route_master"] \
#        and (("route" in r[1] and r[1]["route"] == "bicycle") \
#        or ("route_master" in r[1] and r[1]["route_master"] == "bicycle")),
#    'datasource': 'berlin.osm.pbf',
#    'stopplan': False,
#    'maps': {}
#  },
#  'berlin_hiking': {
#    'shortname': 'berlin_hiking',
#    'name': 'Berlin: Hiking Routes',
#    'rules': rulesets.hiking.Hiking,
#    'filter': lambda r: "type" in r[1] \
#        and r[1]["type"] in ["route", "route_master"] \
#        and (("route" in r[1] and r[1]["route"] == "hiking") \
#        or ("route_master" in r[1] and r[1]["route_master"] == "hiking")),
#    'datasource': 'berlin.osm.pbf',
#    'stopplan': False,
#    'maps': {}
#  },
#  'berlin_power': {
#    'shortname': 'berlin_power',
#    'name': 'Berlin: Powerlines',
#    'rules': rulesets.power.Power,
#    'filter': lambda r: "type" in r[1] \
#        and r[1]["type"] in ["route", "route_master"] \
#        and (("route" in r[1] and r[1]["route"] == "power") \
#        or ("route_master" in r[1] and r[1]["route_master"] == "power")),
#    'datasource': 'berlin.osm.pbf',
#    'stopplan': False,
#    'maps': {
#      'all': ("alle Leitungen", lambda r: True)
#    }
#  },
#  'berlin_other': {
#    'shortname': 'berlin_other',
#    'name': 'Berlin: other (no VBB, no hiking routes, no bicycle routes, no powerlines)',
#    'rules': rulesets.other.Other,
#    'filter': lambda r: ("network" not in r[1] \
#        or r[1]["network"] != "VBB") \
#        and "type" in r[1] \
#        and r[1]["type"] in ["route", "route_master"] \
#        and not( \
#          (("route" in r[1] and r[1]["route"] in ["hiking", "bicycle", "power"]) \
#          or ("route_master" in r[1] and r[1]["route_master"] in ["hiking", "bicycle", "power"]))
#        ),
#    'datasource': 'berlin.osm.pbf',
#    'stopplan': False,
#    'maps': {}
#  }
#  'germany_ice': {
#    'shortname': 'germany_ice',
#    'name': 'Germany: ICE-Routes',
#    'rules': rulesets.berlin.PublicTransportBerlin,
#    'filter': lambda r: "type" in r[1] \
#        and r[1]["type"] in ["route", "route_master"] \
#        and "network" in r[1] and r[1]["network"] in ["DB", "DB-ICE", "DB Fernverkehr"],
#    'datasource': 'germany.osm.pbf',
#    'stopplan': True,
#    'maps': {
#      'all': ("alle Linien", lambda r: True)
#    }
#  }
#  'germany_power': {
#    'shortname': 'germany_power',
#    'name': 'Germany: Powerlines',
#    'rules': rulesets.power.Power,
#    'filter': lambda r: "type" in r[1] \
#        and r[1]["type"] in ["route", "route_master"] \
#        and (("route" in r[1] and r[1]["route"] == "power") \
#        or ("route_master" in r[1] and r[1]["route_master"] == "power")),
#    'datasource': 'germany.osm.pbf',
#    'stopplan': False,
#    'maps': {}
#  }
}

