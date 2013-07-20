PACKAGE=songprint



all: install

install: depends
	python setup.py install

depends: coverage
	pip install  --download-cache=/tmp/pip virtualenv epydoc nose pep8 pylint



##############################################################################
# issue: coverage results are incorrect in Linux
# tracker: https://bitbucket.org/ned/coveragepy/issue/164
# workaround: install the latest code from bitbucket.org until "coverage>3.6"
ifeq ($(shell uname),Linux)

coverage: /tmp/coveragepy
	cd /tmp/coveragepy; pip install --download-cache=/tmp/pip --requirement requirements.txt; python setup.py install

/tmp/coveragepy:
	cd /tmp; hg clone https://bitbucket.org/ned/coveragepy

else

coverage:
	pip install --download-cache=/tmp/pip coverage

endif
##############################################################################



##############################################################################
# issue: epydoc does not install a working CLI on Windows
# tracker: http://sourceforge.net/p/epydoc/bugs/345
# workaround: call the globally installed epydoc.py file directly
ifeq ($(OS),Windows_NT)

doc: install
	@echo WARNING: documentation cannot be created on Windows

else

doc: install
	export VV_NO_TEST_REPO=1; epydoc --config setup.cfg

endif
##############################################################################



test: install
	nosetests

check: install
	$(MAKE) doc
	pep8 --ignore=E501 veracity
	pylint veracity --include-ids yes --reports no --disable W0142,W0511,I0011,R,C

publish: clean
	python setup.py register sdist upload

clean:
	rm -rf *.egg-info dist build .coverage */*.pyc */*/*.pyc apidocs virtualenv
