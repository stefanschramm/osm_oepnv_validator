import profiles.braunschweig
import profiles.halle
import profiles.berlin

_profile_map = {}

profiles = [
  profiles.braunschweig.BraunschweigOepnvProfile,
  profiles.braunschweig.BraunschweigVrbProfile,
  profiles.halle.HalleProfile,
  profiles.berlin.BerlinOepnvProfile,
]

def _register_profiles(profiles):
  for p in profiles:
    _profile_map[p.name] = p

_register_profiles(profiles)


def get_profile(profile_name):
  return _profile_map[profile_name] if profile_name in _profile_map else None

def get_profile_names():
  return _profile_map.keys()

def get_profiles():
  return _profile_map.values()