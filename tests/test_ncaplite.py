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
from ncaplite import transducer_data_access_services
from ncaplite import transducer_services_base
import mock
import time
import xml.etree.ElementTree as ET
import os


class TestNcaplite(unittest.TestCase):
    """This class defines the test runner for an NCAP instance.
    """

    def setUp(self):
        """Setup for NCAP unit tests"""
        if (os.environ.get('USER', '') == 'vagrant') or ('TRAVIS'
                                                         in os.environ):
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
        network_if = network_interface.NetworkClient(
                                                jid, password, broker_address)
        ncap.register_network_interface(network_if)
        ncap.start()
        time.sleep(.5)
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
        network_if = network_interface.NetworkClient(
                                                jid, password, broker_address)
        ncap.register_network_interface(network_if)
        ncap.start()
        time.sleep(.5)
        ncap.stop()

    def test_can_read_ncap_config_file(self):
        """Test that we can read the ncap config file"""
        tree = ET.parse(self.config_file_path)
        root = tree.getroot()

        roster_path = root.find('roster_path').text
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
        ncap_model_number = int(root.find('ncap_identification')
                                .find('model_number').text)
        assert(ncap_model_number == 11111)
        ncap_serial_number = int(root.find('ncap_identification').
                                 find('serial_number').text)
        assert(ncap_serial_number == 22222)
        ncap_mfcr_id = int(root.find('ncap_identification').
                           find('manufacturer_id').text)
        assert(ncap_mfcr_id == 33333)

        ncap = ncaplite.NCAP(ncap_id)
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        ncap.register_network_interface(network_if)
        ncap.start()
        time.sleep(.5)
        ncap.stop()

    def test_client_join_unjoin(self):
        """ Check we can spawn a thread the allows us to join/unjoin the roster
        based on a client request. """
        roster_path = 'tests/testroster.xml'
        ncap = ncaplite.NCAP(12345)
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices(roster_path)
        ncap.register_discovery_service(discovery)

        ncap_client = ncaplite.NCAP(67890)
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))
        ncap_client.register_network_interface(client_if)

        ncap.start()
        ncap_client.start()
        msgs = ['7108', '7109']
        expected_roster_status = [1, 0]
        actual_roster_status = []

        time.sleep(.5)

        for msg in msgs:
            ncap_client.network_interface.send_message(
                                        mto=ncap.jid, mbody=msg, mtype='chat')

            time.sleep(1)

            # check the roster, but ignore the resource identifier for this
            root = ncap.discovery_service.tree.getroot()
            jids = []

            for user in root.findall('user'):
                jids.append(user.find('jid').text.split('/')[0])

            if(client_jid in jids):
                actual_roster_status.append(1)
            else:
                actual_roster_status.append(0)

        ncap_client.stop()
        ncap.stop()

        self.assertListEqual(expected_roster_status, actual_roster_status)

    def test_client_can_read_sample_data(self):
        """ Test that a client can read a Sample from
        a channel of a TIM """

        def open_mock(tim_id, channel_id):
            trans_comm_id = 1
            return trans_comm_id

        def read_data_mock(trans_comm_id, timeout,
                           sampling_mode, result):
            result.append(1024)

        def client_on_data(msg):
            resp = network_interface.NetworkClient.parse_inbound(msg['body'])
            self.actual_response = resp

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.read_data.side_effect = read_data_mock

        tdas = transducer_data_access_services.TransducerDataAccessServices()
        tdas.register_transducer_access_service(tdaccs)

        roster_path = 'tests/testroster.xml'
        ncap = ncaplite.NCAP(12345)
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices(roster_path)
        ncap.register_discovery_service(discovery)
        ncap.register_transducer_data_access_service(tdas)

        ncap_client = ncaplite.NCAP(67890)
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))

        # monkey-patch the data received method
        ncap_client.on_network_if_message = client_on_data

        ncap_client.register_network_interface(client_if)

        ncap.start()
        ncap_client.start()
        time.sleep(.5)

        msgs = ['7211,1234,1,2,100,0']
        expected_response = (7211, 0, 1234, 1, 2, 1024)

        for msg in msgs:
            ncap_client.network_interface.send_message(
                                        mto=ncap.jid, mbody=msg, mtype='chat')

            time.sleep(.5)

        ncap_client.stop()
        ncap.stop()
        self.assertEqual(expected_response, self.actual_response)

    def test_client_can_write_sample_data(self):
        """ Test that a client can write a Sample from
        a channel of a TIM """

        def open_mock(tim_id, channel_id):
            trans_comm_id = 1
            return trans_comm_id

        self.result = []

        def write_data_mock(trans_comm_id, timeout,
                            sampling_mode, sample_value):
            self.result.append(sample_value)

        def client_on_data(msg):
            resp = network_interface.NetworkClient.parse_inbound(msg['body'])
            self.actual_response = resp

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.write_data.side_effect = write_data_mock

        tdas = transducer_data_access_services.TransducerDataAccessServices()
        tdas.register_transducer_access_service(tdaccs)

        roster_path = 'tests/testroster.xml'
        ncap = ncaplite.NCAP(12345)
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices(roster_path)
        ncap.register_discovery_service(discovery)
        ncap.register_transducer_data_access_service(tdas)

        ncap_client = ncaplite.NCAP(67890)
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))

        # monkey-patch the data received method
        ncap_client.on_network_if_message = client_on_data

        ncap_client.register_network_interface(client_if)

        ncap.start()
        ncap_client.start()
        time.sleep(.5)

        msgs = ('7217,1234,1,2,100,0,1024',
                '7217,1234,1,2,100,0,1025',
                '7217,1234,1,2,100,0,1026')

        expected_response = (7217, 0, 1234, 1, 2)
        expected_write_out = [1024, 1025, 1026]

        for msg in msgs:
            ncap_client.network_interface.send_message(
                                        mto=ncap.jid, mbody=msg, mtype='chat')

            time.sleep(.5)
            self.assertEqual(expected_response, self.actual_response)

        ncap_client.stop()
        ncap.stop()

        self.assertEqual(expected_write_out, self.result)

    def test_client_can_read_block_data(self):
        """ Test that a client can read a block of sample data from
        a channel of a TIM """

        self.actual_response = (0, 0, 0)

        def open_mock(tim_id, channel_id):
            trans_comm_id = 1
            return trans_comm_id

        def read_data_mock(trans_comm_id, timeout,
                           sampling_mode, result):
            result.append(read_data_mock.count)
            read_data_mock.count = read_data_mock.count+1
        read_data_mock.count = 1024

        def client_on_data(msg):
            resp = network_interface.NetworkClient.parse_inbound(msg['body'])
            self.actual_response = resp

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.read_data.side_effect = read_data_mock

        tdas = transducer_data_access_services.TransducerDataAccessServices()
        tdas.register_transducer_access_service(tdaccs)

        roster_path = 'tests/testroster.xml'
        ncap = ncaplite.NCAP(12345)
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices(roster_path)
        ncap.register_discovery_service(discovery)
        ncap.register_transducer_data_access_service(tdas)

        ncap_client = ncaplite.NCAP(67890)
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))

        # monkey-patch the data received method
        ncap_client.on_network_if_message = client_on_data

        ncap_client.register_network_interface(client_if)

        ncap.start()
        ncap_client.start()
        time.sleep(.5)

        msgs = ['7212,1234,1,2,100,3,.1,0']
        expected_response = (7212, 0, 1234, 1, 2, [1024, 1025, 1026])

        for msg in msgs:
            ncap_client.network_interface.send_message(
                                        mto=ncap.jid, mbody=msg, mtype='chat')

            time.sleep(.5)

        ncap_client.stop()
        ncap.stop()
        self.assertEqual(expected_response, self.actual_response)

    def test_client_can_read_sample_data_from_multiple_channels(self):
        """ Test that a client can read sample data from multiple channels
        of a TIM """

        self.actual_response = (0, 0, 0)
        self.out_data = {1: 1024, 2: 1025, 3: 1026}
        self.transducer_interfaces = {
                                      1: (1, 1),  # comm_id0 : tim_id0, chanid0
                                      2: (1, 2),  # comm_id1 : tim_id0, chanid1
                                      3: (1, 3),  # comm_id2 : tim_id1, chanid0
                                      }

        def find_com_id(tim_id, channel_id):
            """ Simple helper function to find trans_comm_id given
            a tim_id and channel_id. Assumes 0 is not a valid trans_comm_id.
            """
            for comid, tim in self.transducer_interfaces.iteritems():
                if tim == (tim_id, channel_id):
                    return comid
            return 0  # assumes 0 not valid comid

        def open_mock(tim_id, channel_id):
            trans_comm_id = find_com_id(tim_id, channel_id)
            return trans_comm_id

        def read_data_mock(trans_comm_id, timeout,
                           sampling_mode, result):
            data = self.out_data[trans_comm_id]
            result.append(data)
            data = data+1
            self.out_data[trans_comm_id] = data
            return 0

        def client_on_data(msg):
            resp = network_interface.NetworkClient.parse_inbound(msg['body'])
            self.actual_response = resp

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.read_data.side_effect = read_data_mock

        tdas = transducer_data_access_services.TransducerDataAccessServices()
        tdas.register_transducer_access_service(tdaccs)

        roster_path = 'tests/testroster.xml'
        ncap = ncaplite.NCAP(12345)
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices(roster_path)
        ncap.register_discovery_service(discovery)
        ncap.register_transducer_data_access_service(tdas)

        ncap_client = ncaplite.NCAP(67890)
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))

        # monkey-patch the data received method
        ncap_client.on_network_if_message = client_on_data

        ncap_client.register_network_interface(client_if)

        ncap.start()
        ncap_client.start()
        time.sleep(.5)

        msgs = ['7213,1234,1,1;2;3,100,5']
        expected_response = (7213, 0, 1234, 1, [1, 2, 3], [1024, 1025, 1026])

        for msg in msgs:
            ncap_client.network_interface.send_message(
                                        mto=ncap.jid, mbody=msg, mtype='chat')

            time.sleep(.5)

        ncap_client.stop()
        ncap.stop()
        self.assertEqual(expected_response, self.actual_response)

    def test_client_can_read_block_data_from_multiple_channels(self):
        """ Test that a client can read sample data from multiple channels
        of a TIM """

        self.actual_response = (0, 0, 0)
        self.out_data = {1: 1024, 2: 1024, 3: 1024}
        self.transducer_interfaces = {
                                      1: (1, 1),  # comm_id0 : tim_id0, chanid0
                                      2: (1, 2),  # comm_id1 : tim_id0, chanid1
                                      3: (1, 3),  # comm_id2 : tim_id1, chanid0
                                      }

        def find_com_id(tim_id, channel_id):
            """ Simple helper function to find trans_comm_id given
            a tim_id and channel_id. Assumes 0 is not a valid trans_comm_id.
            """
            for comid, tim in self.transducer_interfaces.iteritems():
                if tim == (tim_id, channel_id):
                    return comid
            return 0  # assumes 0 not valid comid

        def open_mock(tim_id, channel_id):
            trans_comm_id = find_com_id(tim_id, channel_id)
            return trans_comm_id

        def read_data_mock(trans_comm_id, timeout,
                           sampling_mode, result):
            data = self.out_data[trans_comm_id]
            result.append(data)
            data = data+1
            self.out_data[trans_comm_id] = data
            return 0

        def client_on_data(msg):
            resp = network_interface.NetworkClient.parse_inbound(msg['body'])
            self.actual_response = resp

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.read_data.side_effect = read_data_mock

        tdas = transducer_data_access_services.TransducerDataAccessServices()
        tdas.register_transducer_access_service(tdaccs)

        roster_path = 'tests/testroster.xml'
        ncap = ncaplite.NCAP(12345)
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices(roster_path)
        ncap.register_discovery_service(discovery)
        ncap.register_transducer_data_access_service(tdas)

        ncap_client = ncaplite.NCAP(67890)
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))

        # monkey-patch the data received method
        ncap_client.on_network_if_message = client_on_data

        ncap_client.register_network_interface(client_if)

        ncap.start()
        ncap_client.start()
        time.sleep(.5)

        msgs = ['7214,1234,1,1;2;3,100,3,0.1,0.1']
        expected_response = (7214, 0, 1234, 1, [1, 2, 3], [1024, 1025, 1026,
                                                           1024, 1025, 1026,
                                                           1024, 1025, 1026])

        for msg in msgs:
            ncap_client.network_interface.send_message(
                                        mto=ncap.jid, mbody=msg, mtype='chat')

            time.sleep(1.5)

        ncap_client.stop()
        ncap.stop()
        self.assertEqual(expected_response, self.actual_response)

    def test_client_can_write_block_data(self):
        """ Test that a client can write block data to
        a channel of a TIM """

        def open_mock(tim_id, channel_id):
            trans_comm_id = 1
            return trans_comm_id

        self.result = []

        def write_data_mock(trans_comm_id, timeout,
                            sampling_mode, sample_value):
            self.result.append(sample_value)

        def client_on_data(msg):
            resp = network_interface.NetworkClient.parse_inbound(msg['body'])
            self.actual_response = resp

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.write_data.side_effect = write_data_mock

        tdas = transducer_data_access_services.TransducerDataAccessServices()
        tdas.register_transducer_access_service(tdaccs)

        roster_path = 'tests/testroster.xml'
        ncap = ncaplite.NCAP(12345)
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices(roster_path)
        ncap.register_discovery_service(discovery)
        ncap.register_transducer_data_access_service(tdas)

        ncap_client = ncaplite.NCAP(67890)
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))

        # monkey-patch the data received method
        ncap_client.on_network_if_message = client_on_data

        ncap_client.register_network_interface(client_if)

        ncap.start()
        ncap_client.start()
        time.sleep(.5)

        msgs = ('7218,1234,1,2,100,3,0.1,0.1,1024;1025;1026',)

        expected_response = (7218, 0, 1234, 1, 2)
        expected_write_out = [1024, 1025, 1026]

        for msg in msgs:
            ncap_client.network_interface.send_message(
                                        mto=ncap.jid, mbody=msg, mtype='chat')

            time.sleep(1)
            self.assertEqual(expected_response, self.actual_response)

        ncap_client.stop()
        ncap.stop()

        self.assertEqual(expected_write_out, self.result)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
