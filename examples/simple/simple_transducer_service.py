"""
.. module:: transducer_services_Simple
   :platform: Unix, Windows
   :synopsis: Defines a simple example implementation for IEEE1451.0
   Transducer Services for ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ncaplite.transducer_services_base import TransducerAccessBase
from ncaplite.transducer_services_base import TimDiscoveryBase
from ncaplite.transducer_services_base import TedsManagerBase
import ncaplite.ieee1451types as ieee1451
from ncaplite import teds_support
import logging


logger = logging.getLogger(__name__)


vteds  = {1:'RoomTemperatureSensor.xml',
          2:'RoomTemperatureActuator.xml'}



class TimDiscoverySimple(TimDiscoveryBase):
    """
    The TimDiscovery interface is provided by the IEEE 1451.0 layer
    and is called by the application to provide a common mechanism to
    discover available TIMs and TransducerChannels.
    The methods are listed in Table 84 and discussed in 10.1.1 through 10.1.3.
    """

    def report_comm_module(self):
        """This method reports the available communication module
        interfaces that have been registered with this standard. See the:
        IEEE1451Dot0::ModuleCommunication::NetRegistration::registerModule( )
        method, which the IEEE 1451.X layer will invoke when it is ready for
        operation. In that method, the IEEE 1451.0 layer will assign a unique
        moduleId to each IEEE 1451.X interface. Note that the NCAP may have:
        A single IEEE 1451.X interface of a given technology
        (for example, Clause 7 of IEEE Std 1451.5- 2007 [B4]) .
        Multiple interfaces of the same technology
        (for example, IEEE 1451.2-RS232 on COM1 and COM2).
        Multiple IEEE 1451.X interfaces of different technologies
        (for example, Clause 7 of IEEE Std 1451.5-2007
        [B4] and IEEE 1451.3 multidrop).

        Returns:
        ErrorCode error_code: an error code
        UInt8Array module_ids: an array of module ids
        """
        logger.debug("report_comm_module")
        error_code = ieee1451.Error(
                    ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                    ieee1451.ErrorCode.NO_ERROR)
        module_ids = [1]
        result = {'error_code': error_code,
                  'module_ids': module_ids}
        return result


    def report_tims(self, module_id):
        """

        :param module_id: The Module ID for which TIMs are to be reported
        :return: A dictionary with the following entries
            ErrorCode error_code: an ieee1451-1 error code
            UInt16Array tim_ids: A list of TIM IDs
        """
        error_code = ieee1451.Error(
                ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                ieee1451.ErrorCode.NO_ERROR)
        tim_ids = []
        if(module_id == 1):
            tim_ids = [1]

        result = {'error_code': error_code,
                  'tim_ids': tim_ids}

        return result

    def report_channels(self, tim_id):
        """ This returns the TransducerChannel list and names for this TIM.
        This information is retrieved from the cached TEDS.

        Args:
        UInt16 tim_id: the desired TIM.

        Returns:
        ErrorCode error_code: an error code
        UInt16Array channel_ids: is returned to the application and contains
                                all known TransducerChannels on this TIM.
        StringArray channel_names: is returned to the application and contains the
               Transducer Channel names.
        """
        error_code = ieee1451.Error(
                            ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                            ieee1451.ErrorCode.NO_ERROR)
        channel_ids = [1, 2]
        names = ["RoomTemperatureSensor", "RoomTemperatureActuator"]
        result = {'error_code': error_code,
                  'channel_ids': channel_ids,
                  'channel_names': names}

        return result

class TedsManagerBase(object):
    """
    The TedsManager interface is provided by the IEEE 1451.0 layer and is
    called by the application to provide access to the TEDS. The methods in
    this interface are listed in Table 88.
    """

    def __init__(self):
          self.tedcash = dict()

    def read_teds(self, trans_comm_id, timeout, teds_type):
        """

        :param trans_comm_id:
        :param timeout:
        :param teds_type:
        :return:
        """

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


    def write_teds(self, trans_comm_id, timeout, teds_type, teds):
        """

        :param trans_comm_id:
        :param timeout:
        :param teds_type:
        :param teds:
        :return:
        """
        logger.warning(msg="write_teds was called but is not implemented")
        error_code = 0
        return {'error_code': error_code}


    def read_raw_teds(self, trans_comm_id, timeout, teds_type):
        """

        :param trans_comm_id:
        :param timeout:
        :param teds_type:
        :return:
        """
        logger.warning(msg="read_raw_teds was called but is not implemented")
        error_code = 0
        raw_teds = ()
        return {'error_code': error_code, 'raw_teds': raw_teds}


    def write_raw_teds(self, trans_comm_id, timeout, teds_type, raw_teds):
        """

        :param trans_comm_id:
        :param timeout:
        :param teds_type:
        :param raw_teds:
        :return:
        """
        logger.warning(msg="write_raw_teds was called but is not implemented")
        error_code = 0
        return {'error_code': error_code}


    def update_teds_cache(self, trans_comm_id, timeout, teds_type):
        """

        :param trans_comm_id:
        :param timeout:
        :param teds_type:
        :return:
        """
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


class TransducerAccessSimple(TransducerAccessBase):
    """
    The TransducerAccess interface is provided by the IEEE 1451.0 layer and is
    called by the application to provide access to TransducerChannels.
    For most applications, they will primarily be interacting with this
    interface to perform TIM read and write operations. To keep this interface
    small, more advanced methods are placed in the TransducerManager interface.
    Each method is listed in Table 85.
    """

    def __init__(self):
        self.transducer_interfaces = {
                                      1: (0, 0),  # comm_id0 : tim_id0, chanid0
                                      2: (0, 1),  # comm_id1 : tim_id0, chanid1
                                      3: (1, 0),  # comm_id2 : tim_id1, chanid0
                                      }

        self.out_data = {1: 0, 2: 0, 3: 0}
        self.in_data = {1: 0, 2: 0, 3: 0}

    def find_com_id(self, tim_id, channel_id):
        """ Simple helper function to find trans_comm_id given
        a tim_id and channel_id. Assumes 0 is not a valid trans_comm_id.
        """
        for comid, tim in self.transducer_interfaces.iteritems():
            if tim == (tim_id, channel_id):
                return comid
        return 0  # assumes 0 not valid comid

    def open(self, tim_id, channel_id):
        trans_comm_id = self.find_com_id(tim_id, channel_id)
        logger.debug("TransducerAccessSimple.open: " + str(trans_comm_id))
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                    ieee1451.ErrorCode.NO_ERROR)
        return (error_code, trans_comm_id)

    def open_qos(self, tim_id, channel_id, qos_params):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                    ieee1451.ErrorCode.NO_ERROR)
        qos_params = ()
        trans_comm_id = 0
        return (error_code, qos_params, trans_comm_id)

    def open_group(self, tim_ids, channel_ids):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                    ieee1451.ErrorCode.NO_ERROR)
        trans_comm_id = 0
        return (error_code, trans_comm_id)

    def open_group_qos(self, tim_ids, channel_ids, qos_params):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                    ieee1451.ErrorCode.NO_ERROR)
        qos_params = ()
        trans_comm_id = 0
        return (error_code, qos_params, trans_comm_id)

    def close(self, trans_comm_id):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                    ieee1451.ErrorCode.NO_ERROR)
        return error_code

    def read_data(self, trans_comm_id, timeout, sampling_mode):
        data = self.out_data[trans_comm_id]
        tmp = (trans_comm_id, self.out_data[trans_comm_id])
        logger.debug("TransducerAccessSimple.read_data: " + str(tmp))
        data = data+1
        self.out_data[trans_comm_id] = data

        arg = ieee1451.Argument(ieee1451.TypeCode.UINT32_TC, data)
        arg_array = ieee1451.ArgumentArray()
        arg_array.put_by_index(0, arg)
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                    ieee1451.ErrorCode.NO_ERROR)
        return (error_code, arg_array)

    def write_data(self, trans_comm_id, timeout, sampling_mode, value):
        val = value.get_by_index(0).value
        self.in_data[trans_comm_id] = val
        tmp = (trans_comm_id, self.in_data[trans_comm_id])
        print("TransducerAccessSimple.write data: " + str(tmp))
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                    ieee1451.ErrorCode.NO_ERROR)
        return error_code

    def start_read_data(self, trans_comm_id, trigger_time, timeout,
                        sampling_mode, callback):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                    ieee1451.ErrorCode.NO_ERROR)
        operation_id = 0
        return (error_code, operation_id)

    def start_write_data(self, trans_comm_id, trigger_time, timeout,
                         sampling_mode, value, callback):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                    ieee1451.ErrorCode.NO_ERROR)
        operation_id = 0
        return (error_code, operation_id)

    def start_stream(self, trans_comm_id, callback, operation_id):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                    ieee1451.ErrorCode.NO_ERROR)
        operation_id = 0
        return (error_code, operation_id)

    def cancel(self, operation_id):
        error_code = ieee1451.Error(ieee1451.ErrorSource.ERROR_SOURCE_LOCAL_0,
                                    ieee1451.ErrorCode.NO_ERROR)
        return error_code

if __name__ == '__main__':

    print('Subclass:', issubclass(TransducerAccessSimple,
                                  TransducerAccessBase))

    print('Instance:', isinstance(TransducerAccessSimple(),
                                  TransducerAccessBase))


