"""
.. module:: transducer_data_access_services
   :platform: Unix, Windows
   :synopsis: Defines Discovery Services for ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
import ieee1451types as ieee1451


class TransducerDataAccessServices(object):
    """
    Transducer Data Access Services for NCAP.

    This class defines the Transducer Access Services
    exposed by the NCAP.
    """

    def __init__(self, name="Transducer Data Access Services"):
        """Initialize the TransducerDataAccessServices object."""
        self.name = name

    def register_transducer_access_service(self, transducer_access):
        """Register a TimDiscovery service object with the\
        TransducerDataAccessServices object."""
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
            channel_id: the channel ID of the TIM
            timeout: The timeout interval before reporting a timeout error_code
            sampling_mode: The sampling mode selection

        Returns: A tuple containing the following:
            error_code: an error code
            ncap_id: the ncap id
            tim_id: the id of the tim that was read
            channel_id: the id of the channel read from the TIM
            sample_data: the block of sample data given as a list
        """
        sample_data = []
        error_code = ieee1451.Error(
                            ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)

        opened = self.transducer_access.open(tim_id,
                                             channel_id)

        trans_comm_id = opened['trans_comm_id']
        error = opened['error_code']

        read = \
                self.transducer_access.read_data(trans_comm_id,
                                                  timeout,
                                                  sampling_mode)
        error = read['error_code']
        sample_data = read['result']

        self.transducer_access.close(trans_comm_id)

        result = {'error_code': error,
                  'ncap_id': ncap_id,
                  'tim_id': tim_id,
                  'channel_id': channel_id,
                  'sample_data': sample_data}

        return result

    def write_transducer_sample_data_to_a_channel_of_a_tim(self,
                                                           ncap_id,
                                                           tim_id,
                                                           channel_id,
                                                           timeout,
                                                           sampling_mode,
                                                           sample_data):
        """ Write transducer sample data to a channel of a TIM.

        Args:
            ncap_id: ID of the NCAP application being queried
            tim_id: ID of the TIM being queried
            channel_id: the channel ID of the TIM
            timeout: The timeout interval before reporting a timeout error_code
            sampling_mode: The sampling mode selection
            sample_data: The sample data to be written.

        Returns:
            error_code: an error code
            ncap_id: the ncap id
            tim_id: the id of the tim that was read
            channel_id: the id of the channel read from the TIM
        """

        if type(sample_data) is not ieee1451.ArgumentArray:
            arg_array = ieee1451.ArgumentArray()
            arg_array.put_by_index(0, ieee1451.Argument(value=sample_data))
        else:
            arg_array = sample_data

        error = ieee1451.Error(
                            ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)



        opened = self.transducer_access.open(tim_id, channel_id)
        trans_comm_id = opened['trans_comm_id']
        error = opened['error_code']

        written = self.transducer_access.write_data(trans_comm_id,
                                                       timeout,
                                                       sampling_mode,
                                                       arg_array)
        error = written['error_code']
        self.transducer_access.close(trans_comm_id)

        result = {'error_code': error,
                  'ncap_id': ncap_id,
                  'tim_id': tim_id,
                  'channel_id': channel_id}

        return result
