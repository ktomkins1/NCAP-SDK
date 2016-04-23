"""
.. module:: transducer_data_access_services
   :platform: Unix, Windows
   :synopsis: Defines Discovery Services for ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""


class TransducerDataAccessServices(object):
    """TransducerDataAccessServices"""
    def __init__(self, name="Transducer Data Access Services"):
        self.name = name

    def register_transducer_access_service(self, transducer_access):
        """ registter a TimDiscovery service object with
            the TransducerDataAccessServices object."""
        self.transducer_access = transducer_access

    def read_transducer_sample_data_from_a_channel_of_a_tim(self,
                                                            ncap_id,
                                                            tim_id,
                                                            channel_id,
                                                            timeout,
                                                            sampling_mode):

        """
        Read a single sensor data from a channel of a TIM

        Args:
            ncap_id: ID of the NCAP application being queried
            tim_id: ID of the TIM being queried
            channel_id:
        """
        data = []
        trans_comm_id = self.transducer_access.open(tim_id, channel_id)
        self.transducer_access.read_data(trans_comm_id, timeout,
                                         sampling_mode, data)
        self.transducer_access.close(trans_comm_id)
        error_code = 0

        return {'error_code': error_code, 'ncap_id': ncap_id, "tim_id": tim_id,
                'channel_id': channel_id, 'data': data}
