#!/usr/bin/env python

import os
import requests
import sys
import time

query_dir = 'overpass_queries'
data_dir = 'data'

def main():

  query_dir = sys.argv[1]
  data_dir = sys.argv[2]

  for fn in os.listdir(query_dir):
    f = open(query_dir + os.sep + fn)
    query = f.read()
    f.close()

    r = requests.post("http://overpass-api.de/api/interpreter", data={"data": query})

    f = open(data_dir + os.sep + fn + ".xml", 'w')
    f.write(r.text)
    f.close()
    time.sleep(10)

if __name__ == '__main__':
  main()

