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
