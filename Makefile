PACKAGE = $(python setup.py --name)

develop:
	@ python setup.py develop
	@ pip install -r requirements-develop.txt

clean:
	@ rm -rf .tox
	@ $(MAKE) -C tests clean
	@ python setup.py clean
	@ rm -rf *.egg-info .pytest_cache
	@ find . -name '*.pyc' | xargs rm
