import requests
import context

from profiles.base.public_transport import PublicTransportProfile

def download_data(p: PublicTransportProfile):
  r = requests.post("http://overpass-api.de/api/interpreter", data={"data": p.overpass_query})

  f = open(context.data_file_path(p), 'w')
  f.write(r.text)
  f.close()
