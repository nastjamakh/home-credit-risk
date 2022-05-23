#PYTHON_INTERPRETER = {{ cookiecutter.python_interpreter }}
#SHELL = {{ cookiecutter.shell_environment }}
PROJECT_NAME = "home-credit-risk"

PYTHON_INTERPRETER = python3
SHELL = zsh
PROJECT_NAME = "home-credit-risk"

setup_dev:
	/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

setup_local:
	make setup_dev
	make setup_pyenv
	make create_env
	pip install poetry
	poetry install
	pip install wheel
	poetry add `cat requirements.txt`

setup_docker:
	make setup_dev
	./bin/docker-exec.sh poetry install
	./bin/docker-exec.sh poetry add `cat requirements.txt`

## Set up python interpreter environment
setup_pyenv:
	brew install zsh
	brew install openssl readline sqlite3 xz zlib
	brew install pyenv pyenv-virtualenv
	echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
	echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
	echo 'eval "$(pyenv init -)"' >> ~/.zshrc
	pyenv install 3.10.4

create_env:
	pyenv virtualenv 3.10.4 $(PROJECT_NAME)
	pyenv local $(PROJECT_NAME)
	@echo ">>> New pyenv virtualenv created. Activate with:pyenv local $(PROJECT_NAME)"

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

notebook:
	./bin/notebook-start.sh

# code
lint:
	./bin/docker-exec.sh poetry run black -- bin src && poetry run flake8 --max-line-length=90 && poetry run mypy  --follow-imports=skip --ignore-missing-imports --disallow-untyped-defs -- src

test:
	./bin/docker-exec.sh poetry run pytest -s

server:
	./bin/docker-exec.sh ./bin/webserver-start.sh

train:
	./bin/docker-exec.sh poetry run train train --to_s3=$(to_s3)

