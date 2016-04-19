#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ncaplite_test
----------------------------------

Tests for `ncaplite` module.
"""

import unittest

from ncaplite import ncaplite
from ncaplite import network_interface
from ncaplite import discovery_services
import time
import xml.etree.ElementTree as ET
import os


class TestNcaplite(unittest.TestCase):
    """This class defines the test runner for an NCAP instance.

    We'll start with just this test class and then expand as modules are
    added.
    """

    def setUp(self):
        """Setup for NCAP unit tests"""
        if (os.environ.get('USER', '') == 'vagrant') or ('TRAVIS' in os.environ):
            print("environment is virtualized")
            self.config_file_path = 'tests/testconfig.xml'
            self.test_broker_ip = '127.0.0.1'
        else:
            print("environment is dev machine")
            self.config_file_path = 'tests/devconfig.xml'
            self.test_broker_ip = '10.10.100.4'


    def tearDown(self):
        """Teardown for NCAP unit tests"""
        pass

    def test_ncap_can_register_network_if(self):
        """
        Makes sure we can bring up the network
        interface with some basic inputs
        :return:
        """

        ncap_id = 12345
        jid = 'ncap@ncaplite.loc'
        password = 'mypassword'
        broker_address = (self.test_broker_ip, 5222)

        ncap = ncaplite.NCAP(ncap_id)
        network_if = network_interface.NetworkClient(jid, password, broker_address)
        ncap.register_network_interface(network_if)
        ncap.start()
        time.sleep(1)
        ncap.stop()

    def test_ncap_can_take_empty_broker_address(self):
        """
        Check that the we can bring-up the network interface
        without specifying an explicit broker address
        :return:
        """
        ncap_id = 12345
        jid = 'ncap@ncaplite.loc'
        password = 'mypassword'
        broker_address = (self.test_broker_ip, 5222)

        ncap = ncaplite.NCAP(ncap_id)
        network_if = network_interface.NetworkClient(jid, password, broker_address)
        ncap.register_network_interface(network_if)
        ncap.start()
        time.sleep(1)
        ncap.stop()


    def test_can_read_ncap_config_file(self):
        """Test that we can read the ncap config file"""
        tree = ET.parse(self.config_file_path)
        root = tree.getroot()

        roster_path = root.find('roster_path').text
        print(roster_path)
        assert(roster_path == 'tests/testroster.xml')
        broker_ip = root.find('broker_address').find('address').text
        assert(broker_ip == self.test_broker_ip)
        broker_port = int(root.find('broker_address').find('port').text)
        assert(broker_port == 5222)
        jid = root.find('ncap_identification').find('jid').text
        assert(jid == 'ncap@ncaplite.loc')
        password = root.find('ncap_identification').find('password').text
        assert(password == 'mypassword')
        ncap_id = int(root.find('ncap_identification').find('ncap_id').text)
        assert(ncap_id == 12345)
        ncap_type = root.find('ncap_identification').find('ncap_type').text
        assert(ncap_type == 'server')
        ncap_model_number = int(root.find('ncap_identification').find('model_number').text)
        assert(ncap_model_number == 11111)
        ncap_serial_number = int(root.find('ncap_identification').find('serial_number').text)
        assert(ncap_serial_number == 22222)
        ncap_mfcr_id = int(root.find('ncap_identification').find('manufacturer_id').text)
        assert(ncap_mfcr_id == 33333)

        ncap = ncaplite.NCAP(ncap_id)
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        ncap.register_network_interface(network_if)
        ncap.start()
        time.sleep(1)
        ncap.stop()

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
