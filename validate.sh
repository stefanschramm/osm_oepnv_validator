#!/bin/sh

# get current data
# wget -q http://download.geofabrik.de/openstreetmap/europe/germany/berlin.osm.pbf -O /var/www/user1/osm_oepnv_validator/data/berlin.osm.pbf
/usr/bin/python /var/www/user1/osm_oepnv_validator/fetch_overpass_data.py /var/www/user1/osm_oepnv_validator/overpass_queries /var/www/user1/osm_oepnv_validator/data

# generate everything
#/var/www/user1/osm_oepnv_validator/python_env/bin/python /var/www/user1/osm_oepnv_validator/generate.py
/usr/bin/python /var/www/user1/osm_oepnv_validator/generate.py

