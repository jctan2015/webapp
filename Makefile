run:
	python3 server.py

push:
	git add .
	git commit -m "Update"
	git push

history:
	git log --pretty=format:"%h %ad | %s" --date=short

revert-js:
	cp js/script.backup.js js/script.js
