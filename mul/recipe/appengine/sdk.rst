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
