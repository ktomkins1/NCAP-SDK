#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_transducer_data_access_services
----------------------------------

Tests for `transducer_data_access_services` module.
"""

import unittest
import mock
import time
from ncaplite import transducer_data_access_services
from ncaplite import transducer_services_base


class TestTransducerDataAccessServices(unittest.TestCase):
    """This class defines the test runner for Discovery Services"""
    def setUp(self):
        """Setup for unit tests"""
        pass

    def tearDown(self):
        """Teardown for unit tests"""
        pass

    def test_read_transducer_sample_data_from_a_channel_of_a_tim(self):
        """ Test reading transducer sample from channel of a tim """

        # mock version of the TransducerAccess.open function
        def open_mock(tim_id, channel_id):
            trans_comm_id = 1
            return trans_comm_id

        def read_data_mock(trans_comm_id, timeout,
                           sampling_mode, result):
            result.append(1024)

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.read_data.side_effect = read_data_mock

        tdas = transducer_data_access_services.TransducerDataAccessServices()
        tdas.register_transducer_access_service(tdaccs)

        request = {
                'ncap_id': 1234,
                'tim_id': 01,
                'channel_id': 01,
                'timeout': 100,
                'sampling_mode': 0
                }

        expected_response = (0, 1234, 1, 1, [1024])
        response = tdas.read_transducer_sample_data_from_a_channel_of_a_tim(
                                                    request['ncap_id'],
                                                    request['tim_id'],
                                                    request['channel_id'],
                                                    request['timeout'],
                                                    request['sampling_mode'],
                                                    )

        tdaccs.open.assert_called_with(01, 01)
        tdaccs.read_data.assert_called_with(1, 100, 0, mock.ANY)
        self.assertEqual(expected_response, response)

    def test_read_transducer_block_data_from_a_channel_of_a_tim(self):
        """ Test reading transducer block data channel of a tim. """

        def open_mock(tim_id, channel_id):
            trans_comm_id = 1
            return trans_comm_id

        def read_data_mock(trans_comm_id, timeout,
                           sampling_mode, result):
            result.append(read_data_mock.count)
            read_data_mock.count = read_data_mock.count+1
        read_data_mock.count = 1024

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.read_data.side_effect = read_data_mock

        tdas = transducer_data_access_services.TransducerDataAccessServices()
        tdas.register_transducer_access_service(tdaccs)

        request = {
                   'ncap_id': 1234,
                   'tim_id': 01,
                   'channel_id': 02,
                   'timeout': 100,
                   'number_of_samples': 3,
                   'sample_interval': 1,
                   'start_time': 0
                }

        expected_response = (0, 1234, 1, 2, [1024, 1025, 1026])
        t_expected = 3

        t_start = time.time()
        response = tdas.read_transducer_block_data_from_a_channel_of_a_tim(
                                                request['ncap_id'],
                                                request['tim_id'],
                                                request['channel_id'],
                                                request['timeout'],
                                                request['number_of_samples'],
                                                request['sample_interval'],
                                                request['start_time']
                                                )
        t_end = time.time()
        t_actual = int(t_end - t_start)
        tdaccs.open.assert_called_with(01, 02)
        tdaccs.read_data.assert_called_with(1, 100, 5, mock.ANY)
        self.assertEqual(t_expected, t_actual)
        self.assertEqual(expected_response, response)
