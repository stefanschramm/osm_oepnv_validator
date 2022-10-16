import requests
import context
from typing import Type

from profile import PublicTransportProfile

def download_data(p: Type[PublicTransportProfile]):
  r = requests.post("http://overpass-api.de/api/interpreter", data={"data": p.overpass_query})

  f = open(context.data_file_path(p), 'w')
  f.write(r.text)
  f.close()
