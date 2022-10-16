import profiles.braunschweig
import profiles.halle
import profiles.berlin

def get_profiles():
  return [
    profiles.braunschweig.BraunschweigOepnvProfile,
    profiles.braunschweig.BraunschweigVrbProfile,
    profiles.halle.HalleProfile,
    profiles.berlin.BerlinOepnvProfile,
  ]
