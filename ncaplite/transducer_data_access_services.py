"""
.. module:: transducer_data_access_services
   :platform: Unix, Windows
   :synopsis: Defines Discovery Services for ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""

import time


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
        trans_comm_id = self.transducer_access.open(tim_id, channel_id)
        self.transducer_access.read_data(trans_comm_id, timeout,
                                         sampling_mode, sample_data)
        self.transducer_access.close(trans_comm_id)
        error_code = 0

        return (error_code, ncap_id, tim_id, channel_id, sample_data)

    def read_transducer_block_data_from_a_channel_of_a_tim(self,
                                                           ncap_id,
                                                           tim_id,
                                                           channel_id,
                                                           timeout,
                                                           number_of_samples,
                                                           sample_interval,
                                                           start_time):
        """Read a block of sensor data from a channel of a TIM
        at a specified interval.

        Args:
            ncap_id: the ncap ID
            tim_id: the ID of the TIM to read from
            channel_id: the channel ID of the TIM
            timeout: a timeout value for the read attempt
            number_of_samples: the number of samples to read
            sample_interval: the desired interval between each sample
            start_time: the start time to begin reading

        Returns: A tuple containing the following:
            error_code: an error code
            ncap_id: the ncap id
            tim_id: the id of the tim that was read
            channel_id: the id of the channel read from the TIM
            transducer_block_data: the block of sample data given as a list
        """
        error_code = 0
        sampling_mode = 5
        transducer_block_data = []
        args = (ncap_id, tim_id, channel_id, timeout, sampling_mode)

        time.sleep(start_time)

        for _ in range(number_of_samples):
            result = \
                self.read_transducer_sample_data_from_a_channel_of_a_tim(*args)
            if(result[0] != 0):
                error_code = 1
            transducer_block_data.append(result[4][0])
            time.sleep(sample_interval)
        return (error_code, ncap_id, tim_id, channel_id, transducer_block_data)

    def read_transducer_sample_data_from_multiple_channels_of_a_tim(
                                                                self,
                                                                ncap_id,
                                                                tim_id,
                                                                channel_ids,
                                                                timeout,
                                                                sampling_mode):
        """Read transducer sample data from multple channels of a TIM.

            Args:
                ncap_id: ID of the NCAP application being queried
                tim_id: ID of the TIM being queried
                channel_ids: tuple with the channel ids to be read from the TIM
                timeout: The timeout interval before reporting a timeout error
                sampling_mode: The sampling mode selection

            Returns: A tuple containing the following:
                error_code: an error code
                ncap_id: the ncap id
                tim_id: the id of the tim that was read
                channel_ids: tuple with the ids of the channels read
                sample_data: the list of samples read, one for each channel_id
        """

        sample_data = []
        for channel_id in channel_ids:
            trans_comm_id = self.transducer_access.open(tim_id, channel_id)
            self.transducer_access.read_data(trans_comm_id, timeout,
                                             sampling_mode, sample_data)
            self.transducer_access.close(trans_comm_id)
        error_code = 0
        return (error_code, ncap_id, tim_id, channel_ids, sample_data)

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
        trans_comm_id = self.transducer_access.open(tim_id, channel_id)
        self.transducer_access.write_data(trans_comm_id, timeout,
                                          sampling_mode, sample_data)
        self.transducer_access.close(trans_comm_id)
        error_code = 0

        return (error_code, ncap_id, tim_id, channel_id)
