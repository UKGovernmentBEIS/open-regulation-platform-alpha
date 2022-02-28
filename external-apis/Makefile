PYTHON=python3.8
DJANGO_MANAGE=src/orp_apps/manage.py
DJANGO_SRC=src/orp_apps

ENV_DIR=.env_$(PYTHON)

WITH_CONTEXT=export DJANGO_SQLITE_PATH=orp_apps_proj.sqlite && export DJANGO_SETTINGS_MODULE=orp_apps.settings.settings &&
TEST_CONTEXT=export PYTHONUTF8=1 && export DJANGO_SETTINGS_MODULE=tests.settings &&
ifeq ($(OS),Windows_NT)
	IN_ENV=. $(ENV_DIR)/Scripts/activate &&
else
	IN_ENV=. $(ENV_DIR)/bin/activate &&
endif

all: test docs artifacts

env: $(ENV_DIR)

shell:
	$(IN_ENV) pip install ipython
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) shell

test: build_test plain-test

plain-test: plain-lint
	$(IN_ENV) $(TEST_CONTEXT) pytest -n auto -vv

artifacts: build_reqs rpm sdist

$(ENV_DIR):
	virtualenv -p $(PYTHON) $(ENV_DIR)

build_reqs: env
	$(IN_ENV) pip install $(PIP_REPO_CONF) sphinx

build_test: build
	$(IN_ENV) pip install --pre $(PIP_REPO_CONF) --editable .[testing]

build: build_reqs
	$(IN_ENV) pip install $(PIP_REPO_CONF) --editable .

sdist: build_reqs
	$(IN_ENV) python setup.py sdist

rpm: build_reqs
	$(IN_ENV) rpmbuild --define 'dist .el7' --define '_topdir '`pwd` -bb SPECS/*.spec

lint: build plain-lint

plain-lint:
	$(IN_ENV) pydocstyle $(DJANGO_SRC)
	$(IN_ENV) isort $(DJANGO_SRC) tests
	$(IN_ENV) unify -i -r $(DJANGO_SRC) tests
	$(IN_ENV) flake8 $(DJANGO_SRC) tests

docs: build_reqs
	$(IN_ENV) pip install -r docs/requirements.txt
	$(IN_ENV) $(MAKE) -C docs html

serve: build plain-serve

migrations:
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) makemigrations --noinput
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) migrate --noinput

plain-serve: migrations
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) runserver

flush:
	$(IN_ENV) $(WITH_CONTEXT) python $(DJANGO_MANAGE) flush --noinput

freeze: env
	- $(IN_ENV) pip freeze

clean:
	- @rm -rf BUILD
	- @rm -rf BUILDROOT
	- @rm -rf RPMS
	- @rm -rf SRPMS
	- @rm -rf SOURCES
	- @rm -rf docs/build
	- @rm -rf src/*.egg-info
	- @rm -rf build
	- @rm -rf dist
	- @rm -f .coverage
	- @rm -f test_results.xml
	- @rm -f coverage.xml
	- @find ./src ./docs -name '*.pyc' | xargs -r rm

env_clean: clean
	- @rm -rf $(ENV_DIR)
