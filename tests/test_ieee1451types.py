#!/usr/bin/env python
"""
.. module:: test_ieee1451types
   :platform: Unix, Windows
   :synopsis: This module contains unit tests for
   the ieee1451types module.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
# -*- coding: utf-8 -*-

import unittest
from ncaplite import ieee1451types as ieee1451
import os


class TestIEEE1451Types(unittest.TestCase):
    """This class defines the test runner for ieee1451types"""
    def setUp(self):
        if (os.environ.get('USER', '') == 'vagrant') or ('TRAVIS'
                                                         in os.environ):
            self.config_file_path = 'tests/testconfig.xml'
            self.test_broker_ip = '127.0.0.1'
        else:
            self.config_file_path = 'tests/devconfig.xml'
            self.test_broker_ip = '10.10.100.4'

    def tearDown(self):
        pass

    def test_name_from_typecode(self):
        """Test that TypeCode instances return properly fomratted names."""
        tc = ieee1451.TypeCode.UINT16_TC
        assert(str(tc) == 'UINT16_TC')

    def test_argument_initializer(self):
        """Test that Agrument initialization is implemented properly."""
        tc = ieee1451.TypeCode.FLOAT32_ARRAY_TC
        val = (3.14159, 1.2345, 0.6789)

        arg = ieee1451.Argument(tc, val)

        assert(arg.value == val )
        assert(arg.type_code == tc)

    def test_argarray_putget_by_index(self):
        """Test ArgumentArray put/get by index."""

        tclist =  (ieee1451.TypeCode.FLOAT32_ARRAY_TC,
                   ieee1451.TypeCode.UINT16_TC,
                   ieee1451.TypeCode.STRING_TC)

        vals = ((3.14159, 1.2345, 0.6789),
                0xCAFE,
                "Foobar")

        idxs = [0, 1, 23]
        #put by index
        aa = ieee1451.ArgumentArray()

        for i, idx in enumerate(idxs):
            arg = ieee1451.Argument(tclist[i], vals[i])
            aa.put_by_index(idx, arg)
            res = aa.get_by_index(idx)
            assert(arg.value == vals[i])
            assert(arg.type_code == tclist[i])

    def test_argarray_putget_by_name(self):
        """Test ArgumentArray put/get by name."""

        tclist =  (ieee1451.TypeCode.FLOAT32_ARRAY_TC,
                   ieee1451.TypeCode.UINT16_TC,
                   ieee1451.TypeCode.STRING_TC)

        vals = ((3.14159, 1.2345, 0.6789),
                0xCAFE,
                "Foobar")

        names = ["foo", "bar", "baz"]

        aa = ieee1451.ArgumentArray()

        for i, name in enumerate(names):
            arg = ieee1451.Argument(tclist[i], vals[i])
            aa.put_by_name(name, arg)
            res = aa.get_by_name(name)
            assert(arg.value == vals[i])
            assert(arg.type_code == tclist[i])

    def test_argarray_next_index(self):
        """Test the next index helper function of ArgumentArray"""

        aa = ieee1451.ArgumentArray()

        cases =[ {0: 'a', 1: 'b', 2: 'c'},
                 {0: 'a', 1: 'b', 3: 'c'},
                 {1: 'a', 2: 'b', 3: 'c', 4: 'd'},
                 {0: 'a', 1: 'b', 10: 'c', 42: 'd'}
                 ]

        expected  = [3, 2, 0,2]
        for i, test_case in enumerate(cases):
            aa.arguments = test_case
            actual = aa.next_index()
            assert(expected[i] == actual)

    def test_argarray_putbyname_getbyindex(self):
        """Test ArgumentArray put by name, get by index."""

        tclist =  (ieee1451.TypeCode.FLOAT32_ARRAY_TC,
                   ieee1451.TypeCode.UINT16_TC,
                   ieee1451.TypeCode.STRING_TC)

        vals = ((3.14159, 1.2345, 0.6789),
                0xCAFE,
                "Foobar")

        names = ["foo", "bar", "baz"]
        expected_idxs = [0, 1, 2]

        aa = ieee1451.ArgumentArray()

        for i, name in enumerate(names):
            arg = ieee1451.Argument(tclist[i], vals[i])
            aa.put_by_name(name, arg)
            res = aa.get_by_index(i)
            assert(arg.value == vals[i])
            assert(arg.type_code == tclist[i])

    def test_argarray_putbyname_after_arbitrary_index(self):
        """Test we can add type by name at proper index after arbitrary add by
        index"""
        tclist =  (ieee1451.TypeCode.FLOAT32_ARRAY_TC,
                   ieee1451.TypeCode.UINT16_TC,
                   ieee1451.TypeCode.STRING_TC)

        vals = ((3.14159, 1.2345, 0.6789),
                0xCAFE,
                "Foobar")

        keys = [15, 0, "foo"]
        expected_idxs = [15, 0, 1]

        aa = ieee1451.ArgumentArray()

        for i, key  in enumerate(keys):
            arg = ieee1451.Argument(tclist[i], vals[i])
            if(type(key) is int):
                aa.put_by_index(key, arg)
            else:
                aa.put_by_name(key, arg)

            res = aa.get_by_index(expected_idxs[i])
            assert(arg.value == vals[i])
            assert(arg.type_code == tclist[i])

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
