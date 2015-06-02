.PHONY: clean clean-build clean-docs clean-pyc docs

help:
	@echo "clean - remove all coverage, build, docs, test and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-docs - remove docs artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "dist - package"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "install - install the package to the active Python's site-packages"
	@echo "lint - check style with flake8"
	@echo "release - package and upload a release"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"

clean: clean-build clean-docs clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-docs:
	rm -f docs/mul.rst
	rm -f docs/mul.recipe.rst
	rm -f docs/mul.recipe.appengine.rst
	rm -f docs/modules.rst

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 -v mul tests

test:
	python setup.py test

test-all:
	tox

coverage:
	coverage run --source mul.recipe.appengine setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs: clean-docs
	sphinx-apidoc -o docs/ mul
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install
