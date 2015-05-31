#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('./mul/recipe/appengine/lib.rst') as libdoc_file:
    libdoc = libdoc_file.read()

with open('./mul/recipe/appengine/sdk.rst') as sdkdoc_file:
    sdkdoc = sdkdoc_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

install_requirements = [
    'setuptools >= 8.0',
    'zc.buildout >= 2.3.1',
    'zc.recipe.egg >= 2.0.1',
]

test_requirements = [

]

setup(
    author='Michael Lenaghan',
    author_email='metamul -@- gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    description='Buildout recipes for App Engine.',
    entry_points = {
        'zc.buildout': [
            'lib = mul.recipe.appengine.lib:Recipe',
            'sdk = mul.recipe.appengine.sdk:Recipe'
        ]
    },
    include_package_data=True,
    install_requires=install_requirements,
    keywords='app appengine buildout engine gae mul recipe zc.buildout',
    license='BSD',
    long_description=readme + '\n' + sdkdoc + '\n' + libdoc + '\n' + history,
    name='mul.recipe.appengine',
    namespace_packages=['mul', 'mul.recipe'],
    packages=['mul', 'mul.recipe', 'mul.recipe.appengine'],
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/michaellenaghan/mul.recipe.appengine',
    version='0.2.0',
    zip_safe=False,
)
