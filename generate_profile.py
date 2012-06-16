#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import config

def print_available_profiles():
	print "Available profiles:"
	print "\n".join(config.profiles.keys())

def main():

	if len(sys.argv) != 2:
		print "Usage: %s profilename" % sys.argv[0]
		print_available_profiles()
		return

	profile_name = sys.argv[1]
	if profile_name not in config.profiles:
		print 'Unknown profile "%s".' % profile_name
		print_available_profiles()
		return

	profile = config.profiles[profile_name]

	ptn = profile['rules']()
	ptn.profile = profile

	# load data
	datasources = [profile['datasource']] if type(profile['datasource']) == str else profile['datasource']
	for filename in datasources:
		# TODO: check if mixing sources works (data consistency...)
		ptn.load_network(pbf=config.data_dir + "/" + filename, \
				filterfunction=profile['filter'])

	ptn.create_relation_overview(template=config.template_dir + "/mapper/relations.tpl", \
			output=config.output_dir + ("/%s.htm" % profile_name))

	ptn.create_route_list(template=config.template_dir + "/mapper/routes.tpl",
			output=config.output_dir + ("/%s_lines.htm" % profile_name))

	# create maps
	for m in profile['maps']:
		print "Creating map %s..." % m
		ptn.create_network_map(template=config.template_dir + "/mapper/map.tpl", \
				output=config.output_dir + ("/%s_map_%s.htm" % (profile_name, m)), \
				filterfunction=profile['maps'][m][1])

if __name__ == "__main__":
	main()

