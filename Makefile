# poetry
install:
	./bin/docker-exec.sh poetry install

poetry-add:
	./bin/docker-exec.sh poetry add $(package)

# images & containers
build:
	./bin/docker-build.sh

image-pull:
	./bin/docker-pull.sh

image-push:
	./bin/docker-push.sh

start:
	./bin/docker-start.sh

stop:
	./bin/docker-remove.sh

# code
lint:
	./bin/docker-exec.sh poetry run black -- bin src && poetry run flake8 --max-line-length=90 && poetry run mypy  --follow-imports=skip --ignore-missing-imports --disallow-untyped-defs -- src

test:
	./bin/docker-exec.sh poetry run pytest -s

server:
	./bin/docker-exec.sh ./bin/webserver-start.sh

train:
	./bin/docker-exec.sh poetry run train train to_s3=$(to_s3)

