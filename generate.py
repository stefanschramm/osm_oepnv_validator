#!/usr/bin/env python

import os
import sys
from re import I

import context
import network
import profile_repository
import downloader
import generators

def main():
  
  profiles = profile_repository.get_profiles()

  if len(sys.argv) > 2:
    print("Usage: %s [profilename]" % sys.argv[0])
    print("Available profiles:")
    print("\n".join(map(lambda p: p.name, profiles)))
    return
  
  if len(sys.argv) < 2 or sys.argv[1] == 'index':
    print('Generating index...')
    generators.generate_index(profiles)

  for p in profiles:
    if len(sys.argv) == 2 and sys.argv[1] != p.name:
      continue
    generate_profile(p)

def generate_profile(p):
  print('Generating profile %s...' % p.name)
  if not os.path.isfile(context.data_file_path(p)):
    print('Downloading %s...' % p.name)
    downloader.download_data(p)

  print('Reading network %s...' % p.name)
  n = network.create_from_profile(p)
  
  print('Generating relation overview %s...' % p.name)
  generators.generate_relation_overview(n, p)

  if p.stopplan:
    generators.generate_stop_plan(n, p)

  for map in p.maps:
    print('Generating map %s_%s...' % (p.name, map))
    generators.generate_network_map(n, p, map)

if __name__ == '__main__':
  main()
