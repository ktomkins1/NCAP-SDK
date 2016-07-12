"""
test_teds_access_services
----------------------------------

Tests for `teds` module.
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import mock
from ncaplite import ieee1451types as ieee1451
from ncaplite import teds_support
from ncaplite import teds_access_services
from ncaplite import transducer_services_base


class TestTEDSAccessServices(unittest.TestCase):
    """TestCase for TEDS Access Services."""

    def test_read_transducer_channel_teds(self):
        """Test service for reading TransducerChannel TEDS."""
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

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.close.side_effect = close_mock

        tedsmgr = mock.Mock(spec=transducer_services_base.TedsManagerBase)
        tedsmgr.update_teds_cache.side_effect = update_teds_cache_mock
        tedsmgr.read_teds.side_effect = read_teds_mock

        tedsvc = teds_access_services.TEDSAccessServices()
        tedsvc.register_transducer_access_service(tdaccs)
        tedsvc.register_teds_manager(tedsmgr)

        xmlpath = 'tests/SmartTransducerTEDSMock.xml'
        xmlns = {'teds': 'http://localhost/1451HTTPAPI'}
        tc_teds_list = teds_support.teds_element_from_file('teds:TransducerChannelTEDS', xmlns, xmlpath)
        expected = teds_support.teds_dict_from_xml(tc_teds_list[0])

        args = {"ncap_id": 1234,
                "tim_id": 1,
                "channel_id": 1,
                "timeout": ieee1451.TimeDuration(secs=1, nsecs=0)
                }


        result = tedsvc.read_transducer_channel_teds(**args)

        tcted_arg_array = result['transducer_channel_teds']
        tcted = tcted_arg_array.get_by_index(0).value
        ted_dict = teds_support.teds_dict_from_xml(tcted)

        self.assertEqual(ted_dict, expected)

    def test_read_user_transducer_name_teds(self):
        """ Test reading UserTransducerNameTEDS
        """
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

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.close.side_effect = close_mock

        tedsmgr = mock.Mock(spec=transducer_services_base.TedsManagerBase)
        tedsmgr.update_teds_cache.side_effect = update_teds_cache_mock
        tedsmgr.read_teds.side_effect = read_teds_mock

        tedsvc = teds_access_services.TEDSAccessServices()
        tedsvc.register_transducer_access_service(tdaccs)
        tedsvc.register_teds_manager(tedsmgr)

        xmlpath = 'tests/SmartTransducerTEDSMock.xml'
        xmlns = {'teds': 'http://localhost/1451HTTPAPI'}
        tc_teds_list = teds_support.teds_element_from_file('teds:UserTransducerNameTEDS', xmlns, xmlpath)
        expected = teds_support.teds_dict_from_xml(tc_teds_list[0])

        args = {"ncap_id": 1234,
                "tim_id": 1,
                "channel_id": 1,
                "timeout": ieee1451.TimeDuration(secs=1, nsecs=0)
                }


        result = tedsvc.read_user_transducer_name_teds(**args)

        tcted_arg_array = result['transducer_name_teds']
        tcted = tcted_arg_array.get_by_index(0).value
        ted_dict = teds_support.teds_dict_from_xml(tcted)

        self.assertEqual(ted_dict, expected)

if __name__ == '__main__':
    unittest.main()
