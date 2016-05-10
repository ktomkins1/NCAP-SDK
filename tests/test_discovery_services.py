#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ncaplite_test
----------------------------------

Tests for `ncaplite` module.
"""

import unittest


from ncaplite import discovery_services
import xml.etree.ElementTree as ET
import os


class TestDiscoveryServices(unittest.TestCase):
    """This class defines the test runner for Discovery Services"""
    def setUp(self):
        """Setup for NCAP unit tests"""
        if (os.environ.get('USER', '') == 'vagrant') or ('TRAVIS' in os.environ):
            self.config_file_path = 'tests/testconfig.xml'
            self.test_broker_ip = '127.0.0.1'
        else:
            self.config_file_path = 'tests/devconfig.xml'
            self.test_broker_ip = '10.10.100.4'

        # generate a roster xml file for testing
        root = ET.Element("roster")
        tree = ET.ElementTree(root)
        tree.write("tests/testroster.xml")

    def tearDown(self):
        """Teardown for NCAP unit tests"""

        # nuke the testroster.xml to prepare for next test
        os.remove('tests/testroster.xml')
        pass

    def test_ncap_client_join(self):
        """ check that a client is added to the roster when ncap_client_join
        is called """
        on_roster = 0
        roster_path = 'tests/testroster.xml'
        discovery = discovery_services.DiscoveryServices(roster_path)
        client_id = 'unittest@ncaplite.loc'
        discovery.ncap_client_join(client_id)

        # tree = ET.parse(roster_path)
        root = discovery.tree.getroot()

        jids = []
        for user in root.findall('user'):
            jids.append(user.find('jid').text)

        if(client_id in jids):
            on_roster = 1

        assert(on_roster == 1)

    def test_ncap_client_join_unjoin(self):
        """ check that the appropriate client is removed from the roster
            when the unjoin function is called. """
        on_roster = 0
        roster_path = 'tests/testroster.xml'
        discovery = discovery_services.DiscoveryServices(roster_path)
        client_id = 'unittest@ncaplite.loc'

        discovery.ncap_client_join(client_id)

        # tree = ET.parse(roster_path)
        root = discovery.tree.getroot()

        jids = []
        for user in root.findall('user'):
            jids.append(user.find('jid').text)

        if(client_id in jids):
            on_roster = 1
        else:
            on_roster = 0

        assert(on_roster == 1)

        discovery.ncap_client_unjoin(client_id)

        jids = []
        for user in root.findall('user'):
            jids.append(user.find('jid').text)

        if(client_id in jids):
            on_roster = 1
        else:
            on_roster = 0

        assert(on_roster == 0)
