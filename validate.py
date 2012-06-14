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
		net.create_report(pbf=sys.argv[1], template=sys.argv[2], output=sys.argv[3])
	else:
		net.create_report(pbf="berlin.osm.pbf", template="template.tpl", output="berlin.htm")
	#net = PublicTransportNetworkHamburg()
	#net.create_report(pbf="hamburg.osm.pbf", template="template.tpl", output="hamburg.htm")
	#net = PublicTransportNetworkDresden()
	#net.create_report(pbf="sachsen.osm.pbf", template="template.tpl", output="dresden.htm")
	#net = PublicTransportNetworkLeipzig()
	#net.create_report(pbf="sachsen.osm.pbf", template="template.tpl", output="leipzig.htm")

if __name__ == '__main__':
	main()

