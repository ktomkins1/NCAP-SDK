#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ncaplite
----------------------------------

Tests for `ncaplite` module.
"""

import unittest

from ncaplite import ncaplite


class TestNcaplite(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        assert (ncaplite.my_stub() == 1)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
