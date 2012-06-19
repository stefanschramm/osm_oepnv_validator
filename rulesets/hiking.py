#!/usr/bin/env python
# -*- coding: utf-8 -*-

# berlin.py - validation rules for public transport in Berlin

import re

import rn
import rvoc

class Hiking(rn.RouteNetwork, rvoc.RelationValidationOverviewCreator):

	def __init__(self):

		#self.route_validators.append(self.validate_name)
		#self.route_master_validators.append(self.validate_name)
		#self.route_validators.append(self.check_color)
		#self.route_master_validators.append(self.check_color)

		# TODO: remove texts
		self.text_region = "..."
		self.text_filter = "..."
		self.text_datasource = "..."

		self.show_additional_tags = ['ref', 'name', 'osmc:symbol']

	def ignore_relation(self, relation):
		return False;

