#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Tests for `mul.recipe.appengine` package.
"""


import doctest
import os
import unittest


_THERE = os.path.join('..', 'mul', 'recipe', 'appengine')

_LIB_RST = os.path.join(_THERE, 'lib.rst')
_SDK_RST = os.path.join(_THERE, 'sdk.rst')


def load_tests(loader, tests, pattern):
    # pylint: disable=unused-argument
    tests.addTests(
        doctest.DocFileSuite(_LIB_RST)
    )
    tests.addTests(
        doctest.DocFileSuite(_SDK_RST)
    )
    return tests


if __name__ == '__main__':
    unittest.main()
