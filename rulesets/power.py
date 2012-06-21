#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rn
import rvoc
import rmcw

class Power(rn.RouteNetwork, rvoc.RelationValidationOverviewCreator, rmcw.RouteMapCreatorByWays):

	def __init__(self):
		rn.RouteNetwork.__init__(self)
		rvoc.RelationValidationOverviewCreator.__init__(self)
		self.show_additional_tags = ['network', 'operator', 'ref', 'name', 'voltage', 'frequency', 'cables', 'wires']

