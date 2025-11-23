SYNC_TARGET="user1@k:osm_oepnv_validator/"
SYNC_TARGET_PUBLIC="user1@k:htdocs/osm.kesto.de/routes/"

# Crontab entry:
# 23 5 * * 1 /var/www/user1/osm_oepnv_validator/generate.py --data /var/www/user1/osm_oepnv_validator/data --output /var/www/user1/htdocs/osm.kesto.de/routes --download > /dev/null
#
# Note: data dir has to be created before first call

all:

sync:
	rsync -av --delete --exclude="data" --exclude="output/*.htm" --exclude=".git" --exclude="__pycache__" --exclude=".vscode" ./ "$(SYNC_TARGET)"
	rsync -av --delete --exclude="*.htm" --exclude=".git" ./output/ "$(SYNC_TARGET_PUBLIC)"

