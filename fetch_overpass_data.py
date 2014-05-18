#!/usr/bin/env python

import os
import httplib

query_dir = 'overpass_queries'
data_dir = 'data'

def main():

	for fn in os.listdir(query_dir):
		f = open(query_dir + os.sep + fn)
		query = f.read()
		f.close()

		c = httplib.HTTPConnection("overpass-api.de")
		c.request("POST", "/api/interpreter", "data=" + query)

		f = open(data_dir + os.sep + fn + ".xml", 'w')
		r = c.getresponse()
		f.write(r.read())
		f.close()

if __name__ == '__main__':
	main()
