install:
	./bin/docker-exec.sh poetry install

build:
	./bin/docker-build.sh

start:
	./bin/docker-start.sh

stop:
	./bin/docker-remove.sh

lint:
	poetry run black -- bin src && poetry run flake8

test:
	./bin/docker-exec.sh poetry run pytest -s

server:
	./bin/docker-exec.sh ./bin/webserver-start.sh
