all:

deploy:
	rsync -av --delete --exclude="data" --exclude="output/*.htm" --exclude=".git" --exclude="__pycache__" --exclude=".vscode" ./ user1@t:/var/www/user1/osm_oepnv_validator/
	rsync -av --delete --exclude="*.htm" --exclude=".git" ./output/ user1@t:/var/www/user1/htdocs/osm.kesto.de/routes/
