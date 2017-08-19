clean:
	@truncate --size 0 list-songs.csv
	@rm -rf src/cache/**/*

setup:
	@pip3 install -U -r requirements.txt

run: clean
	@python3 src/main.py