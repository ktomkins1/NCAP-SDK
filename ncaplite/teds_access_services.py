"""
.. module:: teds_access_services
   :platform: Unix, Windows
   :synopsis: Defines services used to reading and writing TEDs information via the NCAP

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
# -*- coding: utf-8 -*-
import ieee1451types as ieee1451
import teds_support

class TEDSAccessServices(object):

    def __init__(self):
        """Initialize the TEDSAccessServices object."""
        self.transducer_access = None
        self.teds_manager = None

    def register_transducer_access_service(self, transducer_access):
        """Register an object that implements the TransducerAccess interface with the TEDSAccessService"""
        self.transducer_access = transducer_access


    def register_teds_manager(self, teds_manager):
        """Register an object that implements the TEDSManager interface with the TEDSAccessService"""
        self.teds_manager = teds_manager

    def read_transducer_channel_teds(self, ncap_id, tim_id, channel_id, timeout):
        """

        :param ncap_id: the NCAP ID
        :param tim_id:  the TIM ID
        :param channel_id: the Transducer Channel ID
        :param timeout: TimeDuration indicating the timeout duration
        :return: a dictionary containing:
            error_code: an ErrorCode object
            transducer_channel_teds: An ArgumentArray containing the TransducerChannelTEDS information
        """

        error_code = ieee1451.Error(
                            ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)

        opened = self.transducer_access.open(tim_id,
                                             channel_id)

        trans_comm_id = opened['trans_comm_id']
        error = opened['error_code']

        teds_type = teds_support.TEDSType.CHAN_TEDS

        utcres = self.teds_manager.update_teds_cache(trans_comm_id, timeout, teds_type)
        error = utcres['error_code']

        rtres = self.teds_manager.read_teds(trans_comm_id, timeout, teds_type)
        error = rtres['error_code']
        transducer_channel_teds = rtres['teds']

        self.transducer_access.close(trans_comm_id)

        result = {'error_code': error,
                  'transducer_channel_teds': transducer_channel_teds}

        return result
