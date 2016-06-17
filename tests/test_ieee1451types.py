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

    def test_timerepresentation_to_serializable(self):

        t = ieee1451.TimeRepresentation(secs=1, nsecs=1000)
        expected = {'TimeRepresentation': {'secs': 1, 'nsecs': 1000}}

        s = t.serializable()
        self.assertEqual(expected, s)

    def test_timerepresentation_from_serializable(self):

        expected = ieee1451.TimeRepresentation(secs=1, nsecs=1000)
        s = {'TimeRepresentation': {'secs': 1, 'nsecs': 1000}}

        actual = ieee1451.TimeRepresentation.from_serializable(s)
        self.assertEqual(expected, actual)

    def test_timeduration_to_serializable(self):
        t = ieee1451.TimeDuration(secs=1, nsecs=1000)
        expected = {'TimeDuration': {'secs': 1, 'nsecs': 1000}}

        s = t.serializable()
        self.assertEqual(expected, s)

    def test_argument_initializer(self):
        """Test that Agrument initialization is implemented properly."""
        tc = ieee1451.TypeCode.FLOAT32_ARRAY_TC
        val = (3.14159, 1.2345, 0.6789)

        arg = ieee1451.Argument(tc, val)

        assert(arg.value == val)
        assert(arg.type_code == tc)

    def test_argument_to_serializable(self):
        """Test conversion of argument to serializable format"""
        tc = ieee1451.TypeCode.FLOAT32_ARRAY_TC
        val = (3.14159, 1.2345, 0.6789)

        arg = ieee1451.Argument(tc, val)

        s = arg.serializable()

        expected_output = {
                           'type_code': 'FLOAT32_ARRAY_TC',
                           'value': (3.14159, 1.2345, 0.6789)}

        self.assertEqual(expected_output, s)

    def test_argument_from_serializable(self):
        tc = ieee1451.TypeCode.FLOAT32_ARRAY_TC
        val = (3.14159, 1.2345, 0.6789)
        expected = ieee1451.Argument(tc, val)

        s = {'type_code': 'FLOAT32_ARRAY_TC',
             'value': (3.14159, 1.2345, 0.6789)}

        actual = ieee1451.Argument.from_serializable(s)

        self.assertEqual(expected, actual)

    def test_argarray_putget_by_index(self):
        """Test ArgumentArray put/get by index."""

        tclist = (ieee1451.TypeCode.FLOAT32_ARRAY_TC,
                  ieee1451.TypeCode.UINT16_TC,
                  ieee1451.TypeCode.STRING_TC)

        vals = ((3.14159, 1.2345, 0.6789),
                0xCAFE,
                "Foobar")

        idxs = [0, 1, 23]

        aa = ieee1451.ArgumentArray()

        for i, idx in enumerate(idxs):
            arg = ieee1451.Argument(tclist[i], vals[i])
            aa.put_by_index(idx, arg)
            res = aa.get_by_index(idx)
            assert(arg.value == vals[i])
            assert(arg.type_code == tclist[i])
            assert(res.value == vals[i])

    def test_argarray_putget_by_name(self):
        """Test ArgumentArray put/get by name."""

        tclist = (ieee1451.TypeCode.FLOAT32_ARRAY_TC,
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
            assert(res.value == vals[i])
            assert(arg.type_code == tclist[i])

    def test_argarray_next_index(self):
        """Test the next index helper function of ArgumentArray"""

        aa = ieee1451.ArgumentArray()

        cases = [{0: 'a', 1: 'b', 2: 'c'},
                 {0: 'a', 1: 'b', 3: 'c'},
                 {1: 'a', 2: 'b', 3: 'c', 4: 'd'},
                 {0: 'a', 1: 'b', 10: 'c', 42: 'd'}
                 ]

        expected = [3, 2, 0, 2]
        for i, test_case in enumerate(cases):
            aa.arguments = test_case
            actual = aa.next_index()
            assert(expected[i] == actual)

    def test_argarray_putbyname_getbyindex(self):
        """Test ArgumentArray put by name, get by index."""

        tclist = (ieee1451.TypeCode.FLOAT32_ARRAY_TC,
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
            res = aa.get_by_index(i)
            assert(arg.value == vals[i])
            assert(res.value == vals[i])
            assert(arg.type_code == tclist[i])

    def test_argarray_putbyname_after_arbitrary_index(self):
        """Test we can add type by name at proper index after arbitrary add by
        index"""
        tclist = (ieee1451.TypeCode.FLOAT32_ARRAY_TC,
                  ieee1451.TypeCode.UINT16_TC,
                  ieee1451.TypeCode.STRING_TC)

        vals = ((3.14159, 1.2345, 0.6789),
                0xCAFE,
                "Foobar")

        keys = [15, 0, "foo"]
        expected_idxs = [15, 0, 1]

        aa = ieee1451.ArgumentArray()

        for i, key in enumerate(keys):
            arg = ieee1451.Argument(tclist[i], vals[i])
            if(type(key) is int):
                aa.put_by_index(key, arg)
            else:
                aa.put_by_name(key, arg)

            res = aa.get_by_index(expected_idxs[i])
            assert(arg.value == vals[i])
            assert(res.value == vals[i])
            assert(arg.type_code == tclist[i])

    def test_argarray_equality_comparison(self):
        """Test comparison for equality between ArgumentArray instances"""
        tc = ieee1451.TypeCode.FLOAT32_ARRAY_TC
        vals = (1024.1111, 1025.2222, 1026.3333)

        aa1 = ieee1451.ArgumentArray()
        arg1 = ieee1451.Argument(tc, vals)
        aa1.put_by_name("MyArg", arg1)

        aa2 = ieee1451.ArgumentArray()
        arg2 = ieee1451.Argument(tc, vals)
        aa2.put_by_name("MyArg", arg2)

        self.assertEquals(aa1, aa2)

    def test_argarray_to_tuple(self):
        """Test ArgumentArray.to_list."""
        tc = ieee1451.TypeCode.FLOAT32_ARRAY_TC
        vals = (1024.1111, 1025.2222, 1026.3333)
        arg = ieee1451.Argument(tc, vals)
        aa = ieee1451.ArgumentArray()
        aa.put_by_name("MyArg", arg)
        result = aa.to_tuple()
        self.assertEqual(vals, result[0])

    def test_argarray_find_name_by_index(self):
        """Test finding the name or an argument by it's index in
        an ArgumentArray"""
        tc = ieee1451.TypeCode.UINT16_TC

        indicies = range(0, 10)
        names = ["arg"+str(i) if i != 5 else None for i in indicies]
        args = [ieee1451.Argument(tc, i) for i in indicies]
        aa = ieee1451.ArgumentArray()

        for i, arg in enumerate(args):
            if(i != 5):
                aa.put_by_name(names[i], arg)
            else:
                aa.put_by_index(i, arg)

        actual = [aa.find_name_by_index(i) for i in indicies]
        self.assertEqual(names, actual)

    def test_argarray_from_serializable(self):
        """Test conversion to an ArgumentArray from serializable format."""

        s = {'ArgumentArray': [
                {'name': 'Arg1', 'type_code': 'UINT16_TC', 'value': 1024},
                {'name': 'Arg2', 'type_code': 'UINT16_TC', 'value': 1025},
                {'name': '', 'type_code': 'UINT16_TC', 'value': 1026}
                ]}
        tc = ieee1451.TypeCode.UINT16_TC
        arg1 = ieee1451.Argument(tc, 1024)
        arg2 = ieee1451.Argument(tc, 1025)
        arg3 = ieee1451.Argument(tc, 1026)
        expected = ieee1451.ArgumentArray()
        expected.put_by_name("Arg1", arg1)
        expected.put_by_name("Arg2", arg2)
        expected.put_by_index(2, arg3)

        actual = ieee1451.ArgumentArray.from_serializable(s)

        self.assertEqual(expected, actual)

    def test_argarray_to_serializable(self):
        """Test converting ArgumentArray from serializable format to object."""

        tc = ieee1451.TypeCode.UINT16_TC
        arg1 = ieee1451.Argument(tc, 1024)
        arg2 = ieee1451.Argument(tc, 1025)
        arg3 = ieee1451.Argument(tc, 1026)
        aa = ieee1451.ArgumentArray()
        aa.put_by_name("Arg1", arg1)
        aa.put_by_name("Arg2", arg2)
        aa.put_by_index(2, arg3)

        expected_output = {'ArgumentArray': [
                    {'name': 'Arg1', 'type_code': 'UINT16_TC', 'value': 1024},
                    {'name': 'Arg2', 'type_code': 'UINT16_TC', 'value': 1025},
                    {'name': '', 'type_code': 'UINT16_TC', 'value': 1026}
                    ]}

        s = aa.serializable()
        self.assertEqual(expected_output, s)

    def test_error_to_serializable(self):
        """Test converting Error object to serializable format."""
        source = ieee1451.ErrorSource.ERROR_SOURCE_APPLICATION  # 4
        code = ieee1451.ErrorCode.INVALID_COMMID  # 1
        expected = {'Error': 0x8001}
        error = ieee1451.Error(source=source, code=code)
        result = error.serializable()
        self.assertEqual(expected, result)

    def test_error_from_serializable(self):
        """Test converting to Error object from serializable format."""

        source = ieee1451.ErrorSource.ERROR_SOURCE_APPLICATION  # 4
        code = ieee1451.ErrorCode.INVALID_COMMID  # 1
        expected = ieee1451.Error(source=source, code=code)
        test_data = {'Error': 0x8001}

        result = ieee1451.Error.from_serializable(test_data)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
