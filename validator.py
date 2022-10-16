from profile import PublicTransportProfile
from typing import Type
from network import RouteNetwork

class Validator():

  def __init__(self, n: Type[RouteNetwork], p: Type[PublicTransportProfile]):
    self.n = n
    self.p = p

  def validate_all(self):
    # validate all relations of network
    errors = {}
    for rid in self.n.relations:
      errors[rid] = self.validate_relation(self.n.relations[rid])
    return errors

  def validate_relation(self, relation):
    # validate passed route/route_master

    rid, tags, members = relation
    errors = []

    if self.p.ignore_relation(relation):
      return [("ignored", "(ignoring this relation)")]

    # do validation depending on type of route 
    if "type" not in tags:
      return [("missing_type", "missing type=(route_master|route)")]
    if tags["type"] == "route_master":
      errors.extend(self.validate_route_master(relation))
    if tags["type"] == "route":
      errors.extend(self.validate_route(relation))

    return set(errors)

  def validate_route_master(self, relation):
    errors = []
    # run validators defined by child-class
    for v in self.p.route_master_validators:
      errors.extend(v(self.p, self.n, relation))
    return errors

  def validate_route(self, relation):
    errors = []
    # run validators defined by child-class
    for v in self.p.route_validators:
      errors.extend(v(self.p, self.n, relation))
    return errors
