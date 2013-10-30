#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import osmconfig as config

from mako.template import Template

def print_available_profiles():
	print "Available profiles:"
	print "\n".join(config.profiles.keys())

def main():

	if len(sys.argv) > 2:
		print "Usage: %s [profilename]" % sys.argv[0]
		print_available_profiles()
		return

	if len(sys.argv) == 2:
		if sys.argv[1] == "index":
			generate_index()
			return
		else:
			# generate specific profile
			if sys.argv[1] not in config.profiles:
				print 'Unknown profile "%s".' % sys.argv[1]
				print_available_profiles()
				return
			generate_profile(config.profiles[sys.argv[1]])
	else:
		print "Generating index and all profiles..."
		generate_index()
		for profile_name in config.profiles.keys():
			print "Generating profile \"%s\"..." % profile_name
			generate_profile(config.profiles[profile_name])

def generate_index():
		# write template
		tpl = Template(filename=config.template_dir + "/index.tpl", default_filters=['decode.utf8'], input_encoding='utf-8', output_encoding='utf-8', encoding_errors='replace')
		content = tpl.render(profiles=config.profiles)
		f = open(config.output_dir + "/index.htm", 'w')
		f.write(content)
		f.close()

def generate_profile(profile):
	rn = profile['rules']()
	rn.profile = profile

	# load data
	datasources = [profile['datasource']] if type(profile['datasource']) == str else profile['datasource']
	for filename in datasources:
		# TODO: check if mixing sources (e.g. berlin + brandenburg) works (data consistency...)
		rn.load_network(pbf=config.data_dir + "/" + filename, \
				filterfunction=profile['filter'])

	rn.create_relation_overview(template=config.template_dir + "/relations.tpl", \
			output=config.output_dir + ("/%s.htm" % profile['shortname']))

	# create stop plan
	if profile['stopplan']:
		rn.create_route_list(template=config.template_dir + "/routes.tpl",
				output=config.output_dir + ("/%s_lines.htm" % profile['shortname']))

	# create maps
	for m in profile['maps']:
		print "Creating map %s..." % m
		rn.create_network_map(template=config.template_dir + "/map.tpl", \
				output=config.output_dir + ("/%s_map_%s.htm" % (profile['shortname'], m)), \
				filterfunction=profile['maps'][m][1], \
				mapkey=m)
	del rn

if __name__ == "__main__":
	main()

