#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rn
import rvoc

class Hiking(rn.RouteNetwork, rvoc.RelationValidationOverviewCreator):

	def __init__(self):
		self.show_additional_tags = ['network', 'ref', 'name', 'osmc:symbol']

