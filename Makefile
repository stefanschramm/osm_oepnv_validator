all:

deploy:
	rsync -av --delete --exclude="data" --exclude="output/*.htm" --exclude=".git" --exclude="__pycache__" --exclude=".vscode" ./ user1@t:/var/www/user1/osm_oepnv_validator/

