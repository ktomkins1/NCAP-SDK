#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ncaplite_test
----------------------------------

Tests for `ncaplite` module.
"""

import unittest
import mock
import os

from ncaplite import discovery_services
from ncaplite import transducer_services_base
from ncaplite import ieee1451types as ieee1451
import xml.etree.ElementTree as ET




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
        discovery = discovery_services.DiscoveryServices()
        discovery.open_roster(roster_path)
        client_id = 'unittest@ncaplite.loc'
        discovery.ncap_client_join(client_id)
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
        discovery = discovery_services.DiscoveryServices()
        discovery.open_roster(roster_path)
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

    def test_ncap_tim_discover(self):
        """ Test TIM discovery service."""

        def report_comm_module_mock():
            error_code = ieee1451.Error(
                                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                ieee1451.ErrorCode.NO_ERROR)
            module_ids = [1, 2]
            result = {'error_code': error_code,
                      'module_ids': module_ids}

            return result

        def report_tims_mock(module_id):
            error_code = ieee1451.Error(
                    ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                    ieee1451.ErrorCode.NO_ERROR)
            tim_ids = []
            if(module_id == 1):
                tim_ids = [1, 2]
            else:
                tim_ids = [3]

            result = {'error_code': error_code,
                      'tim_ids': tim_ids}

            return result


        tdisco = mock.Mock(spec=transducer_services_base.TimDiscoveryBase)
        tdisco.report_comm_module.side_effect = report_comm_module_mock
        tdisco.report_tims.side_effect = report_tims_mock

        disco = discovery_services.DiscoveryServices()
        disco.register_transducer_access_service(tdisco)


        request = {'ncap_id': 1234}

        error_code = ieee1451.Error(
                    ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                    ieee1451.ErrorCode.NO_ERROR)

        num_of_tim = 3

        tim_ids = [1, 2, 3]

        expected_reposne = {'error_code': error_code,
                            'num_of_tim': num_of_tim,
                            'tim_ids': tim_ids}

        result = disco.ncap_tim_discover(**request)

        self.assertEqual(result, expected_reposne)

    def test_ncap_transducer_discover(self):
        """ Test transducer discover request. """
        def report_channels_mock(tim_id):

            error_code = ieee1451.Error(
                                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                ieee1451.ErrorCode.NO_ERROR)
            channel_ids = [1, 2, 3]
            names = ["Channel1", "Channel2", "Channel3"]
            result = {'error_code': error_code,
                      'channel_ids': channel_ids,
                      'channel_names': names}

            return result


        tdisco = mock.Mock(spec=transducer_services_base.TimDiscoveryBase)
        tdisco.report_channels.side_effect = report_channels_mock

        disco = discovery_services.DiscoveryServices()
        disco.register_transducer_access_service(tdisco)


        request = {'ncap_id': 1234, 'tim_id': 1}

        error_code = ieee1451.Error(
                    ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                    ieee1451.ErrorCode.NO_ERROR)

        tim_id = 1
        num_trans_channels = 3
        trans_channel_ids = [1, 2, 3]
        trans_channel_names = ["Channel1", "Channel2", "Channel3"]

        expected_reposne = {'error_code': error_code,
                            'ncap_id': 1234,
                            'tim_id': tim_id,
                            'num_of_transducer_channels': num_trans_channels,
                            'trans_channel_ids': trans_channel_ids,
                            'trans_channel_names': trans_channel_names}

        result = disco.ncap_transducer_discover(**request)

        self.assertEqual(result, expected_reposne)
