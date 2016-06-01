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
from ncaplite import ieee1451types as ieee1451

class TestTransducerDataAccessServices(unittest.TestCase):
    """This class defines the test runner for Discovery Services"""
    def setUp(self):
        """Setup for unit tests"""
        self.no_error = ieee1451.Error(
                                     ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                     ieee1451.ErrorCode.NO_ERROR)
        pass

    def tearDown(self):
        """Teardown for unit tests"""
        pass

    def test_read_transducer_sample_data_from_a_channel_of_a_tim(self):
        """ Test reading transducer sample from channel of a tim """

        # mock version of the TransducerAccess.open function
        def open_mock(tim_id, channel_id):
            error_code = ieee1451.Error(
                                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                ieee1451.ErrorCode.NO_ERROR)
            trans_comm_id = 1
            print("open mock")
            return (error_code, trans_comm_id)

        def read_data_mock(trans_comm_id, timeout,
                       sampling_mode):
            error_code = ieee1451.Error(
                                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                ieee1451.ErrorCode.NO_ERROR)
            result = 1024
            print("read mock")
            return (error_code, result)

        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.read_data.side_effect = read_data_mock

        tdas = transducer_data_access_services.TransducerDataAccessServices()
        tdas.register_transducer_access_service(tdaccs)

        request = {
                'ncap_id': 1234,
                'tim_id': 01,
                'channel_id': 01,
                'timeout': ieee1451.TimeDuration(0,1000),
                'sampling_mode': 0
                }

        expected_response = (self.no_error, 1234, 1, 1, 1024)
        response = tdas.read_transducer_sample_data_from_a_channel_of_a_tim(
                                                    request['ncap_id'],
                                                    request['tim_id'],
                                                    request['channel_id'],
                                                    request['timeout'],
                                                    request['sampling_mode'],
                                                    )

        tdaccs.open.assert_called_with(01, 01)
        tdaccs.read_data.assert_called_with(1,
                                            ieee1451.TimeDuration(0,1000),
                                            0)
        self.assertEqual(expected_response, response)

    def test_write_transducer_sample_data_to_a_channel_of_a_tim(self):
        """ Test writing transducer sample data to a channel of a tim """

        # mock version of the TransducerAccess.open function
        def open_mock(tim_id, channel_id):
            error_code = ieee1451.Error(
                                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                ieee1451.ErrorCode.NO_ERROR)
            trans_comm_id = 1
            return (error_code, trans_comm_id)

        self.result = []

        def write_data_mock(trans_comm_id, timeout,
                            sampling_mode, value):
            error_code = ieee1451.Error(
                                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                ieee1451.ErrorCode.NO_ERROR)
            self.result.append(value)
            return error_code


        tdaccs = mock.Mock(spec=transducer_services_base.TransducerAccessBase)
        tdaccs.open.side_effect = open_mock
        tdaccs.write_data.side_effect = write_data_mock

        tdas = transducer_data_access_services.TransducerDataAccessServices()
        tdas.register_transducer_access_service(tdaccs)

        request = {
                'ncap_id': 1234,
                'tim_id': 01,
                'channel_id': 01,
                'timeout': ieee1451.TimeDuration(0,1000),
                'sampling_mode': 0,
                }

        expected_response = (self.no_error, 1234, 1, 1)
        expected_output = [1024, 1025, 1026]

        for sample in expected_output:
            response = tdas.\
                        write_transducer_sample_data_to_a_channel_of_a_tim(
                                                    request['ncap_id'],
                                                    request['tim_id'],
                                                    request['channel_id'],
                                                    request['timeout'],
                                                    request['sampling_mode'],
                                                    sample
                                                    )

        tdaccs.open.assert_called_with(01, 01)
        tdaccs.write_data.assert_called_with(1, ieee1451.TimeDuration(0,1000),
                                             0, mock.ANY)
        self.assertEqual(expected_response, response)
        self.assertEqual(expected_output, self.result)

if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
