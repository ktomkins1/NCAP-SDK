"""
.. module:: transducer_services_base
   :platform: Unix, Windows
   :synopsis: Defines the abstract base class for IEEE1451.0 Transducer Services for
   ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""

import abc


class TimDiscoveryBase(object):
    """
    The TimDiscovery interface is provided by the IEEE 1451.0 layer
    and is called by the application to provide a common mechanism to
    discover available TIMs and TransducerChannels.
    The methods are listed in Table 84 and discussed in 10.1.1 through 10.1.3.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def report_comm_module(self, module_ids):
        return

    @abc.abstractmethod
    def report_tims(self, module_id, tim_ids):
        return

    @abc.abstractmethod
    def report_channels(self, tim_id, channel_ids, names):
        return


class TransducerAccessBase(object):
    """
    The TransducerAccess interface is provided by the IEEE 1451.0 layer and is
    called by the application to provide access to TransducerChannels.
    For most applications, they will primarily be interacting with this
    interface to perform TIM read and write operations. To keep this interface
    small, more advanced methods are placed in the TransducerManager interface.
    Each method is listed in Table 85.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def open(self, tim_id, channel_id):
        trans_comm_id = 0
        return trans_comm_id

    @abc.abstractmethod
    def open_qos(self, tim_id, channel_id, qos_params, trans_comm_id):
        return

    @abc.abstractmethod
    def open_group(self, tim_ids, channel_ids, trans_comm_id):
        return

    @abc.abstractmethod
    def open_group_qos(self, tim_ids, channel_ids, qos_params, trans_comm_id):
        return

    @abc.abstractmethod
    def close(self, trans_comm_id):
        return

    @abc.abstractmethod
    def read_data(self, trans_comm_id, timeout, sampling_mode, result):
        return

    @abc.abstractmethod
    def write_data(self, trans_comm_id, timeout, sampling_mode, value):
        return

    @abc.abstractmethod
    def start_read_data(self, trans_comm_id, trigger_time, timeout,
                        sampling_mode, callback, operation_id):
        return

    @abc.abstractmethod
    def start_write_data(self, trans_comm_id, trigger_time, timeout,
                         sampling_mode, value, callback, operation_id):
        return

    @abc.abstractmethod
    def start_stream(self, trans_comm_id, callback, operation_id):
        return

    @abc.abstractmethod
    def cancel(self, operation_id):
        return


class TransducerManagerBase(object):
    """

    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def lock(self, trans_comm_id, timeout):
        return

    @abc.abstractmethod
    def unlock(self, trans_comm_id):
        return

    @abc.abstractmethod
    def report_locks(self, trans_comm_ids):
        return

    @abc.abstractmethod
    def break_lock(self, rans_comm_id):
        return

    @abc.abstractmethod
    def send_command(self, trans_comm_id, timeout, cmd_class_id,
                     cmd_function_id, args, out_args):
        return

    @abc.abstractmethod
    def start_command(self, trans_comm_id, trigger_time, timeout, cmd_class_id,
                      cmd_function_id, args, callback, operation_id):
        return

    @abc.abstractmethod
    def trigger(self, trans_comm_id, trigger_time, timeout, samplg_mode):
        return

    @abc.abstractmethod
    def configure_attributes(self, trans_comm_id, attribute_names):
        return

    @abc.abstractmethod
    def start_trigger(self, trans_comm_id, trigger_time, timeout, samplg_mode,
                      app_callbackcallback, operation_id):
        return

    @abc.abstractmethod
    def clear(self, trans_comm_id, timeout, clear_mode):
        return

    @abc.abstractmethod
    def register_status_change(self, trans_comm_id, timeout, callback,
                               operation_id):
        return

    @abc.abstractmethod
    def unregister_status_change(self, trans_comm_id):
        return


class TedsManagerBase(object):
    """

    """
    _metaclass_ = abc.ABCMeta

    @abc.abstractmethod
    def read_teds(self, trans_comm_id, timeout, teds_type, teds):
        return

    @abc.abstractmethod
    def write_teds(self, trans_comm_id, timeout, teds_type, teds):
        return

    @abc.abstractmethod
    def read_raw_teds(self, trans_comm_id, timeout, teds_type, raw_teds):
        return

    @abc.abstractmethod
    def write_raw_teds(self, trans_comm_id, timeout, teds_type, raw_teds):
        return

    @abc.abstractmethod
    def update_teds_cache(self, trans_comm_id, timeout, teds_type):
        return


class CommManagerBase(object):
    """

    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_comm_module(self, module_id, comm_object, comm_type,
                        technology_id):
        return


class ApiCallbackBase(object):
    """

    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def measurement_update(self, operation_id, meas_values, status):
        return

    @abc.abstractmethod
    def actuation_complete(self, operation_id, status):
        return

    @abc.abstractmethod
    def status_change(self, operation_id, status):
        return

    @abc.abstractmethod
    def command_complete(self, operation_id, out_args, status):
        return

    @abc.abstractmethod
    def trigger_complete(self, operation_id, status):
        return
