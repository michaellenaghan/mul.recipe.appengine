# -*- coding: utf-8 -*-


"""
mul.recipe.appengine.sdk
"""


import glob
import logging
import os
import os.path
import shutil
import zc.buildout
import zc.buildout.buildout
import zc.buildout.download
import zipfile


# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements


class Recipe(object):
    """
    App Engine SDK Recipe
    """

    BIN_ABS = """\
#! {python}

import os
import sys

os.execl(
    '{python}',
    '{python}',
    '{script}',
    *sys.argv[1:]
)"""
    BIN_REL = """\
#! {python}

import os
import sys

os.execl(
    '{python}',
    '{python}',
    os.path.join(
        os.path.dirname(os.path.abspath(os.path.realpath(__file__))),
        '{script}'
    ),
    *sys.argv[1:]
)"""

    def __init__(self, buildout, name, options):
        """
        Initialize the SDK recipe.

        Configure a logger and record the values of the ``scripts``
        and ``url`` options. Also record the buildout options that
        are used indirectly: ``bin-directory``, ``directory``,
        ``executable``, ``parts-directory``, and ``relative-paths``.
        """
        self.buildout = buildout
        self.name = name
        self.options = options

        self.logger = logging.getLogger(self.name)

        # Copy buildout options to local options
        # in order to indicate our dependency on
        # those values.

        b_options = buildout['buildout']

        options['bin-directory'] = b_options.get('bin-directory')
        self.bin_dir = options.get('bin-directory')
        self.bin_path = os.path.abspath(self.bin_dir)

        options['directory'] = b_options.get('directory')
        self.directory = options.get('directory')

        options['executable'] = b_options.get('executable')
        self.executable = options.get('executable')

        options['parts-directory'] = b_options.get('parts-directory')
        self.parts_dir = options.get('parts-directory')
        self.parts_path = os.path.abspath(self.parts_dir)

        self.part_dir = self.name
        self.part_path = os.path.join(self.parts_path, self.part_dir)

        options['relative-paths'] = b_options.get('relative-paths', 'false')
        self.relative_paths = zc.buildout.buildout.bool_option(
            options,
            'relative-paths'
        )

        self.scripts = options.setdefault('scripts', '*').split()

        self.url = options.get('url', '')
        if not self.url:
            self.logger.error(
                'Option "url" is required.'
            )
            raise zc.buildout.UserError(
                'Option "url" is required.'
            )

        _, ext = os.path.splitext(self.url)
        if not ext == '.zip':
            self.logger.error(
                'Option "url" should point to a zip file: %s.',
                self.url
            )
            raise zc.buildout.UserError(
                'Option "url" should point to a zip file.'
            )

    def install(self):
        """
        Install the part.
        """
        if os.path.isdir(self.part_path):
            self.logger.info(
                'Removing part directory %s.', self.part_path
            )
            shutil.rmtree(self.part_path)

        if not os.path.isdir(self.part_path):
            self.logger.info(
                'Creating part directory %s.', self.part_path
            )
            os.mkdir(self.part_path)

        self.options.created(self.part_path)

        # Download & Extract

        path, path_is_temp = zc.buildout.download.Download(
            self.buildout['buildout'],
            logger=self.logger
        )(self.url)
        with zipfile.ZipFile(path, 'r') as unzipfile:
            unzipfile.extractall(self.part_path)
        if path_is_temp:
            os.remove(path)

        # Scripts

        python = self.executable

        scripts_dir = 'google_appengine'
        scripts_path = os.path.join(self.part_path, scripts_dir)
        scripts_glob = os.path.join(scripts_path, '*.py')
        for script in glob.glob(scripts_glob):
            script_root, _ = os.path.splitext(os.path.basename(script))

            script_name = os.path.basename(script)
            if self.relative_paths:
                script_path = os.path.relpath(script, self.bin_path)
            else:
                script_path = script

            # Including the extension is a bit lame on
            # Linux and Mac, but it's helpful on Windows.

            bin_name = script_name
            bin_path = os.path.join(self.bin_path, bin_name)

            if self.relative_paths:
                bin_template = Recipe.BIN_REL
            else:
                bin_template = Recipe.BIN_ABS

            if '*' in self.scripts or \
                    script_root in self.scripts or \
                    script_name in self.scripts:
                self.logger.info('Generating script %s.', bin_path)

                bin_fd = os.open(bin_path, os.O_CREAT | os.O_WRONLY, 0755)
                try:
                    os.write(
                        bin_fd,
                        bin_template.format(
                            python=python,
                            script=script_path
                        )
                    )
                finally:
                    os.close(bin_fd)

                self.options.created(bin_path)

        return self.options.created()

    def update(self):
        """
        Update the part.
        """
        pass
