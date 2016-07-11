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
from ncaplite import ieee1451types as ieee1451
from ncaplite import simple_json_codec
from ncaplite import teds_access_services
from ncaplite import teds_support
import mock
import time
import xml.etree.ElementTree as ET
import os
import logging
import logging.config


logger = logging.getLogger(__name__)


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
            logging.basicConfig(filename="ncaplite.log", level=logging.DEBUG)

        # generate a roster xml file for testing
        root = ET.Element("roster")
        tree = ET.ElementTree(root)
        tree.write("tests/testroster.xml")
        self.codec = simple_json_codec.SimpleJsonCodec()

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
        ncap = ncaplite.NCAP()
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        network_if.codec = simple_json_codec.SimpleJsonCodec()
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices()
        discovery.open_roster(roster_path)
        ncap.register_discovery_service(discovery)

        ncap_client = ncaplite.NCAP()
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))
        client_if.codec = simple_json_codec.SimpleJsonCodec()
        ncap_client.register_network_interface(client_if)

        ncap.start()
        ncap_client.start()
        msgs = [[7108, {'client_id': client_jid}], [7109, {'client_id': client_jid}]]
        expected_roster_status = [1, 0]
        actual_roster_status = []

        time.sleep(.5)

        for m in msgs:

            msg = client_if.codec.encode(m)
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

    def test_client_can_read_sample_json(self):
        """ Test that a client can read a Sample from a channel of a TIM json.
        """

        def open_mock(tim_id, channel_id):
            error_code = ieee1451.Error(
                                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                ieee1451.ErrorCode.NO_ERROR)
            trans_comm_id = 1
            result = {'error_code': error_code, 'trans_comm_id': trans_comm_id}
            return result

        def read_data_mock(trans_comm_id, timeout,
                           sampling_mode):
            error_code = ieee1451.Error(
                                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                ieee1451.ErrorCode.NO_ERROR)
            tc = ieee1451.TypeCode.UINT32_TC
            value = 1024
            arg = ieee1451.Argument(tc, value)
            arg_array = ieee1451.ArgumentArray()
            arg_array.put_by_index(0, arg)

            result = {'error_code': error_code, 'result': arg_array}
            return result

        def client_on_data(msg):
            resp = self.codec.decode(msg['body'])
            self.actual_response = resp
        self.codec = simple_json_codec.SimpleJsonCodec()

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.read_data.side_effect = read_data_mock

        tdas = transducer_data_access_services.TransducerDataAccessServices()
        tdas.register_transducer_access_service(tdaccs)

        roster_path = 'tests/testroster.xml'
        ncap = ncaplite.NCAP()
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        network_if.codec = simple_json_codec.SimpleJsonCodec()
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices()
        discovery.open_roster(roster_path)
        ncap.register_discovery_service(discovery)
        ncap.register_transducer_data_access_service(tdas)

        ncap_client = ncaplite.NCAP()
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))
        client_if.codec = simple_json_codec.SimpleJsonCodec()

        # monkey-patch the data received method
        ncap_client.on_network_if_message = client_on_data

        ncap_client.register_network_interface(client_if)

        ncap.start()
        ncap_client.start()
        time.sleep(.5)

        request = [7211, {
                'ncap_id': 1234,
                'tim_id': 1,
                'channel_id': 2,
                'timeout': ieee1451.TimeDuration(0, 1000),
                'sampling_mode': 0}]

        ec = ieee1451.Error(
                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                ieee1451.ErrorCode.NO_ERROR)

        aa = ieee1451.ArgumentArray()
        arg = ieee1451.Argument(ieee1451.TypeCode.UINT32_TC,
                                1024)
        aa.put_by_index(0, arg)

        expected_response = [7211, {
                                'error_code': ec,
                                'ncap_id': 1234,
                                'tim_id': 1,
                                'channel_id': 2,
                                'sample_data': aa
                                }]

        msg = ncap_client.network_interface.codec.encode(request)
        ncap_client.network_interface.send_message(
                                    mto=ncap.jid, mbody=msg, mtype='chat')
        time.sleep(.5)

        ncap_client.stop()
        ncap.stop()

        self.assertEqual(expected_response, self.actual_response)

    def test_client_can_write_sample_json(self):
        """ Test that a client can write a Sample from
        a channel of a TIM """

        def open_mock(tim_id, channel_id):
            error_code = ieee1451.Error(
                                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                ieee1451.ErrorCode.NO_ERROR)
            trans_comm_id = 1
            result = {'error_code': error_code, 'trans_comm_id': trans_comm_id}
            return result

        self.result = []

        def write_data_mock(trans_comm_id, timeout,
                            sampling_mode, sample_value):
            error_code = ieee1451.Error(
                                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                ieee1451.ErrorCode.NO_ERROR)
            self.result.append(sample_value)
            return {'error_code': error_code}

        def client_on_data(msg):
            resp = self.codec.decode(msg['body'])
            self.actual_response = resp
        self.codec = simple_json_codec.SimpleJsonCodec()

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.write_data.side_effect = write_data_mock

        tdas = transducer_data_access_services.TransducerDataAccessServices()
        tdas.register_transducer_access_service(tdaccs)

        roster_path = 'tests/testroster.xml'
        ncap = ncaplite.NCAP()
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        network_if.codec = simple_json_codec.SimpleJsonCodec()
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices()
        discovery.open_roster(roster_path)
        ncap.register_discovery_service(discovery)
        ncap.register_transducer_data_access_service(tdas)

        ncap_client = ncaplite.NCAP()
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))
        client_if.codec = simple_json_codec.SimpleJsonCodec()

        # monkey-patch the data received method
        ncap_client.on_network_if_message = client_on_data

        ncap_client.register_network_interface(client_if)

        ncap.start()
        ncap_client.start()
        time.sleep(.5)

        ec = ieee1451.Error(
        ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
        ieee1451.ErrorCode.NO_ERROR)

        aa = ieee1451.ArgumentArray()
        arg = ieee1451.Argument(ieee1451.TypeCode.UINT32_TC,
                                1024)
        aa.put_by_index(0, arg)

        request = [7217, {
            'ncap_id': 1234,
            'tim_id': 1,
            'channel_id': 2,
            'timeout': ieee1451.TimeDuration(0, 1000),
            'sampling_mode': 0,
            'sample_data': aa
        }]

        expected_response =[7217, {
            'error_code': ec,
            'ncap_id': 1234,
            'tim_id': 1,
            'channel_id': 2,
        }]

        msg = ncap_client.network_interface.codec.encode(request)
        ncap_client.network_interface.send_message(
                                    mto=ncap.jid, mbody=msg, mtype='chat')

        time.sleep(.5)
        ncap_client.stop()
        ncap.stop()

        self.assertEqual(expected_response, self.actual_response)
        self.assertEqual(self.result[0], request[1]['sample_data'])

    def test_client_tim_discover(self):
        """ Test that the client can discover tims connected to the ncap
        """

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

        def client_on_data(msg):
            resp = self.codec.decode(msg['body'])
            self.actual_response = resp

        tdisco = mock.Mock(spec=transducer_services_base.TimDiscoveryBase)
        tdisco.report_comm_module.side_effect = report_comm_module_mock
        tdisco.report_tims.side_effect = report_tims_mock

        roster_path = 'tests/testroster.xml'
        ncap = ncaplite.NCAP()
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        network_if.codec = simple_json_codec.SimpleJsonCodec()
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices()
        discovery.open_roster(roster_path)
        ncap.register_discovery_service(discovery)
        discovery.register_transducer_access_service(tdisco)

        ncap_client = ncaplite.NCAP()
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))
        client_if.codec = simple_json_codec.SimpleJsonCodec()

        # monkey-patch the data received method
        ncap_client.on_network_if_message = client_on_data

        ncap_client.register_network_interface(client_if)


        request = [716, {'ncap_id': 1234,}]

        ec = ieee1451.Error(
        ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
        ieee1451.ErrorCode.NO_ERROR)
        num_of_tim = 3
        tim_ids = [1, 2, 3]
        expected_response = [716, {'error_code': ec,
                                   'num_of_tim': num_of_tim,
                                   'tim_ids': tim_ids}]

        ncap.start()
        ncap_client.start()
        time.sleep(.5)

        msg = ncap_client.network_interface.codec.encode(request)
        ncap_client.network_interface.send_message(
                                    mto=ncap.jid, mbody=msg, mtype='chat')
        time.sleep(.5)

        ncap_client.stop()
        ncap.stop()

        self.assertEqual(expected_response, self.actual_response)

    def test_client_transducer_discover(self):
        """ Test that the client can discover transducers connected to a tim
        """

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

        def client_on_data(msg):
            resp = self.codec.decode(msg['body'])
            self.actual_response = resp

        tdisco = mock.Mock(spec=transducer_services_base.TimDiscoveryBase)
        tdisco.report_channels.side_effect = report_channels_mock


        roster_path = 'tests/testroster.xml'
        ncap = ncaplite.NCAP()
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        network_if.codec = simple_json_codec.SimpleJsonCodec()
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices()
        discovery.open_roster(roster_path)
        ncap.register_discovery_service(discovery)
        discovery.register_transducer_access_service(tdisco)

        ncap_client = ncaplite.NCAP()
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))
        client_if.codec = simple_json_codec.SimpleJsonCodec()

        # monkey-patch the data received method
        ncap_client.on_network_if_message = client_on_data

        ncap_client.register_network_interface(client_if)


        request = [717, {'ncap_id': 1234,'tim_id': 1}]

        ec = ieee1451.Error(
        ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
        ieee1451.ErrorCode.NO_ERROR)

        tim_id = 1
        num_trans_channels = 3
        trans_channel_ids = [1, 2, 3]
        trans_channel_names = ["Channel1", "Channel2", "Channel3"]

        expected_response = [717, {'error_code': ec,
                            'ncap_id': 1234,
                            'tim_id': tim_id,
                            'num_of_transducer_channels': num_trans_channels,
                            'trans_channel_ids': trans_channel_ids,
                            'trans_channel_names': trans_channel_names}]

        ncap.start()
        ncap_client.start()
        time.sleep(.5)

        msg = ncap_client.network_interface.codec.encode(request)
        ncap_client.network_interface.send_message(
                                    mto=ncap.jid, mbody=msg, mtype='chat')
        time.sleep(.5)

        ncap_client.stop()
        ncap.stop()

        self.assertEqual(expected_response, self.actual_response)

    def test_client_can_read_transducer_channel_teds(self):
        """ Test that a client can read a transducer channel TEDS."""
        def open_mock(tim_id, channel_id):
            error_code = ieee1451.Error(
                    ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                    ieee1451.ErrorCode.NO_ERROR)
            trans_comm_id = 1
            return {'error_code': error_code, 'trans_comm_id': trans_comm_id}

        def close_mock(trans_comm_id):
            error_code = ieee1451.Error(
                    ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                    ieee1451.ErrorCode.NO_ERROR)
            return {'error_code': error_code}

        def update_teds_cache_mock(trans_comm_id, timeout, teds_type):
            error_code = ieee1451.Error(
                    ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                    ieee1451.ErrorCode.NO_ERROR)
            xmlpath = 'tests/SmartTransducerTEDSMock.xml'
            xmlns = {'teds': 'http://localhost/1451HTTPAPI'}
            teds_types ={teds_support.TEDSType.CHAN_TEDS: "teds:TransducerChannelTEDS",
                         teds_support.TEDSType.XDCR_NAME: "teds:UserTransducerNameTEDS"}
            tc_dict = dict()
            for k, v in iter(teds_types.items()):
                my_teds = teds_support.teds_element_from_file(v, xmlns, xmlpath)
                tc_dict[k] = my_teds[0]
            self.tedcash[trans_comm_id] = tc_dict
            return {'error_code': error_code}
        self.tedcash = dict()

        def read_teds_mock(trans_comm_id, timeout, teds_type):
            error_code = ieee1451.Error(
                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                ieee1451.ErrorCode.NO_ERROR)
            ted = self.tedcash[trans_comm_id][teds_type]
            tc = ieee1451.TypeCode.STRING_TC
            value = ted
            arg = ieee1451.Argument(tc, value)
            arg_array = ieee1451.ArgumentArray()
            arg_array.put_by_index(0, arg)
            return {'error_code': error_code, 'teds': arg_array}

        def client_on_data(msg):
            resp = self.codec.decode(msg['body'])
            self.actual_response = resp
        self.codec = simple_json_codec.SimpleJsonCodec()

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.close.side_effect = close_mock

        tedsmgr = mock.Mock(spec=transducer_services_base.TedsManagerBase)
        tedsmgr.update_teds_cache.side_effect = update_teds_cache_mock
        tedsmgr.read_teds.side_effect = read_teds_mock

        teds_svc = teds_access_services.TEDSAccessServices()
        teds_svc.register_transducer_access_service(tdaccs)
        teds_svc.register_teds_manager(tedsmgr)

        roster_path = 'tests/testroster.xml'
        ncap = ncaplite.NCAP()
        ncap.load_config(self.config_file_path)
        network_if = network_interface.NetworkClient(
                ncap.jid, ncap.password, (ncap.broker_ip, ncap.broker_port))
        network_if.codec = simple_json_codec.SimpleJsonCodec()
        ncap.register_network_interface(network_if)
        discovery = discovery_services.DiscoveryServices()
        discovery.open_roster(roster_path)
        ncap.register_discovery_service(discovery)
        ncap.register_teds_access_service(teds_svc)

        ncap_client = ncaplite.NCAP()
        ncap_client.type = "client"
        client_jid = 'unittest@ncaplite.loc'
        client_password = 'mypassword'
        client_if = network_interface.NetworkClient(
            client_jid, client_password, (ncap.broker_ip, ncap.broker_port))
        client_if.codec = simple_json_codec.SimpleJsonCodec()

        # monkey-patch the data received method
        ncap_client.on_network_if_message = client_on_data

        ncap_client.register_network_interface(client_if)

        ncap.start()
        ncap_client.start()
        time.sleep(.5)

        request = [732, {
                'ncap_id': 1234,
                'tim_id': 1,
                'channel_id': 2,
                'timeout': ieee1451.TimeDuration(1, 0000)}]

        ec = ieee1451.Error(
                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                ieee1451.ErrorCode.NO_ERROR)

        aa = ieee1451.ArgumentArray()

        xmlpath = 'tests/SmartTransducerTEDSMock.xml'
        xmlns = {'teds': 'http://localhost/1451HTTPAPI'}
        tc_teds_list = teds_support.teds_element_from_file('teds:TransducerChannelTEDS', xmlns, xmlpath)
        expected_teds_text = tc_teds_list[0]

        arg = ieee1451.Argument(ieee1451.TypeCode.STRING_TC,
                                expected_teds_text)
        aa.put_by_index(0, arg)

        expected_response = [732, {
                                'error_code': ec,
                                'transducer_channel_teds': aa
                                }]

        msg = ncap_client.network_interface.codec.encode(request)
        ncap_client.network_interface.send_message(
                                    mto=ncap.jid, mbody=msg, mtype='chat')
        time.sleep(.5)

        ncap_client.stop()
        ncap.stop()

        self.assertEqual(expected_response, self.actual_response)

        expected_teds_dict = teds_support.teds_dict_from_xml(expected_teds_text)
        actual_teds_dict = teds_support.teds_dict_from_xml(self.actual_response[1]\
                                                               ['transducer_channel_teds'].get_by_index(0).value)

        self.assertEqual(expected_teds_dict, actual_teds_dict)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
