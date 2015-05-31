# -*- coding: utf-8 -*-


"""
mul.recipe.appengine.lib
"""


import logging
import os
import os.path
import pkg_resources
import setuptools.archive_util
import shutil
import tempfile
import zc.recipe.egg.egg
import zipfile


# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements


class Recipe(object):
    """
    App Engine Lib Recipe
    """

    def __init__(self, buildout, name, options):
        """
        Initialize the lib recipe.

        Configure a logger and record the values of the ``ignore-eggs``,
        ``ignore-packages``, ``ignore-files`` and ``lib-directory`` options.
        """
        self.buildout = buildout
        self.name = name
        self.options = options

        self.logger = logging.getLogger(self.name)

        self.egg = zc.recipe.egg.egg.Scripts(buildout, name, options)

        def _to_list(items):
            """
            Split the items on '\\n' and strip each member of the
            resulting list, keeping each member only if it isn't
            empty.
            """
            return [
                item.strip() for item in items.split('\n') if item.strip()
            ]

        self.ignore_eggs = _to_list(options.get('ignore-eggs', ''))
        self.ignore_packages = _to_list(options.get('ignore-packages', ''))
        self.ignore_files = _to_list(options.get('ignore-files', ''))

        self.lib_dir = options.get('lib-directory')
        self.lib_path = os.path.abspath(self.lib_dir)

    def install(self):
        """
        Install the part.
        """
        if os.path.isdir(self.lib_path):
            self.logger.info(
                'Removing lib-directory %s.', self.lib_path
            )
            shutil.rmtree(self.lib_path)

        if not os.path.isdir(self.lib_path):
            self.logger.info(
                'Creating lib-directory %s.', self.lib_path
            )
            os.mkdir(self.lib_path)

        self.options.created(self.lib_path)

        self.logger.debug('Ignoring files %s.', self.ignore_files)
        ignore = shutil.ignore_patterns(*self.ignore_files)

        # pylint: disable=no-member

        _, working_set = self.egg.working_set()
        for distribution in working_set:
            self.logger.debug('Considering egg %s.', distribution)

            if distribution.project_name in self.ignore_eggs:
                self.logger.debug('Ignoring egg %s.', distribution)
                continue

            self.logger.info('Copying egg %s.', distribution)

            # Create temp dir (if necessary).

            if zipfile.is_zipfile(distribution.location):
                tempdir = tempfile.mkdtemp()

                egg_dir = os.path.basename(distribution.location)
                egg_path = os.path.join(tempdir, egg_dir)
                egg_info_path = os.path.join(egg_path, 'EGG-INFO')

                self.logger.info(
                    'Unpacking egg %s to %s.', distribution, egg_path
                )

                setuptools.archive_util.unpack_archive(
                    distribution.location,
                    egg_path
                )

                # Replace the distribution we were originally looking at...

                distribution = pkg_resources.Distribution.from_filename(
                    egg_path,
                    metadata=pkg_resources.PathMetadata(
                        egg_path,
                        egg_info_path
                    )
                )
            else:
                tempdir = None
            try:

                # Copy egg packages.

                src_root = distribution.location
                dst_root = self.lib_path
                for package in distribution.get_metadata_lines(
                    'top_level.txt'
                ):
                    if package in self.ignore_packages:
                        self.logger.debug(
                            'Ignoring package %s.', package
                        )
                        continue

                    self.logger.info('Copying package %s.', package)

                    package_file = package + '.py'
                    package_dir = package
                    if os.path.isfile(os.path.join(src_root, package_file)):
                        src = os.path.join(src_root, package_file)
                        dst = os.path.join(dst_root, package_file)
                        self.copyfile(src, dst)
                    elif os.path.isdir(os.path.join(src_root, package_dir)):
                        src = os.path.join(src_root, package_dir)
                        dst = os.path.join(dst_root, package_dir)
                        self.copydir(src, dst, ignore=ignore)
                    else:
                        self.logger.warning(
                            'Egg %s is missing package %s.',
                            distribution,
                            package
                        )

                # Copy egg info.

                if os.path.isdir(distribution.egg_info):
                    egg_info_dir = pkg_resources.to_filename(
                        distribution.project_name
                    ) + '.egg-info'
                    src = distribution.egg_info
                    dst = os.path.join(self.lib_path, egg_info_dir)
                    self.copydir(src, dst)
                else:
                    self.logger.warning(
                        'Egg %s is missing egg-info.', distribution
                    )

            finally:

                # Remove temp dir (if necessary).

                if tempdir and os.path.isdir(tempdir):
                    shutil.rmtree(tempdir)

        return self.options.created()

    def update(self):
        """
        Update the part.
        """
        pass

    def copyfile(self, src, dst):
        """
        Copy the src file to dst.
        """
        self.logger.debug('Copying file %s to %s.', src, dst)
        shutil.copy2(src, dst)

    def copydir(self, src, dst, symlinks=False, ignore=None):
        """
        Copy the src dir to dst.

        Adapted from Python 2.7 source.
        """
        self.logger.debug('Copying dir %s to %s.', src, dst)
        names = os.listdir(src)
        if ignore is not None:
            ignored_names = ignore(src, names)
        else:
            ignored_names = set()

        # This is the one and only spot we
        # differ from the original code:
        # we merge directories by allowing
        # existing destination dirs.
        if not os.path.isdir(dst):
            os.makedirs(dst)

        errors = []
        for name in names:
            if name in ignored_names:
                continue

            srcname = os.path.join(src, name)
            dstname = os.path.join(dst, name)

            try:
                if symlinks and os.path.islink(srcname):
                    linkto = os.readlink(srcname)
                    os.symlink(linkto, dstname)
                elif os.path.isdir(srcname):
                    self.copydir(srcname, dstname, symlinks, ignore)
                else:
                    # Will raise a SpecialFileError for unsupported file types
                    self.copyfile(srcname, dstname)
            # catch the Error from the recursive copydir so that we can
            # continue with other files
            except shutil.Error, err:
                errors.extend(err.args[0])
            except EnvironmentError, why:
                errors.append((srcname, dstname, str(why)))

            try:
                shutil.copystat(src, dst)
            except OSError, why:
                # pylint: disable=undefined-variable
                if WindowsError is not None and isinstance(why, WindowsError):
                    # Copying file access times may fail on Windows
                    pass
                else:
                    errors.append((src, dst, str(why)))
        if errors:
            raise shutil.Error, errors
