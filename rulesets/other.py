#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rn
import rvoc

class Other(rn.RouteNetwork, rvoc.RelationValidationOverviewCreator):

	def __init__(self):
		rn.RouteNetwork.__init__(self)
		rvoc.RelationValidationOverviewCreator.__init__(self)
		self.show_additional_tags = ['network', 'operator', 'ref', 'name']

