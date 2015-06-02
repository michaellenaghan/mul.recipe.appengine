#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Tests for `mul.recipe.appengine` package.
"""


import doctest
import os
import unittest


_README_RST = os.path.join('..', 'README.rst')


def test_suite():
    return doctest.DocFileSuite(_README_RST)


def load_tests(loader, tests, pattern):
    # pylint: disable=unused-argument
    tests.addTest(
        test_suite()
    )
    return tests


if __name__ == '__main__':
    unittest.main()
