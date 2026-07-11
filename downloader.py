import requests
import context
import time

from profiles.base.public_transport import PublicTransportProfile

def download_data(p: PublicTransportProfile):
  retry = 0
  while retry < 3:
    r = requests.post(
      "http://overpass-api.de/api/interpreter",
      data={"data": p.overpass_query},
      headers={
        "user-agent": "osm_oepnv_validator",
        "referer": "http://osm.kesto.de/routes/",
        "accept": "*/*",
      },
    )
    if not r.ok:
      if r.status_code == 429:
        retry += 1
        time.sleep(30 * retry)
        continue
      else:
        raise Exception("Error while downloading data: %s" % r.status_code)

    f = open(context.data_file_path(p), 'w')
    f.write(r.text)
    f.close()
    return
  raise Exception("Server was too busy")
