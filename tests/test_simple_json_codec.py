#!/usr/bin/env python
"""
.. module:: test_network_interface
   :platform: Unix, Windows
   :synopsis: This module contains unit tests for
   the network_interface module.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
# -*- coding: utf-8 -*-

import unittest
from ncaplite import ieee1451types as ieee1451
from ncaplite import simple_json_codec


class TestSimpleJsonCodec(unittest.TestCase):
    """This class defines the test runner for network_interface"""
    def setUp(self):
        self.codec = simple_json_codec.SimpleJsonCodec()

    def tearDown(self):
        pass

    def test_from_serializable(self):
        """ Test inbound message from the serializable format"""

        test_data = ['7217', {
                'error_code': {'Error': 0x8001},
                'ncap_id': 1234,
                'tim_id': 01,
                'channel_id': 01,
                'timeout': {'TimeDuration': {'secs': 0, 'nsecs': 1000}},
                'sampling_mode': 0,
                'data_value': {'ArgumentArray': [
                    {'type_code': 'UINT16_TC',
                     'value': 1024,
                     'name': 'ADC1234'}]}
                }]

        source = ieee1451.ErrorSource.ERROR_SOURCE_APPLICATION
        code = ieee1451.ErrorCode.INVALID_COMMID
        error = ieee1451.Error(source=source, code=code)
        aa = ieee1451.ArgumentArray()
        arg = ieee1451.Argument(ieee1451.TypeCode.UINT16_TC,
                                1024)
        aa.put_by_name("ADC1234", arg)

        expected_output = ['7217', {
                'error_code': error,
                'ncap_id': 1234,
                'tim_id': 01,
                'channel_id': 01,
                'timeout': ieee1451.TimeDuration(0, 1000),
                'sampling_mode': 0,
                'data_value': aa
                }]

        actual_output = self.codec.from_serializable(test_data)
        self.assertEqual(expected_output, actual_output)

    def test_to_serializable(self):
        """ Test converting an outbound response to serializable format"""

        source = ieee1451.ErrorSource.ERROR_SOURCE_APPLICATION
        code = ieee1451.ErrorCode.INVALID_COMMID
        error = ieee1451.Error(source=source, code=code)
        aa = ieee1451.ArgumentArray()
        arg = ieee1451.Argument(ieee1451.TypeCode.UINT16_TC,
                                1024)
        aa.put_by_name("ADC1234", arg)

        test_data = ['7217', {
                'error_code': error,
                'ncap_id': 1234,
                'tim_id': 01,
                'channel_id': 01,
                'timeout': ieee1451.TimeDuration(0, 1000),
                'sampling_mode': 0,
                'data_value': aa
                }]

        expected_output = ['7217', {
                'error_code': {'Error': 0x8001},
                'ncap_id': 1234,
                'tim_id': 01,
                'channel_id': 01,
                'timeout': {'TimeDuration': {'secs': 0, 'nsecs': 1000}},
                'sampling_mode': 0,
                'data_value': {'ArgumentArray': [
                    {'type_code': 'UINT16_TC',
                     'value': 1024,
                     'name': 'ADC1234'}]}
                }]

        actual_output = self.codec.to_serializable(test_data)
        self.assertEqual(expected_output, actual_output)

    def test_json_encode_decode(self):
        """Test that the codec can decode and encoded message."""

        source = ieee1451.ErrorSource.ERROR_SOURCE_APPLICATION
        code = ieee1451.ErrorCode.INVALID_COMMID
        error = ieee1451.Error(source=source, code=code)
        aa = ieee1451.ArgumentArray()
        arg = ieee1451.Argument(ieee1451.TypeCode.UINT16_TC,
                                1024)
        aa.put_by_name('ADC1234', arg)

        test_input = ['7217', {
                'error_code': error,
                'ncap_id': 1234,
                'tim_id': 01,
                'channel_id': 01,
                'timeout': ieee1451.TimeDuration(0, 1000),
                'sampling_mode': 0,
                'data_value': aa
                }]

        encoded = self.codec.encode(test_input)
        decoded = self.codec.decode(encoded)

        self.assertEqual(test_input, decoded)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
