def is_bus(r):
  return (("route" in r[1] and r[1]["route"] == "bus") or \
      ("route_master" in r[1] and r[1]["route_master"] == "bus"))

def is_tram(r):
  return (("route" in r[1] and r[1]["route"] == "tram") or \
      ("route_master" in r[1] and r[1]["route_master"] == "tram"))