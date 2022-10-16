#!/bin/sh

# get current data
/usr/bin/python3 /var/www/user1/osm_oepnv_validator/fetch_overpass_data.py /var/www/user1/osm_oepnv_validator/overpass_queries /var/www/user1/osm_oepnv_validator/data

# generate everything
/usr/bin/python3 /var/www/user1/osm_oepnv_validator/generate.py

