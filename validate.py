#!/usr/bin/env python
# -*- coding: utf-8 -*-

# validate.py - example how to generate public transport overviews.
#
# Copyright (C) 2012, Stefan Schramm <mail@stefanschramm.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import re
import os
import stat
import datetime
from berlin import PublicTransportNetworkBerlin
#from rostock import PublicTransportNetworkRostock
#from hamburg import PublicTransportNetworkHamburg
#from dresden import PublicTransportNetworkDresden
#from leipzig import PublicTransportNetworkLeipzig

# required dependencies:
# sudo apt-get install python-imposm
# sudo apt-get install python-mako
	
def main():
	net = PublicTransportNetworkBerlin()
	if len(sys.argv) == 4:
		net.load_network(pbf=sys.argv[1])
		net.create_report(template=sys.argv[2], output=sys.argv[3])
	else:
		net.load_network(pbf="berlin.osm.pbf")
		net.create_report(template="template.tpl", output="berlin.htm")

		# experimental: create html files containing an openlayers map of the network
		# net.draw_station_network()
		# draw tram network:
		# net.draw_station_network(filterfunction=lambda r: "route" in r[1] and r[1]["route"] == "tram" ,output="tram.htm")
		# draw M-bus network:
		# net.draw_station_network(filterfunction=lambda r: "route" in r[1] and r[1]["route"] == "bus" and "ref" in r[1] and re.match("^M[0-9]+$", r[1]["ref"]), output="mbus.htm")
		# net.draw_lines()

	# other regions - highly experimental
	# net = PublicTransportNetworkHamburg()
	# net.create_report(pbf="hamburg.osm.pbf", template="template.tpl", output="hamburg.htm")
	# net = PublicTransportNetworkDresden()
	# net.create_report(pbf="sachsen.osm.pbf", template="template.tpl", output="dresden.htm")
	# net = PublicTransportNetworkLeipzig()
	# net.create_report(pbf="sachsen.osm.pbf", template="template.tpl", output="leipzig.htm")

if __name__ == '__main__':
	main()

