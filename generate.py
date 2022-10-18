#!/usr/bin/env python

import os
import argparse

import context
import network
import profile_repository
import downloader
import generators

def main():

  parser = argparse.ArgumentParser(description='Generate OSM relation overviews', allow_abbrev=False, epilog='In case no specific profile is specified, all available profiles including an index will be generated.')
  parser.add_argument('--profile', help='name of profile to generate (skip to generate all profiles)')
  parser.add_argument('--data', help='directory to use to store data')
  parser.add_argument('--output', help='directory to use to store output (overviews/reports)')
  args = parser.parse_args()

  if args.data != None:
    context.set_data_dir(args.data)
  
  if args.output != None:
    context.set_output_dir(args.output)

  if args.profile != None:
    # single profile
    p = profile_repository.get_profile(args.profile)
    if p == None:
      print('Profile %s not found' % args.profile)
      print("Available profiles:")
      print("\n".join(profile_repository.get_profile_names()))
      return
    generate_profile(p)
  else:
    # generate all profiles including index
    print('Generating index...')
    profiles = profile_repository.get_profiles()
    generators.generate_index(profiles)
    for p in profiles:
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
