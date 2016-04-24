
"""
.. module:: transducer_services_mock
   :platform: Unix, Windows
   :synopsis: Defines the mock implementation for IEEE1451.0
   Transducer Services for ncaplite.

.. moduleauthor:: James Ethridge <jeethridge@gmail.com>

"""

from ncaplite.transducer_services_base import TimDiscoveryBase
from ncaplite.transducer_services_base import TransducerAccessBase
from ncaplite.transducer_services_base import TransducerManagerBase
from ncaplite.transducer_services_base import TedsManagerBase
from ncaplite.transducer_services_base import CommManagerBase
from ncaplite.transducer_services_base import ApiCallbackBase


class TimDiscoveryMock(TimDiscoveryBase):

    def report_comm_module(self, module_ids):
        return

    def report_tims(self, module_id, tim_ids):
        return

    def report_channels(self, tim_id, channel_ids, names):
        return


class TransducerAccessMock(TransducerAccessBase):

    def open(self, tim_id, channel_id):
        trans_comm_id = 0
        return trans_comm_id

    def open_qos(self, tim_id, channel_id, qos_params, trans_comm_id):
        return

    def open_group(self, tim_ids, channel_ids, trans_comm_id):
        return

    def open_group_qos(self, tim_ids, channel_ids, qos_params, trans_comm_id):
        return

    def close(self, trans_comm_id):
        return

    def read_data(self, trans_comm_id, timeout, sampling_mode, result):
        return

    def write_data(self, trans_comm_id, timeout, sampling_mode, value):
        return

    def start_read_data(self, trans_comm_id, trigger_time, timeout,
                        sampling_mode, callback, operation_id):
        return

    def start_write_data(self, trans_comm_id, trigger_time, timeout,
                         sampling_mode, value, callback, operation_id):
        return

    def start_stream(self, trans_comm_id, callback, operation_id):
        return

    def cancel(self, operation_id):
        return


class TransducerManagerMock(TransducerManagerBase):

    def lock(self, trans_comm_id,  timeout):
        return

    def unlock(self, trans_comm_id):
        return

    def report_locks(self, trans_comm_ids):
        return

    def break_lock(self, trans_comm_id):
        return

    def send_command(self, trans_comm_id, timeout, cmd_class_id,
                     cmd_function_id, args, out_args):
        return

    def start_command(self, trans_comm_id, trigger_time, timeout, cmd_class_id,
                      cmd_function_id, args, callback, operation_id):
        return

    def trigger(self, trans_comm_id, trigger_time, timeout, samplg_mode):
        return

    def configure_attributes(self, trans_comm_id, attribute_names):
        return

    def start_trigger(self, trans_comm_id, trigger_time, timeout, samplg_mode,
                      app_callbackcallback, operation_id):
        return

    def clear(self, trans_comm_id, timeout, clear_mode):
        return

    def register_status_change(self, trans_comm_id, timeout, callback,
                               operation_id):
        return

    def unregister_status_change(self, trans_comm_id):
        return


class TedsManagerMock(TedsManagerBase):

    def read_teds(self, trans_comm_id, timeout, teds_type, teds):
        return

    def write_teds(self, trans_comm_id, timeout, teds_type, teds):
        return

    def read_raw_teds(self, trans_comm_id, timeout, teds_type, raw_teds):
        return

    def write_raw_teds(self, trans_comm_id, timeout, teds_type, raw_teds):
        return

    def update_teds_cache(self, trans_comm_id, timeout, teds_type):
        return


class CommManagerMock(CommManagerBase):

    def get_comm_module(self, module_id, comm_object, comm_type,
                        technology_id):
        return


class ApiCallbackMock(ApiCallbackBase):

    def measurement_update(self, operation_id, meas_values, status):
        return

    def actuation_complete(self, operation_id, status):
        return

    def status_change(self, operation_id, status):
        return

    def command_complete(self, operation_id, out_args, status):
        return

    def trigger_complete(self, operation_id, status):
        return


if __name__ == '__main__':
    print('Subclass:', issubclass(TimDiscoveryMock, TimDiscoveryBase))
    print('Subclass:', issubclass(TransducerAccessMock, TransducerAccessBase))
    print('Subclass:', issubclass(TransducerManagerMock,
                                  TransducerManagerBase))
    print('Subclass:', issubclass(TedsManagerMock, TedsManagerBase))
    print('Subclass:', issubclass(CommManagerMock, CommManagerBase))
    print('Subclass:', issubclass(ApiCallbackMock, ApiCallbackBase))

    print('Instance:', isinstance(TimDiscoveryMock(), TimDiscoveryBase))
    print('Instance:', isinstance(TransducerAccessMock(),
                                  TransducerAccessBase))
    print('Instance:', isinstance(TransducerManagerMock(),
                                  TransducerManagerBase))
    print('Instance:', isinstance(TedsManagerMock(), TedsManagerBase))
    print('Instance:', isinstance(CommManagerMock(), CommManagerBase))
    print('Instance:', isinstance(ApiCallbackMock(), ApiCallbackBase))
