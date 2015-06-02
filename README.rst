======================
MuL App Engine Recipes
======================

.. image:: https://readthedocs.org/projects/pip/badge/
        :target: https://mulrecipeappengine.readthedocs.org

.. image:: https://img.shields.io/pypi/v/mul.recipe.appengine.svg
        :target: https://pypi.python.org/pypi/mul.recipe.appengine

.. image:: https://img.shields.io/travis/michaellenaghan/mul.recipe.appengine.svg
        :target: https://travis-ci.org/michaellenaghan/mul.recipe.appengine


Buildout recipes for App Engine.

=====================
App Engine SDK Recipe
=====================

Given a URL pointing to a Google App Engine Python SDK zip file, this recipe
a) downloads the file and b) unzips the file and c) creates top-level Python
scripts that invoke corresponding top-level SDK scripts.

Downloading uses and respects the options in the ``buildout.cfg``'s
``buildout`` section. Specifically, downloaded files are cached in the
``download-cache`` directory and files are never downloaded in ``offline``
mode.

The downloaded file (cached or not) is unzipped into the recipe's part
directory. The top level of the SDK directory is then scanned for Python
scripts. For each SDK script a corresponding script is generated
and placed in buildout's ``bin-directory``. The generated script simply invokes
the SDK script, passing along arguments. Buildout's ``relative-paths`` option
is respected. Or, at least, it should be.

The list of generated scripts can be filtered using the ``scripts`` option. By
default its value is '*'. If a '*' appears anywhere in the list all scripts
will be generated. Otherwise, only those scripts mentioned in the option
(with or without a '.py' extension) will be generated.

Options
-------

:scripts: A space-delimited list of Python script names or '*'.
    The default is '*'.
:url: The url to the Google App Engine Python SDK zip file.
    Required.

Example
-------

::

    [sdk]
    recipe = mul.recipe.appengine:sdk

    url = \
        https://storage.googleapis.com/appengine-sdks/featured/google_appengine_1.9.21.zip

=====================
App Engine Lib Recipe
=====================

Given a list of eggs, this recipe a) computes their working set and then b)
copies that working set into the specified ``lib-directory``.  (This recipe
only copies eggs; it doesn't download or install them.) The ``lib-directory``
is created each time the part is installed and deleted each time the part
is uninstalled.

Eggs are copied unless they're in the ``ignore-eggs`` list. The top-level
packages of each egg are copied unless they're in the ``ignore-packages`` list.
The files and directories of each package are copied unless they're in the
``ignore-files`` list. The ``ignore-files`` list supports globs. You must, of
course, filter packages and files with care; eggs aren't written to expect
that kind of install-time surgery.

When an egg is copied its egg-info is also copied. The egg-info can be used
for example by pkg_resources to locate package resources at runtime. The
egg-info is copied in a manor similar to ``setup.py``'s
``--single-version-externally-managed`` install option; the egg-info
directories are siblings of the package directories.

The eggs that are copied can be either zipped or unzipped.

Options
-------

:eggs: A newline-delimited list of eggs to copy.
    The default is an empty list.
:ignore-eggs: A newline-delimited list of eggs to ignore when copying.
    The default is an empty list.
:ignore-packages: A newline-delimited list of packages to ignore when copying.
    The default is an empty list.
:ignore-files: A newline-delimited list of file globs to ignore when copying.
    The default is an empty list.
:lib-directory: The directory to copy the egg-info and packages to.
    Required.

Example
-------

::

    [lib]
    recipe = mul.recipe.appengine:lib

    eggs =
        pyramid
        pyramid_debugtoolbar
    ignore-eggs =
        MyEgg
    ignore-packages =
        easy_install
        setuptools
        site
    ignore-files =
        *.c
        *.h
        *.pyc
        *.pyo
        *.so
        test
        tests
        testsuite
    lib-directory = develop/MyEgg/lib
