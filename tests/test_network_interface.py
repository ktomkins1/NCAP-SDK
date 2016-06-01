#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: test_network_interface
   :platform: Unix, Windows
   :synopsis: This module contains unit tests for
   the network_interface module.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""

import unittest


from ncaplite import network_interface
from ncaplite import ieee1451types as ieee1451

import os


class TestNetworkInterface(unittest.TestCase):
    """This class defines the test runner for network_interface"""
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

    def test_parse_outbound(self):
        """ Test outbound message parsing """

        test_msg = (1, 2, 3, [4, 5, 6], 7)
        expected_output = "1,2,3,4;5;6,7"
        actual_output = network_interface.NetworkClient.parse_outbound(
                                                                    test_msg)
        self.assertEqual(expected_output, actual_output)

    def test_parse_inbound_simple_request(self):
        """ Test inbound message parsing of simple requests """

        test_msg = "1,2,3,4,5,6,7"
        expected_output = (1, 2, 3, 4, 5, 6, 7)
        actual_output = network_interface.NetworkClient.parse_inbound(
                                                                    test_msg)

        self.assertEqual(expected_output, actual_output)

    def test_parse_inbound_request_with_list(self):
        """ Test inbound message parsing of requests with lists """
        test_msg = "1,2,3,4;5;6,7"
        expected_output = (1, 2, 3, [4, 5, 6], 7)
        actual_output = network_interface.NetworkClient.parse_inbound(
                                                                    test_msg)

        self.assertEqual(expected_output, actual_output)

    def test_parse_outbound_with_error_code(self):
        """ Test outbound message parsing """
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                     ieee1451.ErrorCode.NO_ERROR)

        test_msg = (1, error_code, 3, [4, 5, 6], 7)
        expected_output = "1,0;0,3,4;5;6,7"
        actual_output = network_interface.NetworkClient.parse_outbound(
                                                                    test_msg)
        self.assertEqual(expected_output, actual_output)
